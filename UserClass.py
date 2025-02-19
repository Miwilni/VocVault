from sql_zugriff import execute_query
import time
import main
from hash import generate_hash
class User:
    def __init__(self):
        self.__email:str = ""
        self.__UserID: int = -1
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
                self.sign_up()

    # Get from DB and set
    def db_get_user_id(self):
        self.__UserID = execute_query(f"SELECT UserID FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_username(self):
        self.__username = input("Username: ")
        exists: bool = execute_query(f"SELECT EXISTS (SELECT 1 FROM User WHERE Username = '{self.__username}');")[0][0]
        if exists == 0:
            print("This Username doesn't exist.Please try again.")
            self.introduce_user(False)

    def db_get_password(self):
        self.__password = execute_query(f"SELECT Password FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_native_language(self):
        self.__native_language = \
        execute_query(f"SELECT NativeLanguage FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_foreign_languages(self):
        self.__foreign_languages = execute_query(f"SELECT ForeignLanguages FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_role(self):
        self.__role = execute_query(f"SELECT Role FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_number_vocabulary_relations(self):
        self.__number_vocabulary_relations = execute_query(f"SELECT Role FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_ids_vocabulary_relations(self):
        self.__ids_vocabulary_relations = execute_query(f"SELECT IDsVocabularyRelations FROM User WHERE Username = '{self.__username}'")[0][0]

    def db_get_email(self):
        self.__email = execute_query(f"SELECT Email FROM User WHERE Username = '{self.__username}'")[0][0]

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
            print("Too many Attemps with invalid password. Please try again in 30 seconds.")
            for i in range (6):
                print(f"Time left you need to wait: {30-5*i}")
                time.sleep(5)
            self.introduce_user(False)
        self.db_get_password()
        self.db_get_native_language()
        self.db_get_user_id()
        self.db_get_role()
        self.db_get_number_vocabulary_relations()
        self.db_get_foreign_languages()
        self.db_get_ids_vocabulary_relations()
        print("Signed in successfully!")
    def sign_up(self):
        pass

    def __del__(self):
        print("Signed Out Successfully")

    def sign_out(self):
        del self
        main.main()

    def check_password(self):
        correct_password: str = execute_query(f"SELECT Password FROM User WHERE Username = '{self.__username}'")[0][0]
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