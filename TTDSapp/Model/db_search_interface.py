import MySQLdb


class db_search():

    def __init__(self, host='localhost', port=3306, user='root', passwd='1301410442', db='imdb_ttds'):
        self.db = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)

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

        return results

    def invert_data(self, table_name, token):
        cursor = self.db.cursor()
        sql = "select * from {} where {} = '{}'".format(table_name, table_name[7:] + '_token', token)
        cursor.execute(sql)
        return cursor.fetchall()

    def db_close(self):
        self.db.close()


if __name__ == '__main__':
    print("Begin searching...")
    db_s = db_search()  # Set as default

    info = db_s.film_information('tt0000499')
    print(info)
    results = db_s.invert_data('invert_des', 'pieapple')
    print(results)

    db_s.db_close()
    print("Finish searching")
