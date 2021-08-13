# %%
import os
import time
import sys
import urllib.request

import numpy as np
import datetime as dt
import pandas as pd

import typhoon_utils as tutils
# %%
start_year = 2016
end_year = 2021
WORKDIR="/home/soga/git/Met/DL"
df = pd.concat([pd.read_csv("{0}/csv/table{1}.csv".format(WORKDIR,year),encoding="shift-jis") for year in range(start_year,end_year+1)])
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
    file : str = "HMW8{0}.20{1}.jpg".format(T_Date[2::], T_No)
    base : str = 'http://agora.ex.nii.ac.jp/digital-typhoon/wnp/by-name/20{0}/{1}/512x512/'.format(T_No, band)
    url : str = base + file
    return file, url
#%%
def make_datadir(T_No, T_Date):
    data_dir : str = "/home/soga/data/typhoon/img/hmw/band4/{0}/{1}".format(T_Date[0:4], T_No)
    if(os.path.isdir(data_dir) is True):
        print("Already Exists {0}".format(data_dir))

    else:
        os.makedirs(data_dir)
        print("Completed making {0}".format(data_dir))
    
    return data_dir
#%%
def img_download(url, data_dir, title, band='4'):
    file_path = data_dir + "/" + title
    if(os.path.isfile( file_path ) is True):  
        print("Already Exists {0}".format(file_path))
        return
    else:
        print("Downloading from ", url)
        try:
            urllib.request.urlopen(url)
            urllib.request.urlretrieve(url, file_path)
            print("Completed Download!")
            time.sleep(2)
        except urllib.error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except urllib.error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
#%% 
T_year = df.loc[:, "年"].values
T_month = df.loc[:, "月"].values
T_day = df.loc[:, "日"].values
T_hour = df.loc[:, "時（UTC）"].values
T_Date_list = tutils.make_T_Date(T_year, T_month, T_day, T_hour)
T_No_list = df.loc[:, "台風番号"].values
#%%
def main():
    for no, date in zip(T_No_list, T_Date_list):
        title, url = define_url(str(no).zfill(4), date)
        data_dir = make_datadir(no, date)
        img_download(url, data_dir, title)
# %%
if __name__ == "__main__":
    main()
#%%

