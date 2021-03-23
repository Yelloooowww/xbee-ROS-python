#!/usr/bin/env python3

import rospy
from subt_msgs.srv import xbee
import random
import time


if __name__ == "__main__":
    if len(sys.argv) == 3:
        add = str(sys.argv[1])
        msg = str(sys.argv[2])
    else:
        print('input error')
        sys.exit(1)

    rospy.wait_for_service('handle_xbee')
    try:
        handle_xbee = rospy.ServiceProxy('handle_xbee', xbee)
        result = handle_xbee(add, msg)
        print(result)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
