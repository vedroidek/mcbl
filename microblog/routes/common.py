from flask import Blueprint, jsonify

comm_bp = Blueprint("common", __name__)


@comm_bp.route("/", methods=["GET"])
def index():
    return jsonify({"Test": "Route"})
