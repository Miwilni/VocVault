# screens/vocabulary_test_screen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from services.vocabulary_service import VocabularyService
from widgets.toast import show_toast

import random

Builder.load_file('kv/vocabulary_test_screen.kv')

class VocabularyTestScreen(MDScreen):
    def on_enter(self):
        self.vocab_service = VocabularyService()
        self.load_random_term()

    def load_random_term(self):
        term = self.vocab_service.get_random_term()
        if term:
            self.current_term = term
            self.ids.term_label.text = f"Übersetze: {term['english_term']}"
        else:
            show_toast("Noch keine Vokabeln vorhanden, füge welche hinzu!")
            from kivy.app import App
            app = App.get_running_app()
            app.sm.current = 'vocabulary_import'

    def submit_translation(self):
        if not self.current_term:
            show_toast("Keine aktive Vokabel.")
            return

        user_input = self.ids.translation_input.text.strip()
        if not user_input:
            show_toast("Bitte eine Übersetzung eingeben.")
            return

        correct = self.vocab_service.check_translation(self.current_term, user_input)

        if correct:
            show_toast("Richtig! 🎉")
        else:
            show_toast(f"Falsch. Richtige Antwort: {self.current_term['translated_term']}")

        self.ids.translation_input.text = ""
        self.load_random_term()
