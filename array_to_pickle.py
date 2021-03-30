import pickle
import numpy as np
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *


arr = np.array([[1.0,2.0,3.0], [1.0,2.0,3.0], [1.0,2.0,3.0]],dtype=np.float16)
b = pickle.dumps( arr )

PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200


def main():
    device = DigiMeshDevice(PORT, BAUD_RATE)

    try:
        device.open(force_settings=True)
        device.send_data_64( XBee64BitAddress.from_hex_string("0013A20041AF1B1A"), b )

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
