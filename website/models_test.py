from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer)
    # check this


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer, default=0)
    # check


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    nif = db.Column(db.Integer)
    address = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    cart = db.relationship('Cart')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(200))
    supplier = db.Column(db.String(150))
    supplier_price = db.Column(db.REAL)
    retail_price = db.Column(db.REAL)
    warehouse_location = db.Column(db.String(150))
    stock = db.Column(db.Integer, default=0)
    stock_prev = db.Column(db.Integer, default=0)
    sold = db.Column(db.Integer, default=0)
    # cart = db.relationship('Cart')
