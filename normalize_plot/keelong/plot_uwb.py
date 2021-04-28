# 27183 -> A11
# 27157 -> A24
# 27180 -> A19
# 26453 -> A04

import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats
# plt.rcParams.update({'font.size': 36})

def distance(x,y):
    return (x**2 + y**2)**0.5

def reg(x,y):
    coefficients = np.polyfit(x,y,1) # 利用 polyfit 幫我們算出資料 一階擬合的 a, b 參數
    p = np.poly1d(coefficients) # 做出公式, print 的結果是 coefficients[0] * X + coefficients[1]
    #coefficient_of_dermination = r2_score(y, p(x)) // 計算相關係數用，這裡沒有用到
    return coefficients, p

with open('uwb1.csv', newline='') as f:
    reader = csv.reader(f)
    uwb_data = list(reader)

raw_x = np.array([float(uwb_data[i][1]) for i in range(1,len(uwb_data))])
raw_y = np.array([float(uwb_data[i][2]) for i in range(1,len(uwb_data))])

corner_x = [-40.82715885,-13.83135566,-27.534702,-32.64521703]
corner_y = [28.46655567,7.171049276,19.07831852,36.47249842]

fig = plt.figure()
plt.scatter(raw_x, raw_y)
plt.plot(corner_x, corner_y, marker='^', color='r', linestyle='None')
plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
plt.colorbar()
plt.xlim(-70,0)
plt.ylim(-20,50)
plt.show()
fig.savefig('uwb/raw_odom')

uwb_rssi = [[] for i in range(7)]
carx = [[] for i in range(7)]
cary = [[] for i in range(7)]
# uwb normalize: (D+90)/(-40+90)*100
for i in range(1,len(uwb_data)):
    for j in range(7):
        if float(uwb_data[i][j+3]) !=0:
            carx[j].append([float(uwb_data[i][1])])
            cary[j].append([float(uwb_data[i][2])])
            tmp = (float(uwb_data[i][j+3])+110)/(-80+110)*100
            if tmp > 100:tmp = 100
            if tmp < 0 :tmp = 0
            uwb_rssi[j].append(tmp)

uwb_rssi_part = [[] for i in range(8)]
carx_part = [[] for i in range(8)]
cary_part = [[] for i in range(8)]
# uwb normalize:(D+110)/(-80+110)*100
for i in range(750,1300):
    for j in range(7):
        if float(uwb_data[i][j+3]) !=0:
            carx_part[j].append(float(uwb_data[i][1]))
            cary_part[j].append(float(uwb_data[i][2]))
            tmp = (float(uwb_data[i][j+3])+110)/(-80+110)*100
            if tmp > 100:tmp = 100
            if tmp < 0 :tmp = 0
            uwb_rssi_part[j].append(tmp)

anchor_list = ['26453(A04)', '27170', '27183(A11)', '27157(A24)', '27180(A19)', '27141', '27160']
for j in range(7):
    fig = plt.figure()
    plt.scatter(raw_x, raw_y)
    plt.scatter(carx[j], cary[j], c=uwb_rssi[j])
    plt.plot(corner_x, corner_y, marker='^', color='r', linestyle='None')
    plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
    plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
    plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
    plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
    plt.colorbar()
    plt.xlim(-70,0)
    plt.ylim(-20,50)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('uwb normalize RSSI '+anchor_list[j])
    plt.show()
    fig.savefig('uwb/uwb_normalize_RSSI_'+anchor_list[j])






#LOS: A24,A19,A11
fig = plt.figure()
#regression
dis_for_regA24 = [distance(carx_part[3][i]-corner_x[1],cary_part[3][i]-corner_y[1]) for i in range(len(uwb_rssi_part[3]))]
A24plot, = plt.plot(dis_for_regA24,uwb_rssi_part[3], marker="^", linestyle='None',color='r')
slopeA24, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA24,uwb_rssi_part[3])
xA24 = np.arange(2,30, 0.01)
lineA24 = slopeA24*xA24+intercept
plt.plot(xA24, lineA24, 'r')
plt.text(18,85,'y = {:.2f}x + {:.2f}'.format(slopeA24,intercept),  color='r')

