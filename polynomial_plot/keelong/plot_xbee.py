import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats
plt.rcParams.update({'font.size': 36})

def distance(x,y):
    return (x**2 + y**2)**0.5

def reg(x,y):
    coefficients = np.polyfit(x,y,1) # 利用 polyfit 幫我們算出資料 一階擬合的 a, b 參數
    p = np.poly1d(coefficients) # 做出公式, print 的結果是 coefficients[0] * X + coefficients[1]
    #coefficient_of_dermination = r2_score(y, p(x)) // 計算相關係數用，這裡沒有用到
    return coefficients, p

with open('xbee.csv', newline='') as f:
    reader = csv.reader(f)
    xbee_data = list(reader)

raw_x = np.array([float(xbee_data[i][1]) for i in range(1,len(xbee_data))])
raw_y = np.array([float(xbee_data[i][2]) for i in range(1,len(xbee_data))])

corner_x = [-40.82715885,-13.83135566,-27.534702,-32.64521703]
corner_y = [28.46655567,7.171049276,19.07831852,36.47249842]

# fig = plt.figure()
# plt.scatter(raw_x, raw_y)
# plt.plot(corner_x, corner_y, marker='^', color='r', linestyle='None')
# plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
# plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
# plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
# plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
# plt.colorbar()
# plt.xlim(-70,0)
# plt.ylim(-20,50)
# plt.show()
# fig.savefig('xbee/raw_odom')

xbee_rssi = [[] for i in range(8)]
carx = [[] for i in range(8)]
cary = [[] for i in range(8)]
# xbee normalize: (D+90)/(-40+90)*100
for i in range(1,len(xbee_data)):
    for j in range(8):
        if float(xbee_data[i][j+3]) !=0:
            carx[j].append([float(xbee_data[i][1])])
            cary[j].append([float(xbee_data[i][2])])
            xbee_rssi[j].append([(-float(xbee_data[i][j+3])+90)/(-40+90)*100])

xbee_rssi_part = [[] for i in range(8)]
carx_part = [[] for i in range(8)]
cary_part = [[] for i in range(8)]
# xbee normalize: (D+90)/(-40+90)*100
for i in range(50,75):
    for j in range(8):
        if float(xbee_data[i][j+3]) !=0:
            carx_part[j].append(float(xbee_data[i][1]))
            cary_part[j].append(float(xbee_data[i][2]))
            xbee_rssi_part[j].append((-float(xbee_data[i][j+3])+90)/(-40+90)*100)

anchor_list = ['A24','A19','A05','A20','A12','A18','A04','A11']
# for j in range(8):
#     fig = plt.figure()
#     plt.scatter(raw_x, raw_y)
#     plt.scatter(carx[j], cary[j], c=xbee_rssi[j])
#     plt.plot(corner_x, corner_y, marker='^', color='r', linestyle='None')
#     plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
#     plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
#     plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
#     plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
#     plt.colorbar()
#     plt.xlim(-70,0)
#     plt.ylim(-20,50)
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.title('XBee normalize RSSI '+anchor_list[j])
#     plt.show()
#     fig.savefig('xbee/XBee_normalize_RSSI_'+anchor_list[j])






#LOS: A24,A19,A11
fig = plt.figure()
#regression
dis_for_regA24 = [distance(carx_part[0][i]-corner_x[1],cary_part[0][i]-corner_y[1]) for i in range(len(xbee_rssi_part[0]))]
A24plot, = plt.plot(dis_for_regA24,xbee_rssi_part[0], marker="^", linestyle='None',color='r')
A24model = np.poly1d(np.polyfit(dis_for_regA24, xbee_rssi_part[0], 5))
A24line = np.linspace(5, 33, 100)
plt.plot(A24line, A24model(A24line),color='r')

#regression
dis_for_regA19 = [distance(carx_part[1][i]-corner_x[2],cary_part[1][i]-corner_y[2]) for i in range(len(xbee_rssi_part[1]))]
A19plot, = plt.plot(dis_for_regA19,xbee_rssi_part[1], marker="*", linestyle='None', color='g')
A19model = np.poly1d(np.polyfit(dis_for_regA19, xbee_rssi_part[1], 3))
A19line = np.linspace(2.5, 20, 100)
plt.plot(A19line, A19model(A19line),color='g')


