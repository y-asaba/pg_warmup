# pg_warmup
PostgreSQL起動後にtableやindexをキャッシュにのせるためのツールです。キャッシュは以下の2つを選択できます。

* shared_buffer
* OSのページキャッシュ(デフォルト)

## System Requirements
* Python (2.7, 3.3)
* psycopg2 (pip install psycopg2)

## 使い方
* PostgreSQLを起動しているユーザ(大抵の場合はpostgresユーザ)で実行します
* 場合によってはPG_HOSTなどのPG_*環境変数を設定する必要があります
* -xをつけないとdry runとなり、実際には動かしません
* -i option はionice -c 3で物理ファイルをcatします
* shared bufferは単純にseq scanするだけなので、インデックスはキャッシュに乗りません。


```
Usage: pg_warmup [options]

Options:
  -h, --help            show this help message and exit
  -t TABLE, --table=TABLE
                        warmup the named table
  -d DATABASE, --database=DATABASE
                        dbname
  -i                    use ionice command
  -s                    cache on shared buffer, not page cache
  -x                    execute warmup
```
