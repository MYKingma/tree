from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from functools import wraps
import datetime


db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Text(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    paid = db.Column(db.Boolean(), nullable=False)

    def __init__(self, firstname, lastname, order, amount):
        self.firstname = firstname
        self.lastname = lastname
        self.order = orders
        self.amount = amount
        self.paid = False

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def get_user_roles(self):
        roles = []
        for role in self.roles:
            roles.append(role.name)
        return roles

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)

class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime)
    title = db.Column(db.String(128))
    short = db.Column(db.Text())
    body = db.Column(db.Text())

    def __init__(self):
        self.date = datetime.datetime.now()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(128))
    short = db.Column(db.Text())
    body = db.Column(db.Text())

    def __init__(self):
        self.date = datetime.datetime.now()

class AdminView(ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                if role.name == 'Administrator':
                    return True
            return False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('index'))
