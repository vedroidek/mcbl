import os
from flask import Flask
from .database import engine
from .models import Base


def create_app(config_type=os.environ.get("CONFIG_TYPE")):
    app = Flask(__name__)

    app.config.from_object(config_type)
    dsn = app.config["DATABASE_URI"]

    initial_db(dsn)

    from routes.user import user_routes
    app.register_blueprint(user_routes.bp)
    app.add_url_rule('/', endpoint='index')

    return app


def initial_db(uri):
    Base.metadata.create_all(engine(uri))
