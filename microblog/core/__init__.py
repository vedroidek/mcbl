import os
from flask import Flask
from .database import engine
from .models import Base
from routes.user import user_routes


def create_app(config_type=os.environ.get("CONFIG_TYPE")):
    """Application factory.
    
    Keyword arguments:
    config_type -- development, testing, production
    Return: 'app' instance
    """
    
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
        )

    app.config.from_object(config_type)
    dsn = app.config["DATABASE_URI"]

    initial_db(dsn)

    app.register_blueprint(user_routes.bp, url_prefix="/user")

    return app


def initial_db(uri):
    Base.metadata.create_all(engine(uri))
