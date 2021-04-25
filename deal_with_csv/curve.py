# import matplotlib.pyplot as plt
# import numpy as np
# import csv
# from scipy import stats
#
# with open('xbee_A19.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = list(reader)
#
# def reg(x,y):
#     coefficients = np.polyfit(x,y,1) # 利用 polyfit 幫我們算出資料 一階擬合的 a, b 參數
#     p = np.poly1d(coefficients) # 做出公式, print 的結果是 coefficients[0] * X + coefficients[1]
#     #coefficient_of_dermination = r2_score(y, p(x)) // 計算相關係數用，這裡沒有用到
#     return coefficients, p
# # 70~153
# rssi = np.array([float(data[i][3]) for i in range(70,90)])
# dis = np.array([float(data[i][2]) for i in range(70,90)])
#
# #regression part
# slope, intercept, r_value, p_value, std_err = stats.linregress(dis[2:-1],rssi[2:-1])
# x = np.arange(3,40)
# line = slope*x+intercept
# plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(slope,intercept))
#
# #error part
# err_x = [[i,i] for i in range(5,40,4)] # 要连接的两个点的坐标
# err_y = [ [ max(rssi[i:i+4]), min(rssi[i:i+4]) ] for i in range(0,len(rssi),2)]
# print(len(err_x))
# for i in range(len(err_x)):
#     plt.plot(err_x[i], err_y[i], color='r')
#     plt.text(err_x[i][0], err_y[i][0], 'err='+str(int(err_y[i][0]-err_y[i][1])),  color='r')
#
#
# plt.plot(dis, rssi, marker="s")
# plt.xlabel("meters beyond the corner ")
# plt.ylabel("RSSI")
# plt.title("xbee RSSI")
# plt.show()


import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats
from statistics import mean

with open('uwb_A19.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

def reg(x,y):
    coefficients = np.polyfit(x,y,1) # 利用 polyfit 幫我們算出資料 一階擬合的 a, b 參數
    p = np.poly1d(coefficients) # 做出公式, print 的結果是 coefficients[0] * X + coefficients[1]
    #coefficient_of_dermination = r2_score(y, p(x)) // 計算相關係數用，這裡沒有用到
    return coefficients, p
# 2930~2992
rssi = np.array([float(data[i][3]) for i in range(2923,2992)])
dis = np.array([float(data[i][2]) for i in range(2923,2992)])

#regression part
slope, intercept, r_value, p_value, std_err = stats.linregress(dis[0:-2],rssi[0:-2])
x = np.arange(0.4, 1.6, 0.01)
line = slope*x+intercept
plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(slope,intercept))

#error part
err_x_tmp = np.arange(0.5, 1.6, 0.25)
err_x = [ [i,i] for i in err_x_tmp ]
err_y = [ [-93.02,-97.06],[-94.00,-100.12],[-94.95,-101.98],[-98.00,-104.05],[-99.89,-103.05]]
print(len(err_x),len(err_y))
for i in range(len(err_x)):
    # if i%2 == 0:
    plt.plot(err_x[i], err_y[i], color='r')
    plt.text(err_x[i][0], 0.1+err_y[i][0], 'err='+str(int(err_y[i][0]-err_y[i][1])),  color='r')


plt.plot(dis, rssi, marker="s")
plt.xlabel("meters beyond the corner ")
plt.ylabel("RSSI")
plt.title("uwb RSSI")
plt.show()
