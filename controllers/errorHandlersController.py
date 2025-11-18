from flask import Blueprint, g, render_template, session
from config.db import db
from models.userModel import UserManager

error_bp = Blueprint('errors', __name__)
user_manager = UserManager(db)

@error_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

@error_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html', user=g.user), 404
