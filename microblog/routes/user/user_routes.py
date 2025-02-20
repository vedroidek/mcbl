from http import HTTPStatus
from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError
from core.repo import AuthorRepo

bp = Blueprint('user', __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    try:
        if data := (request.get_json()):
            model = AuthorRepo(
                nickname=data["nickname"],
                email_address=data["email_address"],
                password=data["password"]
            )
            model.save()
            return jsonify({"status_code": HTTPStatus.CREATED})
    except ValidationError as err:
        return jsonify({"status_code": HTTPStatus.BAD_REQUEST,
                        "message": err.json()})
