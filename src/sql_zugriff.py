import os
from dotenv import load_dotenv
import pymysql

# .env-Datei laden (nur lokal)
load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )

def execute_get_query(sql_query):
    """Führt eine SELECT-Abfrage aus und gibt das Ergebnis zurück."""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print("Fehler bei SELECT:", e)
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def execute_insert_query(sql_query, values=None):
    """
    Führt eine INSERT/UPDATE/DELETE-Abfrage aus.
    Übergib `values` als Tuple oder Liste für Platzhalter.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            if values:
                cursor.execute(sql_query, values)
            else:
                cursor.execute(sql_query)
            conn.commit()
        print("Änderung erfolgreich durchgeführt.")
    except pymysql.MySQLError as e:
        print("Fehler bei INSERT/UPDATE/DELETE:", e)
    finally:
        if 'conn' in locals():
            conn.close()
