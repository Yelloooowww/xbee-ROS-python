import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats
plt.rcParams.update({'font.size': 36})

def distance(x,y):
    return (x**2 + y**2)**0.5

with open('uwb.csv', newline='') as f:
    reader = csv.reader(f)
    uwb_data = list(reader)

raw_x = np.array([float(uwb_data[i][1]) for i in range(1,len(uwb_data))])
raw_y = np.array([float(uwb_data[i][2]) for i in range(1,len(uwb_data))])

corner_x = [raw_x[460], raw_x[1330], raw_x[6075]]
corner_y = [raw_y[460], raw_y[1330], raw_y[6075]]

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


# NLOS: 27168,27202
fig = plt.figure()
dis_for_regA06 = [carx[3][i]-111 for i in range(len(carrssi[3]))]
uwb, = plt.plot(dis_for_regA06[0:25],carrssi[3][0:25], marker="+", linestyle='None',c='r')




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


#NLOS: A06
# fig = plt.figure()
dis_for_regA06 = [cary[4][i] for i in range(len(carrssi[4]))]
xbee, = plt.plot(dis_for_regA06,carrssi[4], marker="+", linestyle='None', color='b')
# slopeA06, intercept, r_value, p_value, std_err = stats.linregress(dis_for_regA06[-2:],carrssi[4][-2:])
# xA06 = np.arange(4,12, 0.01)
# lineA06 = slopeA06*xA06+intercept
# plt.plot(xA06, lineA06, 'b')
A0model = np.poly1d(np.polyfit(dis_for_regA06[-2:],carrssi[4][-2:], 2))
A0line = np.linspace(2,12, 100)
plt.plot(A0line, A0model(A0line),color='b')
# plt.text(6, 80,'y = {:.2f}x + {:.2f}'.format(slopeA06,intercept),  color='b')


plt.title('Shimen NLOS')
plt.xlabel('meter')
plt.ylabel('normalized RSSI')
leg = plt.legend([uwb,xbee],['UWB Sample','XBee Sample'])
color_list = ['r','b']
for i,text in enumerate(leg.get_texts()):
    plt.setp(text, color = color_list[i])
plt.show()
fig.savefig('shimen_NLOS')
