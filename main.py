# main.py
import gettext

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import FadeTransition, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from screens.login_screen import LoginScreen
from screens.signup_screen import SignupScreen
from screens.profile_screen import ProfileScreen
from screens.vault_import_screen import VaultImportScreen
from screens.vocabulary_import_screen import VocabularyImportScreen
from screens.vocabulary_test_screen import VocabularyTestScreen
from screens.vocabulary_stats_screen import VocabularyStatsScreen
from screens.admin_user_management_screen import AdminUserManagementScreen
from widgets.header import Header  # Importiere den Header

_ = gettext.gettext

class VocVaultApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # Setzt die Primärfarbe
        self.theme_cls.theme_style = "Dark"  # Setzt das Thema auf Hell oder Dunkel
        layout = MDBoxLayout(orientation='vertical')
        # ScreenManager erstellen
        self.sm = MDScreenManager(transition=FadeTransition())

        # Screens registrieren
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(SignupScreen(name='signup'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        self.sm.add_widget(VocabularyImportScreen(name='vocabulary_import'))
        self.sm.add_widget(VocabularyTestScreen(name='vocabulary_test'))
        self.sm.add_widget(VocabularyStatsScreen(name='vocabulary_stats'))
        self.sm.add_widget(AdminUserManagementScreen(name='admin_user_management'))
        self.sm.add_widget(VaultImportScreen(name='vault_import'))
        layout.add_widget(self.sm)

        return layout

    def switch_language(self, lang_code):
        # Lade die entsprechende Sprachdatei
        lang = gettext.translation(
            domain='messages',
            localedir='locales',
            languages=[lang_code],
            fallback=True
        )
        lang.install()
        global _
        _ = lang.gettext

        # Texte auf allen Screens aktualisieren
        self.update_texts()

    def update_texts(self):
        for screen in self.root.screens:
            if hasattr(screen, "update_texts"):
                screen.update_texts()

    def toggle_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
        print(f"Theme gewechselt: {self.theme_cls.theme_style}")

if __name__ == '__main__':
    VocVaultApp().run()
