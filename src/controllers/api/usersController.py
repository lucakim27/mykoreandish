from flask import Blueprint, g, redirect, request
from ...services.managers import user_manager

users_api_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_api_bp.route('/me', methods=['GET'])
def get_current_user():
    return {"user": g.user}

@users_api_bp.route('/get_total_users', methods=['GET'])
def get_user_count():
    return {"total_users": user_manager.get_total_users()}

@users_api_bp.route('/get_all_users', methods=['GET'])
def get_all_users():
    return {"users": user_manager.get_all_users()}

@users_api_bp.route('/get_user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = user_manager.get_user_by_id(user_id)
    return {"user": user}

@users_api_bp.route('/update_dietary_preference/<user_id>', methods=['POST'])
def update_dietary_preference(user_id):
    dietary_preference = request.form.get('dietary_preference')
    user_manager.update_dietary_preference(user_id, dietary_preference)
    return redirect('/users/profile')