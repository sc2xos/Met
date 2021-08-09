# %%
from datetime import datetime,timezone,timedelta
from download.download_band4 import T_No
import time
import urllib.request
import sys
import os
import pandas as pd
import numpy as np
# %%
start_year = 2020
end_year = 2020
DATADIR="/home/soga/git/Met/download/csv"
df = pd.concat([pd.read_csv("{0}/table{1}.csv".format(DATADIR,year),encoding="shift-jis") for year in range(start_year, end_year+1)])
df.head(3)
# %%
def make_T_Date(T_year, T_month, T_day, T_hour):
    """
    parameters
    ----------
    
    returns
    ----------
    T_date :  日付(YYYYMMDDHH)のリスト
    """
    T_Date = []
    for year, month, day, hour in zip(T_year, T_month, T_day, T_hour):
        T_Date.append(str(year).zfill(4) + str(month).zfill(2) + str(day).zfill(2) + str(hour).zfill(2))
    return T_Date
# %%
def check_file(T_Date, T_No):
    title : str = "HMW8{0}.20{1}.jpg".format(T_Date[2::], T_No)
    data_dir : str = "/home/soga/data/typhoon/img/hmw/band4/{0}".format(T_Date[0:4])
    file_path : str = data_dir + "/" + title
    if(os.path.isfile( file_path ) is True):  
        print("Already Exists {0}".format(title))
        return True
    else:
        print("Not Exists {0}".format(title))
        return False
#%% 
T_No_list = df.loc[:, "台風番号"].values
T_year = df.loc[:, "年"].values
T_month = df.loc[:, "月"].values
T_day = df.loc[:, "日"].values
T_hour = df.loc[:, "時（UTC）"].values
T_Date_list = make_T_Date(T_year, T_month, T_day, T_hour)
print(T_No_list)
# %%
# 同一の台風番号中の連続する6日間を抽出
# 連続する５日間　+ 1日間のデータが存在する場合、配列に追加(日付、file_path)
testT_No_list = df.query('"台風番号" == 2001')
print(testT_No_list)
#%%
def make_1set():
    T_year = df.loc[:, "年"["2001"]].values
    T_month = df.loc[:, "月"].values
    T_day = df.loc[:, "日"].values
    T_hour = df.loc[:, "時（UTC）"].values
# %%
if __name__ == "__main__":
    main()

