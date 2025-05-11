# screens/vocabulary_import_screen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from services.user_service import UserService
from services.vocabulary_service import VocabularyService
from widgets.toast import show_toast

Builder.load_file('kv/vocabulary_import_screen.kv')

class VocabularyImportScreen(MDScreen):
    def on_enter(self, *args):
        user_service = UserService()
        self.ids.language_spinner.values = user_service.get_all_languages(True)
    def import_vocabulary(self):
        english_term = self.ids.english_input.text.strip()
        translated_term = self.ids.translation_input.text.strip()
        language = self.ids.language_spinner.text

        if not (english_term and translated_term and language):
            show_toast("Bitte alle Felder ausfüllen.")
            return

        vocab_service = VocabularyService()
        success = vocab_service.import_term(english_term, translated_term, language)

        if success:
            show_toast("Vokabel erfolgreich importiert!")
            self.ids.english_input.text = ""
            self.ids.translation_input.text = ""
            self.ids.language_spinner.text = "Sprache wählen"
        else:
            show_toast("Fehler beim Importieren der Vokabel.")
