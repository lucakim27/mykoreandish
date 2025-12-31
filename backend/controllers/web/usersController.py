from flask import Blueprint, render_template
from backend.utils.login import login_required

users_web_bp = Blueprint("users_web", __name__, url_prefix="/users")

@users_web_bp.route('/')
@login_required
def historyPage():
    return render_template('userHistory.html')

@users_web_bp.route('/profile')
@login_required
def profilePage():
    return render_template('profile.html')

@users_web_bp.route('/list', methods=['GET'])
def userListPage():
    return render_template('userList.html')

@users_web_bp.route('/<user_id>', methods=['GET'])
def userProfilePage(user_id):
    return render_template('userProfile.html')
