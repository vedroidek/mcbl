from flask import Blueprint

bp = Blueprint('blog', __name__)


@bp.route("/", methods=["GET"])
def index():
    return "<h1>Hello!</h1>"
