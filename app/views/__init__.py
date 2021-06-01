from flask import Flask

from .animes_views import bp as bp_animes


# --------------------------------
def init_app(app: Flask):
    app.register_blueprint(bp_animes)
