from flask import Blueprint, flash, redirect, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from website.dummy_data import add_dummy_data
from .models import Sale_prod_list, User, Product, Sale
from . import db
import json
from sqlalchemy import update, text
import ast
import matplotlib.pyplot as plt
import os


views = Blueprint('views', __name__)


###########################
# home
###########################

@views.route('/', methods=['GET', 'POST'])
def home():
    products = Product.query.all()

<<<<<<< HEAD
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

=======
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

>>>>>>> db-change
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

<<<<<<< HEAD
    return render_template('user.html', user=current_user, sales=sales, cart_session=session["cart"])
=======
    print(os.listdir('./website/static/graphs'))
    if len(os.listdir('./website/static/graphs')) > 0:
        for file in os.listdir('./website/static/graphs'):
            os.remove(f'./website/static/graphs/{file}')

    print(os.listdir('./website/static/graphs'))

    # graph 1 value over time
    date = [sale.date_created.date() for sale in sales]
    value = [sale.total_value for sale in sales]
    # for sale in sales:
    #     date.append(sale.date_created.date())
    #     value.append(sale.total_value)
    print(date)
    print(value)
    # plt.title('Value Spent')
    # plt.xlabel('Date')
    plt.ylabel('Value €')
    plt.xticks(rotation=45)
    plt.plot(date, value, color='red')
    plt.tight_layout()
    plt.savefig('./website/static/graphs/user1.png', dpi=300, format='png')

    return render_template('user.html', user=current_user, sales=sales, cart_session=session["cart"], products=products)
>>>>>>> db-change


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
<<<<<<< HEAD
    return render_template('supplier.html', user=current_user, cart_session=session["cart"])
=======
    products = Product.query.filter_by(supplier=current_user.first_name).all()
    sales = Sale.query.all()
>>>>>>> db-change

    # hist sold products
    names = [x.name for x in products]
    quant = [x.sold for x in products]
    plt.title(' Products Sold')
    # # plt.xlabel('Date')
    plt.ylabel('Quantities')
    # plt.xticks(rotation=45)
    plt.bar(names, quant, color='grey')
    plt.tight_layout()
    plt.savefig('./website/static/graphs/supp1.png', dpi=300, format='png')
    plt.close()

    # Sales over time
    time_ = []
    value = 0
    value_list = []
    for sale in sales:
        for prod in sale.prod_list:
            for product in products:
                if prod.product_id == product.prod_id:
                    time_.append(sale.date_created.date())
                    value += product.supplier_price
                    value_list.append(value)

    print(time_)
    print(value)
    print(value_list)
    plt.title('Sales Over Time')
    plt.xticks(rotation=45)
    plt.hist(time_, color='grey')
    plt.tight_layout()
    plt.savefig('./website/static/graphs/supp2.png', dpi=300, format='png')
    plt.close()

    # income over time
    plt.title('Cumulative Income')
    plt.xticks(rotation=45)
    plt.plot(time_, value_list, color='grey')
    plt.tight_layout()
    plt.savefig('./website/static/graphs/supp3.png', dpi=300, format='png')
    plt.close()

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
<<<<<<< HEAD

=======
            # get info from order
>>>>>>> db-change
            note = request.form.get('delivery-note')
            payment_method = request.form.get('payment_method')

            # create new sale object
            new_sale = Sale(delivery_notes=note,
                            user_id=current_user.id, material=current_user. cart,
                            profit=0,
                            total_value=0,
                            payment_method=payment_method)

<<<<<<< HEAD
            print(new_sale.products)

            for product in new_sale.products:
                product.stock -= 1
                product.sold += 1
                new_sale.total_value += product.retail_price
                new_sale.profit += product.retail_price - product.supplier_price
=======
            # Update values in new sale
            for prod, quant in cart.items():
                for product in products:
                    if product.prod_id == prod:
                        product.stock -= quant
                        product.sold += quant
                        new_sale.total_value += product.retail_price * quant
                        new_sale.profit += product.retail_price * \
                            quant - product.supplier_price * quant
>>>>>>> db-change

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
