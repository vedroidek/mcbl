import os
from datetime import timedelta
from sqlalchemy.engine import URL


class Config(object):
    TESTING = False
    DEBUG = False
    

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URI = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        database=os.environ.get("DB_NAME")
    )
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPLICATION_ROOT = "./"


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True


confdict = {
    "dev": DeprecationWarning,
    "test": TestingConfig,
    "prod": ProductionConfig
    }