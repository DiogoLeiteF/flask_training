from flask import Blueprint, flash, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note
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
    return render_template('admin.html', user=current_user)


@views.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('/cart.html', user=current_user)


@views.route('/delete-note/<id>')
def delete_note(id):
    note = Note.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('views.home'))
