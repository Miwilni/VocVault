from sql_zugriff import execute_get_query, execute_insert_query
import time
import main
from hash import generate_hash
import pwinput

class User:
    def __init__(self):
        self.__UserID: int = -1
        self.__email: str = ""
        self.__username: str = ""
        self.__password: str = ""
        self.__role: str = ""
        self.__number_vocabulary_relations: int = -1
        self.__ids_vocabulary_relations: list[int] = []
        self.__native_language: str = ""
        self.__foreign_languages: list[str] = []
        self.introduce_user(True)

    def introduce_user(self,first_attempt: bool):
        if first_attempt:
            print("Welcome to my Vocabulary Trainer!\n")
        answer:str = ""
        while answer == "":
            answer: str = input("Do you want to sign in (press 1) or sign up (press 2)?\n Your Answer: ")
            if answer == "1":
                self.sign_in()
            elif answer == "2":
                self.sign_up(False)

    # Get from DB and set
    def db_get_user_id(self):
        self.__UserID = execute_get_query(f"SELECT UserID FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_username(self):
        self.__username = input("Username: ")
        exists: bool = execute_get_query(f"SELECT EXISTS (SELECT 1 FROM User WHERE Username = '{self.__username}');")[0][0]
        if exists == 0:
            print("This Username doesn't exist.Please try again.")
            self.introduce_user(False)

    def db_get_password(self):
        self.__password = execute_get_query(f"SELECT Password FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_native_language(self):
        self.__native_language = \
        execute_get_query(f"SELECT NativeLanguage FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_foreign_languages(self):
        self.__foreign_languages = execute_get_query(f"SELECT ForeignLanguages FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_role(self):
        self.__role = execute_get_query(f"SELECT Role FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_number_vocabulary_relations(self):
        self.__number_vocabulary_relations = execute_get_query(f"SELECT Role FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_ids_vocabulary_relations(self):
        self.__ids_vocabulary_relations = execute_get_query(f"SELECT IDsVocabularyRelations FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_email(self):
        self.__email = execute_get_query(f"SELECT Email FROM User WHERE Username = '{self.__username}'")[0][0]

    #Set or update db information
    def update_user_email(self, new_email: str):
        execute_get_query(f"UPDATE User SET Email = '{new_email}' WHERE Username = '{self.__username}'")

    def update_user_role(self, new_role: str):
        execute_get_query(f"UPDATE User SET Role = '{new_role}' WHERE Username = '{self.__username}'")

    def update_user_name(self, new_username: str):
        execute_get_query(f"UPDATE User SET Username = '{new_username}' WHERE Username = '{self.__username}'")

    def update_user_password(self, new_password: str):
        new_password = generate_hash(new_password)
        execute_get_query(f"UPDATE User SET Password = '{new_password}' WHERE Username = '{self.__username}'")

    def update_number_vocabulary_relations(self, new_number_vocabulary_relations: int):
        execute_get_query(f"UPDATE User SET NumberVocabularyRelations = '{new_number_vocabulary_relations}' WHERE Username = '{self.__username}'")

    def add_id_vocabulary_relations(self, new_id_vocabulary_relations: int):
        old_id_vocabulary_relations: list = execute_get_query(f"SELECT IDsVocabularyRelations FROM User WHERE Username = '{self.__username}'")[0][0]
        old_id_vocabulary_relations.append(new_id_vocabulary_relations)
        execute_get_query(f"UPDATE User SET IDsVocabularyRelations = '{old_id_vocabulary_relations}' WHERE Username = '{self.__username}'")
        self.update_number_vocabulary_relations(len(old_id_vocabulary_relations))

    def del_id_vocabulary_relations(self, id_vocabulary_relations: int):#TODO
        pass

    def del_index_id_vocabulary_relations(self, index_id_vocabulary_relation: int):#TODO
        pass

    def set_id_vocabulary_relations(self, new_id_vocabulary_relations: int):#TODO
        pass

    def update_native_language(self, new_native_language: str):
        new_native_language = new_native_language.upper()
        execute_get_query(f"UPDATE User SET NativeLanguage = '{new_native_language}' WHERE Username = '{self.__username}'")

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
        return self.__UserID

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_role(self) -> str:
        return self.__role

    def get_number_vocabulary_relations(self) -> int:
        return self.__number_vocabulary_relations

    def get_ids_vocabulary_relations(self) -> list[int]:
        return self.__ids_vocabulary_relations

    def get_native_language(self) -> str:
        return self.__native_language

    def get_foreign_languages(self) -> list[str]:
        return self.__foreign_languages

    def get_email(self)->str:
        return self.__email

    def sign_in(self):
        self.db_get_username()
        while not self.check_password():
            print("Too many Attempts with invalid password. Please try again in 30 seconds.")
            for i in range (6):
                print(f"Time left you need to wait: {30-5*i}")
                time.sleep(5)
            self.introduce_user(False)
        self.update_me()
        print("Signed in successfully!")

    def add_user(self, email: str,username:str, password:str, role:str, native_language:str, foreign_languages:str):
        self.__UserID = execute_get_query(f"SELECT MAX(UserID) FROM User")[0][0] + 1
        self.__email: str = email
        self.__username: str = username
        self.__password: str = password
        self.__role: str = role
        self.__number_vocabulary_relations: int = 0
        self.__ids_vocabulary_relations: list[int] = []
        self.__native_language: str = native_language.upper()
        self.__foreign_languages: str = foreign_languages.upper()
        query1: str = f"INSERT INTO User (UserID, Email, Role, Username, Password, NumberVocabularyRelations, IDsVocabularyRelations, NativeLanguage, ForeignLanguages, Einmalcode, ZeitEinmalcode) VALUES ({self.__UserID}, '{self.__email}', '{self.__role}', '{self.__username}', '{self.__password}', {self.__number_vocabulary_relations}, '{self.__ids_vocabulary_relations}', '{self.__native_language}', '{self.__foreign_languages}', 0, '20-02-2025');"
        execute_insert_query(query1)
        print("Successfully Signed up")
        self.introduce_user(True)

    def sign_up(self, admin: bool):
        if admin:
            admin = bool(input("Do you want to create a Admin (press True) or User (press False)\nYour Answer: "))
        if admin:
            self.add_user(input("What's your Email address?: "), input("Choose a username: "),
                          generate_hash(pwinput.pwinput()), "Admin", input("Enter your Native Language: "),
                          "[" + input("Enter your Foreign Languages separated by commas: ") + "]")
        else:
            self.add_user(input("What's your Email address?: "), input("Choose a username: "),
                          generate_hash(pwinput.pwinput()), "User", input("Enter your Native Language: "),
                          "[" + input("Enter your Foreign Languages separated by commas: ") + "]")

    def update_me(self):
        self.db_get_password()
        self.db_get_native_language()
        self.db_get_user_id()
        self.db_get_role()
        self.db_get_number_vocabulary_relations()
        self.db_get_foreign_languages()
        self.db_get_ids_vocabulary_relations()

    def __del__(self):
        print("Signed Out Successfully")

    def sign_out(self):
        del self
        main.main()

    def check_password(self):
        correct_password: str = execute_get_query(f"SELECT Password FROM User WHERE Username = '{self.__username}'")[0][0]
        for i in range (0, 3, 1):
            if generate_hash(self.__password) != correct_password:
                if i == 0:
                    self.__password: str = input("Password: ")
                else:
                    print(f"The Password is incorrect, you have {3-i} attempts remaining!")
                    self.__password: str = input("Password: ")
            else:
                return True
        return False