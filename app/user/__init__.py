from flask import Blueprint # pylint: disable=import

user_bp = Blueprint('user_bp_in', __name__, template_folder="templates/user")

from . import view # pylint: disable=import
