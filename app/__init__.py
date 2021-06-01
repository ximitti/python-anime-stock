from flask import Flask
from .views.views import bp_animes

# ----------------------------


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(bp_animes)

    @app.route("/", methods=["GET"])
    def home() -> dict:
        return "<h1>Welcome to home!</h1>"

    return app
