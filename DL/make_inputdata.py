# %%
import os
import time
import sys
import urllib.request

import numpy as np
import datetime as dt
from numpy.lib.shape_base import _make_along_axis_idx
import pandas as pd

import typhoon_utils as tutils
# %%
start_year = 2020
end_year = 2020
WORKDIR="/home/soga/git/Met/DL"
df = pd.concat([pd.read_csv("{0}/csv/table{1}.csv".format(WORKDIR,year),encoding="shift-jis") for year in range(start_year, end_year+1)])
df.head(3)
#%%
T_No_list = df.loc[:, "台風番号"].values
T_No_set = list(set(df.loc[:, "台風番号"].values))
T_year = df.loc[:, "年"].values
T_month = df.loc[:, "月"].values
T_day = df.loc[:, "日"].values
T_hour = df.loc[:, "時（UTC）"].values
T_Date_list = tutils.make_T_Date(T_year, T_month, T_day, T_hour)
#%%
def make_dayarray(no, T_df):
    """
    parameters
    ----------
    T_df : データフレーム
    
    returns
    ----------
    target_date_list : [ 台風番号 : int, 階級が4or5の日付(YYYYMMDDHH) : str] のリスト
    """
    #同一台風番号で階級4or5が日時を抽出
    print("##### Start process : Typhoon No.{0} #####".format(no))
    strong = T_df.query('台風番号 == {0} & ( 階級 == 4 | 階級 == 5)'.format(no) )
    date = np.array((strong.loc[:, ["年","月","日","時（UTC）"]]).values)
    print(("Number of target dates {0}").format(len(strong)))
    
    #抽出した日時が6日以上ある場合、リストに追加する
    if( len(strong) >= 5 ):
        target_date = []
        for i in range(len(date[:,0])):
            target_date.append(str(date[i,0]).zfill(4)+str(date[i,1]).zfill(2)+str(date[i,2]).zfill(2)+str(date[i,3]).zfill(2))
        print("No {0} : {1} days".format(no, len(target_date))  )
    else:
        print("Process is Skipped!")

    return target_date

target_date = make_dayarray(T_No_set[0],df) #階級4or5の台風の抽出 
print(target_date)
#%%
#%%ファイルの存在をチェックする関数
def check_file(no, T_Date):
    """
    parameters
    ----------
    T_Date : 日付(YYYYMMDDHH)
    T_No : str 台風番号
    
    returns
    ----------
    True or False 
    """
    file : str = "HMW8{0}.20{1}.jpg".format(T_Date[2::], no)
    data_dir : str= "/home/soga/data/typhoon/img/hmw/band4/{0}/{1}".format(T_Date[0:4], no)
    file_path : str = data_dir + "/" + file
    if(os.path.isfile( file_path ) is True):
        return file_path, True
        print(file_path, "is exist")
    else:
        return None, False
        print(file_path, "is not exist.")

#%%入力した日付から5ステップの日付のリストを返す
def make_6days(start_date):
    """
    parameters
    ----------
    T_Date : str 日付(YYYYMMDDHH)

    returns
    ----------
    date_list : list of str ( len(date_list) = 6 ) 日付(YYYYMMDDHH)のリスト
    """
    start_date = dt.datetime.strptime(start_date, '%Y%m%d%H')
    end_date = start_date + dt.timedelta(hours=6*5)
    date, date_list  = start_date, []
    
    while(  date <= end_date ):
        date_list.append( date.strftime("%Y%m%d%H") )
        date = date + dt.timedelta(hours=6)

    return date_list

#%%
def make_data(no, daylist): 
    """
    parameters
    ----------
    no int ?: 台風番号
    daylist : [ 日付(YYYYMMDDHH):str ] のリスト
    
    returns
    ----------
    data_list : [date, file_path] のリスト
    """
    input_date, input_img =  [], []
    for i in range(len(daylist) - 6 ):
        six_days = make_6days(daylist[i])

        if( six_days == daylist[i:i+6]  ):

            img_list = []
            for date in six_days:
                file_path, _ = check_file(no, date)
                img_list.append(file_path)
            
            if( (None in img_list) ==  False):
                input_date.append(six_days)
                input_img.append(img_list)
    
    input_date = np.array(input_date)
    input_img = np.array(input_img)

    print("input_date.shape = ", input_date.shape)
    print("input_img.shape = ", input_img.shape)

    return input_date, input_img
test_date, test_img = make_data(T_No_set[0],target_date)

# %%
def main():
    input_date, input_img = [], []
    for no in T_No_set:
        target_date = make_dayarray(no, df)
        test_date, test_img = make_data(no, target_date)
    return input_date, input_img
#%%
if __name__ == "__main__":
    test1, test2 = main()
    print(test1)
    print(test2)
#%%
#%%
# %%
