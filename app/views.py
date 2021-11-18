from app import app
from app.user.models import User, Comment, Like, Post
from flask import render_template


@app.route('/')
def home():
    print("all_posts")
    # posts = Post.query.order_by().desc()
    posts = Post.query.order_by(Post.created_at.desc())
    # posts = Post.query.all()
    return render_template('home.html', title='TechBlog', posts=posts)
