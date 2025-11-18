from flask import Blueprint, g, render_template, session
from config.db import db
from models.userModel import UserManager

footer_bp = Blueprint('footer', __name__)
user_manager = UserManager(db)

@footer_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

@footer_bp.route('/aboutus')
def aboutusController():
    return render_template('aboutus.html', user=g.user)

@footer_bp.route('/privacy')
def privacyController():
    return render_template('privacy.html', user=g.user)

@footer_bp.route('/terms')
def termsController():
    return render_template('terms.html', user=g.user)

@footer_bp.route('/faq')
def faqController():
    return render_template('faq.html', user=g.user)