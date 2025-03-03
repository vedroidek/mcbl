from http import HTTPStatus
from flask import request, jsonify
from flask.views import MethodView
from pydantic import ValidationError
from core.repo import AuthorRepo, gen_hash
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
            users = AuthorRepo.get_all_users()
            return jsonify(
                {"status_code": HTTPStatus.OK,
                 "message": users}
            )


    def post(self):
        """Method for create new user."""
        data = request.get_json()
        try:
            pswd = gen_hash(data["password"])
            model = AuthorRepo(
                nickname=data["nickname"],
                email_address=data["email_address"],
                password=pswd
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
        
        except (ValidationError, TypeError) as err:
            return jsonify({"status_code": HTTPStatus.BAD_REQUEST,
                        "message": err.json()})

    def patch(self, user_id):
        data = request.get_json()
        mv = AuthorRepo.update_author(user_id, data)
        return mv
        
    def delete(self, user_id):
        rm = AuthorRepo.delete_author(user_id)
        return rm


# --- URL's --- #
bp.add_url_rule("/<int:user_id>", view_func=UserAPI.as_view("get_user"),
                methods=["GET", "DELETE", "PATCH"])
bp.add_url_rule("/", view_func=UserAPI.as_view("create_user"),
                methods=["GET", "POST"])