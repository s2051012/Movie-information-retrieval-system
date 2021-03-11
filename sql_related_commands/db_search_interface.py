import MySQLdb  # 安装用pip install mysql

def film_information(film_id):
    """
    Getting film information 根据电影id获得电影数据
    :param film_id: string
    :return: list
    """
    ## 自己MySQL的服务器，端口，用户名，密码，db是Team上下载的sql脚本你在在哪一个数据库中运行，这里就填哪一个
    db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1301410442', db='imdb_ttds')
    cursor = db.cursor()

    results = []

    sql = "select * from film where film_id = '{}';".format(film_id)
    cursor.execute(sql)
    res = cursor.fetchone()

    for i in range(len(res)):
        if i == 5:
            results.append(res[i].split('_keyword_spilt_sign_'))
        elif i == 10:
            results.append(res[i].split('_photo_url_spilt_sign_'))
        else:
            results.append(res[i])

    sql = "select actor_name from actors where film_id = '{}';".format(film_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    actors = []
    for row in res:
        actors.append(row[0])
    results.append(actors)

    sql = "select director_name from directors where film_id = '{}';".format(film_id)
    cursor.execute(sql)
    res = cursor.fetchone()
    results.append(res[0])

    sql = "select country from countries where film_id = '{}';".format(film_id)
    cursor.execute(sql)
    res = cursor.fetchone()
    results.append(res[0])

    sql = "select genres from genres where film_id = '{}';".format(film_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    genres = []
    for row in res:
        genres.append(row[0])
    results.append(genres)

    sql = "select language from languages where film_id = '{}';".format(film_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    languages = []
    for row in res:
        languages.append(row[0])
    results.append(languages)

    sql = "select production_name from productions where film_id = '{}';".format(film_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    productions = []
    for row in res:
        productions.append(row[0])
    results.append(productions)

    db.close()  # 数据库关闭--写在最后的最后
    return results

def invert_data(table_name, token):
    '''
    Getting data from invert tables 根据单词获得倒排表数据
    :param table_name: invert_name/invert_other_name/invert_actor/invert_director/invert_des 五选一 string
    :param token: string
    :return: tuple
    '''
    ## 自己MySQL的服务器，端口，用户名，密码，db是Team上下载的sql脚本你在在哪一个数据库中运行，这里就填哪一个
    db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1301410442', db='imdb_ttds')
    cursor = db.cursor()
    sql = "select * from {} where {} = '{}'".format(table_name, table_name[7:] + '_token', token)
    cursor.execute(sql)
    db.close()
    return cursor.fetchall()


if __name__ == '__main__':
    print("Begin searching...")
    results = invert_data('invert_des', 'pieapple')
    print(results)
    # 每一条数据的第一个数是count，作为PK用的，可以忽略；
    # 第二个是出现在的电影id；第三个是该token；第四个是position

    info = film_information('tt0000499')
    print(info)
