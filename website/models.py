from email.policy import default
from time import timezone
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
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    nif = db.Column(db.Integer, default=0)
    address = db.Column(db.String(200), default='')
    phone = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_type = db.Column(db.String(20), default = 'user')
    # cart = db.relationship('Cart')

