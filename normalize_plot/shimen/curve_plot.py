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

with open('xbee_shimen_202009.csv', newline='') as f:
    reader = csv.reader(f)
    xbee_data = list(reader)

raw_x = np.array([float(xbee_data[i][1]) for i in range(1,len(xbee_data))])
raw_y = np.array([float(xbee_data[i][2]) for i in range(1,len(xbee_data))])

corner1 = np.array(raw_x[15], raw_y[15])
corner2 = np.array(raw_x[75], raw_y[75])
corner3 = np.array(raw_x[162], raw_y[162])

corner_x = [raw_x[15], raw_x[75], raw_x[162]]
corner_y = [raw_y[15], raw_y[75], raw_y[162]]

plt.scatter(raw_x, raw_y)
plt.scatter(corner_x, corner_y)
plt.colorbar()
plt.ylim(-270,30)
plt.xlim(-150,150)
plt.show()

modify_data = []
tmpx, tmpy = raw_x[15], raw_y[15]
fix = 0
dis = 0
for i in range(15,75):
    dis += distance(raw_x[i]-tmpx, raw_y[i]-tmpy)
    # print(dis)
    modify_data.append([dis,fix,float(xbee_data[i][3]),\
                                float(xbee_data[i][4]),\
                                float(xbee_data[i][5]),\
                                float(xbee_data[i][6]),\
                                float(xbee_data[i][7]),\
                                float(xbee_data[i][8]),\
                                float(xbee_data[i][9]),\
                                float(xbee_data[i][10]),\
                                float(xbee_data[i][11]),\
                                float(xbee_data[i][12]),\
                                float(xbee_data[i][13]),\
                                float(xbee_data[i][14]),\
                                float(xbee_data[i][15]),\
                                float(xbee_data[i][16]),\
                                float(xbee_data[i][17])])
    tmpx = raw_x[i]
    tmpy = raw_y[i]

tmpx, tmpy = raw_x[75], raw_y[75]
fix = dis
dis = 0
for i in range(75,162):
    dis += distance(raw_x[i]-tmpx, raw_y[i]-tmpy)
    # print(dis)
    modify_data.append([fix,dis,float(xbee_data[i][3]),\
                                float(xbee_data[i][4]),\
                                float(xbee_data[i][5]),\
                                float(xbee_data[i][6]),\
                                float(xbee_data[i][7]),\
                                float(xbee_data[i][8]),\
                                float(xbee_data[i][9]),\
                                float(xbee_data[i][10]),\
                                float(xbee_data[i][11]),\
                                float(xbee_data[i][12]),\
                                float(xbee_data[i][13]),\
                                float(xbee_data[i][14]),\
                                float(xbee_data[i][15]),\
                                float(xbee_data[i][16]),\
                                float(xbee_data[i][17])])
    tmpx = raw_x[i]
    tmpy = raw_y[i]

# xbee normalize: (D+90)/(-40+90)*100
carx = [ [] for i in range(2,17)]
cary = [ [] for i in range(2,17)]
carrssi = [ [] for i in range(2,17)]
anchor_list = ['A0','A01','A02','A04','A06','A10','A9','A11','A12','A15','A16','A17','A19','A20','A24']
for i in range(len(modify_data)):
    for j in range(2,17):
        if modify_data[i][j]!=0:
            carx[j-2].append(modify_data[i][0])
            cary[j-2].append(modify_data[i][1])
            carrssi[j-2].append((-modify_data[i][j]+90)/(-40+90)*100)

print(np.shape(modify_data))
print(np.shape(carx))
print(np.shape(cary))
print(np.shape(carrssi))
# for i in range(len(carx)):
#     plt.scatter(carx[i], cary[i], c=carrssi[i])
#     plt.colorbar()
#     plt.title('XBee normalized RSSI '+anchor_list[i])
#     plt.xlim(-25,175)
#     plt.ylim(-25,175)
#     plt.show()


#LOS: A0, A04, A17
#regression
dis_for_regA0 = [distance(carx[0][i]-115,cary[0][i]) for i in range(len(carrssi[0]))]
plt.scatter(dis_for_regA0,carrssi[0])
slopeA0, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA0,carrssi[0])
xA0 = np.arange(0,170, 0.01)
lineA0 = slopeA0*xA0+intercept
plt.plot(xA0, lineA0, 'r')
plt.text(24, 14,'y = {:.2f}x + {:.2f}'.format(slopeA0,intercept),  color='r')
plt.show()
# reg_uwb_A19dis,reg_uwb_A19rssi = [], []
# for i,item in enumerate(uwb_A19dis) :
#     if item < 20:
#         reg_uwb_A19dis.append(uwb_A19dis[i])
#         reg_uwb_A19rssi.append(uwb_A19rssi[i])
# slopeuwb_A19, intercept, r_value, p_value, std_err = stats.linregress(reg_uwb_A19dis,reg_uwb_A19rssi)
# xuwb_A19 = np.arange(0,20, 0.01)
# lineuwb_A19 = slopeuwb_A19*xuwb_A19+intercept
# plt.plot(xuwb_A19, lineuwb_A19, 'r')
# plt.text(24, 14,'y = {:.2f}x + {:.2f}'.format(slopeuwb_A19,intercept),  color='r')
