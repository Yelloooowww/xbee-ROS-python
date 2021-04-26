import matplotlib.pyplot as plt
import numpy as np
import csv
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

############################A19################################################
# xbee normalize: (D+90)/(-40+90)*100
xbee_A19LOSrssi = [((float(xbee_A19data[i][3])+90)/(-40+90)*100) for i in range(8,70)]
xbee_A19LOSdis = [float(xbee_A19data[i][1]) for i in range(8,70)]
xbee_A19LOSrssi += [((float(xbee_A19data[i][3])+90)/(-40+90)*100) for i in range(154,164)]
xbee_A19LOSdis += [float(xbee_A19data[i][1]) for i in range(154,164)]
plt.plot(xbee_A19LOSdis, xbee_A19LOSrssi, marker="^", linestyle='None', zorder=0)

xbee_A19NLOSrssi = [((float(xbee_A19data[i][3])+90)/(-40+90)*100) for i in range(70,154)]
xbee_A19NLOSdis = [float(xbee_A19data[i][2]) for i in range(70,154)]
plt.plot(xbee_A19NLOSdis, xbee_A19NLOSrssi, marker="*", linestyle='None', zorder=0)

# uwb normalize:(D+110)/(-80+110)*100
uwb_A19rssi, uwb_A19dis = [],[]
for i in range(444,1430):
    if float(uwb_A19data[i][3])> -110:
        uwb_A19rssi.append( ((float(uwb_A19data[i][3])+110)/(-80+110)*100) )
        uwb_A19dis.append(float(uwb_A19data[i][1]))
plt.plot(uwb_A19dis, uwb_A19rssi, marker=".", linestyle='None', zorder=0)
plt.legend(['A19_XBee_LOS','A19_XBee_NLOS','A19_UWB_LOS'])
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
plt.plot(xbee_A16LOSdis, xbee_A16LOSrssi, marker="^", linestyle='None', zorder=0)

xbee_A16NLOSrssi = [((float(xbee_A16data[i][3])+90)/(-40+90)*100) for i in range(99,127)]
xbee_A16NLOSdis = [abs(float(xbee_A16data[i][1])-float(xbee_A16data[99][1])) for i in range(99,127)]
plt.plot(xbee_A16NLOSdis, xbee_A16NLOSrssi, marker="*", linestyle='None', zorder=0)

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
plt.plot(uwb_A16dis, uwb_A16rssi, marker=".", linestyle='None', zorder=0)
plt.legend(['A16_XBee_LOS','A16_XBee_NLOS','A16_UWB_LOS'])
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
plt.plot(xbee_A12LOSdis, xbee_A12LOSrssi, marker="^", linestyle='None', zorder=0)

xbee_A12NLOSrssi = [((float(xbee_A12data[i][3])+90)/(-40+90)*100) for i in range(1,69)]
xbee_A12NLOSdis = [abs(float(xbee_A12data[i][1])-17) for i in range(1,69)]
xbee_A12NLOSrssi += [((float(xbee_A12data[i][3])+90)/(-40+90)*100) for i in range(144,165)]
xbee_A12NLOSdis += [abs(float(xbee_A12data[i][1])-17) for i in range(144,165)]
plt.plot(xbee_A12NLOSdis, xbee_A12NLOSrssi, marker="*", linestyle='None', zorder=0)

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
plt.plot(uwb_A12dis, uwb_A12rssi, marker=".", linestyle='None', zorder=0)
plt.legend(['A12_XBee_LOS','A12_XBee_NLOS','A12_UWB_LOS'])
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
