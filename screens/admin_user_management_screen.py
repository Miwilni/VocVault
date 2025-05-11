# screens/admin_user_management_screen.py
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from services.auth_service import AuthService
from services.kivy_service import get_widget_from_grid_layout
from services.user_service import UserService
from widgets.toast import show_toast
Builder.load_file('kv/admin_user_management_screen.kv')

class AdminUserManagementScreen(MDScreen):
    def on_enter(self):
        self.load_all_users()

    def load_all_users(self):
        user_service = UserService()
        users = user_service.get_all_users()
        self.ids.users_box.clear_widgets()
        if users:
            num_cols=10
            grid = GridLayout(
                rows=len(users)+2,
                cols=num_cols,
                size_hint= (None, None),
                padding= 10,
                spacing= 20,
                )#size_hint_x=1,
            grid.bind(minimum_height=grid.setter('height'))
            grid.bind(minimum_width=grid.setter('width'))
            self.ids.users_box.add_widget(grid)
            information: list[str] = ["Email", "Password", "Username", "Phone Number", "Admin?", "2FA", "Native Language", "Update User", "Delete User", "Edit User"]
            for info in information:
                from kivymd.uix.label import MDLabel
                if info == "Phone Number" or info == "Native Language":
                    width: int = 190
                else:
                    width: int = 150
                item = MDLabel(
                    text=info,
                    size_hint_x=None,
                    shorten=False,
                    halign="left",
                    width=width
                )
                grid.add_widget(item)  # Add widget *after* binding the texture_size
            for n in range (0,1):
                for col in range(num_cols):
                    if col == 0:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(hint_text=f"Email", size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)
                    elif col == 1:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(hint_text="Password", password=True, size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)
                    elif col == 2:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(hint_text="Username", size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)
                    elif col == 3:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(hint_text=f"Phone Number", size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)
                    elif col == 4:
                        from kivy.uix.switch import Switch
                        item = Switch(active=False, size_hint=(None, None), size=(130, 40),pos_hint={"center_x": 0.5})
                        item.disabled = True
                    elif col == 5:
                        from kivy.uix.switch import Switch
                        item = Switch(active=False, size_hint=(None, None), size=(130, 40),pos_hint={"center_x": 0.5})
                        item.disabled = True
                    elif col == 6:
                        from kivy.uix.spinner import Spinner
                        item = Spinner(text="Select Language", size_hint=(None, None), height=40, values=user_service.get_all_languages(True))
                        def adjust_spinner_width(instance, value):
                            from kivy.uix.label import Label
                            temp = Label(text=value, font_size=item.font_size)
                            temp.texture_update()
                            instance.width = temp.texture_size[0] + 30
                        item.bind(text=adjust_spinner_width)
                        adjust_spinner_width(item, item.text)
                        item.disabled = True
                    elif col == 7:
                        from kivymd.uix.button import MDIconButton
                        item = MDIconButton(icon="update", style="tonal", on_release=self.update_user,
                                            size_hint=(None, None), height=40)
                        item.disabled = True
                        #item.bind(texture_size=lambda inst, val: setattr(inst, 'width', val[0] + 20))
                    elif col == 8:
                        from kivymd.uix.button import MDIconButton
                        item = MDIconButton(icon="account-plus", style="tonal", on_release=self.insert_user, size_hint=(None, None), height=40)
                        item.disabled = True
                        #item.bind(texture_size=lambda inst, val: setattr(inst, 'width', val[0] + 20))
                    elif col == 9:
                        from kivymd.uix.button import MDIconButton
                        item = MDIconButton(icon="account-edit", style="tonal", size_hint=(None, None), height=40, on_release=self.edit_user)
                    else:
                        from kivy.uix.label import Label
                        item = Label(text="not found")
                    grid.add_widget(item)
            for user in users:
                for col in range(num_cols):
                    if col == 0:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(text=f"{user['email']}", hint_text=f"{user['email']}", size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)#size_hint_y=None, height=30,
                    elif col == 1:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(hint_text="Neues Passwort", password=True, size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)#size_hint_y=None, height=30,
                    elif col == 2:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(text=f"{user['username']}", hint_text=f"{user['username']}", size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)#size_hint_y=None, height=30,
                    elif col == 3:
                        from kivy.uix.textinput import TextInput
                        item = TextInput(text=f"{user['phonenumber']}", hint_text=f"{user['phonenumber']}", size_hint=(None, None), size=(150, 40), focus=False, readonly=True, disabled=True)#size_hint_y=None, height=30,
                    elif col == 4:
                        from kivy.uix.switch import Switch
                        from kivy.uix.label import Label
                        isadmin: bool = False
                        if str(user['isadmin']) == "1":
                            isadmin = True
                        item = Switch(active=isadmin, size_hint=(None, None), size=(130, 40), pos_hint={"center_x": 0.5})#size_hint=(None, None), size=(60, 40),
                        item.disabled = True
                        #switch = Switch(active=isadmin, size_hint_x=0.4)#size_hint_y=None,height=30,
                        #label = Label(text= "admin", color= [1, 1, 1, 1], size_hint_x=0.6)
                        #item = BoxLayout(orientation='horizontal',size_hint=(None, None), size=(220, 40), spacing=5)#size_hint_y= None, height= '40dp'
                        #item.add_widget(label)
                        #item.add_widget(switch)
                    elif col == 5:
                        from kivy.uix.switch import Switch
                        from kivy.uix.label import Label
                        twofaactivated: bool = False
                        if str(user['twofaenabled']) == "1":
                            twofaactivated = True
                        item = Switch(active=twofaactivated, size_hint=(None, None), size=(130, 40), pos_hint={"center_x": 0.5})#size_hint=(None, None), size=(60, 40),
                        item.disabled = True
                        #switch = Switch(active=twofaactivated, size_hint_x=0.4)#size_hint_x= None, width='40dp', size_hint_y=None, height=30,
                        #label = Label(text="2FA", color=[1, 1, 1, 1], size_hint_x=0.6)#
                        #item = BoxLayout(orientation='horizontal',size_hint=(None, None), size=(220, 40), spacing=5)#size_hint_y=None, height='40dp', size_hint_x= None, width='40dp'
                        #item.add_widget(label)
                        #item.add_widget(switch)
                    elif col == 6:
                        from kivy.uix.spinner import Spinner
                        item = Spinner(text= user['nativelanguage'], size_hint=(None, None), height=40, values= user_service.get_all_languages(True))#size_hint_y= None, height= '40dp',
                        def adjust_spinner_width(instance, value):
                            # Erzeuge unsichtbares Label, um Textlänge zu messen
                            from kivy.uix.label import Label
                            temp = Label(text=value, font_size=item.font_size)
                            temp.texture_update()
                            instance.width = temp.texture_size[0] + 30  # +30 für Pfeil und Padding
                        item.bind(text=adjust_spinner_width)
                        item.disabled = True
                        adjust_spinner_width(item, item.text)
                    elif col == 7:
                        from kivymd.uix.button import MDIconButton
                        item = MDIconButton(icon="update", style="tonal", on_release = self.update_user, size_hint=(None, None), height=40)
                        item.disabled = True
                        #item.bind(texture_size=lambda inst, val: setattr(inst, 'width', val[0] + 20))
                    elif col == 8:
                        from kivymd.uix.button import MDIconButton
                        item = MDIconButton(icon="delete", style="tonal", on_release = self.insert_user, size_hint=(None, None), height=40)
                        item.disabled = True
                        #item.bind(texture_size=lambda inst, val: setattr(inst, 'width', val[0] + 20))
                        #['standard', 'filled', 'tonal', 'outlined']
                    elif col == 9:
                        from kivymd.uix.button import MDIconButton
                        item = MDIconButton(icon="account-edit", style="tonal", size_hint=(None, None), height=40, on_release=self.edit_user)#
                    else:
                        from kivy.uix.label import Label
                        item=Label(text="not found")
                    grid.add_widget(item)
        else:
            show_toast("Keine Benutzer gefunden oder keine Admin-Rechte")

        """if users:
            for user in users:
                from kivy.uix.label import Label
                label = Label(text=f"{user['username']} - {user['email']}", size_hint_y=None, height=30)
                self.ids.users_box.add_widget(label)
        else:
            show_toast("Keine Benutzer gefunden oder keine Admin-Rechte.")"""


    def edit_user(self, instance):
        disabled_bool: bool = not get_widget_from_grid_layout(instance, 0).disabled
        get_widget_from_grid_layout(instance, 0).disabled = disabled_bool  # email
        get_widget_from_grid_layout(instance, 0).readonly = disabled_bool
        get_widget_from_grid_layout(instance, 2).disabled = disabled_bool  # username
        get_widget_from_grid_layout(instance, 2).readonly = disabled_bool
        get_widget_from_grid_layout(instance, 1).disabled = disabled_bool  # password
        get_widget_from_grid_layout(instance, 1).readonly = disabled_bool
        get_widget_from_grid_layout(instance, 3).disabled = disabled_bool  # phone_number
        get_widget_from_grid_layout(instance, 3).readonly = disabled_bool
        get_widget_from_grid_layout(instance, 6).disabled = disabled_bool  # native_language
        get_widget_from_grid_layout(instance, 5).disabled = disabled_bool  # two_fa_enabled
        get_widget_from_grid_layout(instance, 4).disabled = disabled_bool  # is_admin
        get_widget_from_grid_layout(instance, 7).disabled = disabled_bool
        get_widget_from_grid_layout(instance, 8).disabled = disabled_bool
        if disabled_bool:
            show_toast("Benutzer nicht mehr editierbar.")
        else:
            show_toast("Benutzer editierbar.")


    def update_user(self, instance):
        self.update_user_search(False, instance)

    def update_user_search(self, is_search=True, instance = None):
        if is_search:
            email = self.ids.delete_email_input.text.strip()
        else:
            email = get_widget_from_grid_layout(instance).text
        if not email:
            show_toast("Bitte eine E-Mail eingeben.")
            return
        password = get_widget_from_grid_layout(instance, 1).text
        username = get_widget_from_grid_layout(instance, 2).text
        phone_number = get_widget_from_grid_layout(instance, 3).text
        is_admin_bool = get_widget_from_grid_layout(instance, 4).active
        if is_admin_bool:
            is_admin = 1
        else:
            is_admin = 0
        two_f_a_activated_bool = get_widget_from_grid_layout(instance, 5).active
        if two_f_a_activated_bool:
            two_f_a_activated = 1
        else:
            two_f_a_activated = 0
        nativelanguage = get_widget_from_grid_layout(instance, 6).text
        is_english = True
        user_service = UserService()
        success = user_service.update_user(email, username, password, two_f_a_activated, is_admin, nativelanguage, phone_number,is_english)
        if success:
            show_toast(f"Benutzer {email} geupdated.")
            self.load_all_users()
            self.ids.delete_email_input.text = ""
        else:
            show_toast("Fehler beim Updaten des Benutzers.")
    def delete_user(self, instance):
        self.delete_user_search(False, instance)
    def delete_user_search(self, is_search=True, instance = None):
        if is_search:
            email = self.ids.delete_email_input.text.strip()
        else:
            email = get_widget_from_grid_layout(instance).text
        if not email:
            show_toast("Bitte eine E-Mail eingeben.")
            return
        user_service = UserService()
        success = user_service.delete_user(email)
        if success:
            show_toast(f"Benutzer {email} gelöscht oder Benutzer hat nicht existiert.")
            self.load_all_users()
            self.ids.delete_email_input.text = ""
        else:
            show_toast("Fehler beim Löschen des Benutzers.")

    def insert_user(self, instance):
        username = get_widget_from_grid_layout(instance, 2).text
        email = get_widget_from_grid_layout(instance, 0).text
        password = get_widget_from_grid_layout(instance, 1).text
        phone_number = get_widget_from_grid_layout(instance, 3).text
        native_language = get_widget_from_grid_layout(instance, 6).text
        two_fa_enabled:int = 0
        if get_widget_from_grid_layout(instance, 5).active:
            two_fa_enabled = 1
        is_admin: int = 0
        if get_widget_from_grid_layout(instance, 4).active:
            is_admin = 1
        # Validierungen
        if not (username and email and password and phone_number and native_language):
            show_toast("Bitte alle Felder ausfüllen.")
            return
        auth_service = AuthService()
        success = auth_service.register(username, email, password, phone_number, native_language, two_fa_enabled, is_admin)

        if success:
            show_toast("Registrierung erfolgreich!")
        else:
            show_toast("Registrierung fehlgeschlagen. E-Mail vielleicht schon vergeben?")