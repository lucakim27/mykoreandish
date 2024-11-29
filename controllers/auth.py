from flask import Blueprint, redirect, url_for, session
from flask_dance.contrib.google import google
from models.users import store_google_user
from config.db import db
from flask_dance.contrib.google import google

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/oauth2/v1/userinfo')
    assert resp.ok, resp.text
    user_info = resp.json()

    store_google_user(db, user_info)
    session['google_id'] = user_info.get('id')

    return redirect(url_for('index'))
