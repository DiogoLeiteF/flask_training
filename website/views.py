from flask import Blueprint, flash, redirect, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from website.dummy_data import add_dummy_data
from .models import Sale_prod_list, User, Product, Sale
from . import db
from sqlalchemy import update, text
import ast
import matplotlib.pyplot as plt


views = Blueprint('views', __name__)


###########################
# home
###########################

@views.route('/', methods=['GET', 'POST'])
def home():
    products = Product.query.all()

    # add dummy data to db
    if len(products) < 1:
        add_dummy_data(db=db, User=User, Sale=Sale, Product=Product)

    if current_user.is_authenticated:
        cart = ast.literal_eval(current_user.cart)
        cart_len = 0
        for value in cart.values():
            cart_len += value
        session["cart"] = cart_len
    else:
        session["cart"] = 0

    return render_template('home.html', user=current_user, products=products, cart_session=session["cart"])


@views.route('/add-to-cart/<user_id>/<prod_id>')
@login_required
def add_to_cart(user_id, prod_id):
    prod = Product.query.filter_by(prod_id=int(prod_id)).first()
    user = User.query.filter_by(id=int(user_id)).first()

    cart_dic = ast.literal_eval(user.cart)
    if prod.prod_id not in cart_dic:
        cart_dic[prod.prod_id] = 1
    else:
        cart_dic[prod.prod_id] += 1

    user.cart = str(cart_dic)

    db.session.add(user)
    db.session.commit()
    flash(f'{prod.name} added to cart')
    return redirect(url_for('views.home', ))


###########################
# User
###########################


@views.route('/user/<stat>')
@login_required
def user(stat='all'):
    products = Product.query.all()
    sales = Sale.query.filter_by(user_id=current_user.id).all()

    if stat == 'all':
        sales = Sale.query.filter_by(user_id=current_user.id).all()
    elif stat == 'awaits-payment':
        sales = Sale.query.filter_by(
            user_id=current_user.id, status='Awaits Payment').all()
    elif stat == 'awaits-material':
        sales = Sale.query.filter_by(
            user_id=current_user.id, status='Awaits Material').all()
    elif stat == 'preparation':
        sales = Sale.query.filter_by(
            user_id=current_user.id, status='Preparation').all()
    elif stat == 'sent':
        sales = Sale.query.filter_by(
            user_id=current_user.id, status='Sent').all()
    elif stat == 'done':
        sales = Sale.query.filter_by(
            user_id=current_user.id, status='Done').all()

    return render_template('user.html', user=current_user, sales=sales, cart_session=session["cart"], products=products)


@views.route('/user/all/update-data', methods=['GET', 'POST'])
@login_required
def update_user():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        nif = request.form.get('nif')
        address = request.form.get('address')
        phone = request.form.get('phone')

        update_user = User.query.filter_by(id=current_user.id).first()

        if first_name:
            update_user.first_name = first_name
        if last_name:
            update_user.last_name = last_name
        if nif:
            update_user.nif = nif
        if address:
            update_user.address = address
        if phone:
            update_user.phone = phone

        db.session.add(update_user)
        db.session.commit()
        flash('User updated successfully', category='success')
        return redirect(url_for('views.user', stat='all'))


###########################
# Supplier
###########################

@views.route('/supplier')
@login_required
def supplier():
    products = Product.query.filter_by(supplier=current_user.first_name).all()

    return render_template('supplier.html', user=current_user, cart_session=session["cart"], products=products)


###########################
# Cart
###########################

@views.route('/cart/<id>', methods=['GET', 'POST'])
@login_required
def cart(id):
    products = Product.query.all()
    user = User.query.filter_by(id=int(id)).first()
    cart = ast.literal_eval(user.cart)
    total = 0
    for key, value in cart.items():
        for product in products:
            if product.prod_id == key:
                total += product.retail_price * value

    if request.method == 'POST':
        if user.cart != '{}':
            # get info from order
            note = request.form.get('delivery-note')
            payment_method = request.form.get('payment_method')

            # create new sale object
            new_sale = Sale(delivery_notes=note,
                            user_id=current_user.id, material=current_user. cart,
                            profit=0,
                            total_value=0,
                            payment_method=payment_method)

            # Update values in new sale
            for prod, quant in cart.items():
                for product in products:
                    if product.prod_id == prod:
                        product.stock -= quant
                        product.sold += quant
                        new_sale.total_value += product.retail_price * quant
                        new_sale.profit += product.retail_price * \
                            quant - product.supplier_price * quant

            db.session.add(new_sale)
            db.session.commit()
            # print(new_sale.sale_id)
            for prod, quant in cart.items():
                for x in range(quant):
                    new_sale_prod = Sale_prod_list(sale_id=new_sale.sale_id,
                                                   user_id=user.id, product_id=prod)
                    db.session.add(new_sale_prod)
                    db.session.commit()

            user.cart = '{}'

            db.session.commit()
            flash('Your order has been created', category='success')
            return redirect(url_for('views.payment', id=new_sale.sale_id))
        else:
            flash('Your cart is empty!', category='error')
            return redirect(url_for('views.home'))

    return render_template('/cart.html', user=current_user, products=products, cart=cart, total=total, cart_session=session["cart"])


@views.route('/cart/remove/<prod_id>/<id>')
@login_required
def cart_rm(prod_id, id):
    user = User.query.filter_by(id=int(id)).first()
    product = Product.query.filter_by(prod_id=int(prod_id)).first()

    cart_dic = ast.literal_eval(user.cart)

    cart_dic[product.prod_id] -= 1
    if cart_dic[product.prod_id] == 0:
        del cart_dic[product.prod_id]

    user.cart = str(cart_dic)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('views.cart', id=user.id))


@views.route('/cart/add/<prod_id>/<id>')
@login_required
def cart_add(prod_id, id):
    user = User.query.filter_by(id=int(id)).first()
    product = Product.query.filter_by(prod_id=int(prod_id)).first()

    cart_dic = ast.literal_eval(user.cart)

    cart_dic[product.prod_id] += 1

    user.cart = str(cart_dic)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('views.cart', id=user.id))


@views.route('/cart/delete/<prod_id>/<id>')
@login_required
def cart_del(prod_id, id):
    user = User.query.filter_by(id=int(id)).first()
    product = Product.query.filter_by(prod_id=int(prod_id)).first()

    cart_dic = ast.literal_eval(user.cart)

    del cart_dic[product.prod_id]

    user.cart = str(cart_dic)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('views.cart', id=user.id))


###########################
# Payment
###########################

@views.route('/payment/<id>')
@login_required
def payment(id):

    return render_template('payment.html', id=id, user=current_user, cart_session=session["cart"])
