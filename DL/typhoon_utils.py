# %%
import numpy as np


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