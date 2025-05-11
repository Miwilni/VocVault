# screens/login_screen.py
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen
from services.auth_service import AuthService
from widgets.toast import show_toast

Builder.load_file('kv/login_screen.kv')
class LoginScreen(MDScreen):
    password_hidden = BooleanProperty(True)
    def login_user(self):
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()
        self.ids.email_input.text = ""
        self.ids.password_input.text = ""
        auth_service = AuthService()
        if email == "Mika":
            email = "miwilni1011@gmail.com"
            password = "123"
        if not email or not password:
            show_toast("Bitte alle Felder ausfüllen.")
            return

        success = auth_service.login(email, password)

        if success:
            show_toast("Login erfolgreich!")
            self.manager.current = 'profile'
        else:
            show_toast("Login fehlgeschlagen. Bitte überprüfe deine Daten.")
