# %%
import sys
import json
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt

import pygrib
from bullet import Bullet
from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import seaborn as sns

import cliutils
import figutils
#%%統計量の表示
def view_stat(data):
	print("Average", np.nanmean(data))
	print("Min", np.nanmin(data))
	print("Max", np.nanmax(data))
# %%データの読み込み
def read_data(data):
	grbs = pygrib.open(data)
	grb = grbs.select(forecastTime=0)
	#変数名の取り出し
	value_list = []
	for v in range(len(grb)):
		indexes = [i for i, x in enumerate(str(grb[v])) if x == ":"]
		value_list.append(str(grb[v])[indexes[0]+1:indexes[1]])
	value_name = cliutils.cli("##### Choose valiable #####", value_list)
	# 予報時間の選択
	vgrb = grbs.select(name=value_name)
	ft_list = []
	for i in range(len(vgrb)):
		ft_list.append("Forecast Time : {0},  Valid Date : {1}".format(vgrb[i].forecastTime, vgrb[i].validDate))
	ft_name = cliutils.cli("##### Choose Forecast Time #####", ft_list)
	ft = vgrb[ft_list.index(ft_name)].forecastTime
	valid_date = vgrb[ft_list.index(ft_name)].validDate
	value = grbs.select(name=value_name,forecastTime=ft)[0].values
	#選択した変数の統計量の表示
	view_stat(value)
	#緯度・経度の取り出し
	lats, lons = grb[0].latlons()
	return value, lats, lons, value_name, valid_date
 
# %%jsonからデフォルト値を読み込む
def read_json(kind, param_name):
	default_file = open("default.json", 'r')
	json_data = json.load(default_file)
	param =  json_data[kind][param_name]
	return param

# %%パラメータを定義
def set_default():
	lon_min = float(read_json("Area","lon_min"))
	lon_max = float(read_json("Area","lon_max"))
	lat_min = float(read_json("Area","lat_min"))
	lat_max = float(read_json("Area","lat_max"))
	param_list = [lon_min, lon_max, lat_min, lat_max]
	print("[lon_min, lon_max, lat_min, lat_max] = ",param_list)
	return param_list

#%% 終了処理
def end_process():
	print("#######################")
	print("S : 図を保存")
	print("N : 次の時刻の図を表示")
	print("P : 前の時刻の図を表示")
	print("E : 終了")
	print("#######################")
	input = sys.stdin.readline().rstrip
	end_input = input()
	if(end_input == "S"):
		plt.savefig(titile, dpi=param5, bbox_inches="tight", pad_inches=0.05)    #図の保存
	elif(end_input == "N"):
		print("次の時刻の図を表示します.")
		valid_date = valid_date # + datetime 時刻の更新
		value = grbs.select(name=value_name,valid_date=valid_date)[0].values
		return value, valid_date
	elif(end_input == "P"):
		print("前の時刻の図を表示します.")
		valid_date = valid_date #v- datetime 時刻の更新
		value = grbs.select(name=value_name,valid_date=valid_date)[0].values
		return value, valid_date
	elif(end_input == "E"):
		exit()
# %%実行処理
def main():
	# %%引数の設定(読み込むファイル)
	parser = argparse.ArgumentParser(description='grib2ファイルを引数に指定')
	parser.add_argument('arg1', help='読み込むファイル')
	args = parser.parse_args()
	loop = 0 
	while(True):
		print(loop)
		if(loop == 0):
			print("#### loop 0 ####")
			values, lons, lats, value_name, valid_date = read_data(args.arg1)
			param_list = set_default()
		else:
			end_process()
		title = ( value_name +"\n"+ str(valid_date) )
		figutils.make_figure(values, lons, lats, title, param_list)
		loop += 1
# %%
if __name__ == "__main__":
	main()

# %%
