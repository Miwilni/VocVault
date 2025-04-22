from src.send_mail import *
from src.sql_zugriff import execute_get_query, execute_insert_query
import time
from src import main
from src.hash_it import *
import pwinput
import secrets
import string
from vocabulary import Vocab

def get_lang_id(name):
    langid: int = -1
    while not langid > 0:
        names: [list[str]] = execute_get_query(f"SELECT NameInEnglish FROM Language")
        for db_name in names:
            db_name = db_name[0]
            if db_name.lower() == name.lower():
                langid = int(execute_get_query(f"SELECT Id FROM Language WHERE NameInEnglish = '{db_name}'")[0][0])
        if not langid > 0:
            names: [list[str]] = execute_get_query(f"SELECT NameInLanguage FROM Language")
            for db_name in names:
                db_name = db_name[0]
                if db_name.lower() == name.lower():
                    langid = int(execute_get_query(f"SELECT Id FROM Language WHERE NameInLanguage = '{db_name}'")[0][0])
        if not langid > 0:
            name = input("Enter another Language Name because yours can´t be used or doesn´t exist: ")
    return langid

def choose_data(attribut: str, is_unique: bool):
    data: str = input(f"Choose a {attribut}: ")
    if is_unique:
        user_id: tuple = (None, None)
        while user_id != ():
            user_id: tuple = execute_get_query(f"SELECT Id FROM User WHERE {attribut} = '{data}'")
            if user_id != ():
                user_id = (None, None)
                data = input(f"Your {attribut} is already taken. Please choose another one: ")
            else:
                return data
    else:
        return data


def create_otp():
    found_otp = False
    otp: str = ""
    while not found_otp:
        otp= ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        used_otps = [list(item) for item in execute_get_query("SELECT OtpInHash FROM ValidOtp")]
        for i in range(len(used_otps)):
            used_otps[i] = used_otps[i][0]
        used_otps = [item for item in used_otps]
        if generate_normal_hash(otp) not in used_otps:
            found_otp = True
    return otp


def insert_otp(otp: str, email: str, purpose: str):
    """events: tuple = execute_get_query("SHOW EVENTS;")
    if events != ():
        event_index: int = int(events[len(events) - 1][1][len(events[len(events) - 1][1]) - 1]) + 1
    else:
        event_index = 0"""
    execute_insert_query(
        f"CREATE EVENT `delete_otp{email}{purpose}` ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL {10 * 60} SECOND DO DELETE From ValidOtp WHERE User_Id = (Select Id From User WHERE Email = '{email}')")
    execute_insert_query(
        f"CREATE EVENT `delete_user{email}{purpose}` ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL {10 * 60} SECOND DO DELETE FROM User WHERE Email = '{email}'")
    id:int = execute_get_query("Select max(Id)+1 From ValidOtp")[0][0]
    print(id)
    if id is None:
        id = 1
    print(id)
    execute_insert_query(f"INSERT INTO ValidOtp (Id, OtpInHash, Purpose, CreateDate, User_id) VALUES ({id},'{generate_normal_hash(otp)}', '{purpose}',CURRENT_TIMESTAMP,(SELECT Id From User Where Email = '{email}'))")


def check_otp(email: int, purpose: str)->bool: #TODO ERROR
    input_otp: str =""
    user_id = execute_get_query(f"SELECT Id FROM User WHERE Email = '{email}'")[0][0]
    otp_in_hash = execute_get_query(
        f"SELECT OtpInHash FROM ValidOtp WHERE User_Id = '{user_id}' and Purpose = '{purpose}'")
    if otp_in_hash != ():
        otp_in_hash = otp_in_hash[0][0]
        for i in range(0, 3, 1):
            if generate_normal_hash(input_otp) != otp_in_hash:
                if i == 0:
                    input_otp:str = pwinput.pwinput("Type in your one-time password: ")
                else:
                    print(f"The one-time Password is incorrect, you have {3 - i} attempts remaining!")
                    input_otp = pwinput.pwinput("One-time Password: ")
            else:
                print(f"DROP EVENT IF EXISTS `delete_otp{email}{purpose}`;")
                print(f"DROP EVENT IF EXISTS `delete_user{email}{purpose}`;")
                execute_insert_query(f"DELETE FROM `ValidOtp` WHERE `User_Id` = {user_id} and `Purpose` = '{purpose}'")
                print("2FA and One-Time Password was correct!")
                return True
        return False
    else:
        print("otp_in_hash = ()")
        return False


