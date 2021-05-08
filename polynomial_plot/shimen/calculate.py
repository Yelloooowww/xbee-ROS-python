import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats

################################################################################
XBee_LOS = [-1.11, -0.67, -0.67]
XBee_NLOS = [-7.93]
UWB_LOS = [-2.01, -5.84, -3.07]

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

# XBee_LOS_avg= -0.8166666666666668
# XBee_NLOS_avg= -7.93
# UWB_LOS_avg= -3.64
# XBee_LOS_std= 0.20741798914805396
# XBee_NLOS_std= 0.0
# UWB_LOS_std= 1.6147032751148636
