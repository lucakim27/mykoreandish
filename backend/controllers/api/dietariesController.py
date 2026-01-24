from backend.utils.login import login_required
from flask import Blueprint, g, request
from ...services.managers import dietary_manager, aggregate_manager

dietaries_bp = Blueprint('dietaries', __name__, url_prefix='/api/dietaries')

@dietaries_bp.route('/', methods=['GET'])
def get_all_dietaries():
    dietaries = dietary_manager.get_all_dietaries()
    return dietaries, 200

@dietaries_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_dietary_review(id):
    old_dietary, dietary = dietary_manager.get_dietary_review_by_id(id)
    dietary_manager.delete_dietary(id)
    aggregate_manager.delete_dietary_aggregate(old_dietary, dietary)
    return '', 204

@dietaries_bp.route('/', methods=['PUT'])
@login_required
def update_dietary_review():
    history_id = request.get_json()['history_id']
    new_dietary = request.get_json()['dietary']
    old_dietary, dietary  = dietary_manager.get_dietary_review_by_id(history_id)
    aggregate_manager.update_dietary_aggregate(old_dietary, dietary, new_dietary)
    dietary_manager.update_dietary(history_id, new_dietary)
    return '', 204

@dietaries_bp.route('/<dish_name>', methods=['POST'])
@login_required
def add_dietary_review(dish_name):
    user_id = g.user['google_id']
    dietary = request.get_json()['dietary']
    dietary_manager.add_dietary_review(dish_name, user_id, dietary)
    aggregate_manager.add_dietary_aggregate(dish_name, dietary)
    return '', 204