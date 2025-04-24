import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")

def get_connection():
    try:
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DBNAME
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

def save_data(data):
    query = """
    INSERT INTO publications (
        numero_processo,
        data_disponibilizacao,
        autores,
        advogados,
        valor_principal,
        juros_moratorios,
        honorarios_adv,
        reu,
        status,
        conteudo_publicacao
    ) VALUES (
        %(numero_processo)s,
        %(data_disponibilizacao)s,
        %(autores)s,
        %(advogados)s,
        %(valor_principal)s,
        %(juros_moratorios)s,
        %(honorarios_adv)s,
        %(reu)s,
        %(status)s,
        %(conteudo_publicacao)s
    )
    """
    try:
        connection = get_connection()
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, data)
            connection.commit()
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")
    finally:
        if connection:
            connection.close()
