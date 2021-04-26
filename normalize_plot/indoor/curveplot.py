import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats
plt.rcParams.update({'font.size': 36})

with open('xbee_A19.csv', newline='') as f:
    reader = csv.reader(f)
    xbee_A19data = list(reader)

with open('xbee_A16.csv', newline='') as f:
    reader = csv.reader(f)
    xbee_A16data = list(reader)

with open('xbee_A12.csv', newline='') as f:
    reader = csv.reader(f)
    xbee_A12data = list(reader)

with open('uwb_A19.csv', newline='') as f:
    reader = csv.reader(f)
    uwb_A19data = list(reader)

with open('uwb_A16.csv', newline='') as f:
    reader = csv.reader(f)
    uwb_A16data = list(reader)

with open('uwb_A12.csv', newline='') as f:
    reader = csv.reader(f)
    uwb_A12data = list(reader)


###############################################################################
def reg(x,y):
    coefficients = np.polyfit(x,y,1) # 利用 polyfit 幫我們算出資料 一階擬合的 a, b 參數
    p = np.poly1d(coefficients) # 做出公式, print 的結果是 coefficients[0] * X + coefficients[1]
    #coefficient_of_dermination = r2_score(y, p(x)) // 計算相關係數用，這裡沒有用到
    return coefficients, p



############################A19################################################
# xbee normalize: (D+90)/(-40+90)*100
xbee_A19LOSrssi = [((float(xbee_A19data[i][3])+90)/(-40+90)*100) for i in range(8,70)]
xbee_A19LOSdis = [float(xbee_A19data[i][1]) for i in range(8,70)]
xbee_A19LOSrssi += [((float(xbee_A19data[i][3])+90)/(-40+90)*100) for i in range(154,164)]
xbee_A19LOSdis += [float(xbee_A19data[i][1]) for i in range(154,164)]
LOS, = plt.plot(xbee_A19LOSdis, xbee_A19LOSrssi, marker="^", linestyle='None', zorder=0)
#regression part
slopexbee_A19LOS, intercept, r_value, p_value, std_err = stats.linregress(xbee_A19LOSdis,xbee_A19LOSrssi)
xxbee_A19LOS = np.arange(0,70, 0.01)
linexbee_A19LOS = slopexbee_A19LOS*xxbee_A19LOS+intercept
xbee_LOS = plt.plot(xxbee_A19LOS, linexbee_A19LOS, 'r')
plt.text(47, 55,'y = {:.2f}x + {:.2f}'.format(slopexbee_A19LOS,intercept),  color='r')

xbee_A19NLOSrssi = [((float(xbee_A19data[i][3])+90)/(-40+90)*100) for i in range(70,154)]
xbee_A19NLOSdis = [float(xbee_A19data[i][2]) for i in range(70,154)]
NLOS, = plt.plot(xbee_A19NLOSdis, xbee_A19NLOSrssi, marker="*", linestyle='None', zorder=0)
#regression
reg_xbee_A19NLOSdis,reg_xbee_A19NLOSrssi = [], []
for i,item in enumerate(xbee_A19NLOSdis) :
    if item <25:
        reg_xbee_A19NLOSdis.append(xbee_A19NLOSdis[i])
        reg_xbee_A19NLOSrssi.append(xbee_A19NLOSrssi[i])
slopexbee_A19NLOS, intercept, r_value, p_value, std_err = stats.linregress(reg_xbee_A19NLOSdis,reg_xbee_A19NLOSrssi)
xxbee_A19NLOS = np.arange(0,25, 0.01)
linexbee_A19NLOS = slopexbee_A19NLOS*xxbee_A19NLOS+intercept
plt.plot(xxbee_A19NLOS, linexbee_A19NLOS, 'r')
plt.text(1, 50,'y = {:.2f}x + {:.2f}'.format(slopexbee_A19NLOS,intercept),  color='r')


# uwb normalize:(D+110)/(-80+110)*100
uwb_A19rssi, uwb_A19dis = [],[]
for i in range(444,1430):
    if float(uwb_A19data[i][3])> -110:
        uwb_A19rssi.append( ((float(uwb_A19data[i][3])+110)/(-80+110)*100) )
        uwb_A19dis.append(float(uwb_A19data[i][1]))
uwb, = plt.plot(uwb_A19dis, uwb_A19rssi, marker=".", linestyle='None', zorder=0)
#regression
reg_uwb_A19dis,reg_uwb_A19rssi = [], []
for i,item in enumerate(uwb_A19dis) :
    if item < 20:
        reg_uwb_A19dis.append(uwb_A19dis[i])
        reg_uwb_A19rssi.append(uwb_A19rssi[i])
