from flask_sqlalchemy import SQLAlchemy

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
