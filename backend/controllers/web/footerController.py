from flask import Blueprint, render_template

footer_bp = Blueprint('footer', __name__)

@footer_bp.route('/aboutus')
def aboutusPage():
    return render_template('aboutus.html')

@footer_bp.route('/privacy')
def privacyPage():
    return render_template('privacy.html')

@footer_bp.route('/terms')
def termsPage():
    return render_template('terms.html')

@footer_bp.route('/faq')
def faqPage():
    return render_template('faq.html')