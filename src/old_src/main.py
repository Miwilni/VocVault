from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import UserAdministrationGui
import time
Window.size = (400, 600)


class ImageButton(ButtonBehavior, Image):
    pass
def set_visible(widget, visible):
    widget.opacity = 1 if visible else 0
    widget.disabled = not visible

def try_sign_in(username, password, info_label, user1, sign_in_btn):
    txt = user1.sign_in(username, password)
    print(txt)
    if txt == "Successfully Signed In!":
        info_label.color=(1,1,1)
        info_label.text = txt
    elif txt == "Invalid username":
        info_label.text = "This Username doesn't exist. Please try again."
    elif txt == "Invalid password":
        info_label.text = f"{txt}! You have {3-user1.get_sign_in_attempts()} attempts left"
    elif txt == "Too many attempts with invalid credentials":
        print("attemps")
        info_label.text = "Too many attempts with invalid credentials. Please try again in 30 seconds."
        sign_in_btn.disabled = True
        for i in range(6):
            info_label.text = f"Too many attempts with invalid credentials. Please try again in {30 - 5 * i} seconds."
            time.sleep(5)
        sign_in_btn.disabled = False
    else:
        info_label.text = "An Unknown Error Occured."


def display_agbs(content):
    text = (
        """
Update: 14.04.2025

Terms and Conditions

1. Introduction
These Terms and Conditions ("Terms") govern your use of our website, application, products, and services. By accessing or using any part of our services, you agree to be bound by these Terms.

2. Services Provided
We offer a vocabulary trainer named VocVault for students. We reserve the right to modify or discontinue the services at any time without prior notice.

3. User Responsibilities
You agree to use our services only for lawful purposes and in accordance with these Terms. You must not misuse our services or attempt to access them using unauthorized methods.

4. Intellectual Property
All content provided on our website and services, including text, graphics, logos, and software, is the property of Mika Wilhelm and is protected by intellectual property laws.

5. Payments and Pricing
All prices are listed in Euro and are subject to change without notice. Payment must be made in full before access to any paid features or products is granted.

6. Limitation of Liability
To the maximum extent permitted by law, Mika Wilhelm shall not be liable for any indirect, incidental, or consequential damages arising out of or in connection with your use of our services.

7. Termination
We reserve the right to suspend or terminate your access to our services at any time, without notice, for conduct that we believe violates these Terms.

8. Governing Law
These Terms shall be governed by and construed in accordance with the laws of Germany. Any disputes shall be resolved in the courts of Germany.

9. Changes to the Terms
We may revise these Terms from time to time. The updated Terms will be posted on our website with the effective date. Continued use of our services constitutes acceptance of the changes.

10. Contact Information
If you have any questions about these Terms, please contact us at:
Mika Wilhelm
mika.wilhelm@krs.hanau.schule
"""
    )
    label = Label(
        text=text,
        size_hint_y=None,
        halign='left',
        valign='top',
        color=(1, 1, 1, 1)
    )

    def update_label_size(*args):
        label.text_size = (label.width, None)
        label.height = label.texture_size[1]

    label.bind(width=update_label_size)
    Clock.schedule_once(update_label_size, 0)  # wartet bis width gesetzt ist

    content.add_widget(label)


def display_impressum(content):
    text = (
                """
Impressum (Legal Disclosure for a Private Individual)

Information in accordance with § 5 TMG:

Name:
Mika Wilhelm

Address:
An der Landwehr 5, 61130 Nidderau, Germany

Contact:
Email: mika.wilhelm@krs.hanau.schule

Responsible for content according to § 55 Abs. 2 RStV:
Mika Wilhelm
An der Landwehr 5, 61130 Nidderau, Germany
                """
            )
    label = Label(
        text=text,
        size_hint_y=None,
        halign='left',
        valign='top',
        color=(1, 1, 1, 1)
    )

    def update_label_size(*args):
        label.text_size = (label.width, None)
        label.height = label.texture_size[1]

    label.bind(width=update_label_size)
    Clock.schedule_once(update_label_size, 0)  # wartet bis width gesetzt ist

    content.add_widget(label)


