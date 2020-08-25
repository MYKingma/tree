# config.py for implementing a tree-buy webapp
#
# Maurice Kingma
#
#
# python program for  the configuration of tree.mauricekingma.nl

from flask import Flask
import os
from flask_migrate import Migrate
from models import *


app = Flask(__name__)


# configure Secret-Key
app.secret_key = os.getenv('SECRET_KEY')

# configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# configure migrations
Migrate(app, db, compare_type=True, render_as_batch=True)
