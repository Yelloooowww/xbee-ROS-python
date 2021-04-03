# XBee Communication
## How to run (ROS server)
### System setting
check port `ls /dev/ttyUSB*`

change mode `sudo chmod 777 /dev/ttyUSB0`

### Data packet design
the only one or the last one data packet

| Header | type | bytes | bytes | bytes | bytes | realdata | ...... | realdata | checksun |
|--------|------|-------|-------|-------|-------|----------|--------|----------|----------|

else (not the last one)

| Header | type | bytes | bytes | bytes | bytes | realdata | ...... | realdata |
|--------|------|-------|-------|-------|-------|----------|--------|----------|

+ Header `b'\xAB'`
+ type
  + string msg `b'\x00'`
  + points `b'\x01'`
  + pose `b'\x02'`
  + goal `b'\x03'`
+ bytes `total length (bytes) of real data`


### Usage (robot)
launch server node

`roslaunch xbee_communication xbee_server.launch port:="/dev/ttyUSB0"`

### Usage (base station)
#### Auto
launch server node

`roslaunch xbee_communication xbee_server.launch port:="/dev/ttyUSB0" auto_ask_flag:=True`

The server node will keep updating a table (dictionary) with a timer function

|        | husky1 | husky2 | jackal1 | jackal2 |
|--------|--------|--------|---------|---------|
| Points |        |        |         |         |
| Pose   |        |        |         |         |

#### Manual
##### Terminal 1
launch server node

`roslaunch xbee_communication xbee_server.launch port:="/dev/ttyUSB0"`
##### Terminal 2
send a string (HIHIHI) to a robot or a device with specific address

`rosrun xbee_communication xbee_client.py husky1 HIHIHI` or `rosrun xbee_communication xbee_client.py 41AF1A91 HIHIHI`

ask a robot or a device with specific address to send the points data

`rosrun xbee_communication xbee_client.py husky1 AskPoints` or `rosrun xbee_communication xbee_client.py 41AF1A91 AskPoints`

ask a robot or a device with specific address to send the pose data

`rosrun xbee_communication xbee_client.py husky1 AskPose` or `rosrun xbee_communication xbee_client.py 41AF1A91 AskPose`

ask a robot or a device with specific address to move to the goal (1.23,-5.43,0.79)

`rosrun xbee_communication xbee_client.py husky1 Move 1.23 -5.43 0.79` or `rosrun xbee_communication xbee_client.py 41AF1A91 Move 1.23 -5.43 0.79`
