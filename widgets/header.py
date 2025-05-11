# widgets/header.py
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from functools import partial
from services.auth_service import AuthService
from services.user_service import UserService

Builder.load_file('kv/header.kv')

class Header(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self._last_user_was_admin = None

    def navigate(self, screen_name):
        app = self.get_running_app()
        app.sm.current = screen_name

    def toggle_theme(self):
        app = self.get_running_app()
        app.toggle_theme()

    def get_running_app(self):
        from kivy.app import App
        return App.get_running_app()

    def logout(self):
        auth_service = AuthService()
        auth_service.logout()
        self.navigate("login")

    def toggle_menu(self):
        user_service = UserService()
        is_admin = user_service.check_current_is_admin()

        # Wenn sich Rolle geändert hat oder Menü noch nicht existiert -> neu bauen
        if self.menu is None or self._last_user_was_admin != is_admin:
            if self.menu:
                self.menu.dismiss()
                self.menu = None

            if is_admin:
                menu_items = [
                    {"text": "Profil", "on_release": partial(self.navigate, "profile")},
                    {"text": "Vokabeln hinzufügen", "on_release": partial(self.navigate, "vocabulary_import")},
                    {"text": "Vokabeltraining", "on_release": partial(self.navigate, "vocabulary_test")},
                    {"text": "Statistik", "on_release": partial(self.navigate, "vocabulary_stats")},
                    {"text": "Admin", "on_release": partial(self.navigate, "admin_user_management")},
                    {"text": "Switch Color Scheme", "on_release": self.toggle_theme},
                    {"text": "Logout", "on_release": self.logout},
                ]
            else:
                menu_items = [
                    {"text": "Profil", "on_release": partial(self.navigate, "profile")},
                    {"text": "Vokabeln hinzufügen", "on_release": partial(self.navigate, "vocabulary_import")},
                    {"text": "Vokabeltraining", "on_release": partial(self.navigate, "vocabulary_test")},
                    {"text": "Statistik", "on_release": partial(self.navigate, "vocabulary_stats")},
                    {"text": "Switch Color Scheme", "on_release": self.toggle_theme},
                    {"text": "Logout", "on_release": self.logout},
                ]

            self.menu = MDDropdownMenu(
                caller=self.ids.menu_button,
                items=menu_items,
                max_height=dp(200),
            )
            self._last_user_was_admin = is_admin

        self.menu.open()


