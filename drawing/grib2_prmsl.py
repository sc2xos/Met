#%%
#KeyError: 'PROJ_LIB'が出る場合
import os
import conda
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
# %%
import numpy as np
import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# %%
grbs = pygrib.open("Z__C_RJTD_20180701000000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin")
grb = grbs.select(forecastTime=0)    #予報時間の選択
for i in range(len(grb)):            #収納されている変数の確認
    print(grb[i])
# %%
prmsl = grb[0].values / 100          #変数の取り出し & hPaへの変換
lats, lons = grb[0].latlons()        #緯度経度の取り出し
# %%
fig = plt.figure()
lon_min, lon_max, lat_min, lat_max = 120.0, 150.0, 22.40, 47.60    #描画範囲の設定
m = Basemap(projection="cyl", resolution="l",llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max)     #地図の設定
m.drawcoastlines(color='black',linewidth=1.0)       #海岸線の描画設定
m.drawmeridians(np.arange(0, 360, 5), labels=[True, False, False, True],linewidth=0.3)      #経度の描画設定
m.drawparallels(np.arange(-90, 90, 5), labels=[True, False, True, False],linewidth=0.3)     #緯度の描画設定
x, y = m(lons, lats)    #緯度経度の２次元配列への変換
prmsl_min, prmsl_max = int(np.min(prmsl)), int(np.max(prmsl))
clevs=[ thin for thin in range(prmsl_min, prmsl_max, 2) ]    #等値線の描画間隔の設定
im = plt.contour(x, y, prmsl, clevs, colors='black',alpha=0.5)   #等値線の描画
im.clabel(fontsize=10,fmt="%d")    #数値の表示
plt.title('PRMSL')    #タイトルの挿入
plt.savefig('contour.png',dpi=500,bbox_inches="tight", pad_inches=0.05)    #図の保存
plt.show()    #図の表示

# %%
