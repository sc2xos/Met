#%%
import numpy as np
from datetime import datetime,timezone,timedelta
import time
import urllib.request
import sys
import os
#%%
bst_file = "/home/soga/data/typhoon/bst_all.txt"
#%%
def read_bstfile(file: str):
    """
    ベストトラックデータを1行ずつ読み込み、リストに格納
    parameters
    ----------
    lines: array-like
    
    returns
    ----------
    data_list: list of str
    """
    bst_data = open(file, "r")
    lines = np.array(bst_data.readlines())
    bst_list = [ line.split() for line in lines ]
    print("Lines of Best Track Data : ", len(bst_list))
    return bst_list
test = read_bstfile(bst_file)
#%%
for i in test:
    print(i)
#%%
def make_array(data):
    """
    [台風No,日時,中心気圧]を配列に格納
    parameters
    ----------
    data : list of str
    
    returns
    ----------
    data_list: [T_number:str, T_date:str, T_pres:str]
    """
    Master_array, No_array = [], []
    for line in data:
        Value_array = []
        if(line[0] == '66666'):
            T_Number = line[1]
            No_array.append(T_Number)
        else:
            T_date = line[0]
            T_pres = line[5]
            Value_array.append([T_date, T_pres])
        Master_array.append(Value_array)
    Master_array.append(No_array)
    return Master_array
tarray = make_array(test)
print(tarray)
#%%
"""
    empty = []
    for line in data:
        if(line.split()[0] == '66666'):
            T_number = line.split()[1]
        else:
            T_date = line.split()[0]
            T_pres = line.split()[5]
            empty.append([T_number, T_date, T_pres])
    tarray = np.array(empty)
    print(tarray.shape)
    return tarray
tarray = make_array(test)
"""
#%%
def define_url(T_No, band='4'):
    url = 'http://agora.ex.nii.ac.jp/digital-typhoon/wnp/by-name/20{0}/{1}/128x128/HMW8{2}.20{0}.jpg'.format(T_No, band, T_date)
    return url
#%%
def img_download(url, path, title, band='4'):
    if(os.path.isfile(path + title) is True):
        print("Already Exists {0}".format(title))
    else:
        if not os.path.exists(DLDIR):
            os.mkdir(DLDIR)
        print("Download from",url)
        try:
            urllib.request.urlopen(url)
            urllib.request.urlretrieve(url, path + title)
            print("Complete Download!")
        except urllib.error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except urllib.error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
# %%
for t in range(len(tarray[:,0])):
    T_date = tarray[t, 0]
    if(T_date[0:4] == '1507'):
        print(t)
        break
#%%
for t in range(len(tarray[65000::,0])):
    t0 = t + 65000
    T_date = tarray[t0, 1]
    T_No = tarray[t0, 0]
    DLDIR = '/home/soga/data/typhoon/img/hmw/band4/{0}/{1}/'.format(T_date[0:2], T_No)
    print(DLDIR)
    #download
    url = define_url(T_No)
    img_download(url, DLDIR, T_date + '.png')
    time.sleep(1)
    if(t0 == 70000):
        sys.exit()
#%%
#url = define_url(tarray[-1][1])
url = define_url('20090409')
img_download(url, "test.png")
#%%
