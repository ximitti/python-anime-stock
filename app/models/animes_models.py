from http import HTTPStatus

import psycopg2
from ..services.animes_services import conexao_bd


# -------------------------------------


class TabelaAnimes:
    campos_tabela = ["id", "anime", "released_date", "seasons"]
    campos_validos = ["anime", "released_date", "seasons"]

    def _criar_tabela(self) -> None:
        conn, cur = conexao_bd()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS animes(
                id              BIGSERIAL PRIMARY KEY,
                anime           VARCHAR(100) NOT NULL UNIQUE,
                released_date   DATE NOT NULL,
                seasons         INTEGER NOT NULL
            );
            """
        )

        conn.commit()
        cur.close()
        conn.close()

    # ------------------------------
    def _validacao_campos(self, data: dict) -> list:

        return [campo for campo in data.keys() if campo not in self.campos_validos]

    # ------------------------------
    def pegar_lista_anime(self) -> tuple:
        conn, cur = conexao_bd()

        self._criar_tabela()

        cur.execute(
            """
            SELECT * FROM animes;
            """
        )

        query = cur.fetchall()

        cur.close()
        conn.close()

        animes_list = [dict(zip(self.campos_tabela, anime)) for anime in query]
        for anime in animes_list:
            anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

        return (
            {"data": animes_list},
            HTTPStatus.OK,
        )

    # ---------------------------------
    def pegar_anime_id(self, anime_id: int) -> dict:
        conn, cur = conexao_bd()
        self._criar_tabela()

        cur.execute(
            """
            SELECT * FROM animes
            WHERE id = %s;
            """,
            (anime_id,),
        )

        query = cur.fetchone()

        cur.close()
        conn.close()

        if query:

            anime = dict(zip(self.campos_tabela, query))
            anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

            return {"data": anime}, HTTPStatus.OK

        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    # ------------------------------------
    def criar_anime(self, data: dict) -> tuple:
        conn, cur = conexao_bd()

        self._criar_tabela()

        campos_invalidos = self._validacao_campos(data)
        if campos_invalidos:
            return {
                "available_keys": self.campos_validos,
                "wrong_keys_sended": campos_invalidos,
            }, HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            data["anime"] = data["anime"].title()

            cur.execute(
                """
                INSERT INTO animes
                    (anime, released_date, seasons)
                VALUES
                    (%(anime)s, %(released_date)s, %(seasons)s)
                RETURNING *;
                """,
                data,
            )

            query = cur.fetchone()

            conn.commit()

            anime = dict(zip(self.campos_tabela, query))
            anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

            return anime

        except psycopg2.Error as error:

            print("O retorno do error é:", error)
            return {"error": "anime is already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

        finally:
            cur.close()
            conn.close()

    # ------------------------------------
    def atualizar_anime(self, anime_id: int) -> dict:
        pass

    # ------------------------------------
    def apagar_anime(self, anime_id: int) -> None:
        pass
