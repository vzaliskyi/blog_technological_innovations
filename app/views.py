from app import app
from app.user.models import User, Comment, Like, Post
from flask import render_template, redirect, url_for, request, flash


@app.route('/')
def home():
    # print("all_posts")
    # posts = Post.query.order_by().desc()
    posts = Post.query.order_by(Post.created_at.desc())
    print('кількість лайків', posts.first().total_likes())
    # posts = Post.query.all()
    return render_template('home.html', title='TechBlog', posts=posts)


# сюди передавати мабуть ще повідомлення про помилку
@app.errorhandler(401)
def unauthorized(e):
    if 'like' in request.path or 'dislike' in request.path:
        flash('Авторизуйтеся або зареєструйтеся, щоб мати можливість оцінювати'
              ' публікації', 'info')
    return redirect(url_for('user_bp_in.login'))
