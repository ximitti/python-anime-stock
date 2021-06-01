import psycopg2
from environs import Env

# -----------------------
env = Env()
env.read_env()

# -----------------------


def conexao_bd():
    conn = psycopg2.connect(host=env("host"), database=env("database"), user=env("user"), password=env("password"))
    cur = conn.cursor()

    return conn, cur
