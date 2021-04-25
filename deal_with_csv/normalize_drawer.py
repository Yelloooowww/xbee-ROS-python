import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import csv

with open('uwb_A19.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# print(data)
x, y, rssi = [],[],[]
# x = [float(data[i][0]) for i in range(1,len(data))]
# y = [float(data[i][1]) for i in range(1,len(data))]
# rssi = [int(data[i][8]) for i in range(1,len(data))]
for i in range(1,len(data)):
    if data[i][4] != '':
        if (int(data[i][3])>-110) and (int(data[i][3])<-60):
            x.append( float(data[i][1]) )
            y.append( float(data[i][2]) )
            # xbee normalize: (D+90)/(-40+90)*100
            # UWB normalize:(D+110)/(-60+110)*100
            rssi.append( (int(data[i][3])+110)/(-60+110)*100 )

anchor_x = [-1.5,17,17]
anchor_y = [0,0,52]
anchor_text = ['A19','A16','A12']
startx = [-1.5]
starty = [-3]

img=mpimg.imread('EE6F.png')
imgplot = plt.imshow(img,extent=(-14.6,73.66, -7.324, 60))

plt.scatter(anchor_x, anchor_y, color='r', marker='^',zorder=30)
for i in range(3): plt.text(anchor_x[i]+0.75, anchor_y[i]-0.75, anchor_text[i],color='r',zorder=10+i)
plt.scatter(startx, starty, color='c', marker='*')
plt.scatter(x, y, c=rssi)
plt.colorbar()
plt.title("XBee normalized RSSI")
plt.axis('off')
plt.legend(['node','start point'])
plt.show()
