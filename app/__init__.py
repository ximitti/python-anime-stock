from flask import Flask

from .views import init_app

# ----------------------------


def create_app() -> Flask:
    app = Flask(__name__)

    init_app(app)

    @app.route("/", methods=["GET"])
    def home() -> str:
        return "<h1>Welcome to home!</h1>"

    return app
