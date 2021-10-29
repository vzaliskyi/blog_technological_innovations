from flask import Blueprint

blog_bp = Blueprint('blog_bp_in', __name__, template_folder="templates/blog")

from . import view