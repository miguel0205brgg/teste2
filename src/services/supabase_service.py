import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Configurações do banco
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT", 5432)

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )
    return conn

# -------- Usuário / Leitor --------
def criar_usuario_completo(nome, email, senha, telefone=None, cep=None, logradouro=None, numero=None, complemento=None):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Inserir usuario
        cur.execute("""
            INSERT INTO usuario (nome, email, senha) 
            VALUES (%s, %s, %s)
            RETURNING id
        """, (nome, email, senha))
        usuario_id = cur.fetchone()["id"]

        # Inserir endereco
        if cep or logradouro or numero or complemento:
            cur.execute("""
                INSERT INTO enderecos (cep, logradouro, numero, complemento)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (cep, logradouro, numero, complemento))
            endereco_id = cur.fetchone()["id"]
        else:
            endereco_id = None

        # Inserir leitor
        cur.execute("""
            INSERT INTO leitor (nome, email, telefone, id_usuario, id_endereco)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (nome, email, telefone, usuario_id, endereco_id))
        leitor_id = cur.fetchone()["id"]

        conn.commit()
        return {"usuario_id": usuario_id, "leitor_id": leitor_id}

    except Exception as e:
        conn.rollback()
        print("Erro ao criar usuário:", e)
        return None
    finally:
        cur.close()
        conn.close()

def autenticar_usuario(email, senha):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT u.id AS usuario_id, u.nome, u.email, u.senha, l.id AS leitor_id,
                   l.telefone, l.id_endereco, e.cep, e.logradouro, e.numero, e.complemento
            FROM usuario u
            LEFT JOIN leitor l ON l.id_usuario = u.id
            LEFT JOIN enderecos e ON l.id_endereco = e.id
            WHERE u.email = %s
        """, (email,))
        usuario = cur.fetchone()
        if usuario and usuario["senha"] == senha:
            # Remove senha antes de retornar
            usuario.pop("senha")
            return usuario
        return None
    except Exception as e:
        print("Erro ao autenticar usuário:", e)
        return None
    finally:
        cur.close()
        conn.close()

def buscar_leitor_por_id(leitor_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT l.id, l.nome, l.email, l.telefone, e.cep, e.logradouro, e.numero, e.complemento
            FROM leitor l
            LEFT JOIN enderecos e ON l.id_endereco = e.id
            WHERE l.id = %s
        """, (leitor_id,))
        return cur.fetchone()
    except Exception as e:
        print("Erro ao buscar leitor:", e)
        return None
    finally:
        cur.close()
        conn.close()
