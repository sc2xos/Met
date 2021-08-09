# %%
from datetime import datetime,timezone,timedelta
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
df = pd.concat([pd.read_csv("{0}/table{1}.csv".format(DATADIR,year),encoding="shift-jis") for year in range(start_year,end_year+1)])
df.head(3)
# %%
def define_url(T_No, T_Date, band='4'):
    """
    衛星画像DL先のURLを定義
    parameters
    ----------
    T_No : 台風番号(4桁)
    T_Date : 日付(YYYYMMDDHH)
    band : 帯域(赤外画像の4で固定)
    
    returns
    ----------
    title : str  DL対象のファイル名
    url : str  DL先のURL
    """
    title : str = "HMW8{0}.20{1}.jpg".format(T_Date[2::], T_No)
    base : str = 'http://agora.ex.nii.ac.jp/digital-typhoon/wnp/by-name/20{0}/{1}/512x512/'.format(T_No, band)
    url : str = base + title
    return title, url
#%%
def make_datadir(T_Date):
    data_dir = "/home/soga/data/typhoon/img/hmw/band4/{0}".format(T_Date[0:4])
    if(os.path.isdir(data_dir) is True):
        print("Already Exists {0}".format(data_dir))

    else:
        os.makedirs(data_dir)
        print("Completed making {0}".format(data_dir))
    return data_dir
#%%
def img_download(url, data_dir, title, band='4'):
        if(os.path.isfile(data_dir + "/" + title ) is True):  
            print("Already Exists {0}".format(data_dir))
        else:
            print("Downloading from ", url)
            try:
                urllib.request.urlopen(url)
                urllib.request.urlretrieve(url, (data_dir + title) )
                print("Completed Download!")
            except urllib.error.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            except urllib.error.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
#%%
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
#%% 
T_No_list = df.loc[:, "台風番号"].values
T_year = df.loc[:, "年"].values
T_month = df.loc[:, "月"].values
T_day = df.loc[:, "日"].values
T_hour = df.loc[:, "時（UTC）"].values
T_Date_list = make_T_Date(T_year, T_month, T_day, T_hour)
print(T_Date_list)
#%%
def main():
    for no, date in zip(T_No_list, T_Date_list):
        title, url = define_url(str(no).zfill(4), date)
        data_dir = make_datadir(date)
        img_download(url, data_dir, title)
        time.sleep(3)
# %%
if __name__ == "__main__":
    main()