slopeuwb_A19, intercept, r_value, p_value, std_err = stats.linregress(reg_uwb_A19dis,reg_uwb_A19rssi)
xuwb_A19 = np.arange(0,20, 0.01)
lineuwb_A19 = slopeuwb_A19*xuwb_A19+intercept
plt.plot(xuwb_A19, lineuwb_A19, 'r')
plt.text(24, 14,'y = {:.2f}x + {:.2f}'.format(slopeuwb_A19,intercept),  color='r')


plt.legend([LOS,NLOS,uwb],['A19_XBee_LOS','A19_XBee_NLOS','A19_UWB_LOS'])
plt.xlabel("meters")
plt.ylabel("normalized RSSI")
plt.title("indoor UWB & XBee RSSI")
plt.show()



############################A16################################################
# xbee normalize: (D+90)/(-40+90)*100
xbee_A16LOSrssi = [((float(xbee_A16data[i][3])+90)/(-40+90)*100) for i in range(1,68)]
xbee_A16LOSdis = [float(xbee_A16data[i][1]) for i in range(1,68)]
xbee_A16LOSrssi += [((float(xbee_A16data[i][3])+90)/(-40+90)*100) for i in range(69,99)]
xbee_A16LOSdis += [float(xbee_A16data[i][2]) for i in range(69,99)]
xbee_A16LOSrssi += [((float(xbee_A16data[i][3])+90)/(-40+90)*100) for i in range(128,154)]
xbee_A16LOSdis += [float(xbee_A16data[i][2]) for i in range(128,154)]
LOS, = plt.plot(xbee_A16LOSdis, xbee_A16LOSrssi, marker="^", linestyle='None', zorder=0)
#regression part
slopexbee_A16LOS, intercept, r_value, p_value, std_err = stats.linregress(xbee_A16LOSdis,xbee_A16LOSrssi)
xxbee_A16LOS = np.arange(0,70, 0.01)
linexbee_A16LOS = slopexbee_A16LOS*xxbee_A16LOS+intercept
plt.plot(xxbee_A16LOS, linexbee_A16LOS, 'r')
plt.text(47, 55,'y = {:.2f}x + {:.2f}'.format(slopexbee_A16LOS,intercept),  color='r')


xbee_A16NLOSrssi = [((float(xbee_A16data[i][3])+90)/(-40+90)*100) for i in range(99,127)]
xbee_A16NLOSdis = [abs(float(xbee_A16data[i][1])-float(xbee_A16data[99][1])) for i in range(99,127)]
NLOS, = plt.plot(xbee_A16NLOSdis, xbee_A16NLOSrssi, marker="*", linestyle='None', zorder=0)
# #regression
# reg_xbee_A16NLOSdis,reg_xbee_A16NLOSrssi = [], []
# for i,item in enumerate(xbee_A16NLOSdis) :
#     if item < 2.5:
#         reg_xbee_A16NLOSdis.append(xbee_A16NLOSdis[i])
#         reg_xbee_A16NLOSrssi.append(xbee_A16NLOSrssi[i])
# slopexbee_A16NLOS, intercept, r_value, p_value, std_err = stats.linregress(reg_xbee_A16NLOSdis,reg_xbee_A16NLOSrssi)
# xxbee_A16NLOS = np.arange(0,2.5, 0.01)
# linexbee_A16NLOS = slopexbee_A16NLOS*xxbee_A16NLOS+intercept
# plt.plot(xxbee_A16NLOS, linexbee_A16NLOS, 'r')
# plt.text(1, 50,'y = {:.2f}x + {:.2f}'.format(slopexbee_A16NLOS,intercept),  color='r')

# uwb normalize:(D+110)/(-80+110)*100
uwb_A16rssi, uwb_A16dis = [],[]
for i in range(1,4075):
    if float(uwb_A16data[i][3])> -110 and float(uwb_A16data[i][3])<-80:
        uwb_A16rssi.append( ((float(uwb_A16data[i][3])+110)/(-80+110)*100) )
        uwb_A16dis.append(abs(float(uwb_A16data[i][1])-17))
for i in range(4075,7669):
    if float(uwb_A16data[i][3])> -110 and float(uwb_A16data[i][3])<-80:
        uwb_A16rssi.append( ((float(uwb_A16data[i][3])+110)/(-80+110)*100) )
        uwb_A16dis.append(abs(float(uwb_A16data[i][2])))
