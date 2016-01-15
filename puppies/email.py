from puppies import app
from flask_mail import Message,Mail


mail = Mail(app)

def send_email(recipient,message):
    msg = Message(message, recipients=[recipient])
    mail.send(msg)