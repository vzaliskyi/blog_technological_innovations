from . import blog_bp
from .forms import FormPostCreate, FormPostUpdate
from app import db
from .models import Category, Post
from app.user.models import User
from flask import redirect, url_for, flash, request, render_template, abort
from flask_login import current_user, login_required


@blog_bp.route('/post_create', methods=['GET', 'POST'])
@login_required
def post_create():
    form = FormPostCreate.new()
    if form.validate_on_submit():
        category_id = form.category.data
        title = form.title.data
        content = form.content.data
        category = db.session.query(Category.id).filter(
            Category.id == category_id)
        post = Post(category_id=category, user_id=current_user.id, title=title,
                    content=content)
        try:
            db.session.add(post)
            db.session.commit()
            flash('Публікація успішно створена', 'success')
            return redirect(url_for('blog_bp_in.post_view', post_id=post.id))
        except:
            db.session.rollback()
            flash('Помилка при додаванні публікації до бази даних', 'danger')
            return redirect(url_for('blog_bp_in.post_create'))
    # elif request.method == 'POST':
    #     flash(form.errors, 'danger')
    #     return redirect(url_for('blog_bp_in.post_create'))
    return render_template('post_create.html', form=form,
                           title='Створення публікації')


@blog_bp.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def post_update(post_id):
    form = FormPostUpdate.new()
    post = Post.query.get_or_404(post_id)
    if current_user.id == post.user_id:
        if request.method == 'GET':  # якщо ми відкрили сторнку
            # для редагування, записуємо у поля форми значення з БД
            form.category.data = post.category_br.id
            form.title.data = post.title
            form.content.data = post.content
            return render_template('post_update.html',
                                   title='Оновити публікацію', form=form)
        else:  # інакше якщо ми змінили дані і натиснули кнопку
            if form.validate_on_submit():
                category_id = form.category.data
                post.category_id = db.session.query(Category.id).filter(
                    Category.id == category_id)
                post.title = form.title.data
                post.content = form.content.data
                try:
                    db.session.commit()
                    flash('Публікація успішно оновлена', 'info')
                except:
                    db.session.rollback()
                    flash('Помилка при оновленні публікації', 'danger')
                return redirect(url_for('user_bp_in.account'))
            else:
                flash('Помилка валідації', 'danger')
                # url_for('blog_bp_in.post_update', post_id=post_id)
                return redirect(f'/post/{post_id}/update')
    else:
        flash('Ви не маєте прав на редагування даної публікації', 'danger')
        return redirect(url_for('user_bp_in.account'))


@blog_bp.route('/post/<int:post_id>/delete', methods=["GET", "POST"])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id == post.user_id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash('Публікацію успішно видалено!', 'success')
        except:
            flash('Помилка при видаленні публікації', 'danger')
        return redirect(url_for('user_bp_in.account'))
    else:
        flash('Ви не маєте прав на видалення даної публікації', 'danger')
        return redirect(url_for('user_bp_in.account'))


@blog_bp.route('/post_view/<int:post_id>')
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_view.html', post=post)


@blog_bp.route('/user_posts/<int:user_id>')
def user_posts(user_id):
    posts = Post.query.filter_by(user_id=user_id)
    if posts.first() is None:
        abort(404, description="Користувача не знайдено")
    return render_template('user_posts.html', posts=posts)


@blog_bp.route('/category/<int:category_id>')
def posts_by_category(category_id):
    posts = Post.query.filter_by(category_id=category_id)
    if posts.first() is None:
        abort(404, description="Категорію не знайдено")
    return render_template('posts_by_category.html', posts=posts)
