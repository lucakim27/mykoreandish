from flask import Blueprint, render_template, session
from config.db import db
from models.userModel import UserManager

privacy_bp = Blueprint('privacy', __name__)
user_manager = UserManager(db)

@privacy_bp.route('/')
def privacyController():
    user = user_manager.get_user_by_session(session)
    return render_template('privacy.html', user=user)