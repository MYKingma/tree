# config.py for implementing a tree-buy webapp
#
# Maurice Kingma
#
#
# python program for  the configuration of tree.mauricekingma.nl


import os
import rq
import logging
import locale
import shutil
import base64
import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from github import Github
from logging.handlers import SMTPHandler
from flask_wtf.csrf import CSRFProtect
from hashlib import blake2b
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from hashlib import blake2b
from models import *


app = Flask(__name__)


# configure Secret-Key
app.secret_key = os.getenv('SECRET_KEY')

# configure ADMINS
app.config['ADMINS'] = os.getenv('ADMINS')

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
app.config['MAIL_SERVER']='smtp.strato.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = "noreply@studio-t-landje.nl"
app.config['SECURITY_PASSWORD_SALT'] = os.getenv("SECURITY_PASSWORD_SALT")
mail = Mail(app)

# configure migrations
Migrate(app, db, compare_type=True, render_as_batch=True)

# configure admin interface tabs
admin = Admin(app, name='Dashboard', index_view=AdminView(User, db.session, url='/admin', endpoint='admin'))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(UserRoles, db.session))
admin.add_view(AdminView(Order, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Item, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Update, db.session))

# set locale to dutch
locale.setlocale(locale.LC_ALL, "nl_NL")

# configure link admin menu
admin.add_link(MenuLink(name='Back to site', url='/dashboard'))

# configure Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# set Flask WTF CSRFProtect
csrf = CSRFProtect(app)

# configure file upload
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
app.config['ALLOWED_EXTENSIONS'] = os.getenv("ALLOWED_EXTENSIONS")

# set up GitHub for file upload
g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
repo = g.get_repo("MYKingma/tree")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# email logged errors
if not app.debug:
    logger = logging.getLogger(__name__)
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_DEFAULT_SENDER'],
            toaddrs=app.config['ADMINS'], subject='Stadsgids error',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.DEBUG)
        logger.addHandler(mail_handler)

if os.getenv("PRODUCTION_SERVER") == "True":
    # set session cookie secure
    app.config["SESSION_COOKIE_SECURE"] = True

    # import worker
    from runworker import conn

    # set worker Queue
    queue = rq.Queue('default', connection=conn)

    # set redirect to https
    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
