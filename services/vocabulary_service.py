# services/vocabulary_service.py
from services.db_service import DBService
import random
from widgets.toast import show_toast

class VocabularyService:
    def __init__(self):
        self.db = DBService()

    def import_term(self, english_term, translated_term, language):
        insert_english = "INSERT INTO TermEnglish (EnglishTerm) VALUES (%s)"
        if not self.db.execute_query(insert_english, (english_term,)):
            return False

        # ID des eingefügten englischen Terms holen
        select_query = "SELECT Id FROM TermEnglish WHERE EnglishTerm = %s ORDER BY CreateDate DESC LIMIT 1"
        term_id = self.db.fetch_one(select_query, (english_term,))
        if not term_id:
            return False
        term_id = term_id[0]

        insert_translation = """
            INSERT INTO TermTranslation (TranslatedTerm, TermId, LanguageId)
            VALUES (%s, %s, (SELECT Id FROM Language WHERE NameInEnglish = %s LIMIT 1))
        """
        return self.db.execute_query(insert_translation, (translated_term, term_id, language))

    def get_random_term(self):
        user = self.db.get_current_user()
        if not user:
            return None

        learning_query = """
            SELECT LearningLanguageId FROM UserLearningLanguage WHERE UserId = (
                SELECT Email FROM UserAdministration WHERE Email = %s LIMIT 1
            )
        """
        learning_lang_id = self.db.fetch_one(learning_query, (user['email'],))
        if not learning_lang_id:
            return None
        learning_lang_id = learning_lang_id[0]

        query = """
            SELECT te.Id, te.EnglishTerm, tt.TranslatedTerm
            FROM TermEnglish te
            JOIN TermTranslation tt ON te.Id = tt.TermId
            WHERE tt.LanguageId = %s
            ORDER BY RAND()
            LIMIT 1
        """
        result = self.db.fetch_one(query, (learning_lang_id,))
        if result:
            return {
                'term_id': result[0],
                'english_term': result[1],
                'translated_term': result[2]
            }
        return None

    def check_translation(self, term_data, user_translation):
        correct = term_data['translated_term'].strip().lower() == user_translation.strip().lower()

        # Antwort loggen
        log_query = """
            INSERT INTO LogVocab (IsCorrect, TermId, UserId)
            VALUES (%s, %s,
                (SELECT Id FROM UserAdministration WHERE Email = %s LIMIT 1)
            )
        """
        self.db.execute_query(log_query, (int(correct), term_data['term_id'], self.db.get_current_user()['email']))

        return correct

    def get_statistics(self):
        user = self.db.get_current_user()
        if not user:
            return None

        query = """
            SELECT
                SUM(CASE WHEN IsCorrect = 1 THEN 1 ELSE 0 END) AS Correct,
                SUM(CASE WHEN IsCorrect = 0 THEN 1 ELSE 0 END) AS Incorrect
            FROM LogVocab
            WHERE UserId = (SELECT Id FROM UserAdministration WHERE Email = %s LIMIT 1)
        """
        result = self.db.fetch_one(query, (user['email'],))

        if result:
            return {'correct': result[0] or 0, 'incorrect': result[1] or 0}
        return None
