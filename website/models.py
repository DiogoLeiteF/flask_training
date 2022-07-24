from email.policy import default
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    nif = db.Column(db.Integer, default=000000000)
    address = db.Column(db.String(200), default='missing info')
    phone = db.Column(db.Integer, default=000000000)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_type = db.Column(db.String(20), default='user')
    # cart = db.relationship('Cart')


class Product(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(
        db.String(200), default='some sort of product description')
    supplier = db.Column(db.String(150), default='supplier')
    supplier_price = db.Column(db.REAL, default=00.00)
    retail_price = db.Column(db.REAL, default=00.00)
    warehouse_location = db.Column(
        db.String(150), default='far away from thieves')
    stock = db.Column(db.Integer, default=0)
    stock_prev = db.Column(db.Integer, default=100)
    sold = db.Column(db.Integer, default=0)
