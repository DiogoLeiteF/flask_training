from turtle import update
from flask import Blueprint, flash, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is to short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('home.html', user=current_user)


@views.route('/user')
def user():
    return render_template('user.html', user=current_user)


@views.route('/supplier')
def supplier():
    return render_template('supplier.html', user=current_user)


@views.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', user=current_user, users=users)


@views.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('/cart.html', user=current_user)


@views.route('/delete-user/<id>')
def delete_user(id):
    user = User.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('views.admin'))


# not working

@views.route('/make-admin/<id>')
def make_admin(id):
    user = User.query.filter_by(id=int(id))
    
    setattr(user, 'user_type', 'admin')
    db.session.commit()

#     user_update = (
#         update(user).where(user.id == id_)
#         values(user_type='admin'))
    return redirect(url_for('views.admin'))


@views.route('/delete-note/<id>')
def delete_note(id):
    note = Note.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('views.home'))
