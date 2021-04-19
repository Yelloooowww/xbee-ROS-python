#!/usr/bin/env python3
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *
from datetime import datetime

device = DigiMeshDevice("/dev/ttyUSB0", 115200)
device.open(force_settings=True)
device.send_data_broadcast("Hihi")
