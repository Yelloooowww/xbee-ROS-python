# XBee Communication

## How to run (ROS server)

### send messages to a specify device

check port

`ls /dev/ttyUSB*`

change mode

`sudo chmod 777 /dev/ttyUSB0`

launch server node

`roslaunch xbee_communication xbee_server.launch port:="/dev/ttyUSB0"`

send a string "MSG_FROM_ROS" to a device with 64-bit address (0013A20041AF1A91)

`rosrun xbee_communication xbee_client.py 41AF1A91 MSG_FROM_ROS`
