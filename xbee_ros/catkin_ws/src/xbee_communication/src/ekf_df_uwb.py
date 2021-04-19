#!/usr/bin/env python
import roslib
import rospy
import message_filters
import numpy as np
import math
from tf import transformations as tr
import tf
from geometry_msgs.msg import PoseStamped, TransformStamped
import matplotlib.pyplot as plt
import time


# # Covariance for EKF simulation
# Q = np.diag([
# 		0.005,  # variance of location on x-axis
# 		0.005,  # variance of location on y-axis
# 		0.1,  # variance of yaw angle
# 		]) ** 2  # predict state covariance
# R = np.diag([1.0, 1.0]) ** 2  # Observation x,y position covariance

# DT = 0.1  # time tick [s]
# SIM_TIME = 50.0  # simulation time [s]

# show_animation = True

# State Vector [x y yaw]'
xEst = np.zeros((3, 1))
xTrue = np.zeros((3, 1))
PEst = np.eye(3)

xDR = np.zeros((3, 1))  # Dead reckoning

# history
hxEst = xEst
hxTrue = xTrue
hxDR = xTrue
hz = np.zeros((2, 1))



class EkfSbl(object):
	def __init__(self):
		super(EkfSbl, self).__init__()
		# subscriber
		self.sub = rospy.Subscriber('/0x6a45/localize/local_tag_pose', PoseStamped, self.point_cb, queue_size = 3)
		self.x_last = None
		self.y_last = None

	def point_cb(self, point_msg):
		global xEst, PEst, hxEst, hxDR, hxTrue, hz

		if point_msg.pose.position.x == 0 and point_msg.pose.position.y == 0:
			return

		if (self.x_last == None) and (self.y_last == None):
			print('init value')
			(self.x_last, self.y_last) = (point_msg.pose.position.x, point_msg.pose.position.y)
			quaternion = (point_msg.pose.orientation.x,point_msg.pose.orientation.y,point_msg.pose.orientation.z,point_msg.pose.orientation.w)
			euler = tf.transformations.euler_from_quaternion(quaternion)
			self.yaw_last = euler[2]

			xEst = np.array([[self.x_last],[self.y_last],[self.yaw_last]])
			p_t = np.eye(3)
			p_t[2, 0] = 0.75
			hxEst = xEst
			PEst = p_t
			return

		else :
			x, y = point_msg.pose.position.x, point_msg.pose.position.y
			quaternion = (point_msg.pose.orientation.x,point_msg.pose.orientation.y,point_msg.pose.orientation.z,point_msg.pose.orientation.w)
			euler = tf.transformations.euler_from_quaternion(quaternion)
			yaw = euler[2]
			u = np.array([[(x-self.x_last)*0.1], [(y-self.y_last)*0.1], [(yaw-self.yaw_last)*0.1]])
			z = [[x],[y]]

			xEst, PEst = self.ekf_estimation(xEst, PEst, z, u)
			print('z,xEst',z,xEst)

			# store data history
			hxEst = np.hstack((hxEst, xEst))
			hxDR = np.hstack((hxDR, xDR))
			hxTrue = np.hstack((hxTrue, xTrue))
			hz = np.hstack((hz, z))

			# if show_animation:
			plt.cla()
			# for stopping simulation with the esc key.
			plt.gcf().canvas.mpl_connect('key_release_event',
					lambda event: [exit(0) if event.key == 'escape' else None])
			plt.plot(hz[0, :].flatten(),hz[1, :].flatten(), ".g")
			plt.plot(hxEst[0, :].flatten(),hxEst[1, :].flatten(), "-r")
			plt.axis("equal")
			plt.grid(True)
			plt.pause(0.001)
			# time.sleep(0.1)



	def motion_model(self, x, u):
		F = np.array([[1.0, 0, 0],
					[0, 1.0, 0],
					[0, 0, 1.0]])

		# We have input respect to xt
		# Remeber to transform to be respect to map
		B = np.array([[math.cos(x[2]), 0, 0],
					[math.sin(x[2]), 0, 0],
					[0.0, 0.0, 1.0]])

		# x_pred = np.matmul(F,x) + np.matmul(B,u)
		x_pred = np.matmul(F,x)
		return x_pred


	def observation_model(self, x):
		H = np.array([
			[1, 0, 0],
			[0, 1, 0]
		])
		z = np.matmul(H, x) # z = H @ x
		return z

	def jacob_f(self, x, u):
		yaw = x[2,0]
		dx = u[0,0]
		dyaw = u[2,0]
		jF = np.array([
			[1.0, 0.0, -1*dx*math.sin(yaw)],
			[0.0, 1.0, dx*math.cos(yaw)],
			[0.0, 0.0, 1.0]])

		return jF


	def jacob_h(self):
		jH = np.array([
			[1, 0, 0],
			[0, 1, 0]
		])

		return jH


	def ekf_estimation(self, xEst, PEst, z, u):
		Q = np.diag([
				0.005,  # variance of location on x-axis
				0.005,  # variance of location on y-axis
				0.1,  # variance of yaw angle
				]) ** 2  # predict state covariance
		R = np.diag([1, 3]) ** 2

		xPred = self.motion_model(xEst, u)
		jF = self.jacob_f(xEst, u)
		jH = self.jacob_h()
		zPred = self.observation_model(xPred)
		PPred = np.matmul(np.matmul(jF, PEst), jF.T) + Q # PPred = jF @ PEst @ jF.T + Q
		S = np.matmul(np.matmul(jH,PPred),np.transpose(jH)) + R
		K = np.matmul(np.matmul(PPred,jH.T),np.linalg.inv(S))
		y = z - zPred
		xEst = xPred + np.matmul(K,y)
		PEst = np.matmul((np.eye(len(xEst)) - np.matmul(K,jH)),PPred)

		return xEst, PEst



if __name__ == '__main__':
	try :
		rospy.init_node('ekf_pozyx_node',anonymous=False)
		ekf = EkfSbl()
		rospy.spin()
	finally:
		plt.close('all')
