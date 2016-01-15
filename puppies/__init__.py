from flask import Flask
app = Flask(__name__)


from puppies import views, views_adopters, views_login, views_puppies, views_shelters

from flask_mail import Mail
mail = Mail(app)

