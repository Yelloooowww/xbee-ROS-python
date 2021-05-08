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

with open('uwb.csv', newline='') as f:
    reader = csv.reader(f)
    uwb_data = list(reader)

raw_x = np.array([float(uwb_data[i][1]) for i in range(1,len(uwb_data))])
raw_y = np.array([float(uwb_data[i][2]) for i in range(1,len(uwb_data))])

corner_x = [raw_x[460], raw_x[1330], raw_x[6075]]
corner_y = [raw_y[460], raw_y[1330], raw_y[6075]]
fig = plt.figure()
plt.scatter(raw_x, raw_y)
plt.scatter(corner_x, corner_y)
plt.colorbar()
plt.ylim(-270,30)
plt.xlim(-150,150)
plt.show()
fig.savefig('uwb/raw_odom')

modify_data = []
tmpx, tmpy = raw_x[460], raw_y[460]
fix = 0
dis = 0
for i in range(460,1330):
    dis += distance(raw_x[i]-tmpx, raw_y[i]-tmpy)
    # print(dis)
    modify_data.append([dis,fix,float(uwb_data[i][3]),\
                                float(uwb_data[i][4]),\
                                float(uwb_data[i][5]),\
                                float(uwb_data[i][6]),\
                                float(uwb_data[i][7]),\
                                float(uwb_data[i][8]),\
                                float(uwb_data[i][9]),\
                                float(uwb_data[i][10]),\
                                float(uwb_data[i][11]),\
                                float(uwb_data[i][12]),\
                                float(uwb_data[i][13]),\
                                float(uwb_data[i][14]),\
                                float(uwb_data[i][15])])
    tmpx = raw_x[i]
    tmpy = raw_y[i]

tmpx, tmpy = raw_x[1330], raw_y[1330]
fix = dis
dis = 0
for i in range(1330,6075):
    dis += distance(raw_x[i]-tmpx, raw_y[i]-tmpy)
    # print(dis)
    modify_data.append([fix,dis,float(uwb_data[i][3]),\
                                float(uwb_data[i][4]),\
                                float(uwb_data[i][5]),\
                                float(uwb_data[i][6]),\
                                float(uwb_data[i][7]),\
                                float(uwb_data[i][8]),\
                                float(uwb_data[i][9]),\
                                float(uwb_data[i][10]),\
                                float(uwb_data[i][11]),\
                                float(uwb_data[i][12]),\
                                float(uwb_data[i][13]),\
                                float(uwb_data[i][14]),\
                                float(uwb_data[i][15])])
    tmpx = raw_x[i]
    tmpy = raw_y[i]

# xbee normalize: (D+90)/(-40+90)*100
carx = [ [] for i in range(2,15)]
cary = [ [] for i in range(2,15)]
carrssi = [ [] for i in range(2,15)]
anchor_list = [26453, 27204, 26380, 27168, 27202, 27151, 27238, 27141, 27258, 27211, 27180, 27208, 27228]
for i in range(len(modify_data)):
    for j in range(2,15):
        if modify_data[i][j]!=0:
            carx[j-2].append(modify_data[i][0])
            cary[j-2].append(modify_data[i][1])
            # uwb normalize:(D+110)/(-80+110)*100
            tmp = (modify_data[i][j]+110)/(-80+110)*100
            if tmp > 100: tmp = 100
            if tmp < 0: tmp = 0
            carrssi[j-2].append(tmp)

print(np.shape(modify_data))
print(np.shape(carx))
print(np.shape(cary))
print(np.shape(carrssi))
# for i in range(len(carx)):
#     fig = plt.figure()
#     plt.scatter(carx[i], cary[i], c=carrssi[i])
#     plt.colorbar()
#     plt.title('UWB normalized RSSI, tag='+str(anchor_list[i]))
#     plt.xlim(-25,175)
#     plt.ylim(-25,175)
#     plt.show()
#     fig.savefig('uwb/'+'UWB_normalized_RSSI_'+str(anchor_list[i]))


#LOS: A0, A04, A17
fig = plt.figure()
#regression
dis_for_regA0 = [distance(carx[2][i]-115,cary[2][i]) for i in range(len(carrssi[2]))]
A0plot, = plt.plot(dis_for_regA0,carrssi[2], marker="^", linestyle='None')
slopeA0, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA0,carrssi[2])
xA0 = np.arange(0,50, 0.01)
lineA0 = slopeA0*xA0+intercept
plt.plot(xA0, lineA0, 'r')
plt.text(20, 108,'y = {:.2f}x + {:.2f}'.format(slopeA0,intercept),  color='r')

dis_for_regA04 = [carx[0][i] for i in range(len(carrssi[0]))]
A04plot, = plt.plot(dis_for_regA04,carrssi[0], marker="*", linestyle='None')
slopeA04, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA04[0:-50],carrssi[0][0:-50])
xA04 = np.arange(0,10, 0.01)
lineA04 = slopeA04*xA04+intercept
plt.plot(xA04, lineA04, 'g')
plt.text(20, 100,'y = {:.2f}x + {:.2f}'.format(slopeA04,intercept),  color='g')

dis_for_regA17 = [distance(0,cary[9][i]-165) for i in range(len(carrssi[9]))]
A17plot, = plt.plot(dis_for_regA17,carrssi[9], marker="+", linestyle='None')
slopeA17, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA17[100:],carrssi[9][100:])
xA17 = np.arange(0,35, 0.01)
lineA17 = slopeA17*xA17+intercept
plt.plot(xA17, lineA17, 'b')
plt.text(20, 92,'y = {:.2f}x + {:.2f}'.format(slopeA17,intercept),  color='b')
plt.hlines((-90+110)/(-80+110)*100,xmin=0,xmax=50)
plt.title('shimen UWB LOS')
plt.xlabel('meter')
plt.ylabel('normalized RSSI')
# plt.legend([A0plot,A04plot,A17plot],['26380','26453','27211'])
plt.show()
fig.savefig('uwb/shimenUWBLOS')


# NLOS: 27168,27202
fig = plt.figure()
dis_for_regA06 = [carx[3][i]-111 for i in range(len(carrssi[3]))]
A06plot, = plt.plot(dis_for_regA06[0:25],carrssi[3][0:25], marker="*", linestyle='None')
slopeA06, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA06[20:25],carrssi[3][20:25])
xA06 = np.arange(2.75,3, 0.01)
lineA06 = slopeA06*xA06+intercept
plt.plot(xA06, lineA06, 'g')
plt.text(1.52, 35,'y = {:.2f}x + {:.2f}'.format(slopeA06,intercept),  color='g')

dis_for_regA = [carx[4][i]-111 for i in range(len(carrssi[4]))]
Aplot, = plt.plot(dis_for_regA[0:25],carrssi[3][0:25], marker="*", linestyle='None')
# slopeA, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA[20:25],carrssi[4][20:25])
# xA = np.arange(2.75,3, 0.01)
# lineA = slopeA*xA+intercept
# plt.plot(xA, lineA, 'g')
# plt.text(6, 80,'y = {:.2f}x + {:.2f}'.format(slopeA,intercept),  color='g')

plt.title('shimen UWB NLOS')
plt.xlabel('meter')
plt.ylabel('normalized RSSI')
plt.legend([A06plot,Aplot],['27168','27202'])
plt.show()
fig.savefig('uwb/shimenUWBNLOS')
