from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Sale_prod_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.ForeignKey('sale.sale_id'))
    user_id = db.Column(db.ForeignKey('user.id'))
    product_id = db.Column(db.ForeignKey('product.prod_id'))



class Sale(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    material = db.Column(db.String(300))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    total_value = db.Column(db.REAL, default=0)
    profit = db.Column(db.REAL, default=0)
    delivery_notes = db.Column(db.String(200))
    payment_method = db.Column(db.String(20))
    status = db.Column(db.String(30), default='Awaits Payment')
    prod_list = db.relationship('Sale_prod_list', backref='sale')

    def __repr__(self):
        return f'sale number: {self.sale_id}'


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
    cart = db.Column(db.String(200), default='{}')
    buys = db.relationship('Sale', backref='user')

    def __repr__(self):
        return f'Name: {self.first_name}'


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
    sales_list = db.relationship('Sale_prod_list', backref='product')

    def __repr__(self):
        return f'{self.name}'
