# 项目使用flask里面的SQLAcademy包来进行db的连接与操作
# 但是flask要求很多其他的文件才能进行，如果只是自己进行测试，那么就直接使用mysqldb来进行连接即可
# 最后的把可以运行的sql语句 交给数据接口负责人

import MySQLdb  # 安装用pip install mysql

## 自己MySQL的服务器，端口，用户名，密码，db是Team上下载的sql脚本你在在哪一个数据库中运行，这里就填哪一个
db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1301410442', db='imdb_ttds')
cursor = db.cursor()


sql = ""  # 里面填要进行的数据库操作的sql语句
cursor.execute(sql)
# 得到返回结果，返回的算是元组，不可修改，获取值的方式跟list一样
results = cursor.fetchall()
for row in results: # 每次得到一条数据,每一条数据也是元组（属性1，属性2，...属性n）
    ...


## 如果要对数据库进行修改增删改查的话...还要使用下面这一句
db.commit()  # 提交修改，不然不会生效

db.close()  # 数据库关闭--写在最后的最后



##下面是每一个数据库的结构：

# film：film_id, actor_string, name, other_name, description, keywords, storyline, storyline_writer, storyline_writer_hyperlink, image, photos, time, date, imdb_url, rating_count, rating_value, more_reviews_url, gross
#       电影id,     电影演员    电影名 电影别名     电影描述     电影关键字 故事情节     故事情节作者       故事情节作者超链接          海报   电影图片  时长 上映日期 imdb的链接  打分人数     评分          评分链接          票房
# NOTE：取电影演员信息不要使用film表里的actor_string，该字符串用于创建actor倒排表

# actors: count, actor_name, pos, film_id
#         主键      演员名   处在演员表的第几个位置 参演电影id
# NOTE：有些电影imdb没有记录演员名字，因此也没有出现在这个数据库里面，这一点同样适用于下面几个表

# countries: count, country, film_id
#             主键  电影生产国 电影id

# directors：count，director_name，film_id
#            主键   导演姓名        导演电影id

# genres：count，genres，film_id
#         主键  电影类别  电影id

# languages：count，language，film_id
#            主键    电影语言  电影id

# productions：count，production_name，film_id
#              主键    制片厂           制片id

# user_movie：count，user_id，film_id
#             主键   用户id 用户喜爱电影id
# NOTE：这里由于数据库并不完全，因此imdb中有些用户看的电影没有收录到这个数据库中，所以对用户喜爱电影的id进行了一些筛选，只保留了数据库中存在的电影id

## 下面是倒排索引包
# INVERT_NAME：count，film_id，name_token，pos
#              主键     电影id   单词      位置

# INVERT_OTHER_NAME: count，film_id，other_name_token，pos
#                    主键    电影id

# INVERT_DES：count，film_id，des_token，pos
# 这个是description的倒排索引

# INVERT_ACTOR：count，film_id，actor_token，pos

# INVERT_DIRECTOR：count，film_id，director_token，pos
