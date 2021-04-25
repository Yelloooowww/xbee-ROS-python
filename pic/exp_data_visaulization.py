import matplotlib.pyplot as plt
import numpy as np

# x = np.linspace(0,10,31)
#
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
#
# #Plot analytic solution
# ax.plot(x,2*x**2, color='b', label="husky path")
# ax.plot(x,1*x**2, color='r', label="jackal path")
# #Plot simulation
# ax.plot(x,3*x**2, color='yellow', linestyle='', marker='o', label="husky map")
# ax.plot(x,4*x**2, color='lime', linestyle='', marker='o', label="jackal map")
#
# N = 45
# x, y = np.random.rand(2, N)
# c = np.random.randint(1, 5, size=N)
# s = np.random.randint(10, 220, size=N)
#
#
# #Get artists and labels for legend and chose which ones to display
# handles, labels = ax.get_legend_handles_labels()
# display = (0,1,2)
# ax.legend()
# ax.set_facecolor('xkcd:salmon')
# ax.set_facecolor((0,0,0))
#
# plt.show()



# y = [40,48,44,45,43,55,46,48,50,44,57,55,48,57,58,56,60,59,57,58,59,66]
# x = [i for i in range(22)]
# plt.plot(x, y, marker="s")
# plt.xlabel("meters beyond the corner ")
# plt.ylabel("RSSI")
# plt.title("xbee RSSI")
# plt.show()

# y = [5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5222.4,3072.0,3993.6,3276.8,3481.6,3174.4,3379.2,3276.8,3993.6,3686.4,3788.8,3891.2,102.4,0]
# x = [i for i in range(22)]
# plt.plot(x, y, marker="s")
# plt.xlabel("meters beyond the corner ")
# plt.ylabel("bytes per second")
# plt.title("xbee transition speed")
# plt.show()


y = [5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5222.4,3072.0,3993.6,3276.8,3481.6,3174.4,3379.2,3276.8,3993.6,3686.4,3788.8,3891.2,102.4,0]
x = [40,48,44,45,43,55,46,48,50,44,57,55,48,57,58,56,60,59,57,58,59,66]
plt.plot(x, y, marker="s")
plt.xlabel("RSSI")
plt.ylabel("bytes per second")
plt.title("xbee RSSI v.s. transition speed")
plt.show()
y = [5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5324.8,5222.4,3072.0,3993.6,3276.8,3481.6,3174.4,3379.2,3276.8,3993.6,3686.4,3788.8,3891.2,102.4,0]
x = [i for i in range(22)]
plt.plot(x, y, marker="s")
plt.xlabel("meters beyond the corner ")
plt.ylabel("bytes per second")
plt.title("xbee transition speed")
plt.show()




# # Fixing random state for reproducibility
# np.random.seed(19680801)
#
#
#
# N = 50
# x = np.random.rand(N)
# y = np.random.rand(N)
# colors = np.random.rand(N)
# area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
#
# plt.scatter(x, y, s=area, c=colors, alpha=0.5)
# plt.show()

# anchor_x = [10*2,10*2+28,10*2]
# anchor_y = [-1.75,1.75,2*26+1.75]
#
# startx = [1]
# starty = [1]
#
# x1 = [2*i for i in range(37)]
# x2 = [10*2 for i in range(26)]
# x3 = [10*2-2*i for i in range(13)]
# y1 = [0 for i in range(37)]
# y2 = [2*i for i in range(26)]
# y3 = [2*26 for i in range(13)]
#
# rssi = [40,40,40,40,40, \
#         40,40,40,40,44, \
#         44,40,40,41,40, \
#         40,44,42,45,40, \
#         52,52,53,51,48, \
#         48,48,58,51,47, \
#         42,43,49,44,46, \
#         43,43,44,45,43, \
#         41,60,68,54,59, \
#         59,60,62,69,60, \
#         64,66,99,99,67,\
#         ]
# rssi = rssi + [99 for i in range(21)]
#
# x = np.array(x1 + x2 + x3)
# y = np.array(y1 + y2 + y3)
# x, y = -1*x, -1*y #rotate
# anchor_x, anchor_y = -1*np.array(anchor_x), -1*np.array(anchor_y)
#
# plt.scatter(anchor_x, anchor_y, color='k', marker='^')
# plt.scatter(startx, starty, color='c', marker='*')
# plt.scatter(x, y, c=rssi, cmap='RdYlGn')
# plt.colorbar()
# plt.title("xbee RSSI")
# plt.axis('off')
# plt.legend(['node','start point(base station)'])
# plt.show()
# #
# #
# speed = [7987.2 for i in range(12)]
# speed = speed + [ 7884.8,7884.8,7987.2,7987.2,7987.2, \
#                   7680.0,7680.0,7884.8,7065.6,7270.4, \
#                   7680.0,6860.8,7782.4,7475.2,5836.8, \
#                   3174.4,1843.2,2969.6,7270.4,6041.6, \
#                   6348.8,7270.4,7680.0,7475.2,3584.0, \
#                   7782.4,1024.0,1228.8,2048.0,5120.6, \
#                   5222.4,5222.4,5120.0,5120.0,5120.0, \
#                   5222.4,5120.0,5222.4,5222.4,5222.4, \
#                   5120.0,5120.0,5120.0,5120.0,5017.6, \
#                   5017.6,5120.0,5017.6,5120.0,4812.8, \
#                   3481.6,3788.8,3686.4,3891.2,3788.8, \
#                   3891.2,3788.8,3686.4,3891.2,3788.8, \
#                   3686.4,3584.0,3584.0,3584.0]
#
# plt.scatter(anchor_x, anchor_y, color='k', marker='^')
# plt.scatter(startx, starty, color='c', marker='*')
# plt.scatter(x, y, c=speed, cmap='hsv')
# plt.colorbar()
# plt.title("xbee transition speed (bytes per second)")
# plt.axis('off')
# plt.legend(['node','start point(base station)'])
# plt.show()


# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import numpy as np
# img=mpimg.imread('/home/yellow/Pictures/rviz_screenshot_2021_04_23-14_41_50.png')
# imgplot = plt.imshow(img,extent=(60,-22, 25, -22.5))
# plt.xlabel("x(m)")
# plt.ylabel("y(m)")
# plt.show()
