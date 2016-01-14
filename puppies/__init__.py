from flask import Flask
app = Flask(__name__)

from config import configure_app
from puppies import views, views_adopters, views_login, views_puppies, views_shelters

from flask_mail import Mail
mail = Mail(app)

configure_app(app)

app.config.from_pyfile('config.py')