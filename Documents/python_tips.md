# Python Tips

## ディレクトリ・ファイル操作
* ディレクトリ(ファイル)の存在確認
`os.path.exists()  == ( True or False )`
* ディレクトリの作成
`os.makedirs()`
* カレントディレクトリの取得
`os.getcwd()`
* ディレクトリの移動
`os.chdir()`
**


## ◎連続したデータの読み込み

`202001010000.bin` ~ `202001100000.bin`のファイルを一気に読み込みたいとき

```python
import datetime as dt
start_date = dt.datetime(2020, 1, 1, 0)    #初期時刻
end_date = dt.datetime(2020, 1, 10, 0)     #終了時刻
read_date = start_date
data_array = []                            #空のリストの作成
while(  read_date <= end_date ):
    read_file = read_date.strftime("%Y%m%d%H%MM") + ".bin"
    print("Read Data : {}".format(read_file))
    data = np.fromfile(read_file, dtype=np.float32)         #データの読み込み(np.float32=4by浮動小数点数)
    data_array.append(data)                                 #リストに追加
    read_date = read_date + dt.timedelta(hours=6)           #6時間ごとに時刻を更新する
output = np.array(data_array)                               #ndarrayに変換
print(output.shape)
```

## ◎欠損値の処理

* 欠損値が-9999.0で指定されているとき

```python
TMP = np.where(APCP == -9999.0, np.nan, TMP)
```

* 降水量を描画するとき、降水なしの領域をマスクしたいとき

```
APCP  = np.where( APCP <= 0., np.nan, APCP)
```

numpyにおける欠損値は`np.nan`で指定される。  
`np.nan`が含まれる配列に対して`np.sum`を使用すると、出力結果が`np.nan`で返ってきてしまう。  
代わりに`np.nansum`を使用することで欠損値を除いて計算をしてくれる。  
(同様に、`np.nanmean`、`np.nanmax`、`np.nanmin`、`np.nanstd`なども)

## ◎降水量スコアの計算

### サンプルコード

```python
def calc_score(model, obs, threshold):
    model = model.flatten()   #1次元配列に変換
    obs = obs.flatten()
    FO = 0
    FX = 0
    XO = 0
    XX = 0
    others = 0
    for i in range(len(model)):
        if( model[i] >= 0 and obs[i] >= 0 ):
            if( model[i] >= threshold and obs[i] >= threshold ):
                FO = FO + 1
            elif( model[i] >= threshold and obs[i] < threshold ):
                FX = FX + 1
            elif( model[i] < threshold and obs[i] >= threshold ):
                XO = XO + 1
            elif( model[i] < threshold and obs[i] < threshold ):
                XX = XX + 1
            else:
                others = others + 1
    bias=(FO + FX) / (FO + XO)
    threat= FO / (FO + FX + XO)
    print('########## Threshold : {} ##########'.format(threshold))
    print('Bias_score : {}'.format(bias))
    print('Threat_score : {}'.format(threat))
    return bias,threat
```
