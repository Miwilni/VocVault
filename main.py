import VocabularyTraining
import UserAdministration
def main():
    user1:UserAdministration.User = UserAdministration.User()
    """print(user1.get_user_id())
    print(user1.get_email())
    print(user1.get_role())
    print(user1.get_username())
    print(user1.get_password())
    print(user1.get_number_vocabulary_relations())
    print(user1.get_ids_vocabulary_relations())
    print(user1.get_native_language())
    print(user1.get_foreign_languages"""

    VocabularyTraining.main()

if __name__ == '__main__':
    main()