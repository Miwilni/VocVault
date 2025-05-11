# services/user_service.py
from services.db_service import DBService
from utils.hash_it import generate_normal_hash, verify_secure_hash
from widgets.toast import show_toast

class UserService:
    def __init__(self):
        self.db = DBService()

    def check_current_is_admin(self):
        user = self.db.get_current_user()
        if not user:
            return None

        check_admin_query = "SELECT IsAdmin FROM UserAdministration WHERE Email = %s"
        is_admin = self.db.fetch_one(check_admin_query, (user['email'],))
        if not is_admin or not is_admin[0]:
            return False
        else:
            return True

    def get_current_user(self):
        user = self.db.get_current_user()
        if not user:
            return None

        query = """
            SELECT Username, Email, PhoneNumber, 
                   (SELECT NameInEnglish FROM Language WHERE Id = NativeLanguageId) AS NativeLanguage, IsAdmin, TwoFAEnabled
            FROM UserAdministration
            WHERE Email = %s
        """
        result = self.db.fetch_one(query, (user['email'],))
        if result:
            return {
                'username': result[0],
                'email': result[1],
                'phone_number': result[2],
                'native_language': result[3],
                'is_admin': result[4],
                'two_f_a_enabled': result[5]
            }
        return None

    def update_profile(self, phone_number, native_language, username, two_fa_enabled, is_english="NameInEnglish"):
        user = self.db.get_current_user()
        if not user:
            return False
        update_query = f"""
            UPDATE UserAdministration
            SET PhoneNumber = %s,
                NativeLanguageId = (SELECT Id FROM Language WHERE {is_english} = %s LIMIT 1),
                Username = %s,
                TwoFAEnabled = %s
            WHERE Email = %s
        """
        values = (phone_number, native_language, username, two_fa_enabled, user['email'])

        return self.db.execute_query(update_query, values)

    def change_password(self, old_password, new_password):
        user = self.db.get_current_user()
        if not user:
            return False

        check_query = "SELECT PasswordHash FROM UserAdministration WHERE Email = %s"
        stored_hash = self.db.fetch_one(check_query, (user['email'],))
        if not stored_hash:
            return False

        stored_hash = stored_hash[0]

        if verify_secure_hash(old_password, stored_hash) or generate_normal_hash(old_password) == stored_hash:
            new_hash = generate_normal_hash(new_password)
            update_query = "UPDATE UserAdministration SET PasswordHash = %s WHERE Email = %s"
            return self.db.execute_query(update_query, (new_hash, user['email']))
        else:
            return False

    def get_all_users(self):
        user = self.db.get_current_user()
        if not user:
            return None

        check_admin_query = "SELECT IsAdmin FROM UserAdministration WHERE Email = %s"
        is_admin = self.db.fetch_one(check_admin_query, (user['email'],))
        if not is_admin or not is_admin[0]:
            return None  # Nicht Admin

        query = "SELECT Username, Email, PhoneNumber, IsAdmin, TwoFAEnabled, NameInEnglish FROM UserAdministration, Language WHERE Language.Id = UserAdministration.NativeLanguageId"
        users = self.db.fetch_all(query)
        return [{'username': u[0], 'email': u[1], 'phonenumber': u[2], 'nativelanguage': u[5], 'isadmin': u[3], 'twofaenabled': u[4]} for u in users]

    def delete_user(self, email):
        user = self.db.get_current_user()
        if not user:
            return False

        check_admin_query = "SELECT IsAdmin FROM UserAdministration WHERE Email = %s"
        is_admin = self.db.fetch_one(check_admin_query, (user['email'],))
        if not is_admin or not is_admin[0]:
            return False  # Nicht Admin

        delete_query = "DELETE FROM UserAdministration WHERE Email = %s"
        return self.db.execute_query(delete_query, (email,))

    def get_all_languages(self, in_english: bool=False):
        if not in_english:
            get_query = "SELECT NameInLanguage FROM Language"
        else:
            get_query = "SELECT NameInEnglish FROM Language"
        languages = self.db.fetch_all(get_query)
        languages_list: list = []
        for language in languages:
            languages_list.append(str(language[0]))
        return languages_list

    def update_user(self, email, username, password, twofaenabled, isadmin, native_language, phone_number, is_english):
        from utils.hash_it import generate_normal_hash
        if email == self.get_current_user()['email']:
            show_query = "Go to profile to update your own profile!"
            return False
        password= generate_normal_hash(password)
        update_query = "UPDATE UserAdministration SET "
        args = locals()  # Gibt Dictionary mit allen lokalen Variablen zurück
        parameter_liste = list(args.values())
        parameter_liste.pop(0)
        parameter_liste.pop(len(parameter_liste)-1)
        parameter_liste_1=[]
        for i in range(len(parameter_liste)):
            if i != 0 and i!= len(parameter_liste) and i!= len(parameter_liste)-1 and i!= len(parameter_liste)-2:
                parameter_liste_1.append(parameter_liste[i])
        language = "NameInEnglish"
        if is_english:
            language = "NameInEnglish"
        else:
            language = "NameInLanguage"
        attributes: list[str] = ["Username", "PasswordHash", "TwoFAEnabled", "isAdmin", "NativeLanguageId", "PhoneNumber"]
        for i in range(len(parameter_liste_1)):
            if parameter_liste_1[i] == "":
                attributes.pop(i)

        for i in range(len(attributes)):
            if i == 0:
                update_query = f"{update_query} {attributes[i]} = '{parameter_liste_1[i]}'" #'hinzufügen
            elif i == 4:
                update_query = f"{update_query}, {attributes[i]} = (SELECT Id FROM Language WHERE {language} = '{native_language}' LIMIT 1)"
            else:
                update_query = f"{update_query}, {attributes[i]} = '{parameter_liste_1[i]}'"
        update_query = f"{update_query} WHERE Email = %s"
        values = email
        return self.db.execute_query(update_query, values)