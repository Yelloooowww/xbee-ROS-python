import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import csv

# with open('husky1front_rightranges.csv') as f:
#     reader = csv.reader(f)
#     data = list(reader)
#
# file = open('uwb_A19.csv', 'wb')
# writer = csv.writer(file)
#
# x, y, rssi = [],[],[]
# for i in range(len(data)):
#     if data[i][12] != '':
#         # writer.writerow(["time","x", "y","rssi","distance","tag_id"])
#         writer.writerow([data[i][10],data[i][0], data[i][1],data[i][12],data[i][11],data[i][13]])
# file.close()

with open('husky1rssi_neighbour.csv') as f:
    reader = csv.reader(f)
    data = list(reader)

file = open('xbee_A19.csv', 'wb')
writer = csv.writer(file)

x, y, rssi = [],[],[]
for i in range(len(data)):
    # writer.writerow(["time","x", "y","rssi","tag_id"])
    writer.writerow([data[i][8],data[i][0], data[i][1],data[i][9],data[i][10]])
file.close()
