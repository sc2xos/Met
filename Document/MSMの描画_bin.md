# MSMの描画
## 事前準備 
1. モジュールのインストール  
※一度インストールした環境を使用する場合はスキップしてよい。
```Bash
$conda install conda
$conda install -c conda-forge pygrib
$conda install -c conda-forge basemap
$conda install -c conda-forge colormap
```
1. データの用意
```Bash
$wget http:://..(略).../Z__C_RJTD_201807010000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin
$wgrib2  <grib2.bin> | grep "anl" | wgrib2 -i <grib2.bin> -no_header -bin anl.bin
1.1:0:d=2018070100:PRMSL:mean sea level:anl:
1.2:0:d=2018070100:PRES:surface:anl:
1.3:0:d=2018070100:UGRD:10 m above ground:anl:
1.4:0:d=2018070100:VGRD:10 m above ground:anl:
1.5:0:d=2018070100:TMP:1.5 m above ground:anl:
1.6:0:d=2018070100:RH:1.5 m above ground:anl:
1.7:0:d=2018070100:LCDC:surface:anl:
1.8:0:d=2018070100:MCDC:surface:anl:
1.9:0:d=2018070100:HCDC:surface:anl:
1.10:0:d=2018070100:TCDC:surface:anl:
```
　まず、wgetコマンドで京都大学生存研のサーバーからデータをダウンロードする。次に、wgrib2コマンドを用いて4バイトバイナリデータへ変換する。この際、grepコマンドを用いて描画したい変数のみを抽出する設定にする。これをせずに一括変換をすると、なぜかデータのサイズが合わなくなる。

* wgrib2を用いた抽出変換の例
```Bash
$wgrib2  <grib2.bin> | grep "APCP" | wgrib2 -i <grib2.bin> -no_header -bin <.bin> #予報時刻ごとの降水量を抜き出す

$wgrib2  <grib2.bin> | grep "anl" | wgrib2 -i <grib2.bin> -no_header -bin <.bin> #全変数の解析値のみ抜き出す

$wgrib2  <grib2.bin> | grep "anl" | grep "TMP" | wgrib2 -i <grib2.bin> -no_header -bin <.bin> #気温の解析値のみを抜き出す
```


## 描画
1. モジュールのインポート
```python
import numpy as np
from mpl_toolkits.basemap import Basemap
from colormap import Colormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
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

1. カラーマップの作成
```python
def generate_cmap(colors):
    values = range(len(colors))
    vmax = np.ceil(np.max(values))
    color_list = []
    for v, c in zip(values, colors):
        color_list.append( ( v/ vmax, c) )
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)
```