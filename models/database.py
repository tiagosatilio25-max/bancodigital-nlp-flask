import sqlite3
import pandas as pd

DB_NAME = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            intencao TEXT NOT NULL,
            lemmas TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salvar_mensagem(texto, intencao, lemmas):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mensagens (texto, intencao, lemmas) VALUES (?, ?, ?)",
        (texto, intencao, ",".join(lemmas))
    )
    conn.commit()
    conn.close()

def obter_historico_df():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT id, texto, intencao, lemmas, data_criacao FROM mensagens ORDER BY id DESC", conn)
    conn.close()
    return df