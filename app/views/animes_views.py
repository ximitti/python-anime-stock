from flask import Blueprint, request, jsonify
from psycopg2 import errors
from http import HTTPStatus

from ..models.animes_models import TabelaAnimes

# -----------------------------
bp = Blueprint("bp_animes", __name__)


# -----------------------------


@bp.route("/animes", methods=["GET", "POST"])
def get_create() -> dict:
    animes = TabelaAnimes()

    if request.method == "POST":
        try:
            return animes.criar_anime(request.get_json()), HTTPStatus.CREATED

        except errors.UniqueViolation:
            return {"error": "anime is already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

        except KeyError as e:
            return e.args[0], HTTPStatus.UNPROCESSABLE_ENTITY

    return jsonify(animes.pegar_lista_anime()), HTTPStatus.OK


# ---------------------------------------------
@bp.route("/animes/<int:anime_id>", methods=["GET"])
def filter(anime_id: int) -> dict:
    animes = TabelaAnimes()

    try:
        return animes.pegar_anime_id(anime_id), HTTPStatus.OK

    except Exception as e:
        return e.args[0], HTTPStatus.NOT_FOUND


# ---------------------------------------------
@bp.route("/animes/<int:anime_id>", methods=["PATCH"])
def update(anime_id: int) -> tuple:
    animes = TabelaAnimes()

    try:
        return animes.atualizar_anime(anime_id, request.get_json()), HTTPStatus.OK

    except KeyError as e:
        return e.args[0], HTTPStatus.UNPROCESSABLE_ENTITY

    except errors.UniqueViolation as e:
        print(e)
        return {"error": "anime is already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

    except Exception as e:
        return e.args[0], HTTPStatus.NOT_FOUND


# ---------------------------------------------
@bp.route("/animes/<int:anime_id>", methods=["DELETE"])
def delete(anime_id: int) -> str:
    animes = TabelaAnimes()

    try:
        return animes.apagar_anime(anime_id), HTTPStatus.NO_CONTENT

    except Exception as e:

        return e.args[0], HTTPStatus.NOT_FOUND
