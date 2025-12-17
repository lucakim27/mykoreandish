from flask import Blueprint, redirect, url_for, session
from flask_dance.contrib.google import google
from ..services.managers import user_manager

auth_bp = Blueprint('auth_bp', __name__)

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