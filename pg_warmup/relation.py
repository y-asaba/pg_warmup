#/* -*- coding: utf-8 -*- */

import sys
import psycopg2
from subprocess import check_output
import os.path


class RelationNotFoundException(Exception):
    pass


class RelationFileAccessDeniedException(Exception):
    pass


class Relation(object):
    def __init__(self, dbname, relname, size, path):
        self.dbname = dbname
        self.relname = relname
        self.size = int(size)
        self.path = path
        self.indexes = []
        self.make_db_connection()

    def __del__(self):
        self.conn.close()
        self.conn = None

    def make_db_connection(self):
        self.conn = psycopg2.connect("dbname=%s" % self.dbname)

    def add_index(self, index):
        self.indexes.append(index)

    def warmup(self, dryrun=True, use_shared_buffer=False, use_ionice=True):
        print("#### WARMUP ####")
        if (use_shared_buffer):
            cur = self.conn.cursor()
            sql = "SELECT count(*) from %s" % self.relname
            print("Query: %s" % sql)
            if not dryrun:
                cur.execute("SELECT count(*) from %s" % self.relname)
        else:
            if use_ionice:
                ionice = 'ionice -c 3'
            else:
                ionice = ''

            # cat relation file
            for p in self.path:
                cmd = "%s cat %s > /dev/null" % (ionice, p)
                print(cmd)
                if not dryrun:
                    check_output(cmd, shell=True)

            for i in self.indexes:
                for index_path in i.path:
                    cmd = "%s cat %s > /dev/null" % (ionice, index_path)
                    print(cmd)
                    if not dryrun:
                        check_output(cmd, shell=True)
            print("Done")

    @classmethod
    def get_relation(cls, dbname, relname):

        def get_path_list(basepath):
            if not os.path.exists(basepath):
                raise RelationFileAccessDeniedException

            #
            # get relfilenode.%d files
            #
            path_list = [basepath]
            num = 1
            while True:
                path = "%s.%d" % (row[1], num)

                if os.path.exists(path):
                    path_list.append(path)
                    num += 1
                else:
                    break

            return path_list


        data = Relation(dbname, relname, 0, '')
        cur = data.conn.cursor()

        #
        # get table name, size and file path
        #
        cur.execute("""
SELECT relname, current_setting('data_directory') || '/' ||  pg_relation_filepath(oid) AS filepath,
       pg_relation_size(oid) AS filesize
   FROM pg_class WHERE relname = %s;
""", (relname,))
        rows = cur.fetchall()
        if (len(rows) == 0):
            raise RelationNotFoundException
        for row in rows:
            data.path = get_path_list(row[1])
            data.size = int(row[2])
            print(data.path)

        #
        # get index name, size and file path
        #
        cur.execute("""
SELECT relname, current_setting('data_directory') || '/' ||  pg_relation_filepath(oid) AS filepath,
       pg_relation_size(oid) AS filesize
   FROM pg_class WHERE oid IN (SELECT indexrelid FROM pg_index
                                  WHERE indrelid = (SELECT oid FROM pg_class WHERE relname = %s))
""", (relname,))
        rows = cur.fetchall()
        for row in rows:
            data.add_index(Index(row[0], get_path_list(row[1]), row[2]))

        return data

    def print_relation(self):
        print("#### TABLE ####")
        print("name: %s, size: %.2lfMB" % (self.relname, (self.size / 1024 / 1024)))
        print("filepath:")
        for p in self.path:
            print("\t%s" % p)

        if (len(self.indexes) != 0):
            print("")
            print("#### INDEX ####")
            for i in self.indexes:
                print("name: %s, size: %.2lfMB" % (i.index_name, (i.size / 1024 / 1024)))
                print("filepath:")
                for p in i.path:
                    print("\t%s" % p)
                print("")


class Index(object):
    def __init__(self, index_name, path, size):
        self.index_name = index_name
        self.size = int(size)
        self.path = path
