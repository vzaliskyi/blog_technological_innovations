from flask import Blueprint
user_bp = Blueprint('user_bp_in', __name__, template_folder="templates/user")

from . import views  # pylint: enable=unused-import
