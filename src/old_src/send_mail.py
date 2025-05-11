import os
import yagmail
from dotenv import load_dotenv

def send_mail(adress: str, subject: str, content: str, console_message: str)->None:
    load_dotenv()
    sender_email = os.getenv("MAIL_SENDER_EMAIL")
    password = os.getenv("MAIL_PASSWORD")
    yag = yagmail.SMTP(sender_email, password)
    yag.send(adress, subject, content)
    print(console_message)
