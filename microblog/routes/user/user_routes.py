from http import HTTPStatus
from flask import Blueprint, request, jsonify, redirect, url_for, \
    make_response
from pydantic import ValidationError
from core.repo import AuthorRepo

bp = Blueprint('user', __name__)


@bp.route("/index", methods=["GET", "POST"])
def index():
    pass


@bp.route("/register", methods=["GET", "POST"])
def register():
    data = request.get_json()

    if request.method == "POST":
        try:
            model = AuthorRepo(
                nickname=data["nickname"],
                email_address=data["email_address"],
                password=data["password"]
            )
            if model.is_exists(model.nickname):
                return jsonify({"status_code": HTTPStatus.CONFLICT,
                                "message": "User already exists."})
            else: 
                model.save()
                response = make_response(
                    jsonify({"status_code": HTTPStatus.CREATED})
                    )
                response.set_cookie("user", model.user.nickname,
                                    max_age=3600*24,)
                return response
        
        except ValidationError as err:
            return jsonify({"status_code": HTTPStatus.BAD_REQUEST,
                            "message": err.json()})
        
    elif request.method == "GET":
        return redirect(
            url_for(".login"), code=HTTPStatus.UNAUTHORIZED
            )


@bp.route("/login", methods=["GET", "POST"])
def login():
    data = request.get_json()
    # // TO DO! //
    return data

