import pickle
import numpy as np
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.exception import *
from digi.xbee.models.address import *
import struct

arr = np.array([[1.0,2.0,3.0], [1.0,2.0,3.0], [1.0,2.0,3.0]], dtype=np.float16)
byte_arr = pickle.dumps(arr)

pack = bytearray(b'0xAB') #Header
pack.extend(bytearray(b'0x01')) #Type
pack.extend( byte_arr[0:5] ) #data

print(pack[0:4])
print(pack[4:8])
print(pack[8:])

tmp = bytearray()
tmp.extend(pack[8:])

pack = bytearray(b'0xAB') #Header
pack.extend(bytearray(b'0x01')) #Type
pack.extend( byte_arr[5:] ) #data
print(pack[0:4])
print(pack[4:8])
print(pack[8:])
tmp.extend(pack[8:])
print( pickle.loads(tmp) )


print(len(byte_arr))
print(byte_arr[0:175])
