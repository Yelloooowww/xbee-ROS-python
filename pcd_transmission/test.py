from digi.xbee.devices import XBeeDevice
from digi.xbee.util.utils import bytes_to_int


PORT = "/dev/ttyUSB1"
BAUD_RATE = 9600
receive_status = "Header"

def data_receive_callback(xbee_message):
	get_64bit_addr , get = xbee_message.remote_device.get_64bit_addr(), bytes_to_int(xbee_message.data)
	# print(get,receive_status)

	if receive_status == "Header" :
		if get == 0xAB :
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

def main():
	print(" +-----------------------------------------+")
	print(" | XBee Python Library Receive Data Sample |")
	print(" +-----------------------------------------+\n")


	device = XBeeDevice(PORT, BAUD_RATE)
	receive_status = "Header"


	try:
		device.open(force_settings=True)
		device.add_data_received_callback(data_receive_callback)




		print("Waiting for data...\n")
		input()

	finally:
		if device is not None and device.is_open():
			device.close()


if __name__ == '__main__':
	main()