class User:
    def __init__(self):
        self.__user_id: int = -1
        self.__email: str = ""
        self.__phone_number: int = -1
        self.__username: str = ""
        self.__password: str = ""
        self.__is_admin: str = ""
        self.__native_language: str = ""
        self.__otp: str = ""
        self.__vocab: Vocab = Vocab()
        self.__sign_in_attemps: int = 0

    def set_username(self, username: str):
        self.__username: str = username
        exists: int = \
        execute_get_query(f"SELECT EXISTS (SELECT 1 FROM `User` WHERE Username = '{self.__username}');")[0][0]
        if exists == 0:
            return False
        else:
            return True

    # Get from DB and set
    def db_get_user_id(self):
        self.__user_id = execute_get_query(f"SELECT `Id` FROM `User` WHERE `Username` = '{self.__username}'")[0][0]

    def db_get_password(self):
        self.__password = execute_get_query(f"SELECT Password FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_native_language(self):
        self.__native_language = \
        execute_get_query(f"SELECT Language_Id FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_role(self):
        if execute_get_query(f"SELECT `isAdmin` FROM User WHERE Username = '{self.__username}'")[0][0] == "0":
            self.__is_admin = False
        else:
            self.__is_admin = True

    # def db_get_number_vocabulary_relations(self):
    #     self.__number_vocabulary_relations = execute_get_query(f"SELECT Role FROM User WHERE Username = '{self.__username}'")[0][0]

    # def db_get_ids_vocabulary_relations(self):
    #     self.__ids_vocabulary_relations = execute_get_query(f"SELECT IDsVocabularyRelations FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_email(self):
        self.__email = execute_get_query(f"SELECT Email FROM User WHERE Username = '{self.__username}'")[0][0]

    # def db_get_otp(self):
    #     self.__otp = execute_get_query(f"SELECT OTP FROM User WHERE Username = '{self.__username}'")[0][0]

    #Set or update db information
    def update_user_email(self, new_email: str):
        execute_get_query(f"UPDATE User SET Email = '{new_email}' WHERE Username = '{self.__username}'")

    def update_user_role(self, new_is_admin: str):
        execute_get_query(f"UPDATE User SET IsAdmin = '{new_is_admin}' WHERE Username = '{self.__username}'")

    def update_user_name(self, new_username: str):
        execute_get_query(f"UPDATE User SET Username = '{new_username}' WHERE Username = '{self.__username}'")

    def update_user_password(self, new_password: str):
        new_password = generate_normal_hash(new_password)
        execute_get_query(f"UPDATE User SET Password = '{new_password}' WHERE Username = '{self.__username}'")

    def update_native_language(self, new_native_language: str):
        new_native_language = new_native_language.upper()
        execute_get_query(f"UPDATE User SET Language_id = '{new_native_language}' WHERE Username = '{self.__username}'")

    def add_foreign_language(self, new_foreign_languages: list[str]):
        pass

    def del_foreign_language(self, foreign_languages: list[str]):#TODO
        pass

    def del_index_foreign_language(self, index_foreign_language: int):#TODO
        pass

    def set_foreign_languages(self, new_foreign_languages: list[str]):#TODO
        pass


    # Get from py code
    def get_user_id(self):
        return self.__user_id

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_role(self) -> str:
        return self.__is_admin

    def get_native_language(self) -> str:
        return self.__native_language

    def get_email(self)->str:
        return self.__email

    def check_otp_overall(self, purpose, email):
        if not check_otp(email, purpose):
            print("Too many Attempts with invalid One-time Password. Please try again in 30 seconds.")
            for i in range(6):
                print(f"Time left you need to wait: {30 - 5 * i}")
                time.sleep(5)
            user_id = execute_get_query(f"SELECT Id FROM User WHERE Email = '{email}'")[0][0]
            execute_insert_query(f"DELETE FROM `ValidOtp` WHERE `User_Id` = {user_id} and `Purpose` = '{purpose}'")
            self.send_otp(purpose, email)

    def send_otp(self, purpose: str, email: str):
        user_id = execute_get_query(f"SELECT Id FROM User where Email = '{email}'")[0][0]
        if execute_get_query(f"SELECT OtpInHash FROM ValidOtp WHERE User_Id = '{user_id}'") == ():
            otp = create_otp()
            insert_otp(otp, email, purpose)
            send_mail(email, f"Your VocVault One-Time Password: {otp}", f"You requested a One-Time Password from VocVault. \nIt is '{otp}'.\n You can only use it in the next ten minutes {purpose}.\n If you didn't request it and don´t want to be a user of VocVault, just answer with 'delete' and if you are and want to be a member of VocVault but didn't request the code, please change your password or reset it.", f"Your Code has been successfully sent to: {email}!")
            self.check_otp_overall(purpose, email)
        else:
            print("You already have an OTP. Do you remember it (press '2') or do you want a new one (press '1')?")
            answer: str = input("Answer: ")
            if answer == '1':
                user_id = execute_get_query(f"SELECT Id FROM User WHERE Email = '{email}'")[0][0]
                execute_insert_query(f"UPDATE ValidOtp SET OtpInHash = '0' WHERE User_id = {user_id}")
                self.send_otp(purpose, email)
            else:
                self.check_otp_overall(purpose, email)
            self.check_otp_overall(purpose, email)

    def sign_in(self, username:str, password:str):
        if self.__sign_in_attemps == 3:
            self.__sign_in_attemps = 0
            return "Too many attempts with invalid credentials"
        self.__sign_in_attemps += 1
        if not self.set_username(username):
            return "Invalid username"
        if not self.set_password(password):
            return "Invalid password"
        if not self.check_password():
            return "Invalid password"
        self.update_me()
        # self.send_otp("for 2 FA", email) TODO
        return"Successfully Signed In!"



    def add_user(self, email: str, username:str, password:str, is_admin:bool, native_language:str, phone_number: str, two_fa_activated:bool = False):
        max_user_id: int = execute_get_query(f"SELECT MAX(Id) FROM User")[0][0]
        user_id: int
        if max_user_id is None:
            user_id:int = 1
        else:
            user_id: int = int(max_user_id) + 1
        native_language_id:int = get_lang_id(native_language)
        if two_fa_activated:
            two_fa_activated_int: int = 1
        else:
            two_fa_activated_int = 0
        if is_admin:
            is_admin_int: int = 1
        else:
            is_admin_int = 0
        query1: str = f"INSERT INTO User (Id, Email, isAdmin, Username, Password, 2FaActivated, PhoneNumber, Language_id) VALUES ('{user_id}' ,'{email}', '{is_admin_int}', '{username}', '{password}', '{two_fa_activated_int}', '{phone_number}', '{native_language_id}');"#TODO
        execute_insert_query(query1)
        self.send_otp("for signing up", email)
        print("Successfully Signed up")
        self.introduce_user(True)

    def sign_up(self):
        user_name = choose_data("Username", True)
        password = generate_normal_hash(pwinput.pwinput())
        if password == generate_normal_hash(pwinput.pwinput()):
            if self.__is_admin:
                is_admin = bool(
                    input("Do you want to create a Admin (press True) or User (press False)\nYour Answer: "))
            else:
                is_admin = False
            phone_number: str = choose_data("PhoneNumber", False)
            email: str = choose_data("Email", True)
            native_language: str = choose_data("Native Language", False)
            self.add_user(email, user_name, password, is_admin, native_language, phone_number, False)
        else:
            print("Passwords do not match. Please try again.")
            self.sign_up()


    def update_me(self):
        self.db_get_password()
        self.db_get_native_language()
        self.db_get_user_id()
        self.db_get_role()
        self.db_get_email()

    def __del__(self):
        print("Signed Out Successfully")

    def sign_out(self):
        del self
        main.main()

    def check_password(self):
        correct_password: str = execute_get_query(f"SELECT Password FROM User WHERE Username = '{self.__username}'")
        correct_password = correct_password[0][0]
        if generate_normal_hash(self.__password) != correct_password:
            return False
        else:
            return True

    def set_password(self, password):
        self.__password = password
        return True

    def get_sign_in_attempts(self):
        return self.__sign_in_attemps