#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import MySQLdb
from .preprocess import preprocessing


def create_word_dir():
    # open database connection
    db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1301410442', db='imdb_ttds')
    # use cursor() method
    cursor = db.cursor()

    # SQL query sentence
    name_query_sql = "SELECT film_id, name FROM film"
    other_query_sql = "SELECT film_id, other_name FROM film"
    description_query_sql = "SELECT film_id, description FROM film"
    actor_query_sql = "SELECT film_id, actor_string FROM film"
    director_query_sql = "SELECT film_id, director_name FROM directors"

    try:
        # execute SQL sentence
        cursor.execute(name_query_sql)
        # obtain all records
        results = cursor.fetchall()
        for row in results:
            name_list = preprocessing(row[1])
            f_index = 1
            for f_name in name_list:
                # print(row[1])
                f_sql = "INSERT INTO INVERT_NAME(film_id, name_token, pos) VALUES ('%s', '%s', '%s')" % \
                      (row[0], f_name, f_index)

                try:
                    cursor.execute(f_sql)
                    db.commit()
                    f_index += 1
                except:
                    # Rollback in case there is any error
                    db.rollback()

        # execute SQL sentence
        cursor.execute(other_query_sql)
        # obtain all records
        results = cursor.fetchall()
        for row in results:
            other_name_list = preprocessing(row[1])
            o_index = 1
            for o_name in other_name_list:
                o_sql = "INSERT INTO INVERT_OTHER_NAME(film_id, other_name_token, pos) VALUES ('%s', '%s', '%s')" % \
                        (row[0], o_name, o_index)
                try:
                    cursor.execute(o_sql)
                    db.commit()
                    o_index += 1
                except:
                    # Rollback in case there is any error
                    db.rollback()

        # execute SQL sentence
        cursor.execute(description_query_sql)
        # obtain all records
        results = cursor.fetchall()
        for row in results:
            description_list = preprocessing(row[1])
            d_index = 1
            for des in description_list:
                d_sql = "INSERT INTO INVERT_DES(film_id, des_token, pos) VALUES ('%s', '%s', '%s')" % \
                        (row[0], des, d_index)
                try:
                    cursor.execute(d_sql)
                    db.commit()
                    d_index += 1
                except:
                    # Rollback in case there is any error
                    db.rollback()

        # execute SQL sentence
        cursor.execute(actor_query_sql)
        # obtain all records
        results = cursor.fetchall()
        for row in results:
            actor_list = re.split("[,.-: ]+", row[1])
            a_index = 1
            for actor in actor_list:
                a_sql = "INSERT INTO INVERT_ACTOR(film_id, actor_token, pos) VALUES ('%s', '%s', '%s')" % \
                        (row[0], actor, a_index)

                try:
                    cursor.execute(a_sql)
                    db.commit()
                    a_index += 1
                except:
                    # Rollback in case there is any error
                    db.rollback()

        # execute SQL sentence
        cursor.execute(director_query_sql)
        # obtain all records
        results = cursor.fetchall()
        for row in results:
            director_list = preprocessing(row[1]).split(',|.|-|:| ')
            dir_index = 1
            for director in director_list:
                dir_sql = "INSERT INTO INVERT_DIRECTOR(film_id, director_token, pos) VALUES ('%s', '%s', '%s')" % \
                        (row[0], director, dir_index)

                try:
                    cursor.execute(dir_sql)
                    db.commit()
                    dir_index += 1
                except:
                    # Rollback in case there is any error
                    db.rollback()

    except:
        print("Error: unable to fetch data")

    # close db connection
    db.close()


'''
sql_list = []
sql_list.append("CREATE TABLE `INVERT_NAME` ("
                "`count` int(11) NOT NULL,"
                "`film_id` varchar(40) NOT NULL COMMENT '参演电影id',"
                "`name_token` text NOT NULL,"
                "`pos` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `INVERT_OTHER_NAME` ("
                "`count` int(11) NOT NULL,"
                "`film_id` varchar(40) NOT NULL COMMENT '参演电影id',"
                "`other_name_token` text NOT NULL,"
                "`pos` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `INVERT_DES` ("
                "`count` int(11) NOT NULL,"
                "`film_id` varchar(40) NOT NULL COMMENT '参演电影id',"
                "`des_token` text NOT NULL,"
                "`pos` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
# add primary keu
sql_list.append("ALTER TABLE `INVERT_NAME` ADD PRIMARY KEY (`count`);")
sql_list.append("ALTER TABLE `INVERT_OTHER_NAME` ADD PRIMARY KEY (`count`);")
sql_list.append("ALTER TABLE `INVERT_DES` ADD PRIMARY KEY (`count`);")
# auto-incremental sqls
sql_list.append("ALTER TABLE `INVERT_NAME` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `INVERT_OTHER_NAME` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `INVERT_DES` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")

# open database connection
db = MySQLdb.connect("localhost", "root", "1301410442", "imdb_ttds", charset='utf8')
# use cursor() method
cursor = db.cursor()
for sql in sql_list:
    cursor.execute(sql)
print("Create successfully")
db.commit
db.close
'''

# create_word_dir()
