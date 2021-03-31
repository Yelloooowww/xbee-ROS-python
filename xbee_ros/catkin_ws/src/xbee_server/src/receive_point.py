#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Float32, Int32
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs import point_cloud2
from xbee_server.srv import xbee
import struct
import roslib
import pickle
import time
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *
from datetime import datetime


class XBee(object):
	def __init__(self):
		self.PORT = rospy.get_param("~port")
		self.BAUD_RATE = 115200
		self.device = DigiMeshDevice(self.PORT, self.BAUD_RATE)
		self.device.open(force_settings=True)
		self.device.add_data_received_callback(self.xbee_msg_cb)

		self.service = rospy.Service('xbee', xbee, self.handle_xbee_msg)
		self.cloud_sub = rospy.Subscriber(rospy.get_param("~pointcloud_topic"), PointCloud2,self.callback,queue_size=1)
		self.raw_point = []

		self.timer = rospy.Timer(rospy.Duration(5), self.auto_ask)
		self.auto_ask_flag = rospy.get_param("~auto_ask_flag")

		self.pose_dict, self.points_dict = dict(), dict()

		self.check = 0
		self.get_register = bytearray()

		self.get_OK = None
		self.sourceAddr = str(self.device.get_64bit_addr())
		print("xbee node initialized, I am ", self.sourceAddr[8:])

	def auto_ask(self,event):
		if not self.auto_ask_flag: return

		husky1_address = rospy.get_param("/xbee_address/husky1")
		husky2_address = rospy.get_param("/xbee_address/husky2")
		jackal1_address = rospy.get_param("/xbee_address/jackal1")
		jackal2_address = rospy.get_param("/xbee_address/jackal2")
		robot_list = ["husky1", "husky2", "jackal1", "jackal2"]
		address_list = [husky1_address, husky2_address, jackal1_address, jackal2_address]
		# ask_list = ["AskPoints", "AskPose"]
		ask_list = ["AskPoints"]
		for i,address in enumerate(address_list) :
			for ask in ask_list :
				print("ask ",robot_list[i])
				self.pose_dict["address"], self.points_dict["address"], self.get_OK = [],[],None
				reqqq = xbee()
				reqqq.address = address
				reqqq.message = ask
				xbee_msg_send_success = self.handle_xbee_msg(reqqq)
				if xbee_msg_send_success :
					rospy.loginfo('wait ok')
					time0 = time.time()
					while self.get_OK==None :
						if time.time() - time0 > 20 :
							rospy.loginfo("TimeOut (wait get_OK)")
							break
					if self.get_OK == 'OK':
						rospy.loginfo("wait points")
						time1 = time.time()
						while self.points_dict["address"]==[] :
							if time.time() - time1 > 150 :
								rospy.loginfo("TimeOut (wait points)")
								break
						print(self.points_dict["address"])

		rospy.loginfo("Done ask robot")

	def callback(self, msg): # PointCloud2 to numpy
		cloud_points = []
		for p in point_cloud2.read_points(msg, field_names = ("x", "y", "z"), skip_nans=True):
			cloud_points.append(p)
		self.raw_point = np.array(cloud_points, dtype=np.float16)


	def handle_xbee_msg(self,req):
		ADDRESS_H = '0013A200'
		ADDRESS_L = req.address
		ADDRESS = ADDRESS_H + ADDRESS_L
		try :
			# print('xbee send msg to address:', ADDRESS)
			pack = bytearray(b'0xAB') #Header
			pack.extend(bytearray(b'0x00')) #Type
			pack.extend( pickle.dumps(req.message) ) #data
			self.device.send_data_64( XBee64BitAddress.from_hex_string(ADDRESS), pack)
			# print("send success")
			return True
		except :
			# print("send fail")
			return False



	def xbee_msg_cb(self, xbee_message):
		ADDRESS = str(xbee_message.remote_device.get_64bit_addr())

		if not xbee_message.data[0:4] == b'0xAB' : # Header wrong
			self.check = 0
			self.get_register = bytearray()
			return

		if xbee_message.data[4:8] == b'0x00' : # type: msg
			get_msg = pickle.loads(xbee_message.data[8:])
			print('get type 0x00 msg= ',get_msg)
			if get_msg == "AskPoints":
				print(" AskPoints from ", ADDRESS[8:])
				self.xbee_send_point(ADDRESS[8:])
			if get_msg == "AskPose":
				print(" AskPose from ", ADDRESS[8:])

			if get_msg == "OK": self.get_OK = "OK"
			if get_msg == "Not OK": self.get_OK = "Not OK"



		elif xbee_message.data[4:8] == b'0x01' : # type: pointcloud
			self.get_register.extend(xbee_message.data[8:])
			self.check += (0xff & xbee_message.data[-1])

		elif xbee_message.data[4:8] == b'0x03' : # type: check
			get_check = pickle.loads(xbee_message.data[8:])
			print('get_check= ',get_check)
			if self.check == get_check :
				self.points_dict["ADDRESS"] = pickle.loads(self.get_register)
				print( self.points_dict["ADDRESS"] )
			else :
				rospy.loginfo('CheckSum error')
				self.points_dict["address"] = "CheckSum error"
			self.check = 0
			self.get_register = bytearray()

		else : # type wrong
			self.check = 0
			self.get_register = bytearray()
			return


	def xbee_send_point(self, ADDRESS_L):
		ADDRESS_H = '0013A200'
		ADDRESS = ADDRESS_H + ADDRESS_L

		reqqq = xbee()
		reqqq.address = ADDRESS_L
		reqqq.message = 'Not OK' if self.raw_point == [] else 'OK'
		self.handle_xbee_msg(reqqq)

		if self.raw_point == []:
			rospy.loginfo('No point to send')
			return
		print( datetime.now().strftime("%H:%M:%S"),' Start to send points to ', ADDRESS)

		byte_arr = pickle.dumps( self.raw_point )
		length, index, check= len(byte_arr), 0, 0

		try :
			for index in range(0,length,248) :
				pack = bytearray(b'0xAB') #Header
				pack.extend(bytearray(b'0x01')) #Type
				index_end = index+248 if index+248 < length else length
				pack.extend( byte_arr[index:(index_end)] ) #data

				self.device.send_data_64( XBee64BitAddress.from_hex_string(ADDRESS), pack)
				check += (0xff & pack[-1])
				# print(index, length, len(pack))
		except :
			print('send point fail')


		print('check= ',check)
		try :
			pack = bytearray(b'0xAB') #Header
			pack.extend(bytearray(b'0x03')) #Type
			pack.extend( pickle.dumps( check ) ) #data
			self.device.send_data_64( XBee64BitAddress.from_hex_string(ADDRESS), pack)
		except :
			print('send checksum fail')

		check = 0
		print( datetime.now().strftime("%H:%M:%S"),' End to send points')


if __name__ == "__main__":
	rospy.init_node("xbee_node")
	xbee_node = XBee()
	rospy.spin()
