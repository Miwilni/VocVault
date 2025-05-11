# screens/signup_screen.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from services.auth_service import AuthService
from widgets.toast import show_toast
from services.user_service import UserService

Builder.load_file('kv/signup_screen.kv')

class SignupScreen(Screen):
    def on_enter(self):
        self.load_screen()
    def load_screen(self):
        user_service = UserService()
        self.ids.native_language_spinner.values = user_service.get_all_languages(True)

    def signup_user(self):
        username = self.ids.username_input.text.strip()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()
        repeat_password = self.ids.repeat_password_input.text.strip()
        phone_number = self.ids.phone_input.text.strip()
        native_language = self.ids.native_language_spinner.text
        two_fa_enabled = int(self.ids.two_fa_switch.active)

        # Validierungen
        if not (username and email and password and repeat_password and phone_number and native_language):
            show_toast("Bitte alle Felder ausfüllen.")
            return

        if len(password) < 8:
            show_toast("Passwort muss mindestens 8 Zeichen lang sein.")
            return

        if password != repeat_password:
            show_toast("Passwörter stimmen nicht überein.")
            return

        auth_service = AuthService()
        success = auth_service.register(username, email, password, phone_number, native_language, two_fa_enabled)

        if success:
            show_toast("Registrierung erfolgreich! Du kannst dich jetzt einloggen.")
            self.manager.current = 'login'
        else:
            show_toast("Registrierung fehlgeschlagen. E-Mail vielleicht schon vergeben?")
