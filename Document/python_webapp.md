# Python Webアプリ作成

## Flask
メインディレクトリを作成。   
メインディレクトリ直下にメインプログラム(*.py)を配置。  

* Template Engine:HTMLをレンダリングする。    
メインディレクトリ配下にtemplateディレクトリを作成。  
templateディレクトリにhtmlを配置。  

* Static Files:
メインディレクトリ配下にstaticディレクトリを作成。  
HTMLファイル以外の、CSSファイル・JSファイル・画像ファイル等を配置。  

* Images:  
staticフォルダ内にimagesフォルダを作成し、その中に任意の画像を配置。  

* クエリストリングを受け取ってhtmlに送る。
requestモジュールをインポートして、request.args.get(paramater)で、クエリストリングを受け取ることができます。  
また、受け取ったクエリストリングをrender_template()の引数に入れることで、html側に送ることができます。  
html内で変数を表示するには{{ var }}を埋め込めばOKです。

* index.htmlにif文を導入する。
htmlファイル内では{% %}ブロック内にpythonコードを埋め込んであげればOKです。　

* POSTリクエストを受け取る
htmlにPOSTリクエストを送信するフォームを追加する。  
(formタグ、action属性)  
app.pyにPOSTリクエストを受け取る機構を用意する。  
フォームのテキスト要素を取得し、nameとしてhtml側に値を渡す。  

* Databaseの追加
sqlalchemyというモジュールを使用。  
メインディレクトリ配下にmodelsディレクトリを作成。  
__init__.py(中身は空)  
models.py:テーブルのカラム情報を定義するためのクラスを格納。 
(テーブル操作を行う際のレコード生成もこのクラスを通して行う。)  
database.py:DBとの直接的な接続情報を格納する。  





app.run
threaded:並列処理による同時アクセスを可能にする。
