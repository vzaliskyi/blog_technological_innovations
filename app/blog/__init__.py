from flask import Blueprint# pylint: disable=import-error

blog_bp = Blueprint('blog_bp_in', __name__, template_folder="templates/blog")

from . import view# pylint: disable=import-error
