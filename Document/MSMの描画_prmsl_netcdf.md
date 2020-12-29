## 事前準備 
1. モジュールのインストール  
※一度インストールした環境を使用する場合はスキップしてよい。
```Bash
$conda install conda
$conda install -c anaconda netcdf4
$conda install -c conda-forge basemap
$conda install -c conda-forge basemap-data-hires
```
* 今回はECMWFのERA-interiumの2018年の月平均のデータを用いる。

## 描画
1. モジュールのインポート
```python
import numpy as np
import netcdf4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
```
* basemapのインポートでエラーが出る場合、以下を追加すると改善するかも
```python
import os
import conda
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
```

2. データの読み込み
```Python
data = nc.Dataset('ERA_interium_201807_monthly.nc','r')   #データの読み込み
print(data)   #格納されている変数の情報を表示
```

3. 変数の取り出し
```Python
data.variables.keys()   #変数を読み込むための準備
lon = data.variables['longitude'][:]   #経度の読み込み(1次元配列)
lat = data.variables['latitude'][:]   #緯度の読み込み(1次元配列)
prmsl = data.variables['msl'][:] / 100   #海面更正気圧の読み込み(Pa ⇒ hPa)
```
4. 緯度経度を２次元配列に変換
緯度経度が１次元配列で読み込まれるた２次元配列に変換する必要がある。
```Python
flon, flat = np.meshgrid(lon,lat)   #【重要】緯度経度を二次元配列に変換
```
5. 描画
基本的に以下はpygribのときと同じ。
```Python
fig = plt.figure()
lon_min, lon_max, lat_min, lat_max = 120.0, 150.0, 22.40, 47.60   #描画範囲の設定
m = Basemap(projection="cyl", resolution="h",llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max) #地図の設定
m.drawcoastlines(color='black',linewidth=1.0)   #海岸線の描画設定
m.drawmeridians(np.arange(0, 360, 5), labels=[True, False, False, True],linewidth=0.3)  #軽度の描画設定
m.drawparallels(np.arange(-90, 90, 5), labels=[True, False, True, False],linewidth=0.3)  #緯度の描画設定
x, y = m(flon, flat)  #緯度経度の変換
prmsl_min, prmsl_max = int(np.min(prmsl)), int(np.max(prmsl))
clevs=[ thin for thin in range(prmsl_min, prmsl_max, 2) ]   #等値線の描画間隔の設定
im = plt.contour(x, y, prmsl[0,:,:], clevs, colors='black',alpha=0.5)    #等値線の描画
im.clabel(fontsize=10,fmt="%d")   #数値の表示
plt.title('PRMSL')    #タイトルの描画
plt.savefig('netcdf_prmsl_contour.png',dpi=500,bbox_inches="tight", pad_inches=0.05)  #図の保存
plt.show()   #図の表示
```


