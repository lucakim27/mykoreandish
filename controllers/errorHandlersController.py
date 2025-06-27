from flask import Blueprint, render_template, session
from config.db import db
from models.userModel import UserManager

error_bp = Blueprint('errors', __name__)
user_manager = UserManager(db)

@error_bp.app_errorhandler(404)
def page_not_found():
    user = user_manager.get_user_by_session(session)
    return render_template('page_not_found.html', user=user), 404
