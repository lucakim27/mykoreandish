from functools import wraps
from flask import Blueprint, redirect, url_for, session
from flask_dance.contrib.google import google
from models.usersModel import UserManager
from config.db import db
from flask_dance.contrib.google import google

auth_bp = Blueprint('auth_bp', __name__)
user_manager = UserManager(db)

@auth_bp.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/oauth2/v1/userinfo')
    assert resp.ok, resp.text
    user_info = resp.json()

    user_manager.store_google_user(user_info)
    session['google_id'] = user_info.get('id')

    return redirect(url_for('home.home'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'google_id' not in session:
            return redirect(url_for('google.login'))
        return f(*args, **kwargs)
    return decorated_function