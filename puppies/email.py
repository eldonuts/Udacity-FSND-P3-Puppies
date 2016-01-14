from puppies import app
from flask_mail import Message,Mail
from config import configure_app

configure_app(app)
mail = Mail(app)

def send_email(recipient,message):
    msg = Message(message, recipients=[recipient])
    mail.send(msg)