import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import pika
import json

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "publications_queue")

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

def create_tables():
    create_publications_table = """
    CREATE TABLE IF NOT EXISTS publications (
        id SERIAL PRIMARY KEY,
        numero_processo TEXT,
        data_disponibilizacao DATE,
        autores TEXT,
        advogados TEXT,
        valor_principal NUMERIC,
        juros_moratorios NUMERIC,
        honorarios_adv NUMERIC,
        reu TEXT,
        status TEXT,
        conteudo_publicacao TEXT
    );
    """
    create_hashes_table = """
    CREATE TABLE IF NOT EXISTS hashes (
        id SERIAL PRIMARY KEY,
        hash TEXT UNIQUE
    );
    """
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(create_publications_table)
            cursor.execute(create_hashes_table)
            connection.commit()
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        if connection:
            connection.close()

def send_to_queue(data):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
    except Exception as e:
        print(f"Erro ao enviar mensagem para a fila RabbitMQ: {e}")

def save_data(data):
    hash_value = data.get("hash")
    if not hash_value:
        print("Hash não encontrado nos dados.")
        return

    check_hash_query = "SELECT id FROM hashes WHERE hash = %s"
    insert_hash_query = "INSERT INTO hashes (hash) VALUES (%s)"
    insert_publication_query = """
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
            cursor.execute(check_hash_query, (hash_value,))
            if cursor.fetchone():
                print("Hash já existe. Dados duplicados não serão salvos.")
                return

            cursor.execute(insert_hash_query, (hash_value,))
            cursor.execute(insert_publication_query, data)
            connection.commit()
            send_to_queue(data)  # Envia os dados para a fila após salvar com sucesso
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")
    finally:
        if connection:
            connection.close()

def check_hash_existence(hash_value):
    query = "SELECT id FROM hashes WHERE hash = %s"
    try:
        connection = get_connection()
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (hash_value,))
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar existência do hash no banco de dados: {e}")
        return False
    finally:
        if connection:
            connection.close()
