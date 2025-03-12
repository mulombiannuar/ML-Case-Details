import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def execute_query(query: str, params: tuple):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        results = cursor.fetchall()

        return results  # Return raw results for further processing

    except psycopg2.Error as e:
        print("Database error:", e)
        return []

    finally:
        cursor.close()
        conn.close()