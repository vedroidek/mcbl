import microblog
from flask import render_template


@app.route("/", methods=["GET"])
def index():
    vasya = "Вася"
    render_template("user/greetengs.html", username=vasya)
