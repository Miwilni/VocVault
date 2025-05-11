# screens/profile_screen.py
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen

#from main import VocVaultApp
from services.user_service import UserService
from widgets.toast import show_toast

Builder.load_file('kv/profile_screen.kv')

class ProfileScreen(MDScreen):
    password_hidden = BooleanProperty(True)
    def toggle_password_visibility(self):
        self.password_hidden = not self.password_hidden
    def on_enter(self):
        self.load_user_data()

    def load_user_data(self):
        user_service = UserService()
        user_data = user_service.get_current_user()

        self.ids.native_language_spinner.values = user_service.get_all_languages(True)
        if user_data:
            self.ids.username_field.text = f"{user_data['username']}"
            self.ids.email_field.text = f"{user_data['email']}"
            self.ids.phone_input.text = user_data['phone_number'] or ""
            self.ids.native_language_spinner.text = user_data['native_language'] or "Sprache wählen"
            self.ids.two_fa_switch.active = user_data['two_f_a_enabled'] == 1
        else:
            show_toast("Fehler beim Laden der Profildaten.")

    def update_profile(self):
        phone_number = self.ids.phone_input.text.strip()
        native_language = self.ids.native_language_spinner.text
        username = self.ids.username_field.text.strip()
        two_fa_enabled = int(self.ids.two_fa_switch.active)
        user_service = UserService()
        success = user_service.update_profile(phone_number, native_language, username, two_fa_enabled)

        if success:
            show_toast("Profil aktualisiert!")
        else:
            show_toast("Fehler beim Aktualisieren des Profils.")

    def change_password(self):
        old_password = self.ids.old_password_input.text.strip()
        new_password = self.ids.new_password_input.text.strip()
        repeat_new_password = self.ids.repeat_new_password_input.text.strip()

        if not (old_password and new_password and repeat_new_password):
            show_toast("Bitte alle Felder ausfüllen.")
            return

        if len(new_password) < 8:
            show_toast("Neues Passwort muss mindestens 8 Zeichen lang sein.")
            return

        if new_password != repeat_new_password:
            show_toast("Neue Passwörter stimmen nicht überein.")
            return

        user_service = UserService()
        success = user_service.change_password(old_password, new_password)

        if success:
            show_toast("Passwort erfolgreich geändert.")
            # Eingabefelder leeren
            self.ids.old_password_input.text = ""
            self.ids.new_password_input.text = ""
            self.ids.repeat_new_password_input.text = ""
        else:
            show_toast("Fehler beim Ändern des Passworts. Prüfe dein aktuelles Passwort.")
