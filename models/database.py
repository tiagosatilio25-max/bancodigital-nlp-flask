import os
import psycopg2
from psycopg2 import pool
import pandas as pd

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://usuario:senha@ep-exemplo.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

# Pool de conexões para reaproveitar conexões abertas e zerar o tempo de espera
pg_pool = None

def get_pool():
    global pg_pool
    if pg_pool is None or pg_pool.closed:
        try:
            pg_pool = psycopg2.pool.ThreadedConnectionPool(1, 5, DATABASE_URL, connect_timeout=5)
        except Exception as e:
            print(f"[ERRO POOL] Não foi possível criar o pool de conexões: {e}")
            return None
    return pg_pool

def init_db():
    try:
        pool_obj = get_pool()
        if not pool_obj:
            return
        conn = pool_obj.getconn()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solicitacoes (
                id SERIAL PRIMARY KEY,
                texto TEXT NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                lemmas TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cursor.close()
        pool_obj.putconn(conn)
        print("[DATABASE] Tabela inicializada com sucesso!")
    except Exception as e:
        print(f"[AVISO DATABASE] Inicialização ignorada/falhou: {e}")

def salvar_solicitacao(texto, categoria, lemmas):
    try:
        pool_obj = get_pool()
        if not pool_obj:
            return
        conn = pool_obj.getconn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO solicitacoes (texto, categoria, lemmas) VALUES (%s, %s, %s);",
            (texto, categoria, ",".join(lemmas))
        )
        conn.commit()
        cursor.close()
        pool_obj.putconn(conn)
    except Exception as e:
        print(f"[ERRO DATABASE] Falha ao salvar: {e}")

def obter_historico_df():
    try:
        pool_obj = get_pool()
        if not pool_obj:
            return pd.DataFrame(columns=['id', 'texto', 'categoria', 'lemmas', 'data_criacao'])
        conn = pool_obj.getconn()
        df = pd.read_sql_query(
            "SELECT id, texto, categoria, lemmas, TO_CHAR(data_criacao, 'DD/MM/YYYY HH24:MI:SS') as data_criacao FROM solicitacoes ORDER BY id DESC LIMIT 20;", 
            conn
        )
        pool_obj.putconn(conn)
        return df
    except Exception as e:
        print(f"[ERRO DATABASE] Falha ao obter histórico: {e}")
        return pd.DataFrame(columns=['id', 'texto', 'categoria', 'lemmas', 'data_criacao'])