from flask.views import MethodView
from . import bp


class PostAPI(MethodView):

    def get(self):
        return "PostAPI: GET"

bp.add_url_rule("/", view_func=PostAPI.as_view("posts"),
                methods=["GET"])
