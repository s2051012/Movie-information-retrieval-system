import os, json
import pymysql

# MySQL connection
from pymysql.converters import escape_string

conn = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '1301410442',
        db = 'imdb_ttds',
        charset = 'utf8',
    )
cur = conn.cursor()

sql = ""  # init sql


json_path = "../raw-data-imdb/json"
user_path = "../raw-data-imdb/user"

json_files = [pos_json for pos_json in os.listdir(json_path) if pos_json.endswith('.json')]
user_files = [pos_json for pos_json in os.listdir(user_path) if pos_json.endswith('.json')]
# print(len(json_files))
# print(len(user_files))


filmid_list = []

file_counter = 0
print("Inserting film json files... {} in total".format(len(json_files)))
# Extract film informations
for js in json_files:
    with open(os.path.join(json_path, js)) as json_file:

        # Read json contents
        try:
            json_text = json.load(json_file)

            # Decoding json contents
            film_id = json_text['id']
            film_name = json_text['name']
            director = json_text['director']
            genres = json_text['genres']  # list
            actor = json_text['actor']  # list
            date = json_text['date']
            imdb_url = json_text['imdb_url']
            description = json_text['description']
            image = json_text['image']
            keywords = json_text['keywords']  # list
            rating_count = json_text['rating_count']  # int
            rating_value = json_text['rating_value']
            more_reviews_url = json_text['more_reviews_url']
            storyline = json_text['storyline']
            storylineWriter = json_text['storylineWriter']
            storylineWriterHyperlink = json_text['storylineWriterHyperlink']
            time = json_text['time']
            productions = json_text['productions']  # list
            country = json_text['country']
            languages = json_text['languages']  # list
            otherName = json_text['otherName']
            gross = json_text['gross']
            photos = json_text['photos']  # list
            # print(photos, country)

            if len(keywords) > 0:
                keyword_string = '_keyword_spilt_sign_'.join(keywords)  # Convert list to str
            else:
                keyword_string = ''
            if len(photos) > 0:
                photos_string = '_photo_url_spilt_sign_'.join(photos)
            else:
                photos_string = ''
            if len(actor) > 0:
                actor_string = ' '.join(actor)
            else:
                actor_string = ''
            filmid_list.append(film_id)

            # Insert into film
            sql = "INSERT INTO film ( " \
                  "film_id, actor_string, name, other_name, description, keywords, storyline, " \
                  "storyline_writer, storyline_writer_hyperlink, image, photos, " \
                  "time, date, imdb_url, rating_count, rating_value, more_reviews_url, gross ) VALUES ( " \
                  "'{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
                  "'{}', '{}', '{}', '{}', " \
                  "'{}', '{}', '{}', {}, '{}', '{}', '{}' );".format(
                film_id, escape_string(actor_string), escape_string(film_name), escape_string(otherName),
                escape_string(description),
                escape_string(keyword_string), escape_string(storyline),
                escape_string(storylineWriter), escape_string(storylineWriterHyperlink), escape_string(image),
                escape_string(photos_string),
                escape_string(time), escape_string(date), escape_string(imdb_url), int(rating_count), rating_value,
                escape_string(more_reviews_url), gross
            )

            # print(sql)
            cur.execute(sql)
            # Insert into actors
            if actor:
                for i in range(len(actor)):
                    sql = "INSERT INTO actors ( actor_name, pos, film_id ) VALUES ( '{}', '{}', '{}' );".format(
                        escape_string(actor[i]), i, film_id)
                    # print(a, film_id)
                    cur.execute(sql)
            # Insert into countries
            if country and country != '':
                sql = "INSERT INTO countries ( country, film_id ) VALUES ( '{}', '{}' );".format(escape_string(country),
                                                                                                 film_id)
                cur.execute(sql)
            # Insert into directors
            if director != '':
                sql = "INSERT INTO directors ( director_name, film_id ) VALUES ( '{}', '{}' );".format(
                    escape_string(director), film_id)
                cur.execute(sql)
            # Insert into genres
            if genres:
                if isinstance(genres, list):
                    for g in genres:
                        sql = "INSERT INTO genres ( genres, film_id ) VALUES ( '{}', '{}' );".format(escape_string(g),
                                                                                                     film_id)
                        cur.execute(sql)
                else:  # Only one genres
                    sql = "INSERT INTO genres ( genres, film_id ) VALUES ( '{}', '{}' );".format(escape_string(genres),
                                                                                                 film_id)
                    cur.execute(sql)

            # Insert into languages
            if languages:
                for l in languages:
                    sql = "INSERT INTO languages ( language, film_id ) VALUES ( '{}', '{}' );".format(escape_string(l),
                                                                                                      film_id)
                    cur.execute(sql)
            # Insert into productions
            if productions:
                for p in productions:
                    sql = "INSERT INTO productions ( production_name, film_id ) VALUES ( '{}', '{}' );".format(
                        escape_string(p), film_id)
                    cur.execute(sql)

            # User reminder
            file_counter += 1
            if file_counter % 1000 == 0:
                print(
                    "Already inserted {} user files... {} left...".format(file_counter, len(json_files) - file_counter))
            # Reminder block finish

            # testing block
            # if file_counter == 10:
            #    break

        except:
            print(js)



# Extract user favorite films
print("Inserting user json files... {} in total".format(len(user_files)))
file_counter = 0
for ur in user_files:
    with open(os.path.join(user_path, ur)) as user_file:
        # Read json contents
        user_id = ur[:-5]
        favorite_film = json.load(user_file)
        # print(user_id, favorite_film)

        # Insert into database
        if len(favorite_film) > 0:
            for ff in favorite_film:
                if ff in filmid_list:
                    sql = "INSERT INTO user_movie ( user_id, film_id ) VALUES ( '{}', '{}' );".format(user_id, ff)
                    cur.execute(sql)

        # User reminder
        file_counter += 1
        if file_counter % 1000 == 0:
            print("Already inserted {} user files... {} left...".format(file_counter, len(user_files) - file_counter))
        # Reminder block finish

    # testing block
    # if file_counter == 100:
    #     break

conn.commit()
conn.close()