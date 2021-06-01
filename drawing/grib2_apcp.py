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
from colormap import Colormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm

# %%
grbs = pygrib.open("Z__C_RJTD_20180701000000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin")
grb = grbs.select(forecastTime=0) #予報時間の選択
for i in range(len(grb)):   #収納されている変数の確認
    print(grb[i])
# %%
apcp = grb[10].values * 100 #変数の取り出し ※要素の数え方は0から始まることに注意
lats, lons = grb[10].latlons()  #緯度経度の取り出し
# %%
def generate_cmap(colors):
    values = range(len(colors))
    vmax = np.ceil(np.max(values))
    color_list = []
    for v, c in zip(values, colors):
        color_list.append( ( v/ vmax, c) )
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)
# %%
fig = plt.figure()
cm = generate_cmap(['white','aqua','lime','yellow','orange','red'])   #カラーマップの生成
lon_min, lon_max, lat_min, lat_max = 120.0, 150.0, 22.40, 47.60   #描画範囲の設定
m = Basemap(projection="cyl", resolution="l",llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max) #地図の設定
m.drawcoastlines(color='black',linewidth=1.0)   #海岸線の描画設定
m.drawmeridians(np.arange(0, 360, 5), labels=[True, False, False, True],linewidth=0.3)  #軽度の描画設定
m.drawparallels(np.arange(-90, 90, 5), labels=[True, False, True, False],linewidth=0.3)  #緯度の描画設定
x, y = m(lons, lats)  #緯度経度の変換
apcp_min, apcp_max = int(np.min(apcp)), int(np.max(apcp))
clevs = [ i for i in range(apcp_min, apcp_max, 1) ]   #等値線の描画間隔の設定
im = plt.contourf(x, y, apcp, clevs, cmap=cm,extend="both",alpha=0.8)    #等値線の描画
#ticks = [ l for l in range(apcp_min, apcp_max, 2) ]
#cb = m.colorbar(im, "right", size="5.0%", ticks=ticks)   #カラーバーの描画
#cb.set_label("mm")  #カラーバーの単位の設定
plt.title('APCP')    #タイトルの描画
plt.savefig('apcp_conoturf.png',dpi=500,bbox_inches="tight", pad_inches=0.05)  #図の保存
plt.show()   #図の表示 
# %%