uwb, = plt.plot(uwb_A16dis, uwb_A16rssi, marker=".", linestyle='None', zorder=0)
#regression
reg_uwb_A16dis,reg_uwb_A16rssi = [], []
for i,item in enumerate(uwb_A16dis) :
    if item < 20:
        reg_uwb_A16dis.append(uwb_A16dis[i])
        reg_uwb_A16rssi.append(uwb_A16rssi[i])
slopeuwb_A16, intercept, r_value, p_value, std_err = stats.linregress(reg_uwb_A16dis,reg_uwb_A16rssi)
xuwb_A16 = np.arange(0,20, 0.01)
lineuwb_A16 = slopeuwb_A16*xuwb_A16+intercept
plt.plot(xuwb_A16, lineuwb_A16, 'r')
plt.text(9, 50,'y = {:.2f}x + {:.2f}'.format(slopeuwb_A16,intercept),  color='r')

plt.legend([LOS,NLOS,uwb],['A16_XBee_LOS','A16_XBee_NLOS','A16_UWB_LOS'])
plt.xlabel("meters")
plt.ylabel("normalized RSSI")
plt.title("indoor UWB & XBee RSSI")
plt.show()



############################A12################################################
# xbee normalize: (D+90)/(-40+90)*100
xbee_A12LOSrssi = [((float(xbee_A12data[i][3])+90)/(-40+90)*100) for i in range(69,98)]
xbee_A12LOSdis = [abs(float(xbee_A12data[i][2])-50.5) for i in range(69,98)]
xbee_A12LOSrssi += [((float(xbee_A12data[i][3])+90)/(-40+90)*100) for i in range(98,124)]
xbee_A12LOSdis += [abs(float(xbee_A12data[i][1])-17) for i in range(98,124)]
xbee_A12LOSrssi += [((float(xbee_A12data[i][3])+90)/(-40+90)*100) for i in range(124,144)]
xbee_A12LOSdis += [abs(float(xbee_A12data[i][2])-50.5) for i in range(124,144)]
LOS, = plt.plot(xbee_A12LOSdis, xbee_A12LOSrssi, marker="^", linestyle='None', zorder=0)
#regression part
slopexbee_A12LOS, intercept, r_value, p_value, std_err = stats.linregress(xbee_A12LOSdis,xbee_A12LOSrssi)
xxbee_A12LOS = np.arange(0,70, 0.01)
linexbee_A12LOS = slopexbee_A12LOS*xxbee_A12LOS+intercept
plt.plot(xxbee_A12LOS, linexbee_A12LOS, 'r')
plt.text(47, 55,'y = {:.2f}x + {:.2f}'.format(slopexbee_A12LOS,intercept),  color='r')

xbee_A12NLOSrssi = [((float(xbee_A12data[i][3])+90)/(-40+90)*100) for i in range(1,69)]
xbee_A12NLOSdis = [abs(float(xbee_A12data[i][1])-17) for i in range(1,69)]
xbee_A12NLOSrssi += [((float(xbee_A12data[i][3])+90)/(-40+90)*100) for i in range(144,165)]
xbee_A12NLOSdis += [abs(float(xbee_A12data[i][1])-17) for i in range(144,165)]
NLOS, = plt.plot(xbee_A12NLOSdis, xbee_A12NLOSrssi, marker="*", linestyle='None', zorder=0)
#regression
reg_xbee_A12NLOSdis,reg_xbee_A12NLOSrssi = [], []
for i,item in enumerate(xbee_A12NLOSdis) :
    if item < 10:
        reg_xbee_A12NLOSdis.append(xbee_A12NLOSdis[i])
        reg_xbee_A12NLOSrssi.append(xbee_A12NLOSrssi[i])
slopexbee_A12NLOS, intercept, r_value, p_value, std_err = stats.linregress(reg_xbee_A12NLOSdis,reg_xbee_A12NLOSrssi)
xxbee_A12NLOS = np.arange(0,10, 0.01)
linexbee_A12NLOS = slopexbee_A12NLOS*xxbee_A12NLOS+intercept
plt.plot(xxbee_A12NLOS, linexbee_A12NLOS, 'r')
plt.text(1, 20,'y = {:.2f}x + {:.2f}'.format(slopexbee_A12NLOS,intercept),  color='r')

# uwb normalize:(D+110)/(-80+110)*100
uwb_A12rssi, uwb_A12dis = [],[]
for i in range(100,1600):
    if float(uwb_A12data[i][3])> -110 and float(uwb_A12data[i][3])<-80:
        uwb_A12rssi.append( ((float(uwb_A12data[i][3])+110)/(-80+110)*100) )
        uwb_A12dis.append(abs(float(uwb_A12data[i][2])-50.5))
