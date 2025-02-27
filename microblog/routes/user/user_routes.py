from http import HTTPStatus
from flask import request, jsonify
from flask.views import MethodView
from pydantic import ValidationError
from core.repo import AuthorRepo
from . import bp


class UserAPI(MethodView):

    init_every_request = False

    def get(self, user_id: int=None):
        if user_id:
            user = AuthorRepo.get_author_by_id(user_id=user_id)
            return jsonify(
                {"status_code": HTTPStatus.OK,
                 "message": user}
            )
        else:
            pass

    def post(self):
        """Method for create new user."""
        data = request.get_json()
        try:
            model = AuthorRepo(
                nickname=data["nickname"],
                email_address=data["email_address"],
                password=data["password"]
            )
            if model.is_exists(data["nickname"], data["email_address"]):
                return jsonify({
                    "status_code": HTTPStatus.CONFLICT,
                    "message": "User already exists."
                    })
            else: 
                model.save()
                return jsonify(
                    {"status_code": HTTPStatus.CREATED,
                    "message": f'User {data["nickname"]} was created successfull'}
                    )
        
        except ValidationError as err:
            return jsonify({"status_code": HTTPStatus.BAD_REQUEST,
                        "message": err.json()})


# --- URL's --- #
bp.add_url_rule("/<int:user_id>", view_func=UserAPI.as_view("get_user"),
                methods=["GET"])
bp.add_url_rule("/", view_func=UserAPI.as_view("create_user"),
                methods=["GET", "POST"])