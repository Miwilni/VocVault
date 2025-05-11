# services/db_service.py
import pymysql
from utils.env_loader import load_env

class DBService:
    _current_user = None

    def __init__(self):
        self.env = load_env()
        self.connection = None

    def connect(self):
        if not self.connection or not self.connection.open:
            self.connection = pymysql.connect(
                host=self.env["DB_HOST"],
                user=self.env["DB_USER"],
                password=self.env["DB_PASSWORD"],
                database=self.env["DB_NAME"],
                cursorclass=pymysql.cursors.Cursor
            )
        return self.connection

    def execute_query(self, query, params=None):
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"DB Fehler: {e}")
            return False

    def fetch_one(self, query, params=None):
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"DB Fehler: {e}")
            return None

    def fetch_all(self, query, params=None):
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"DB Fehler: {e}")
            return None

    @classmethod
    def set_current_user(cls, email, username):
        cls._current_user = {'email': email, 'username': username}

    @classmethod
    def get_current_user(cls):
        return cls._current_user

    @classmethod
    def logout(cls):
        cls._current_user = None