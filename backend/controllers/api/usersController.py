from flask import Blueprint, g, jsonify, redirect, request
from ...services.managers import user_manager

users_api_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_api_bp.route('/me', methods=['GET'])
def get_current_user():
    if g.user is None:
        return {"error": "Unauthorized"}, 401
    return g.user, 200

@users_api_bp.route('/count', methods=['GET'])
def get_user_count():
    total_users = user_manager.get_total_users()
    return jsonify(total_users), 200

@users_api_bp.route('/', methods=['GET'])
def get_all_users():
    all_users = user_manager.get_all_users()
    return all_users, 200

@users_api_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = user_manager.get_user_by_id(user_id)
    return user, 200

@users_api_bp.route('/<user_id>', methods=['POST'])
def update_dietary_preference(user_id):
    dietary_preference = request.form.get('dietary_preference')
    user_manager.update_dietary_preference(user_id, dietary_preference)
    return redirect('/users/profile')