import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1301410442',
    db='imdb_ttds',
    charset='utf8',
)
cur = conn.cursor()

sql_list = []

# Create table sqls
sql_list.append("CREATE TABLE `actors` ("
                "`count` int(11) NOT NULL,"
                "`actor_name` VARCHAR(256) NOT NULL COMMENT '演员名',"
                "`pos` text NOT NULL COMMENT '演员位置',"
                "`film_id` varchar(40) NOT NULL COMMENT '参演电影id',"
                "index(actor_name)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `countries` ("
                "`count` int(11) NOT NULL,"
                "`country` VARCHAR(256) NOT NULL COMMENT '电影生产国',"
                "`film_id` varchar(40) NOT NULL COMMENT '电影id',"
                "index(country)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `directors` ("
                "`count` int(11) NOT NULL,"
                "`director_name` VARCHAR(256) NOT NULL COMMENT '导演姓名',"
                "`film_id` varchar(40) NOT NULL COMMENT '导演电影id',"
                "index(director_name)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `film` ("
                "`film_id` varchar(40) NOT NULL COMMENT '电影id',"
                "`actor_string` text NOT NULL COMMENT '电影演员',"
                "`name` text DEFAULT NULL COMMENT '电影名',"
                "`other_name` text DEFAULT NULL COMMENT '电影别名',"
                "`description` text DEFAULT NULL COMMENT '电影描述',"
                "`keywords` text DEFAULT NULL COMMENT '电影关键字',"
                "`storyline` text DEFAULT NULL COMMENT '电影故事情节简述',"
                "`storyline_writer` text DEFAULT NULL COMMENT '故事情节作者',"
                "`storyline_writer_hyperlink` text DEFAULT NULL COMMENT '故事情节作者超链接',"
                "`image` text DEFAULT NULL COMMENT '电影海报链接',"
                "`photos` text DEFAULT NULL COMMENT '电影节选海报链接',"
                "`time` text DEFAULT NULL COMMENT '电影时长',"
                "`date` text DEFAULT NULL COMMENT '电影上映时间',"
                "`imdb_url` text DEFAULT NULL COMMENT 'imdb的链接',"
                "`rating_count` int(11) DEFAULT NULL,"
                "`rating_value` text DEFAULT NULL,"
                "`more_reviews_url` text DEFAULT NULL,"
                "`gross` text DEFAULT NULL COMMENT '票房') ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `genres` ("
                "`count` int(11) NOT NULL,"
                "`genres` VARCHAR(256) NOT NULL COMMENT '电影类别',"
                "`film_id` varchar(40) NOT NULL COMMENT '电影id',"
                "index(genres)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `languages` ("
                "`count` int(11) NOT NULL,"
                "`language` VARCHAR(256) NOT NULL COMMENT '电影语言',"
                "`film_id` varchar(40) NOT NULL COMMENT '电影id',"
                "index(language)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `productions` ("
                "`count` int(11) NOT NULL,"
                "`production_name` VARCHAR(256) NOT NULL COMMENT '制片厂',"
                "`film_id` varchar(40) NOT NULL COMMENT '制片id',"
                "index(production_name)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
sql_list.append("CREATE TABLE `user_movie` ("
                "`count` int(11) NOT NULL,"
                "`user_id` varchar(40) NOT NULL COMMENT '用户id',"
                "`film_id` varchar(40) NOT NULL COMMENT '用户喜爱电影id',"
                "index(user_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")

# indexes sqls
sql_list.append("ALTER TABLE `actors` ADD PRIMARY KEY (`count`),ADD KEY `film_id` (`film_id`);")
sql_list.append("ALTER TABLE `countries` ADD PRIMARY KEY (`count`),ADD KEY `film_id` (`film_id`);")
sql_list.append("ALTER TABLE `directors` ADD PRIMARY KEY (`count`),ADD KEY `film_id` (`film_id`);")
sql_list.append("ALTER TABLE `film` ADD PRIMARY KEY (`film_id`);")
sql_list.append("ALTER TABLE `genres` ADD PRIMARY KEY (`count`),ADD KEY `film_id` (`film_id`);")
sql_list.append("ALTER TABLE `languages` ADD PRIMARY KEY (`count`), ADD KEY `film_id` (`film_id`);")
sql_list.append("ALTER TABLE `productions` ADD PRIMARY KEY (`count`), ADD KEY `film_id` (`film_id`);")
sql_list.append("ALTER TABLE `user_movie` ADD PRIMARY KEY (`count`), ADD KEY `film_id` (`film_id`);")

# auto-incremental sqls
sql_list.append("ALTER TABLE `actors` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `countries` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `directors` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `genres` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `languages` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `productions` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
sql_list.append("ALTER TABLE `user_movie` MODIFY `count` int(11) NOT NULL AUTO_INCREMENT;")
'''
'''
# relation and restrictions sqls
sql_list.append("ALTER TABLE `actors` ADD CONSTRAINT `actors_ibfk_1` "
                "FOREIGN KEY (`film_id`) REFERENCES `film` (`film_id`)"
                "ON DELETE CASCADE;")
sql_list.append("ALTER TABLE `countries` ADD CONSTRAINT `countries_ibfk_1` "
                "FOREIGN KEY (`film_id`) REFERENCES `film` (`film_id`)"
                "ON DELETE CASCADE;")
sql_list.append("ALTER TABLE `directors` ADD CONSTRAINT `directors_ibfk_1` "
                "FOREIGN KEY (`film_id`) REFERENCES `film` (`film_id`)"
                "ON DELETE CASCADE;")
sql_list.append("ALTER TABLE `genres` ADD CONSTRAINT `genres_ibfk_1` "
                "FOREIGN KEY (`film_id`) REFERENCES `film` (`film_id`)"
                "ON DELETE CASCADE;")
sql_list.append("ALTER TABLE `languages` ADD CONSTRAINT `languages_ibfk_1` "
                "FOREIGN KEY (`film_id`) REFERENCES `film` (`film_id`)"
                "ON DELETE CASCADE;")
sql_list.append("ALTER TABLE `productions` ADD CONSTRAINT `productions_ibfk_1` "
                "FOREIGN KEY (`film_id`) REFERENCES `film` (`film_id`)"
                "ON DELETE CASCADE;")
sql_list.append("ALTER TABLE `user_movie` ADD CONSTRAINT `user_movie_ibfk_1` "
                "FOREIGN KEY (`film_id`) REFERENCES `film` (`film_id`)"
                "ON DELETE CASCADE;")

for sql in sql_list:
    cur.execute(sql)

conn.commit()
conn.close()
