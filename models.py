from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from functools import wraps
import datetime
import ast


db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    street = db.Column(db.String(128), nullable=True)
    number = db.Column(db.String(128), nullable=True)
    location = db.Column(db.String(128), nullable=True)
    zipcode = db.Column(db.String(128), nullable=True)
    date = db.Column(db.DateTime())
    paid = db.Column(db.Boolean(), nullable=False)
    sendpayment = db.Column(db.Boolean(), nullable=False)
    items = db.relationship('Item', cascade="all, delete-orphan")

    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.date = datetime.datetime.now()
        self.paid = False
        self.sendpayment = False

    def add_product(self, product, amount):
        item = Item(order_id=self.id, name=product.name, amount=amount, price=product.price)
        db.session.add(item)
        db.session.commit()

    def get_total(self):
        amount = 0.00
        for item in self.items:
            amount = amount + (item.amount * item.price)
        return format(amount, '.2f')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    image = db.Column(db.String(128))
    donation = db.Column(db.Boolean(), nullable=False)
    faqs = db.relationship('FAQ', cascade="all, delete-orphan")
    categories = db.relationship('Category', back_populates="products")

    def __init__(self, name, price, stock, description, image, donation):
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description
        self.image = image
        self.donation = donation

    def get_sold_amount(self):
        amount = 0
        orders = Order.query.all()
        for order in orders:
            for item in order.items:
                if item.name == self.name:
                    amount = amount + item.amount
        return amount

    def get_percentage_sold(self):
        amount = self.get_sold_amount()
        percentage = amount / self.stock
        return percentage

    def get_current_stock(self):
        amount = self.get_sold_amount()
        current_stock = self.stock - amount
        return current_stock

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    products = db.relationship('Product', back_populates="categories")

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    order = db.relationship('Order')

    def get_item_total(self):
        return format(self.amount * self.price, '.2f')

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    website_img = db.Column(db.String(128))
    youtube_link = db.Column(db.String(128))
    youtube_length = db.Column(db.Integer())
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
    date = db.Column(db.DateTime())
    title = db.Column(db.String(128))
    short = db.Column(db.Text())
    body = db.Column(db.Text())
    images = db.Column(db.String(128))

    def __init__(self):
        self.date = datetime.datetime.now()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    title = db.Column(db.String(128))
    short = db.Column(db.Text())
    body = db.Column(db.Text())
    images = db.Column(db.String(128))

    def __init__(self):
        self.date = datetime.datetime.now()

class FAQ(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    question = db.Column(db.Text(), nullable=False)
    answer = db.Column(db.Text(), nullable=False)
    product = db.relationship('Product')

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