for i in range(1600,4370):
    if float(uwb_A12data[i][3])> -110 and float(uwb_A12data[i][3])<-80:
        uwb_A12rssi.append( ((float(uwb_A12data[i][3])+110)/(-80+110)*100) )
        uwb_A12dis.append(abs(float(uwb_A12data[i][1])-17))
for i in range(4370,4900):
    if float(uwb_A12data[i][3])> -110 and float(uwb_A12data[i][3])<-80:
        uwb_A12rssi.append( ((float(uwb_A12data[i][3])+110)/(-80+110)*100) )
        uwb_A12dis.append(abs(float(uwb_A12data[i][2])-50.5))
uwb, = plt.plot(uwb_A12dis, uwb_A12rssi, marker=".", linestyle='None', zorder=0)
#regression
reg_uwb_A12dis,reg_uwb_A12rssi = [], []
for i,item in enumerate(uwb_A12dis) :
    if item < 30:
        reg_uwb_A12dis.append(uwb_A12dis[i])
        reg_uwb_A12rssi.append(uwb_A12rssi[i])
slopeuwb_A12, intercept, r_value, p_value, std_err = stats.linregress(reg_uwb_A12dis,reg_uwb_A12rssi)
xuwb_A12 = np.arange(0, 30, 0.01)
lineuwb_A12 = slopeuwb_A12*xuwb_A12+intercept
plt.plot(xuwb_A12, lineuwb_A12)
plt.text(25, 40,'y = {:.2f}x + {:.2f}'.format(slopeuwb_A12,intercept),  color='r')

plt.legend([LOS,NLOS,uwb],['A12_XBee_LOS','A12_XBee_NLOS','A12_UWB_LOS'])
plt.xlabel("meters")
plt.ylabel("normalized RSSI")
plt.title("indoor UWB & XBee RSSI")
plt.show()

###################################ALL#########################################
xbee_allLOSrssi = xbee_A19LOSrssi + xbee_A16LOSrssi + xbee_A12LOSrssi
xbee_allNLOSrssi = xbee_A19NLOSrssi + xbee_A16NLOSrssi + xbee_A12NLOSrssi
xbee_allLOSdis = xbee_A19LOSdis + xbee_A16LOSdis + xbee_A12LOSdis
xbee_allNLOSdis = xbee_A19NLOSdis + xbee_A16NLOSdis + xbee_A12NLOSdis
uwb_allrssi = uwb_A19rssi + uwb_A16rssi + uwb_A12rssi
uwb_alldis = uwb_A19dis + uwb_A16dis + uwb_A12dis
plt.plot(xbee_allLOSdis, xbee_allLOSrssi, marker="^", linestyle='None', zorder=0)
plt.plot(xbee_allNLOSdis, xbee_allNLOSrssi, marker="*", linestyle='None', zorder=0)
plt.plot(uwb_alldis, uwb_allrssi, marker=".", linestyle='None', zorder=0)
# plt.legend(['A19_XBee_LOS','A19_XBee_NLOS','A19_UWB_LOS','A16_XBee_LOS','A16_XBee_NLOS','A16_UWB_LOS','A12_XBee_LOS','A12_XBee_NLOS','A12_UWB_LOS'])
plt.legend(['XBee_LOS','XBee_NLOS','UWB_LOS'])
plt.xlabel("meters")
plt.ylabel("normalized RSSI")
plt.title("indoor UWB & XBee RSSI")
plt.show()

################################################################################
XBee_LOS = [slopexbee_A12LOS, slopexbee_A16LOS, slopexbee_A19LOS]
XBee_NLOS = [slopexbee_A12NLOS, slopexbee_A19NLOS]
UWB_LOS = [slopeuwb_A12, slopeuwb_A16, slopeuwb_A19]

XBee_LOS_avg = np.average(XBee_LOS)
XBee_NLOS_avg = np.average(XBee_NLOS)
UWB_LOS_avg = np.average(UWB_LOS)
XBee_LOS_std = np.std(XBee_LOS)
XBee_NLOS_std = np.std(XBee_NLOS)
UWB_LOS_std = np.std(UWB_LOS)
print('XBee_LOS_avg=',XBee_LOS_avg)
print('XBee_NLOS_avg=',XBee_NLOS_avg)
print('UWB_LOS_avg=',UWB_LOS_avg)
print('XBee_LOS_std=',XBee_LOS_std)
print('XBee_NLOS_std=',XBee_NLOS_std)
print('UWB_LOS_std=',UWB_LOS_std)
