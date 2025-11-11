import os
from logging.config import dictConfig
from datetime import timedelta
from sqlalchemy.engine import URL


class Config(object):
    TESTING = False
    DEBUG = False

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @staticmethod
    def init_logging(environment):
        """
        Initializing the logging configuration for the environment.
        """

        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": Config.LOG_FORMAT,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": Config.LOG_LEVEL,
                "handlers": ["console"],
            },
            "loggers": {
                "werkzeug": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }

        dictConfig(log_config)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DB_SERVER = "localhost"
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
    LOG_LEVEL = "DEBUG"


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    LOG_LEVEL = "INFO"


confdict = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig,
    }
