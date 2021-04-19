import pickle
import numpy as np
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *

PORT = "/dev/ttyUSB1"
BAUD_RATE = 115200

tmp = bytearray()
global check
check = 0

def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = DigiMeshDevice(PORT, BAUD_RATE)

    try:
        device.open(force_settings=True)

        def data_receive_callback(xbee_message):
            print(xbee_message.data)
            print(str(xbee_message.remote_device.get_64bit_addr()))

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()
            # print( pickle.loads(tmp) )


if __name__ == '__main__':
    main()
