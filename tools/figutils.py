#%%
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

# %%作図処理(Cartopy)
def make_figure(data, lons, lats, title, param_list):
	lon_min, lon_max, lat_min, lat_max = param_list
	print("作図処理を開始します")
	fig = plt.figure()
	proj = ccrs.PlateCarree() 
	ax = fig.add_subplot(1, 1, 1, projection=proj)
	ax.set_extent((lon_min, lon_max, lat_min, lat_max), proj) # 緯度経度の範囲を指定
	data = data / 10
	data_min, data_max = int(np.min(data)), int(np.max(data))
	levels = [ thin for thin in range(data_min, data_max, 2) ]
	CS = ax.contour(lons, lats, data, levels, transform=proj)
	#ax.clabel(CS,fmt='%.0f') 
	fig.colorbar(CS,shrink=0.5)
	ax.gridlines()
	ax.coastlines(resolution='10m')
	ax.set_title("test")
	plt.show()
#%%
# %%作図処理
"""
def make_figure(data, lons, lats, title, param_list):
	lon_min, lon_max, lat_min, lat_max = param_list
	print("作図処理を開始します")
	fig = plt.figure()
	m = Basemap(projection="cyl", resolution="l", llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max)     #地図の設定
	m.drawcoastlines(color='black',linewidth=1.0)
	m.drawmeridians(np.arange(0, 360, 5), labels=[True, False, False, True], linewidth=0.3)
	m.drawparallels(np.arange(-90, 90, 5), labels=[True, False, True, False], linewidth=0.3)
	x, y = m(lons, lats)
	data = data / 10
	data_min, data_max = int(np.min(data)), int(np.max(data))
	clevs=[ thin for thin in range(data_min, data_max, 2) ]
	im = plt.contour(x, y, data, clevs, colors='black', alpha=0.5)
	print(data.shape)
	im.clabel(fontsize=10,fmt="%d")
	plt.title(title)
	plt.show()
"""