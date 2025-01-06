from flask import Blueprint, render_template, session
from config.db import db
from models.usersModel import UserManager

terms_bp = Blueprint('terms', __name__)
user_manager = UserManager(db)

@terms_bp.route('/')
def termsController():
    user = user_manager.get_user_by_session(session)
    return render_template('terms.html', user=user)