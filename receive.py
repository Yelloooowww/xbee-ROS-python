import pickle
import numpy as np
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *

PORT = "/dev/ttyUSB1"
BAUD_RATE = 115200


def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open(force_settings=True)

        def data_receive_callback(xbee_message):
            print('callback')
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     bytes_to_int(xbee_message.data)))

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
