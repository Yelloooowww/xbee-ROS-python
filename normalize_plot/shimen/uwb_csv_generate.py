import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats

with open('uwb_shimen_202009.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

uwb_tag_list = []
for i in range(1,len(data)):
    if not int(data[i][5]) in uwb_tag_list:
        uwb_tag_list.append(int(data[i][5]))

print(len(uwb_tag_list))
print(uwb_tag_list)
file = open('uwb.csv', 'w')
writer = csv.writer(file)
writer.writerow(['time','x','y']+uwb_tag_list)


for i in range(1,len(data)):
    row = [data[i][0],data[i][1], data[i][2]]
    for j in range(len(uwb_tag_list)):
        if int(data[i][5]) == uwb_tag_list[j]:
            row += [int(data[i][3])]
        else :
            row += [0]

    writer.writerow(row)
file.close()
