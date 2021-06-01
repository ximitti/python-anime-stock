from flask import Blueprint, request

# -----------------------------
bp_animes = Blueprint("animes", __name__)


# -----------------------------


@bp_animes.route("/animes", methods=["GET", "POST"])
def get_create() -> str:
    if request.method == "POST":
        return f"<h1>Method {request.method}</h1>"

    return f"<h1>Method {request.method}</h1>"


@bp_animes.route("/animes/<int:anime_id>", methods=["GET"])
def filter(anime_id: int) -> str:

    return f"<h1>Anime {anime_id}</h1>"


@bp_animes.route("/animes/<int:anime_id>", methods=["PATCH"])
def update(anime_id: int) -> str:
    return f"<h1>Method {anime_id} {request.method}</h1>"


@bp_animes.route("/animes/<int:anime_id>", methods=["DELETE"])
def delete(anime_id: int) -> str:
    return f"<h1>Method {anime_id} {request.method}</h1>"
