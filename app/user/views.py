from .models import User
from . import user_bp
from app import db
from .forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_in_db = User.query.filter(User.username == username).first()
        if user_in_db and user_in_db.veryfy_password(password):
            login_user(user_in_db)
            flash('Ви успішно ввійшли!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Неправильні дані!', category='danger')
    return render_template('login.html', form=form, title='Login')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Account cereated for {form.username.data}!',
                  category='success')
        except:
            db.session.rollback()
            flash('Error adding data in DB!', 'danger')
        return redirect(url_for('user_bp_in.login'))
    return render_template('register.html', form=form, title='Register')

@user_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли зі свого акаунту!', 'info')
    return redirect(url_for("home"))