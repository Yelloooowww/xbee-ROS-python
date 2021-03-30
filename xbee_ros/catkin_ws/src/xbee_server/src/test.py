from digi.xbee.devices import XBeeDevice
from digi.xbee.util import utils
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.models.status import PowerLevel
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.util.utils import int_to_bytes, bytes_to_int
import threading
import rospy
import random
import time


class xbee_transporter():
	def __init__(self,port):
		self.point_storage = [None, None, None]
		self.map_storage = []
		self.PORT = port # "/dev/ttyUSB0"
		self.BAUD_RATE = 9600

		try:

			self.device = XBeeDevice(self.PORT, self.BAUD_RATE)
			self.device.open(force_settings=True)
			self.device.add_data_received_callback(self.data_receive_callback)
			print("Waiting for data...\n")
	        
			# self.remote = RemoteXBeeDevice(
			# 	self.device,
			# 	x64bit_addr=XBee64BitAddress.from_hex_string("0013A20041AF1B1A"),node_id="manually_added")

			rospy.loginfo('xbee init done')
		except:
			rospy.loginfo('xbee init fail')

	def send_point(self, point_array):
		assert len(point_array) == 3

		package = []
		package.append(0xAB) # Header
		package.append(1) # type
		package.append(3) # bytes
		for i in range(3): package.append(point_array[i]) #data
		package.append(sum(point_array) & 0xFF) # checksum
		print('package=',package)
		for item in package :
			self.device.send_data( self.remote, int_to_bytes(item) )
			print('send=',int_to_bytes(item) )
		return

	def data_receive_callback(self,xbee_message):
		print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),bytes_to_int(xbee_message.data)))
		global receive_status
		try : _ = receive_status
		except NameError : receive_status = "Header"

		get_64bit_addr , get = xbee_message.remote_device.get_64bit_addr(), bytes_to_int(xbee_message.data)
		print(get,receive_status)

		if receive_status == "Header" :
			if int(get) == 171 :
				receive_status = "Type"

		if receive_status == "Type" :
			# if get == 0 :
			# 	receive_status = "Bytes"
			# if get == 1 :
			# 	receive_status = "Bytes"
			# if get == 2 :
			receive_status = "Bytes"
			# else :
			# 	receive_status =="Header"


		if receive_status == "Bytes" :
			# if get > 0:
			# 	get_data_lenght, bytes_num, checksum = get, 0, 0
			# 	# print('get_data_lenght=',get_data_lenght)
			receive_status = "Data"
			# else :
				# receive_status = "Header"

		if receive_status == "Data" :
			# if bytes_num < get_data_lenght-1 :
			# 	self.point_storage[bytes_num] = get
			# 	bytes_num += 1
			# 	checksum += 1
			# if bytes_num == get_data_lenght-1 :
			# 	self.point_storage[bytes_num] = get
			# 	bytes_num += 1
			# 	checksum += 1
			receive_status = "Checksum"
			# else :
			# 	receive_status = "Header"

		if receive_status == "Checksum" :
			# if get == (checksum & 0xFF) :
			# 	# print(self.point_storage)
			# 	self.map_storage.append(self.point_storage)
			# else :
			# 	print('WRONG DATA')
			receive_status = "Header"



		# print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
		#                          bytes_to_int(xbee_message.data)))
		rospy.spinOnce()



if __name__ == '__main__':
	rospy.init_node("xbee_transporter")
	M = xbee_transporter("/dev/ttyUSB0")
	# try:
	# 	rospy.spin()
	# finally:
	# 	M.device.close()



	# M.send_point([8,88,888])
