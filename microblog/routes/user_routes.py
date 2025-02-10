from microblog.main_instances import app


def index():
    return "<h1>Hello!</h1>"


app.add_url_rule("/index", view_func=index)