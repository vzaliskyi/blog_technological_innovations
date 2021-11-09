from flask import Flask, render_template, url_for, redirect, flash, session
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:#якщо користувач вже увійшов
        return redirect(url_for('/home'))

    form = LoginForm()

    if form.validate_on_submit():#якщо валідація пройшла успішно
        user = User.query.filter_by(user_login=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            
            #переходимо на домашню сторінку
            return redirect(url_for('/home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:#якщо користувач вже увійшов
        return redirect(url_for('/home'))

    form = RegistrationForm()

    if form.validate_on_submit():# якщо валідація пройшла успішно
        # flash(form.username.data + ' ' + form.email.data + ' ' + form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # id
        id_ = db.session.query(User).order_by(User.id.desc()).first().id + 1

        # додаємо користувача до бд
        user = User(id=id_ ,user_login=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # flash('Account created succesfully', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
