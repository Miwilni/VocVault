import pymysql

# Verbindung herstellen
conn = pymysql.connect(
    host="localhost:3306",
    user="infolk",
    password="oy6BUiYn4veZ4Jss.",
    database="infolk"
)

# Cursor erstellen
cursor = conn.cursor()

# Abfrage ausführen
cursor.execute("SELECT * FROM mika_häftlinge")

# Ergebnisse abrufen
rows = cursor.fetchall()
for row in rows:
    print(row)

# Verbindung schließen
cursor.close()
conn.close()
