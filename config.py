import os


# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'Xa\xb9^\x95R\xc2\xdd\xcc\xdf\xa5\x9b\xf8{G\x97\x1c\xc4\xda\xd8u\xc9\xc0\x10'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)


class DevelopmentConfig(BaseConfig): 
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
