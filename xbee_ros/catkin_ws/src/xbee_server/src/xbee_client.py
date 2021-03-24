#!/usr/bin/env python3

import rospy
from xbee_server.srv import xbee
import random
import time
import sys


if __name__ == "__main__":
    if len(sys.argv) == 3:
        add = str(sys.argv[1])
        msg = str(sys.argv[2])
    else:
        print('input error')
        sys.exit(1)

    rospy.wait_for_service('xbee')
    try:
        handle_xbee = rospy.ServiceProxy('xbee', xbee)
        result = handle_xbee(add, msg)
        print(result)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
