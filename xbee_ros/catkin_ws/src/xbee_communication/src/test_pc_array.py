#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Float32, Int32
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs import point_cloud2
import struct
import roslib
import pickle
import time

class XBee(object):
	def __init__(self):
		self.raw_point = []
		self.sub_points = rospy.Subscriber("/velodyne1/velodyne_points", PointCloud2, self.cb_points, queue_size=1)
		self.pub_points = rospy.Publisher("pub_points", PointCloud2, queue_size=1)

		print("initialized")

	# for robot
	def cb_points(self, msg): # PointCloud2 to numpy
		cloud_points = []
		for p in point_cloud2.read_points(msg, field_names = ("x", "y", "z"), skip_nans=True):
			cloud_points.append(p)
		self.raw_point = np.array(cloud_points, dtype=np.float16)

		msgggg = self.xyzrgb_array_to_pointcloud2(self.raw_point, frame_id="base_link")
		self.pub_points.publish(msgggg)
		print('pubbbbbbbbbbbbbbbbbbbbbbbbb')


	def xyzrgb_array_to_pointcloud2(self, points, frame_id=None):
		'''
		Create a sensor_msgs.PointCloud2 from an array
		of points.
		'''
		msg = PointCloud2()

		buf = []


		msg.header.frame_id = frame_id
		if len(points.shape) == 3:
			msg.height = points.shape[1]
			msg.width = points.shape[0]
		else:
			N = len(points)
			xyzrgb = np.array(np.hstack([points]), dtype=np.float32)
			msg.height = 1
			msg.width = N

		msg.fields = [
			PointField('x', 0, PointField.FLOAT32, 1),
			PointField('y', 4, PointField.FLOAT32, 1),
			PointField('z', 8, PointField.FLOAT32, 1)
		]
		msg.is_bigendian = False
		msg.point_step = 12
		msg.row_step = msg.point_step * N
		msg.is_dense = True
		msg.data = xyzrgb.tostring()

		return msg






if __name__ == "__main__":
	rospy.init_node("xbee_node")
	xbee_node = XBee()
	rospy.spin()