def display_functions(content):
    text = (
        """From Now on, this application is just for testing purposes.
        Thats why it is just possible to read the Introduction, AGBs and Impressum!
        """
    )
    label = Label(
        text=text,
        size_hint_y=None,
        halign='left',
        valign='top',
        color=(1, 1, 1, 1)
    )

    def update_label_size(*args):
        label.text_size = (label.width, None)
        label.height = label.texture_size[1]

    label.bind(width=update_label_size)
    Clock.schedule_once(update_label_size, 0)  # wartet bis width gesetzt ist

    content.add_widget(label)


def display_sign_in(content):
    User1 = UserAdministrationGui.User()
    row1 = BoxLayout(orientation='horizontal', spacing=40)
    row1.add_widget(Label(text='Username:', size_hint_x=0.3, size_hint_y=None, height=40, halign='center'))
    username=TextInput(size_hint_y=None, height=40, halign='center', hint_text='Username')
    row1.add_widget(username)

    # Zeile 2: E-Mail
    row2 = BoxLayout(orientation='horizontal', spacing=40)
    row2.add_widget(Label(text='Password:', size_hint_x=0.3, size_hint_y=None, height=40, halign='center'))
    password = TextInput(password=True, size_hint_y=None, height=40, halign='center', hint_text='Password')
    row2.add_widget(password)
    info_label = Label(color=(1, 0, 0, 1))
    sign_in_btn = Button(text="Sign In", size_hint_y=None, height=60, background_color=(1, 0, 0, 1), on_release=lambda instance: try_sign_in(username.text, password.text, info_label, User1, sign_in_btn))
    content.add_widget(row1)
    content.add_widget(row2)
    content.add_widget(info_label)
    content.add_widget(sign_in_btn)
def display_sign_up(content):
    print(1)


def display_home(content):
    text = (
        "Welcome to VocVault!\n\nVocVault is a vocabulary trainer thoughtfully developed by a student "
        "to encompass all the essential features of an effective language learning tool.\n\n"
        "If you already have an account, please select Sign In from the dropdown menu. "
        "Otherwise, click Sign Up to create a new account.\n\n"
        "Thank you for choosing VocVault!\n\n"
        "Your Developer"
    )
    label = Label(
        text=text,
        size_hint_y=None,
        halign='left',
        valign='top',
        color=(1, 1, 1, 1)
    )

    def update_label_size(*args):
        label.text_size = (label.width, None)
        label.height = label.texture_size[1]

    label.bind(width=update_label_size)
    Clock.schedule_once(update_label_size, 0)  # wartet bis width gesetzt ist

    content.add_widget(label)


class Header(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_button = None
        self.dropdown = None
        Clock.schedule_once(self.post_init)

    def post_init(self, dt):
        self.dropdown = DropDown(auto_width=False)  # WICHTIG: auto_width=False
        options = ['Home', 'Sign in', 'Sign up', 'Functions', 'AGBs', 'Impressum']
        for option in options:
            btn = Button(
                text=option,
                size_hint_y=None,
                height=40,
                size_hint_x=None,
                width=150,
                background_color=(0.5, 0.5, 0.5)  # Ein mittleres Grau
            )
            btn.bind(on_release=lambda btn=btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.main_button = self.ids.menu_button
        self.main_button.bind(on_release=self.open_dropdown)
        self.dropdown.bind(on_select=self.on_select)

    def open_dropdown(self, instance):
        # Hier setzen wir die gewünschte Breite des Dropdowns
        self.dropdown.width = 150
        self.dropdown.open(instance)

    def on_select(self, instance, value):
        self.ids.screen_name.text = f"{value}"
        app = App.get_running_app()
        root = app.root
        content = root.ids.content_box
        content.clear_widgets()  # Alles entfernen
        if value == 'Home':
            display_home(content)
        elif value == 'Sign in':
            display_sign_in(content)
        elif value == 'Sign up':
            display_sign_up(content)
        elif value == 'Functions':
            display_functions(content)
        elif value == 'AGBs':
            display_agbs(content)
        elif value == 'Impressum':
            display_impressum(content)


class VocVaultApp(App):
    def get_application_icon(self):
        return r'img/icon.png'

    def build(self):
        return Builder.load_file("main.kv")


if __name__ == '__main__':
    VocVaultApp().run()
