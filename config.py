# config.py for implementing a tree-buy webapp
#
# Maurice Kingma
#
#
# python program for  the configuration of tree.mauricekingma.nl

from flask import Flask
import os
from flask_migrate import Migrate
from flask_mail import Mail, Message
import rq
from models import *


app = Flask(__name__)


# configure Secret-Key
app.secret_key = os.getenv('SECRET_KEY')

# configure sessions
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = 'Lax'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# configure Flask-Mail
app.config['MAIL_SERVER']='smtp.mail.me.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = "mauricekingma@me.com"
mail = Mail(app)

# configure migrations
Migrate(app, db, compare_type=True, render_as_batch=True)

if os.getenv("PRODUCTION_SERVER") == "True":
    # set session cookie secure
    app.config["SESSION_COOKIE_SECURE"] = True

    # import worker
    from runworker import conn

    # set worker Queue
    queue = rq.Queue('default', connection=conn)
