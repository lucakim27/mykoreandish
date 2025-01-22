from flask import Blueprint, render_template, session
from config.db import db
from models.userModel import UserManager

aboutus_bp = Blueprint('aboutus', __name__)
user_manager = UserManager(db)

@aboutus_bp.route('/')
def aboutusController():
    user = user_manager.get_user_by_session(session)
    return render_template('aboutus.html', user=user)