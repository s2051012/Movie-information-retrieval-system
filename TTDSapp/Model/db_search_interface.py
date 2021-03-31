import sys
import pymysql

sys.path.append('../')
from config import Config


class db_search():
    c = Config()

    def __init__(self, host=c.server, port=3306, user=c.user, passwd=c.password, db=c.database):
        self.db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    def film_information(self, film_id):
        cursor = self.db.cursor()
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
        if res is None:
            results.append('No Records')
        else:
            actors = []
            for row in res:
                actors.append(row[0])
            results.append(actors)

        sql = "select director_name from directors where film_id = '{}';".format(film_id)
        cursor.execute(sql)
        res = cursor.fetchone()
        if res is None:
            results.append('No Records')
        else:
            results.append(res[0])

        sql = "select country from countries where film_id = '{}';".format(film_id)
        cursor.execute(sql)
        res = cursor.fetchone()
        if res is None:
            results.append('No Records')
        else:
            results.append(res[0])

        sql = "select genres from genres where film_id = '{}';".format(film_id)
        cursor.execute(sql)
        res = cursor.fetchall()
        if res is None:
            results.append('No Records')
        else:
            genres = []
            for row in res:
                genres.append(row[0])
            results.append(genres)

        sql = "select language from languages where film_id = '{}';".format(film_id)
        cursor.execute(sql)
        res = cursor.fetchall()
        if res is None:
            results.append('No Records')
        else:
            languages = []
            for row in res:
                languages.append(row[0])
            results.append(languages)

        sql = "select production_name from productions where film_id = '{}';".format(film_id)
        cursor.execute(sql)
        res = cursor.fetchall()
        if res is None:
            results.append('No Records')
        else:
            productions = []
            for row in res:
                productions.append(row[0])
            results.append(productions)

        return results

    def invert_data(self, table_name, token):
        cursor = self.db.cursor()
        sql = "select * from {} where {} = '{}'".format(table_name, table_name[7:] + '_token', token)
        cursor.execute(sql)
        return cursor.fetchall()


    def db_close(self):
        self.db.close()

    def top_film_info(self):
        #c = Config()
        # db2 = pymysql.connect(host=c.server, port=3306, user=c.user, passwd=c.password, db=c.database)
        cursor = self.db.cursor()
        sql = "select * from (select * from film limit 50000) as t where rating_value > 9;"
        cursor.execute(sql)
        res = cursor.fetchall()
        topmovies = []
        for i in res:
            topmovies.append(i)
        return topmovies


if __name__ == '__main__':
    print("Begin searching...")
    db_s = db_search()  # Set as default

    info = db_s.film_information('tt1146278')
    print(info)
    results = db_s.invert_data('invert_des', 'pieapple')
    print(results)

    db_s.db_close()
    print("Finish searching")
