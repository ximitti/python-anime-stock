from flask import Blueprint, request

from ..models.animes_models import TabelaAnimes

# -----------------------------
bp = Blueprint("bp_animes", __name__)


# -----------------------------


@bp.route("/animes", methods=["GET", "POST"])
def get_create() -> dict:
    animes = TabelaAnimes()

    if request.method == "POST":
        return animes.criar_anime(request.get_json())

    return animes.pegar_lista_anime()


@bp.route("/animes/<int:anime_id>", methods=["GET"])
def filter(anime_id: int) -> dict:
    animes = TabelaAnimes()

    return animes.pegar_anime_id(anime_id)


@bp.route("/animes/<int:anime_id>", methods=["PATCH"])
def update(anime_id: int) -> str:

    return f"<h1>Method {anime_id} {request.method}</h1>"


@bp.route("/animes/<int:anime_id>", methods=["DELETE"])
def delete(anime_id: int) -> str:

    return f"<h1>Method {anime_id} {request.method}</h1>"
