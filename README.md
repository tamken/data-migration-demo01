# data-migration-demo01

## 概要
1. CSVファイルをDB（MySQL）へインポート
	- 設定ファイルをほんの少し書き換えるだけで、（おそらく）どんなCSVも楽々データ取り込み可能です（たぶん）
1. DB（MySQL）からデータ抽出/加工を実施し、CSVファイルへエクスポート
	-  ※ 準備中
## 動作環境
- 必須
	- Python: >=3.7 （3.9推奨）
	- pipenv: (any)
	- MySQL: >=5.7
- 任意
	- Docker: (any)
		- MySQLコンテナ起動用途（Dockerがインストールされていれば手っ取り早く動作確認できます）
## 使い方等
### ■ 処理実施
1. CSVインポート（CSV to DB）
	- インポート対象のCSVの情報の定義方法は後述参照
	```
	# 既存テーブルにアペンド
	> pipenv run python 01_import.py {code}

	# 既存テーブルのレコードをすべてクリアした後にインポート
	> pipenv run python 01_import.py {code} truncate

	# CSVの内容でテーブルを（再）作成した後にインポート
	> pipenv run python 01_import.py {code} recreate
	```
1. CSVエクスポート（DB to CSV）
	```
	（準備中です）
	```

### ■ セットアップ

※ macの方向けの内容です（windowsの方、ごめんなさい）

1. クローン
	- developブランチをクローン
	```
	> git clone -b develop https://github.com/tamken/data-migration-demo01.git
	```
1. pipenvインストール（未インストール時のみ）
	```
	> pip install pipenv
	or
	> pip3 install pipenv
	```
1. pythonのパッケージインストール
	```
	> pipenv install
	```
1. envファイルコピー
	```
	> cp .env.example .env
	```
1. envファイル設定
	- 自前のMySQLで実施/確認する場合は接続情報を設定してください
	- 当リポジトリで用意してるシェルファイルでMySQLコンテナを起動する場合は設定不要です（.envデフォルトのままでOKです）
	```
	> vi .env
	# DB接続情報を編集する
	```
1. 【補足】当リポジトリで用紙してるシェルファイルでのMySQL起動/停止手順
	1. 起動
		```
		> ./docker/boot.sh
		```
	1. 停止
		```
		> ./docker/stop.sh
		```
### ■ インポート対象のCSVの情報の定義方法
1. CSVの情報を定義するファイル
	- ./src/enums/in_csv_conf_enum.py
	- ↑の中の下記を変更またはコピーして追記する
		```
		IN_SAMPLE = {
			"code": "sample",
			"table": {
				"name": "t_sample_001",
				"column_prefix": "s001_",
			},
			"input": {
				"dir": "input/01_sample",
				"encode": EncodeEnum.UTF8,
				"delimiter": ",",
				"quotechar": "\"",
				"exists_header": True,
			},
		}
		```
1. CSVの情報を定義内容
	|Enum名/キー|設定値|補足|
	|:---|:---|:---|
	|{`IN_SAMPLE`} 箇所|Enum名|<ul><li>一意にすること</li></ul>|
	|code|CSVコード|<ul><li>一意にすること</li><li>`実行時、第１引数に指定する値です`</li></ul>|
	|table.name|インポート先のDBテーブル名|<ul><li>一意にすること</li></ul>|
	|table.column_prefix|インポート先DBテーブルの項目名の接頭辞|<ul><li>未設定時は`c`</li></ul>|
	|imput.dir|インポート対象CSVファイルを格納するディレクトリ||
	|imput.encode|インポート対象CSVファイルの文字コードを設定<br><ul><li>utf8 -> EncodeEnum.UTF8</li><li>utf8(BOM付) -> EncodeEnum.UTF8BOM</li><li>SJIS -> EncodeEnum.SJIS</li><li>cp932 -> EncodeEnum.CP932</li><li>その他 -> ごめんなさい</li></ul>|<ul><li>文字コードはCSVファイルを任意のエディタ等で開いて確認してみてください</li></ul>|
	|imput.delimiter|インポート対象CSVファイルの区切り文字|<ul><li>ので「`,`」</li><li>.tsvファイルなら「`\t`」かなぁ</li></ul>|
	|imput.quotechar|インポート対象CSVファイル内の値の囲み文字|<ul><li>「`\"`」ダブルクォート指定で基本問題無し</li></ul>|
	|imput.exists_header|インポート対象CSVファイルの1行目が項目名のヘッダか否か<ul><li>ヘッダ行有り -> True</li><li>ヘッダ行無し -> False</li></ul>||
1. 【例】郵便番号データを取り込み場合の設定
	1. [日本郵便](https://www.post.japanpost.jp/zipcode/dl/oogaki-zip.html)のサイトから任意の郵便番号CSVをDL
	1. DLしたcsvを任意のエディタで開いて諸々調べる
		|||
		|:---|:---|
		|文字コード|Shift JIS（SJIS）|
		|区切り文字|カンマ（,）|
		|囲い文字|ダブルクォート（"）|
		|項目名ヘッダの有無|無し|
	1. 調べた情報を元にCSV定義を追加する
		```
		POSTCD = {
			"code": "postcd",
			"table": {
				"name": "t_postcd",
				"column_prefix": "pc",
			},
			"input": {
				"dir": "input/02_postcd",
				"encode": EncodeEnum.SJIS,
				"delimiter": ",",
				"quotechar": "\"",
				"exists_header": False,
			},
		}
		```
	1. DLしたcsvファイルを↑で定義したディレクトリに格納する
	1. 実行する
		```
		# 最初はテーブル無いので第2引数に recreate を指定する
		> pipenv run python 01_import.py postcd recreate
		```
	1. 以上
## 参照
- [pipenv](https://github.com/pypa/pipenv)
	- パッケージ管理
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)
	- MySQLクライアント
- [python-dotenv](https://github.com/theskumar/python-dotenv)
	- 環境変数設定
## その他
- 当リポジトリに掲載してるプログラムの使用から生ずるいかなる損害に対しても責任を負いません。
