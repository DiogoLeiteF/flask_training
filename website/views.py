from flask import Blueprint, flash, redirect, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from website.dummy_data import add_dummy_data
from .models import User, Product, Sale
from . import db
import json
from sqlalchemy import update, text
import ast


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    products = Product.query.all()

    if current_user.is_authenticated:
        cart = ast.literal_eval(current_user.cart)
        cart_len = 0
        for value in cart.values():
            cart_len += value
        session["cart"] = cart_len
    else:
        session["cart"] = 0

    ###################################
    ####     ADD DATA to DB      ######
    ##################################
    
    # add_dummy_data(db=db, User=User, Sale=Sale, Product=Product)

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
    print(user.cart)
    print(len(user.cart))
    return redirect(url_for('views.home', ))


@views.route('/user/<stat>')
@login_required
def user(stat='all'):
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

    return render_template('user.html', user=current_user, sales=sales, cart_session=session["cart"])


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


@views.route('/supplier')
@login_required
def supplier():
    return render_template('supplier.html', user=current_user, cart_session=session["cart"])


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

            note = request.form.get('delivery-note')
            payment_method = request.form.get('payment_method')
            new_sale = Sale(delivery_notes=note,
                            user_id=current_user.id, material=current_user. cart,
                            profit=0,
                            total_value=0,
                            payment_method=payment_method)
            for prod, quant in cart.items():
                for x in range(quant):
                    new_sale.products.append(
                        Product.query.filter_by(prod_id=prod).first())

            print(new_sale.products)

            for product in new_sale.products:
                product.stock -= 1
                product.sold += 1
                new_sale.total_value += product.retail_price
                new_sale.profit += product.retail_price - product.supplier_price

            db.session.add(new_sale)
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


@views.route('/payment/<id>')
@login_required
def payment(id):

    return render_template('payment.html', id=id, user=current_user, cart_session=session["cart"])


########################################
#            NOT IN USE                #
########################################


# @views.route('/delete-note/<id>')
# def delete_note(id):
#     note = Note.query.filter_by(id=int(id)).delete()
#     db.session.commit()

#     return redirect(url_for('views.home'))


# @views.route('/make/<type>/<id>')
# # @login_required
# def make_supplier(type, id):
#     user = User.query.filter_by(id=int(id)).first()
#     if type == 'user':
#         user.user_type = 'user'
#     elif type == 'supplier':
#         user.user_type = 'supplier'
#     elif type == 'admin':
#         user.user_type = 'admin'
#     db.session.add(user)
#     db.session.commit()
#     return redirect(url_for('views.admin'))

    # NOT IN USE
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 1:
    #         flash('Note is to short', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added!', category='success')
