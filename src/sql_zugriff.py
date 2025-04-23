#import mysql.connector
import os
import pymysql
# Verbindung herstellen
#query1: str = "select UserID from User where Username = 'Mika'"
def execute_get_query(query):
    conn = pymysql.connect(
        host="nwallner.de",
        user="infolk-vokabel",
        password=os.getenv("DB_PASSWORD"),  # Passwort aus Secret oder Umgebungsvariable
        database="infolk-vokabel"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def execute_insert_query(query):
    conn = pymysql.connect(
        host="nwallner.de",
        user="infolk-vokabel",
        password=os.getenv("DB_PASSWORD"),  # Passwort aus Secret oder Umgebungsvariable
        database="infolk-vokabel"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
"""def execute_get_query(query):
    conn = mysql.connector.connect(
        host="nwallner.de",
        user="infolk-vokabel",
        password="14UaMW3bYJJK8opT",
        database="infolk-vokabel"
    )
    # Cursor erstellen
    cursor = conn.cursor()
    # Abfrage ausführen
    cursor.execute(query)
    # Ergebnisse abrufen
    rows:list = cursor.fetchall()
    # Verbindung schließen
    cursor.close()
    conn.close()
    return rows

def execute_insert_query(query):
    conn = mysql.connector.connect(
        host="nwallner.de",
        user="infolk-vokabel",
        password="14UaMW3bYJJK8opT",
        database="infolk-vokabel"
    )

    cursor = conn.cursor()
    # Abfrage ausführen
    cursor.execute(query)
    conn.commit()
    conn.close()"""

print(execute_get_query("Select * From USER"))