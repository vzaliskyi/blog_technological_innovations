from .models import User
from . import user_bp
from app import db
from .forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter_by(email=form.email.data).first()

        if user_in_db:
            if user_in_db.verify_password(form.password.data):
                login_user(user_in_db, remember=form.remember.data)
                flash(f'Користувач успішно увійшов у свій аккаунт!', 'success')
                next_page = request.args.get('next')
                print('next post', next_page)

                if next_page:
                    return redirect(next_page)
                return redirect(url_for('user_bp_in.account'))
            else:
                flash('Введено невірний пароль.', 'danger')
                return redirect(url_for('user_bp_in.login'))
        else:
            flash('Користувач із вказаним емейлом не зареєстрований на сайті.',
                  'danger')

    return render_template('login.html', form=form, title='Login')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.username.data, form.email.data, form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Користувач {form.username.data} успішно зареєстрований!',
                  'success')
        except:
            db.session.rollback()
            flash('Трапилась помилка під час реєстрації корисутвача, '
                  'спробуйте ще раз.', 'danger')
        return redirect(url_for('user_bp_in.login'))
    return render_template('register.html', form=form, title='Register')


@user_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли зі свого облікового запису', 'info')
    return redirect(url_for("home"))


@user_bp.route("/account")
@login_required
def account():
    return render_template('account.html')
