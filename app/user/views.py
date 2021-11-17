from .models import User
from app.user.models import Post
from . import user_bp
from app import db, bcrypt, mail
from .forms import (LoginForm, RegistrationForm,
                    RequestPasswordResetForm, ResetPasswordForm)
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


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
    user_img = url_for('static',
                       filename='profile_pictures/' + current_user.picture)
    posts = Post.query.filter_by(user_id=current_user.id)
    return render_template('account.html', user_img=user_img, posts=posts)


def send_reset_token_to_email(user):
    token = user.get_reset_token()
    msg = Message('Запит на скидання паролю',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Щоб скинути пароль, перейдіть за наступним посиланням:
{url_for('user_bp_in.reset_password', token=token, _external=True)}
Якщо ви не подавали запит на зміну паролю - проігноруйте дане повідомлення'''
    mail.send(msg)


@user_bp.route("/reset_password", methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_token_to_email(user)
        flash('Лист з посиланням на відновлення паролю було надіслано на '
              'вашу пошту', 'info')
        return redirect(url_for('user_bp_in.login'))
    return render_template('request_password_reset.html', form=form)


@user_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Посилання на зміну паролю більше не активне', 'warning')
        return redirect(url_for('request_password_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(
            form.new_password.data).decode('utf-8')
        db.session.commit()
        try:
            db.session.commit()
            flash('Ваш пароль оновлено!', 'success')
        except:
            db.session.rollback()
            flash('Трапилась помилка. От халепа!', 'danger')

        return redirect(url_for('user_bp_in.login'))
    return render_template('reset_password.html', form=form)
