from flask import Blueprint, g, render_template

footer_bp = Blueprint('footer', __name__)

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