#regression
dis_for_regA19 = [distance(carx_part[4][i]-corner_x[2],cary_part[4][i]-corner_y[2]) for i in range(len(uwb_rssi_part[4]))]
A19plot, = plt.plot(dis_for_regA19,uwb_rssi_part[4], marker="*", linestyle='None', color='g')
slopeA19, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA19,uwb_rssi_part[4])
xA19 = np.arange(0,12.5, 0.01)
lineA19 = slopeA19*xA19+intercept
plt.plot(xA19, lineA19, 'g')
plt.text(18,80,'y = {:.2f}x + {:.2f}'.format(slopeA19,intercept),  color='g')

#regression
dis_for_regA11 = [distance(carx_part[2][i]-corner_x[0],cary_part[2][i]-corner_y[0]) for i in range(len(uwb_rssi_part[2]))]
A11plot, = plt.plot(dis_for_regA11,uwb_rssi_part[2], marker="+", linestyle='None', color='b')
slopeA11, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA11,uwb_rssi_part[2])
xA11 = np.arange(0,7.5, 0.01)
lineA11 = slopeA11*xA11+intercept
plt.plot(xA11, lineA11, 'b')
plt.text(18,75,'y = {:.2f}x + {:.2f}'.format(slopeA19,intercept),  color='b')

plt.title('BHCave uwb LOS')
plt.xlabel('meter')
plt.ylabel('normalized RSSI')
plt.legend([A24plot,A19plot,A11plot],['A24','A19','A11'])
plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
plt.show()
fig.savefig('uwb/BHCave_uwb_LOS')


#NLOS:A04
fig = plt.figure()
carx_part_NLOS,cary_part_NLOS,uwb_rssi_part_NLOS = [[] for i in range(7)], [[] for i in range(7)], [[] for i in range(7)]
for i in range(2740,2800):
    for j in range(7):
        if float(uwb_data[i][j+3]) !=0:
            carx_part_NLOS[j].append(float(uwb_data[i][1]))
            cary_part_NLOS[j].append(float(uwb_data[i][2]))
            tmp = (float(uwb_data[i][j+3])+110)/(-80+110)*100
            if tmp > 100:tmp = 100
            if tmp < 0 :tmp = 0
            uwb_rssi_part_NLOS[j].append(tmp)

# for j in range(7):
#     plt.xlim(-70,0)
#     plt.ylim(-20,50)
#     plt.scatter(raw_x, raw_y)
#     plt.scatter(carx_part_NLOS[j],cary_part_NLOS[j],c=uwb_rssi_part_NLOS[j])
#     plt.plot(corner_x, corner_y, marker='^', color='r', linestyle='None')
#     plt.title('uwb normalize RSSI '+anchor_list[j])
#     plt.show()


c_A04x, c_A04y = -45.7,36.5
c_A11x, c_A11y = -49.3,30.8
#regression
dis_for_reg_NA04 = [distance(carx_part_NLOS[0][i]-c_A04x,cary_part_NLOS[0][i]-c_A04y) for i in range(len(uwb_rssi_part_NLOS[0]))]
_NA04plot, = plt.plot(dis_for_reg_NA04,uwb_rssi_part_NLOS[0], marker="+", linestyle='None', color='b')
slope_NA04, intercept, r_value, p_value, std_err = stats.linregress(dis_for_reg_NA04,uwb_rssi_part_NLOS[0])
x_NA04 = np.arange(0,5, 0.01)
line_NA04 = slope_NA04*x_NA04+intercept
plt.plot(x_NA04, line_NA04, 'b')
plt.text(1,50,'y = {:.2f}x + {:.2f}'.format(slope_NA04,intercept),  color='b')

plt.text(corner_x[0]+1,corner_y[0]+1,'A11',  color='r')
plt.text(corner_x[1]+1,corner_y[1]+1,'A24',  color='r')
plt.text(corner_x[2]+1,corner_y[2]+1,'A19',  color='r')
plt.text(corner_x[3]+1,corner_y[3]+1,'A04',  color='r')
plt.title('BHCave uwb NLOS')
plt.xlabel('meter')
plt.ylabel('normalized RSSI')
plt.legend([_NA04plot],['A04'])
plt.show()
fig.savefig('uwb/BHCave_uwb_NLOS')
