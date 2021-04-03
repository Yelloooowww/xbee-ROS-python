#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Float32, Int32
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs import point_cloud2
from xbee_communication.srv import xbee
import struct
import roslib
import pickle
import time
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *
from datetime import datetime

# generate test data
generate_points = np.array( [[1.23, 2.34, 3.45] for i in range(12)] ,dtype=np.float16)
generate_pose = np.array( [1.23, 2.34, 3.45, 4.56, 5.67, 6.78, 7.89] ,dtype=np.float16)


class XBee(object):
	def __init__(self):
		self.PORT = rospy.get_param("~port")
		self.BAUD_RATE = 115200
		self.device = DigiMeshDevice(self.PORT, self.BAUD_RATE)
		self.device.open(force_settings=True)
		self.device.add_data_received_callback(self.xbee_callback_and_decode)
		self.sourceAddr = str(self.device.get_64bit_addr())

		self.service = rospy.Service('xbee', xbee, self.handle_ros_service)

		self.data_points, self.data_pose = [], []
		self.data_points, self.data_pose = generate_points, generate_pose # only for test
		self.check, self.get_register = 0, bytearray()

		self.auto_ask_flag = rospy.get_param("~auto_ask_flag")
		if self.auto_ask_flag:
			self.timer = rospy.Timer(rospy.Duration(5), self.auto_ask_timer)
			self.get_ACK, self.get_array_checksum = None, None
			self.address_to_robot = {	rospy.get_param("/xbee_address/husky1"):"husky1", \
										rospy.get_param("/xbee_address/husky2"):"husky2", \
										rospy.get_param("/xbee_address/jackal1"):"jackal1", \
										rospy.get_param("/xbee_address/jackal2"):"jackal2"  }
			self.robot_to_address = {v: k for k, v in self.address_to_robot.items()}
			self.all_robot_date = dict()
			for robot in ["husky1", "husky2", "jackal1", "jackal2"]:
				one_robot_date = dict()
				for ask in ["AskPoints", "AskPose"]:
					one_robot_date[ask] = []
				self.all_robot_date[robot] = one_robot_date

		print("xbee node initialized, I am ", self.sourceAddr[8:])

	def auto_ask_timer(self,event):
		for robot in ["husky1", "husky2", "jackal1", "jackal2"]:
			for ask in ["AskPoints", "AskPose"]:
				print('------ ', datetime.now().strftime("%H:%M:%S "),robot,' ',ask,' ------')
				self.get_ACK, self.get_array_checksum = None, False

				if self.xbee_encode_and_send(self.robot_to_address[robot], ask, data_type=b'\x00') :
					time0 = time.time()
					while self.get_ACK == None :
						if ((time.time() - time0) > 1) :
							print('wait ACK TimeOut')
							break
					if self.get_ACK :
						time1 = time.time()
						while not self.get_array_checksum :
							if ((time.time() - time1) > 10) :
								print('wait checksum TimeOut')
								break
						if self.get_array_checksum :
							print('success,',self.all_robot_date[robot][ask])



	def moving_to_goal(self,x,y,z):
		# TODO
		print("I am moving to ",x,y,z,' ~~~')


	def handle_ros_service(self,req): # deal with the client (xbee_client.py)
		ADDRESS_L = req.address
		if req.address == "husky1": ADDRESS_L = rospy.get_param("/xbee_address/husky1")
		elif req.address == "husky2": ADDRESS_L = rospy.get_param("/xbee_address/husky2")
		elif req.address == "jackal1": ADDRESS_L = rospy.get_param("/xbee_address/jackal1")
		elif req.address == "jackal2": ADDRESS_L = rospy.get_param("/xbee_address/jackal2")

		if req.message == "Move":
			goal_array = np.array([req.x,req.y,req.z],dtype=np.float16)
			return self.xbee_encode_and_send(ADDRESS_L, goal_array, data_type=b'\x03') #send goal array
		else:
			return self.xbee_encode_and_send(ADDRESS_L, req.message, data_type=b'\x00') #send string msg


	def xbee_callback_and_decode(self, xbee_message):
		ADDRESS = str(xbee_message.remote_device.get_64bit_addr()) # msg from who

		if not xbee_message.data[0:1] == b'\xAB' : # Header wrong
			self.check, self.get_register = 0, bytearray()
			print('get xbee_message with wrong Header')
			return

		if not ((xbee_message.data[1:2] == b'\x00') or (xbee_message.data[1:2] == b'\x01') or (xbee_message.data[1:2] == b'\x02') or (xbee_message.data[1:2] == b'\x03')):
			self.check, self.get_register = 0, bytearray()
			print('get xbee_message with wrong type')
			return

		self.get_register.extend(xbee_message.data[6:])
		data_bytes = int.from_bytes(xbee_message.data[2:6], byteorder="big",signed=False)

		if not (data_bytes == len(self.get_register) -1): # still not the last data pkg
			self.check = 0xff & (self.check + xbee_message.data[-1])

		else : # the last one of data pkgs
			if not (xbee_message.data[-1] == self.check) : #checksum error
				print('checksum error QQ?')
				self.check, self.get_register = 0, bytearray()

			else : #get data with correct checksum
				if xbee_message.data[1:2] == b'\x00': # type: string msg
					get_msg = pickle.loads(self.get_register)
					self.check, self.get_register = 0, bytearray()
					print('get string msg= ',get_msg)
					if get_msg == "AskPoints":
						print(" AskPoints from ", ADDRESS[8:])
						self.xbee_encode_and_send(ADDRESS[8:], self.data_points, data_type=b'\x01') #send points
					elif get_msg == "AskPose":
						print(" AskPose from ", ADDRESS[8:])
						self.xbee_encode_and_send(ADDRESS[8:], self.data_pose, data_type=b'\x02') #send pose

					elif get_msg == "OK": self.get_ACK = True
					elif get_msg == "Not OK": self.get_ACK = False

				elif xbee_message.data[1:2] == b'\x01': # type: points
					get_points = pickle.loads(self.get_register)
					self.check, self.get_register = 0, bytearray()
					if self.auto_ask_flag:
						self.all_robot_date[self.address_to_robot[ADDRESS[8:]]]["AskPoints"] = get_points
						self.get_array_checksum = True
					else : print('get_points= ',get_points)


				elif xbee_message.data[1:2] == b'\x02': # type: pose
					get_pose = pickle.loads(self.get_register)
					self.check, self.get_register = 0, bytearray()
					if self.auto_ask_flag:
						self.all_robot_date[self.address_to_robot[ADDRESS[8:]]]["AskPose"] = get_pose
						self.get_array_checksum = True
					else : print('get_pose= ',get_pose)


				elif xbee_message.data[1:2] == b'\x03': # type: goal
					get_goal = pickle.loads(self.get_register)
					self.check, self.get_register = 0, bytearray()
					print('get_goal= ',get_goal)
					self.moving_to_goal(get_goal[0], get_goal[1], get_goal[2])




	def xbee_encode_and_send(self, ADDRESS_L, data_via_xbee, data_type):
		data = data_via_xbee
		ADDRESS_H = '0013A200'
		ADDRESS = ADDRESS_H + ADDRESS_L

		if not data_type==b'\x00': # tell the base_station that I am ready
			OK_msg = 'Not OK' if data == [] else 'OK'
			self.xbee_encode_and_send(ADDRESS_L, OK_msg, data_type=b'\x00') #send string msg


		# send data
		# print( datetime.now().strftime("%H:%M:%S"),' Start to send data to ', ADDRESS[8:])
		byte_arr = pickle.dumps( data )
		length, index, check= int(len(byte_arr)), 0, 0
		try :
			for index in range(0,length,250) :
				pack = bytearray(b'\xAB') #Header
				pack.extend(bytearray(data_type)) #Type
				pack.extend( length.to_bytes(4, byteorder='big') ) #bytes
				index_end = index+250 if index+250 < length else length
				pack.extend( byte_arr[index:(index_end)] ) #data

				# print('keep sending ', index, length, len(pack))
				if index_end == length : pack.extend(check.to_bytes(1, byteorder='big')) # checksum
				else: check = 0xff & (check + pack[-1])
				self.device.send_data_64( XBee64BitAddress.from_hex_string(ADDRESS), pack)

		except :
			print('send data_via_xbee fail')
			return False

		# print( datetime.now().strftime("%H:%M:%S"),' End to send')
		return True




if __name__ == "__main__":
	rospy.init_node("xbee_node")
	xbee_node = XBee()
	rospy.spin()
