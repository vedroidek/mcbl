import os
from microblog import create_app


conf_type = os.environ["CONFTYPE"]
app = create_app(conf_type)


if __name__ == "__main__":
    app.run()
