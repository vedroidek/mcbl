from http import HTTPStatus
import json
from . import logger
from flask import Blueprint, Response, request
from microblog.core.db_connect import Session
from microblog.services.users.register import register_new_user
from microblog.services.users.user_actions import get_all_users, get_one_user, \
    delete_one_user


user_bp = Blueprint('user', __name__)


@user_bp.route("/", methods=["GET"])
def get_users() -> Response:
    res = get_all_users(Session())
    return Response(        
        response=json.dumps({"message": res}),
        status=HTTPStatus.OK,
        mimetype='application/json'
        )


@user_bp.route("/<int:id>", methods=["GET"])
def get_user(id: int) -> Response:
    status = HTTPStatus.NOT_FOUND
    user = "User is not found"   

    if user := get_one_user(Session(), id):
        status = HTTPStatus.OK
        user = user.as_dict()

    return Response(
        response=json.dumps({"message": user}),
        status=status,
        mimetype="application/json"
    )


@user_bp.route("/", methods=["POST"])
def add_user() -> Response:
    is_success = False
    resp_status = HTTPStatus.BAD_REQUEST

    data = request.get_json()
    resp_status = HTTPStatus.BAD_REQUEST

    if not all([data["name"], data["email_address"], data["password_hash"]]):
        is_success = "Required data missing."
    else:
        register_new_user(Session(), data["name"], data["email"], data["password_hash"])
        resp_status = HTTPStatus.CREATED
        is_success = True
        logger.info("new user was created")

    return Response(
        response=json.dumps({"message": is_success}),
        status=resp_status,
        mimetype="application/json"
    )


@user_bp.route("/<int:id>", methods=["DELETE"])
def delete_user(id) -> Response:
    is_success = False
    if delete_one_user(Session(), id):
        is_success = True

    return Response(
        response=json.dumps({"message": is_success}),
        status=HTTPStatus.NO_CONTENT,
        mimetype="application/json"
    )


@user_bp.route("/<int:id>", methods=["PUT"])
def put_user(id) -> Response:

    data = request.get_json()

    # TODO
    user = ""
    
    return Response({"message": user, "ok": True})  # 200