import psycopg2
from environs import Env

# -----------------------
env = Env()
env.read_env()

# -----------------------


def conexao_bd():
    conn = psycopg2.connect(host=env("HOST"), database=env("DATABASE"), user=env("USER"), password=env("PASSWORD"))
    cur = conn.cursor()

    return conn, cur


def encerra_conexao_cursor(conn, cur) -> None:
    conn.commit()
    cur.close()
    conn.close()
