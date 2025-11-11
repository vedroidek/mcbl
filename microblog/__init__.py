import logging  # noqa: F401
from flask import Flask
from .config import confdict
from .routes import comm_bp, user_bp


def create_app(config_name=None):
    app = Flask(__name__)

    if not config_name:
        app.config.from_object(confdict["default"])
    else:
        app.config.from_object(confdict[config_name])

    confdict[config_name].init_logging(config_name)

    # blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(comm_bp, url_prefix='/')

    return app
