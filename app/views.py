from app import db
from app.user.models import User, Comment, Like, Post
from flask import render_template, redirect, url_for, request, flash, \
    current_app as app


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    print("page=", page)

    posts = Post.query.order_by(Post.created_at.desc())

    posts = posts.paginate(page=page, per_page=5)

    return render_template('home.html', title='TechBlog', posts=posts)
