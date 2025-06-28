from flask import Blueprint, render_template, session
from config.db import db
from models.userModel import UserManager

footer_bp = Blueprint('footer', __name__)
user_manager = UserManager(db)

@footer_bp.route('/aboutus')
def aboutusController():
    user = user_manager.get_user_by_session(session)
    return render_template('aboutus.html', user=user)

@footer_bp.route('/privacy')
def privacyController():
    user = user_manager.get_user_by_session(session)
    return render_template('privacy.html', user=user)

@footer_bp.route('/terms')
def termsController():
    user = user_manager.get_user_by_session(session)
    return render_template('terms.html', user=user)

@footer_bp.route('/faq')
def faqController():
    user = user_manager.get_user_by_session(session)
    return render_template('faq.html', user=user)