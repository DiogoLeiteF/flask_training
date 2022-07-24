from flask import Blueprint, flash, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import User, Product
from . import db
import json
from sqlalchemy import update, text


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    products = Product.query.all()

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
    return render_template('home.html', user=current_user, products=products)


@views.route('/user')
def user():
    return render_template('user.html', user=current_user)


@views.route('/supplier')
def supplier():
    return render_template('supplier.html', user=current_user)


@views.route('/admin')
def admin():
    users = User.query.all()
    products = Product.query.all()
    return render_template('admin.html', user=current_user, users=users, products=products)


@views.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('/cart.html', user=current_user)


@views.route('/delete-user/<id>')
def delete_user(id):
    user = User.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('views.admin'))


@views.route('/make/<type>/<id>')
# @login_required
def make_supplier(type, id):
    user = User.query.filter_by(id=int(id)).first()
    if type == 'user':
        user.user_type = 'user'
    elif type == 'supplier':
        user.user_type = 'supplier'
    elif type == 'admin':
        user.user_type = 'admin'
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('views.admin'))


@views.route('/admin/add-product', methods=['GET', 'POST'])
# @login_required
def add_prod():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        supplier = request.form.get('supplier')
        supplier_price = request.form.get('supplier_price')
        retail_price = request.form.get('retail_price')
        warehouse_location = request.form.get('warehouse_location')
        stock = request.form.get('stock')
        stock_prev = request.form.get('stock_prev')

        new_product = Product(name=name, description=description, supplier=supplier, supplier_price=supplier_price,
                              retail_price=retail_price, warehouse_location=warehouse_location, stock=stock, stock_prev=stock_prev)
        db.session.add(new_product)
        db.session.commit()

        flash('Product created!', category='success')
        return redirect(url_for('views.admin'))

    return render_template('sign_up.html', user=current_user)


########################################
#            NOT IN USE                #
########################################


@views.route('/delete-note/<id>')
def delete_note(id):
    note = Note.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('views.home'))
