import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats

################################################################################
XBee_LOS = [-1.34, -2.83, -2.83]
XBee_NLOS = [-10.87]
UWB_LOS = [-2.81, -5.73, -5.73]

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

# XBee_LOS_avg= -2.3333333333333335
# XBee_NLOS_avg= -10.87
# UWB_LOS_avg= -4.756666666666667
# XBee_LOS_std= 0.7023927359786372
# XBee_NLOS_std= 0.0
# UWB_LOS_std= 1.3765012007098127
