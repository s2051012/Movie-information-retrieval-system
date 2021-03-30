class Config:
    DEBUG = True
    SECRET_KEY = "random string"
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root',
                                                                                                    password='qazwsx971219',
                                                                                                    server='localhost',
                                                                                                    database='ttds')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
