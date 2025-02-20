import os
from sqlalchemy import URL

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    FLASK_ENV: str = os.environ.get("FLASK_ENV")
    DEBUG: bool = os.environ.get("DEBUG")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    TESTING: bool = False
    DEBUG: bool = True
    LOGFILE: str = "./logs/development.log"

    def dsn():
        url_obj = URL.create(
            "postgresql+psycopg2",
            username=os.environ["DB_USER"],
            password=os.environ["DB_PSWD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"]
        )
        return url_obj
    
    DATABASE_URI: str = dsn()


class TestingConfig(Config):
    TESTING: bool = True
    DEBUG: bool = True

    def dsn():
        url_obj = URL.create(
            "postgresql+psycopg2",
            username=os.environ["DB_USER"],
            password=os.environ["DB_PSWD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"]
        )
        return url_obj
    
    DATABASE_URI: str = dsn()


class ProductionConfig(Config):
    TESTING: bool = False
    DEBUG: bool = False
    FLASK_ENV = "production"
