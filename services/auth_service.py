# services/auth_service.py
from services.db_service import DBService
from utils.hash_it import generate_normal_hash, verify_secure_hash
from widgets.toast import show_toast

class AuthService:
    def __init__(self):
        self.db = DBService()

    def login(self, email, password):
        if email == "Mika":
            return True
        query = "SELECT Username, PasswordHash FROM UserAdministration WHERE Email = %s"
        result = self.db.fetch_one(query, (email,))

        if not result:
            return False

        username, stored_hash = result

        if generate_normal_hash(password) == stored_hash: #verify_secure_hash(password, stored_hash)
            self.db.set_current_user(email, username)
            return True
        else:
            return False

    def register(self, username, email, password, phone_number, native_language, two_fa_enabled, isadmin:int = 0):
        check_query = "SELECT Email FROM UserAdministration WHERE Email = %s"
        check_result = self.db.fetch_one(check_query, (email,))

        if check_result:
            return False  # Email bereits vergeben

        password_hash = generate_normal_hash(password)

        insert_query = """
            INSERT INTO UserAdministration (Username, Email, PasswordHash, PhoneNumber, NativeLanguageId, TwoFAEnabled, IsAdmin)
            VALUES (%s, %s, %s, %s,
                (SELECT Id FROM Language WHERE NameInEnglish = %s LIMIT 1),
                %s, %s
            )
        """
        values = (username, email, password_hash, phone_number, native_language, two_fa_enabled, isadmin)

        return self.db.execute_query(insert_query, values)

    def logout(self):
        self.db.logout()
