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
start_year = 2020
end_year = 2020
WORKDIR="/home/soga/git/Met/DL"
df = pd.concat([pd.read_csv("{0}/csv/table{1}.csv".format(WORKDIR,year),encoding="shift-jis") for year in range(start_year, end_year+1)])
df.head(3)
#%%
def make_daylist(T_df):
    """
    parameters
    ----------
    T_df : データフレーム
    
    returns
    ----------
    target_date_list : [ 台風番号 : int, 階級が4or5の日付(YYYYMMDDHH) : str] のリスト
    """
    T_No_set = set(T_df.loc[:, "台風番号"].values)
    target_list = []
    for no in T_No_set:
        #同一台風番号で階級4or5が日時を抽出
        print("##### Start process : Typhoon No.{0} #####".format(no))
        strong = T_df.query('台風番号 == {0} & ( 階級 == 4 | 階級 == 5)'.format(no) )
        date = (strong.loc[:, ["年","月","日","時（UTC）"]]).values
        print(("Number of target dates {0}").format(len(strong)))
        
        #抽出した日時が6日以上ある場合、リストに追加する
        if( len(strong) >= 5 ):
            for i in range(len(date[:,0])):
                target_list.append([no,str(date[i,0]).zfill(4)+str(date[i,1]).zfill(2)+str(date[i,2]).zfill(2)+str(date[i,3]).zfill(2)])
        else:
            print("Process is Skipped!")
       
    return target_list
#%%
T_No_list = df.loc[:, "台風番号"].values
T_year = df.loc[:, "年"].values
T_month = df.loc[:, "月"].values
T_day = df.loc[:, "日"].values
T_hour = df.loc[:, "時（UTC）"].values
T_Date_list = tutils.make_T_Date(T_year, T_month, T_day, T_hour)
#%%
list = make_daylist(df) #階級4or5の台風宇野抽出 
print(list)
#%%ファイルの存在をチェックする関数
def check_file(T_No, T_Date):
    """
    parameters
    ----------
    T_Date : 日付(YYYYMMDDHH)
    T_No : str 台風番号
    
    returns
    ----------
    True or False 
    """
    file : str = "HMW8{0}.20{1}.jpg".format(T_Date[2::], T_No)
    data_dir : str= "/home/soga/data/typhoon/img/hmw/band4/{0}".format(T_Date[0:4])
    file_path : str = data_dir + "/" + file
    print(file_path)
    if(os.path.isdir( file_path ) is True):
        return True
    else:
        return False
#%%
for i,j in list:
    print(check_file(i,j))
#%%入力した日付から5ステップの日付のリストを返す
def make_6days(T_Date):
    """
    parameters
    ----------
    T_Date : str 日付(YYYYMMDDHH)

    returns
    ----------
    date_list : list of str ( len(date_list) = 6 ) 日付(YYYYMMDDHH)のリスト
    """
    start_date = dt.datetime(T_Date)
    end_date = start_date + dt.timedelta(hours=6*5)
    date = start_date
    date_list = [] 
    while(  read_date <= end_date ):
        date_list.append( date.strftime("%Y%m%d%H%MM") )
        read_date = read_date + dt.timedelta(hours=6)
    return date_list

#%%
list = np.array(list)
print(list.shape)
print(list[0:10,1])
#%%
def make_data(target_list): 
    """
    parameters
    ----------
    date_list : [ 台風番号:int , 日付(YYYYMMDDHH):str ] のリスト
    
    returns
    ----------
    data_list : [date, file_path] のリスト
    """
    target_array = np.array(target_list)
    input_data = []
    for i in range(len(target_list[:, 0])):
        no = target_list[i, 0]
        day_list = target_list[i:i+6, 1]
        six_days = make_6days(target_list[i, 1])
        if(day_list == six_days):
            input_data.append(day_list)
    return input_data
            


# %%
def main():
    return None

if __name__ == "__main__":
    main()
