# Movie Information Retrieval System

This repo is developed by Team23 for TTDS.

Require:

```
pip install pymysql
pip install mysql
pip install flask
pip install flask_sqlalchemy
pip install autocorrect
pip install nltk
pip install requests
pip install beautifulsoup4
pip install lxml
```

Also, require MySQL, and please modify [config.py](https://raw.githubusercontent.com/s2051012/Movie-information-retrieval-system/main/TTDSapp/config.py) with your MySQL database name / password.

Keep default port = 3306

Require NLTK WordNet:

```
python>> import nltk
python>> nltk.download()
```

Run:

```
python run.py
```

---------

Crawl data from IMDb:

```
python scrapy.py -g <genre> -p <start_page_num>  # page < 200
python scrapy.py -g <genre> -m <how_many_pages_crawl>
```

