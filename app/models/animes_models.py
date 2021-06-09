from ..services.animes_services import conexao_bd, encerra_conexao_cursor
from psycopg2 import sql


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

        encerra_conexao_cursor(conn, cur)

    # ------------------------------
    def _validacao_campos(self, data: dict) -> list:

        return [campo for campo in data.keys() if campo not in self.campos_validos]

    # ------------------------------
    def pegar_lista_anime(self) -> list:
        conn, cur = conexao_bd()

        self._criar_tabela()

        cur.execute(
            """
            SELECT * FROM animes;
            """
        )

        query = cur.fetchall()

        encerra_conexao_cursor(conn, cur)

        animes_list = [dict(zip(self.campos_tabela, anime)) for anime in query]
        for anime in animes_list:
            anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

        return animes_list

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

        encerra_conexao_cursor(conn, cur)

        if query:
            anime = dict(zip(self.campos_tabela, query))
            anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

            return anime

        raise Exception({"error": "Not Found"})

    # ------------------------------------
    def criar_anime(self, data: dict) -> dict:
        conn, cur = conexao_bd()

        self._criar_tabela()

        campos_invalidos = self._validacao_campos(data)
        if campos_invalidos:
            raise KeyError(
                {
                    "available_keys": self.campos_validos,
                    "wrong_keys_sended": campos_invalidos,
                }
            )

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

        encerra_conexao_cursor(conn, cur)

        anime = dict(zip(self.campos_tabela, query))
        anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

        return anime

    # ------------------------------------
    def atualizar_anime(self, anime_id: int, data: dict) -> dict:
        conn, cur = conexao_bd()

        self._criar_tabela()

        campos_invalidos = self._validacao_campos(data)

        if campos_invalidos:
            raise KeyError(
                {
                    "available_keys": self.campos_validos,
                    "wrong_keys_sended": campos_invalidos,
                }
            )

        if data.get("anime"):
            data["anime"] = data["anime"].title()

        sql_query = sql.SQL("UPDATE animes SET {data} WHERE id = {id} RETURNING *;").format(
            data=sql.SQL(", ").join(
                sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in data.keys()
            ),
            id=sql.Placeholder("id"),
        )

        data.update(id=anime_id)

        cur.execute(sql_query, data)

        query = cur.fetchone()

        encerra_conexao_cursor(conn, cur)

        if query:
            anime = dict(zip(self.campos_tabela, query))
            anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

            return anime

        raise Exception({"error": "Not Found"})

    # ------------------------------------
    def apagar_anime(self, anime_id: int) -> None:
        conn, cur = conexao_bd()

        self._criar_tabela()

        cur.execute(
            """
            DELETE FROM animes
            WHERE id = %(id)s
            RETURNING *;
            """,
            {"id": anime_id},
        )

        query = cur.fetchone()

        encerra_conexao_cursor(conn, cur)

        if query:
            return "No content"

        raise Exception({"error": "Not Found"})
