from flask import Blueprint, session, request
from microblog.core.repo import AuthorRepo

bp = Blueprint('user', __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    data = request.get_json()
    user = AuthorRepo()
    return
