#%%
import numpy as np
from datetime import datetime,timezone,timedelta
import time
import urllib.request
import sys
import os
#%%
bst_data = open("/home/soga/data/typhoon/bst_all.txt", "r")
lines = np.array(bst_data.readlines())
print(lines[0].split())
print(lines.shape)
#%%
def make(lines):
    empty = []
    for line in lines:
        if(line.split()[0] == '66666'):
            T_number = line.split()[1]
        else:
            T_date = line.split()[0]
            T_pres = line.split()[5]
            empty.append([T_number, T_date, T_pres])
    tarray = np.array(empty)
    print(tarray.shape)
    return tarray
tarray = make(lines)
#%%