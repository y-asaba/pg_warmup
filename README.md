# pg_warmup
This is a tool to put PostgreSQL's table and index data onto cache memory.
You can put contents onto not only kernel cache but also shared buffer.

## System Requirements
* Python (2.7, 3.3)
* psycopg2 (pip install psycopg2)

## How to install
* Using pip
```
  % pip install pg_warmup
```
* Build from souce code
```
  % pip install psycopg2
  % python setup.py install
```


## Usage
* You need to run pg_warmup by postgres superuser
* You may also need to set PG_* environment variables to connect the server
* Use -x option if you want to warm up actually. Default is dry-run mode
* Run "ionice -c 3 cat filename" when -i option is passed


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
