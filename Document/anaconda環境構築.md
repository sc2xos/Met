
Python2系がデフォルトで入っている場合が多いが、Anacondaに導入されているPython3系を利用すると便利
## Anacondaのインストール
1. pyenvをインストール
```Bash
$git clone https://github.com/yyuu/pyenv.git ~/.pyenv  
$echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc  
$echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc  
$echo 'eval "$(pyenv init -)"' >> ~/.bashrc  
$source ~/.bashrc
```
2. Anacondaをインストール
```Bash
$pyenv install -l | grep anaconda #配布されているバージョンを確認
$pyenv install anaconda3-5.3.1 #最新版をインストール
$pyenv global anaconda3-5.3.1 #Anacondaのpythonをデフォルトに指定
$echo 'export PATH="$PYENV_ROOT/versions/anaconda3-5.3.1/bin/:$PATH"' >> ~/.bashrc
$source ~/.bashrc
$conda update conda
```
## Anacondaの使い方(コマンド)
* パッケージのインストール
```Bash
$conda install (パッケージ名) #単純なインストール
$conda install (パッケージ名)==x.x.x #バージョン指定
```
* パッケージのアンインストール
```Bash
$conda uninstall (パッケージ名)
```
* インストール済みパッケージを表示
```Bash
$conda list
```
* パッケージのアップデート
```Bash
$conda update --all #すべてをアップデート
$conda update (パッケージ名) #特定のパッケージをアップデート
$conda update conda #condaじたいをアップデート
```
※update --allは特定のバージョンなど環境に依存している場合は、むやみにしないほうが良い

* 仮想環境
```Bash
$conda create -n (name) python=[version] [library] #仮想環境の構築
$conda activate (仮想環境名) #仮想環境の有効化
$conda deactivate (仮想環境名) #仮想環境の無効化
$conda remove -n (仮想環境名) --all #仮想環境の削除
```

【参考】  
[Anaconda公式](https://www.anaconda.com/)  
[Anacondaでよく使うコマンド(Qiita)](https://qiita.com/naz_/items/84634fbd134fbcd25296)


## <参考>intel Pythonの有効化
通常のpythonよりも高速(らしい)ので、intel pythonをデフォルトにした仮想環境を構築

```Bash
$conda update conda #condaのアップデート
$conda config --add channels intel #intelのチャンネルの登録
```

どちらか選んで実行(フルパッケージのほうが無難)
* コアパッケージのみ(numpy, scipyなどのみ)の仮想環境を構築
```Bash
$conda create -n intel intelpython3_core python=3
```
* フルバージョンの仮想環境を構築
```Bash
$conda create -n intel intelpython3_full python=3
```

作った仮想環境を有効化
```Bash
$conda activate intel
$source activate intel #condaでできない場合はこっちで
```

* yamlファイルを使った仮想環境の作り方 　

以下のようなフォーマットでyamlファイルを作成する.

```yml
name: hoge
channels:
- <channel_name>
dependicies:
- <pakcage_name>
pip:
- <package_name>
```

以下のコマンドで、yamlファイルの内容で仮想環境を作成.

```Bash
$conda env craete -f hoge.yml
```  

* conda仮想環境からyamlファイルを作成する.

```Bash
$conda env export >> hoge.yaml
```