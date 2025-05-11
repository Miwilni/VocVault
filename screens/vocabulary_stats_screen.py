# screens/vocabulary_stats_screen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from services.vocabulary_service import VocabularyService
from widgets.toast import show_toast

Builder.load_file('kv/vocabulary_stats_screen.kv')

class VocabularyStatsScreen(MDScreen):
    def on_enter(self):
        self.load_statistics()

    def load_statistics(self):
        vocab_service = VocabularyService()
        stats = vocab_service.get_statistics()

        if stats:
            correct = stats.get('correct', 0)
            incorrect = stats.get('incorrect', 0)
            total = correct + incorrect

            self.ids.correct_label.text = f"Richtige Antworten: {correct}"
            self.ids.incorrect_label.text = f"Falsche Antworten: {incorrect}"
            self.ids.total_label.text = f"Gesamt beantwortet: {total}"
        else:
            show_toast("Noch keine Statistiken verfügbar.")
            self.ids.correct_label.text = "Richtige Antworten: 0"
            self.ids.incorrect_label.text = "Falsche Antworten: 0"
            self.ids.total_label.text = "Gesamt beantwortet: 0"
