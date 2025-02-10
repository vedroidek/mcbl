import os
from logging.handlers import RotatingFileHandler
from logging import Formatter
import logging
from flask import Flask
from .database import engine
from .models import Base


def create_app(config_type=os.environ.get("CONFIG_TYPE")):
    app = Flask(__name__)

    app.config.from_object(config_type)
    dsn = app.config["DATABASE_URI"]

    handler = RotatingFileHandler(app.config['LOGFILE'],
                                  maxBytes=10**6, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
                               '[in %(pathname)s:%(lineno)d]'))
    
    # logging.disable(logging.CRITICAL)
    # # Расскоментарь это для прекращения логов

    app.logger.addHandler(handler)
    
    initial_db(dsn)

    return app


def initial_db(uri):
    Base.metadata.create_all(engine(uri))
