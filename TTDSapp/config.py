class Config:
    DEBUG = True
    SECRET_KEY = "random string"
    password = 'qazwsx971219'
    user = 'root'
    server = 'localhost'
    database = 'ttds'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user=user,
                                                                                                    password=password,
                                                                                                    server=server,
                                                                                                    database=database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False