# %%
import numpy as np
import cv2
import os
# %%
def make_T_Date(T_year, T_month, T_day, T_hour):
    """
    parameters
    ----------
    
    returns
    ----------
    T_date :  日付(YYYYMMDDHH)のリスト
    """
    T_Date_list = []
    for year, month, day, hour in zip(T_year, T_month, T_day, T_hour):
        T_Date_list.append(str(year).zfill(4) + str(month).zfill(2) + str(day).zfill(2) + str(hour).zfill(2))
    return T_Date_list
# %%
def cutout_center(input_img:str):
    pos = input_img.index('/')
    input_dir, input_name = input_img[pos:], input_img[:pos]
    output_img = (cv2.imread(input_img))[100:420, 100:420]
    #出力先ディレクトリの作成
    output_dir = input_dir + "center"
    if(os.path.isdir(output_dir) is True):
        print("Already Exists {0}".format(output_dir))

    else:
        os.makedirs(output_dir)
        print("Completed making {0}".format(output_dir))
    cv2.imwrite(output_dir + "/" + input_name, output_img)
    return output_img


test = cutout_center("/home/soga/data/typhoon/img/hmw/band4/2020/2022/HMW820111418.202022.jpg")