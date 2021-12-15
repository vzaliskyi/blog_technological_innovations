from app.user.models import Post
from flask import render_template, request, current_app as app
from app.utils import handle_posts_view


@app.route('/')
def home():
    posts, sort_by = handle_posts_view(Post.query, request.args)
    return render_template('home.html', title='TechBlog', posts=posts,
                           sort_by=sort_by)
