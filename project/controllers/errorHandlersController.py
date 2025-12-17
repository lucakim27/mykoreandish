from flask import Blueprint, render_template

error_bp = Blueprint('errors', __name__)

@error_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404
