from http import HTTPStatus
from . import logger
from flask import Blueprint, jsonify, request, Response
from microblog.core.db_connect import Session
from microblog.services.user.register import register_new_user


user_bp = Blueprint('user', __name__)


@user_bp.route("/register", methods=["POST"])
def register() -> Response:
    """Handle user registration with JSON data.

    Args:
        *name*: User's name
        *email_address*: User's email

    Returns:
        JSON with 201 CREATED on success, 409 CONFLICT if user exists
    """

    data = request.get_json()

    try:
        session = Session()
        if not register_new_user(session,
                                 data["name"],
                                 data["email_address"],
                                 data["password"]):
            return jsonify({"status": HTTPStatus.CONFLICT})

        logger.info("New user was created.")

    except Exception as e:
        logger.warning(f"The request to create a new user was rejected.\n{e}")
        return jsonify({"status": HTTPStatus.CONFLICT})

    return jsonify({"status": HTTPStatus.CREATED})
