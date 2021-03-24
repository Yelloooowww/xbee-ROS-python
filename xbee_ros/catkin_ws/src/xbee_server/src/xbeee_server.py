#!/usr/bin/env python3

from digi.xbee.devices import XBeeDevice
from digi.xbee.util import utils
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.models.status import PowerLevel
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice

import sys
sys.path.append('../')

import rospy
from xbee_server.srv import xbee
import random
import time


class XBee_server(object):
    def __init__(self):
        self.PORT = rospy.get_param("~port")
        self.BAUD_RATE = 9600
        self.device = XBeeDevice(self.PORT, self.BAUD_RATE)
        self.device.open(force_settings=True)
        self.service = rospy.Service('xbee', xbee, self.handle_xbee)
        rospy.loginfo("XBee_server init")


    def handle_xbee(self,req):
        ADDRESS_H = '0013A200'
        ADDRESS_L = req.address
        ADDRESS = ADDRESS_H + ADDRESS_L


        try :
            print('send xbee to address:', ADDRESS)
            remote = RemoteXBeeDevice(
                self.device,
                x64bit_addr=XBee64BitAddress.from_hex_string("0013A20041AF1A91"),
                node_id="manually_added")
            self.device.send_data(remote,req.message)
            print("send success")
            return True
        except :
            print("send fail")
            return False

    def on_shutdown(self):
        if self.device is not None and self.device.is_open():
            self.device.close()

if __name__ == "__main__":
    rospy.init_node("xbee_server")

    xbee_server = XBee_server()
    try:
        rospy.spin()
    finally:
        xbee_server.on_shutdown()
