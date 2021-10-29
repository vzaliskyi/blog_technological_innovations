from . import blog_bp


@blog_bp.route('/blog')
def home():
    return 'Hello from blog bp'