#regression
dis_for_regA11 = [distance(carx_part[7][i]-corner_x[0],cary_part[7][i]-corner_y[0]) for i in range(len(xbee_rssi_part[7]))]
A11plot, = plt.plot(dis_for_regA11,xbee_rssi_part[7], marker="+", linestyle='None', color='b')
A11model = np.poly1d(np.polyfit(dis_for_regA11, xbee_rssi_part[7], 3))
A11line = np.linspace(2.5, 30, 100)
plt.plot(A11line, A11model(A11line),color='b')

plt.title('BHCave XBee LOS')
plt.xlabel('meter')
plt.ylabel('normalized RSSI')
plt.legend([A24plot,A19plot,A11plot],['node 4','node 5','node 6'])
# plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
# plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
# plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
# plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
plt.show()
fig.savefig('xbee/BHCave_XBee_LOS')


# #NLOS:A04
# fig = plt.figure()
# carx_part_NLOS,cary_part_NLOS,xbee_rssi_part_NLOS = [[] for i in range(8)], [[] for i in range(8)], [[] for i in range(8)]
# for i in range(26,31):
#     for j in range(8):
#         if float(xbee_data[i][j+3]) !=0:
#             carx_part_NLOS[j].append(float(xbee_data[i][1]))
#             cary_part_NLOS[j].append(float(xbee_data[i][2]))
#             xbee_rssi_part_NLOS[j].append((-float(xbee_data[i][j+3])+90)/(-40+90)*100)
#
# # for j in range(8):
# #     plt.xlim(-70,0)
# #     plt.ylim(-20,50)
# #     plt.scatter(raw_x, raw_y)
# #     plt.scatter(carx_part_NLOS[j],cary_part_NLOS[j],c=xbee_rssi_part_NLOS[j])
# #     plt.plot(corner_x, corner_y, marker='^', color='r', linestyle='None')
# #     plt.title('XBee normalize RSSI '+anchor_list[j])
# #     plt.show()
#
#
# c_A04x, c_A04y = -45.7,36.5
# c_A11x, c_A11y = -49.3,30.8
# #regression
# dis_for_reg_NA04 = [distance(carx_part_NLOS[6][i]-c_A04x,cary_part_NLOS[6][i]-c_A04y) for i in range(len(xbee_rssi_part_NLOS[6]))]
# _NA04plot, = plt.plot(dis_for_reg_NA04,xbee_rssi_part_NLOS[6], marker="+", linestyle='None', color='b')
# slope_NA04, intercept, r_value, p_value, std_err = stats.linregress(dis_for_reg_NA04[1:],xbee_rssi_part_NLOS[6][1:])
# x_NA04 = np.arange(2,5, 0.01)
# line_NA04 = slope_NA04*x_NA04+intercept
# plt.plot(x_NA04, line_NA04, 'b')
# plt.text(1,50,'y = {:.2f}x + {:.2f}'.format(slope_NA04,intercept),  color='b')
#
# #regression
# dis_for_reg_NA11 = [distance(carx_part_NLOS[7][i]-c_A11x,cary_part_NLOS[7][i]-c_A11y) for i in range(len(xbee_rssi_part_NLOS[7]))]
# _NA11plot, = plt.plot(dis_for_reg_NA11,xbee_rssi_part_NLOS[7], marker="*", linestyle='None', color='g')
# slope_NA11, intercept, r_value, p_value, std_err = stats.linregress(dis_for_reg_NA11,xbee_rssi_part_NLOS[7])
# x_NA11 = np.arange(2,5, 0.01)
# line_NA11 = slope_NA11*x_NA11+intercept
# plt.plot(x_NA11, line_NA11, 'g')
# plt.text(1,45,'y = {:.2f}x + {:.2f}'.format(slope_NA11,intercept),  color='g')
# plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
# plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
# plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
# plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
# plt.title('BHCave XBee NLOS')
# plt.xlabel('meter')
# plt.ylabel('normalized RSSI')
# plt.legend([_NA04plot,_NA11plot],['A04','A11'])
# plt.show()
# fig.savefig('xbee/BHCave_XBee_NLOS')
