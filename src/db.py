import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_logs(connection, limit=100):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, level, message, response_time, endpoint
            FROM logs
            WHERE processed = 0
            LIMIT %s
        """, (limit,))
        return cursor.fetchall()


def mark_as_processed(connection, ids):
    if not ids:
        return

    with connection.cursor() as cursor:
        format_strings = ','.join(['%s'] * len(ids))

        sql = f"""
            UPDATE logs
            SET processed = 1
            WHERE id IN ({format_strings})
        """

        cursor.execute(sql, ids)
        connection.commit()