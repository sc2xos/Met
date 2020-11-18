※CentOS7に/usr/localにversion2.2.1をインストールする場合
1. [Grads公式ページ](http://cola.gmu.edu/grads/downloads.php)からソースコードをダウンロード
```Bash
$wget ftp://cola.gmu.edu/grads/2.2/grads-2.2.1-bin-centos7.4-x86_64.tar.gz
```

2. ソースコードの展開
```Bash
$tar -xvf grads-2.2.1-bin-centos7.4-x86_64.tar.gz
$sudo mv grads-2.2.1 /usr/local/
```

3. 必要なライブラリを追加する

※環境によってはこれをしないと起動できない場合がある
```Bash
$wget ftp://cola.gmu.edu/grads/Supplibs/2.2/builds/supplibs-centos7.4-x86_64.tar.gz
$tar -xvf supplibs-centos7.4-x86_64.tar.gz
$sudo mv supplibs /usr/local/
$echo "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/supplibs/lib" >> ~/.bashrc
```

4. Gradsライブラリをダウンロード

[ダウンロードページ](https://researchmap.jp/multidatabases/multidatabase_contents/detail/232785/5dc1aaaf5a0d631c7e4b20d34f002f6c?frame_id=822841)

```Bash
$unzip gradslib.zip
$sudo cp gradslib/* /usr/local/grads-2.2.1/lib
```

5. 地図データをダウンロード
```Bash
$wget ftp://cola.gmu.edu/grads/data2.tar.gz
$sudo mv data2.tar.gz /usr/local/grads-2.2.1/data/
$cd /usr/local/grads-2.2.1/data
$sudo tar -xvf data2.tar.gz
```

6. 高解像度マップのダウンロード
```Bash
$cd /usr/local/grads-2.2.1/data
$sudo wget ftp://cola.gmu.edu/grads/boundaries/newmap
$sudo wget ftp://cola.gmu.edu/grads/boundaries/worldmap
```

7. udptファイルの作成(2.2.1以降)
grads-2.2.1で
```Bash
$vim udpt
```
でテキストファイルを作成し、中身を
```text
# Type     Name     Full path to shared object file
# ----     ----     -------------------------------
gxdisplay  Cairo    /usr/local/lib/grads-2.2.1/libgxdCairo.so
gxdisplay  X11      /usr/local/lib/grads-2.2.1/libgxdX11.so
gxdisplay  gxdummy  /usr/local/lib/grads-2.2.1/libgxdummy.so
*
gxprint    Cairo    /usr/local/lib/grads-2.2.1/libgxpCairo.so
gxprint    GD       /usr/local/lib/grads-2.2.1/libgxpGD.so
gxprint    gxdummy  /usr/local/lib/grads-2.2.1/libgxdummy.so
*
function   dothis   /home/username/grads-2.2.1/udp/dothis.so
```

8. ~/.bashrcにパスを追加する
```Bash
$echo "export GRADSHOME=/usr/local/grads-2.2.1" >> ~/.bashrc
$echo "export GADDIR=${GRADSHOME}/data" >> ~/.bashrc
$echo "export GASCRP=${GRADSHOME}/lib" >> ~/.bashrc
$echo "export GAUDPT=${GRADSHOME}/udpt"  >> ~/.bashrc
$echo "export PATH=${PATH}:${GRADSHOME}/bin" >> ~/.bashrc
$echo "alias grads=grads" >> ~/.bashrc
$source ~/.bashrc

```



9. 起動確認
```Bash
$grads
```

sudo yum install libjpeg-turbo
sudo yum install libX11
sudo yum install libXext
sudo yum install 