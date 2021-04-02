import pickle
import numpy as np
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *
import struct

arr = np.array([[1.0,2.0,3.0], [1.0,2.0,3.0], [1.0,2.0,3.0]], dtype=np.float16)
byte_arr = pickle.dumps(arr)

pack = bytearray(b'0xAB') #Header
size = ( len(byte_arr) ).to_bytes(4, byteorder='big')
print(size)
print(int.from_bytes( size, byteorder="big",signed=False))

pack = bytearray(b'\xAB') #Header
pack.extend(bytearray(b'\x01')) #Type
pack.extend( size ) #bytes
pack.extend( byte_arr ) #data
print(pack[0:1])
print(pack[1:2])
print(pack[2:6])
print(int.from_bytes(pack[2:6], byteorder="big",signed=False))
print(pack[6:])
print( pickle.loads(pack[6:]) )
#
#
# print(len(byte_arr))
# print(byte_arr[0:175])
