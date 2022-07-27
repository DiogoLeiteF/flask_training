from flask import Blueprint, flash, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import User, Product, Sale
from . import db
import json
from sqlalchemy import update, text
import ast


admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def admin_():
    users = User.query.all()
    products = Product.query.all()
    sales = Sale.query.all()
    return render_template('admin.html', user=current_user, users=users, products=products, sales=sales)


################################################
# Users
###############################################


@admin.route('/admin-users-management')
@login_required
def users_management():
    users = User.query.all()
    return render_template('admin-users-management.html', user=current_user, users=users)


@admin.route('/admin/user-search', methods=['GET', 'POST'])
@login_required
def user_search():
    if request.method == "POST":
        users = User.query.all()
        search = request.form.get('search')
        users_list = []

        for usr in users:
            if search in usr.first_name or search in usr.last_name or search == str(usr.id) or search in usr.email or search == str(usr.nif) or search == str(usr.phone) or search in usr.user_type:
                users_list.append(usr)
                print(users_list)
        if users_list == []:
            flash('User NOT found, try again', category='error')

    return render_template('admin-users-management.html', users=users, user=current_user, users_search=users_list)


@admin.route('/delete-user/<id>')
@login_required
def delete_user(id):
    user = User.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('admin.users_management'))


@admin.route('/change-type/<id>')
@login_required
def change_type(id):
    user = User.query.filter_by(id=int(id)).first()
    if user.user_type == 'user':
        user.user_type = 'supplier'
        flash('User Type Changed to SUPPLIER', category='success')
    elif user.user_type == 'supplier':
        user.user_type = 'admin'
        flash('User Type Changed to ADMIN', category='success')
    elif user.user_type == 'admin':
        user.user_type = 'user'
        flash('User Type Changed to USER', category='success')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users_management'))


################################################
# Products
###############################################


@admin.route('/admin-products-management')
@login_required
def products_management():
    users = User.query.all()
    products = Product.query.all()
    sales = Sale.query.all()
    return render_template('admin-products-management.html', user=current_user, users=users, products=products, sales=sales)


@admin.route('/delete-product/<id>')
@login_required
def delete_product(id):
    product = Product.query.filter_by(prod_id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('admin.products_management'))


@admin.route('/products-management/add-product', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('admin.products_management'))

    return render_template('sign_up.html', user=current_user)



#######################################
######################################
# NOT WORKING
########################################
########################################


@admin.route('/products-management/update-product', methods=['GET', 'POST'])
@login_required
def update_prod():
    if request.method == "POST":
        id = request.form.get('prod_id')
        name = request.form.get('name')
        description = request.form.get('description')
        supplier = request.form.get('supplier')
        supplier_price = request.form.get('supplier_price')
        retail_price = request.form.get('retail_price')
        warehouse_location = request.form.get('warehouse_location')
        stock = request.form.get('stock')
        stock_prev = request.form.get('stock_prev')

        print(type(id))
        print(type(name))

        update_product = Product.query.filter_by(prod_id=id).first()
        
        if name:
            update_product.name = name
            
        if description:
            update_product.description = description

        if supplier:
            update_product.supplier = supplier

        if supplier_price:
            update_product.supplier_price = supplier_price

        if retail_price:
            update_product.retail_price = retail_price

        if warehouse_location:
            update_product.warehouse_location = warehouse_location
            
        if stock:
            update_product.stock = stock

        if stock_prev:
            update_product.stock_prev = stock_prev

        db.session.add(update_product)
        db.session.commit()

        flash('Product updated!', category='success')
        return redirect(url_for('admin.products_management'))

    return render_template('sign_up.html', user=current_user)


################################################
# Sales
###############################################


@admin.route('/admin-sales-management')
@login_required
def sales_management():
    users = User.query.all()
    products = Product.query.all()
    sales = Sale.query.all()
    return render_template('admin-sales-management.html', user=current_user, users=users, products=products, sales=sales)
