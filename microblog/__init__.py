import logging
from flask import Flask
from flask_cors import CORS
from .config import confdict
from .routes import comm_bp, user_bp


def create_app(config_name="default"):
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5050"], methods=["GET", "POST"])

    app.config.from_object(confdict[config_name])

    confdict[config_name].init_logging(config_name)

    # blueprints
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(comm_bp, url_prefix='/api')

    return app
