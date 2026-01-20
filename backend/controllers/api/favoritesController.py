from flask import Blueprint
from ...services.managers import favorite_manager
from ...utils.login import login_required

favorites_bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')

@favorites_bp.route('/<user_id>', methods=['GET'])
def get_favorite_dishes(user_id):
    favorite_dishes = favorite_manager.get_all_favorites(user_id)
    return favorite_dishes, 200

@favorites_bp.route('/<name>/<user_id>', methods=['GET'])
def is_favorite(name, user_id):
    is_favorite = favorite_manager.is_favorite(name, user_id)
    return is_favorite, 200

@favorites_bp.route('/<name>/<user_id>', methods=['POST'])
@login_required
def add_favorite(name, user_id):
    favorite_manager.add_favorite(name, user_id)
    return '', 204

@favorites_bp.route('/<name>/<user_id>', methods=['DELETE'])
@login_required
def delete_favorite(name, user_id):
    favorite_manager.delete_favorite(name, user_id)
    return '', 204