# XBee Communication

This package allows you to transfer Apriltags messages or SubTInfo (artifacts poses + robots poses) with XBee modules.

Note: Please use the spelling 'XBee' with capital X and B in any formal documents.

## How to run (One to One)
### Give XBee a static usb port /dev/xbee
Do it on every machine you wanna use XBee
```
$ source set_xbee_port.sh
```

### On the machine sending messages
```
$ rosrun xbee_communication xbee_encoder
```
another terminal
```
$ python3 misc/xbee_operation.py
```
### On the machine receiving messages
```
$ rosrun xbee_communication xbee_decoder
```
another terminal
```
$ python3 misc/xbee_operation.py
```

## How to run (Mesh)
### Give XBee a static usb port /dev/xbee
Do it on every machine you wanna use XBee
```
$ source set_xbee_port.sh
```

### On the machine sending messages
```
$ rosrun xbee_communication xbee_encoder
```
another terminal
```
$ python3 misc/xbee_mesh_robot.py
```
### On the mesh nodes machines
```
$ python3 misc/xbee_mesh.py
```
### On the machine receiving messages
```
$ rosrun xbee_communication xbee_decoder
```
another terminal
```
$ python3 misc/xbee_mesh_base.py
```

## Topic info
### On machine sending messages

Subscribe:
```
# Apriltags Detection Array - type: AprilTagDetectionArray
topic:
/tag_detections

# SubT info (robot pose + artifact pose) - type: SubTInfo
topic:
/subt_info
```

### On machine receiving messages

Publish:
```
# Apriltags Detection Array - type: AprilTagDetectionArray
topic:
/apriltags_from_xbee

# SubT info (robot pose + artifact pose) - type: SubTInfo
topic:
/xBee_subt_info

# Artifact Pose - type: ArtifactPoseArray
topic:
/artifact_pose_list
```


## How to run (ROS server)
### System setting
check port

`ls /dev/ttyUSB*`

change mode

`sudo chmod 777 /dev/ttyUSB0`

### Data packet design
the only one or the last one data packet

| Header | type | bytes | bytes | bytes | bytes | realdata | ...... | realdata |
|--------|------|-------|-------|-------|-------|----------|--------|----------|

else (not the last one)

| Header | type | bytes | bytes | bytes | bytes | realdata | ...... | realdata | checksun |
|--------|------|-------|-------|-------|-------|----------|--------|----------|----------|

### Usage (robot)
launch server node

`roslaunch xbee_communication xbee_server.launch port:="/dev/ttyUSB0"`

### Usage (base station)
launch server node

`roslaunch xbee_communication xbee_server.launch port:="/dev/ttyUSB0"`

send a string (HIHIHI) to a device with specific address (41AF1A91)

`rosrun xbee_communication xbee_client.py 41AF1A91 HIHIHI`

ask a device with specific address (41AF1A91) to send the points data

`rosrun xbee_communication xbee_client.py 41AF1A91 AskPoints`

ask a device with specific address (41AF1A91) to send the pose data

`rosrun xbee_communication xbee_client.py 41AF1A91 AskPose`

ask a device with specific address (41AF1A91) to move to the goal (1.23,-5.43,0.79)

`rosrun xbee_communication xbee_client.py 41AF1A91 Move 1.23 -5.43 0.79`
