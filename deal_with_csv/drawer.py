import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import csv

with open('xbee_A19.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# print(data)
x, y, rssi = [],[],[]
x = [float(data[i][1]) for i in range(1,len(data))]
y = [float(data[i][2]) for i in range(1,len(data))]
rssi = [int(data[i][3]) for i in range(1,len(data))]
# for i in range(1,len(data)):
#     if data[i][4] != '':
#         x.append( float(data[i][0]) )
#         y.append( float(data[i][1]) )
#         rssi.append( int(data[i][4]) )

anchor_x = [-1.5,17,17]
anchor_y = [-1.5,-1.5,52]
anchor_text = ['A19','A16','A12']
startx = [-1.5]
starty = [-3]


plt.scatter(anchor_x, anchor_y, color='k', marker='^')
for i in range(3): plt.text(anchor_x[i]+0.75, anchor_y[i]-0.75, anchor_text[i])
plt.scatter(startx, starty, color='c', marker='*')
plt.scatter(x, y, c=rssi, cmap='RdYlGn')
plt.colorbar()
plt.title("UWB RSSI")
plt.axis('off')
plt.legend(['node','start point'])
plt.show()
