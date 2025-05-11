# widgets/toast.py
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

def show_toast(message, duration=2):
    popup = Popup(
        title='',
        content=Label(text=message, color=(1, 1, 1, 1)),
        size_hint=(0.6, 0.1),
        auto_dismiss=True,
        separator_height=0,
        background_color=(0, 0, 0, 0.7)
    )
    popup.open()
    Clock.schedule_once(lambda dt: popup.dismiss(), duration)
