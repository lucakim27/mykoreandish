from flask import Blueprint, g, request
from backend.utils.login import login_required
from ...services.managers import nutrient_manager

nutrients_bp = Blueprint('nutrients', __name__, url_prefix='/api/nutrients')

@nutrients_bp.route('/', methods=['GET'])
def get_all_nutrients():
    all_nutrients = nutrient_manager.get_all_nutrients()
    return all_nutrients, 200

@nutrients_bp.route('/<ingredient_name>', methods=['GET'])
def get_ingredient_nutrients(ingredient_name):
    nutrients = nutrient_manager.get_ingredient_nutrients(ingredient_name)
    return nutrients, 200

@nutrients_bp.route('/', methods=['PUT'])
@login_required
def update_nutrient_review():
    history_id = request.get_json()['history_id']
    nutrient = request.get_json()['nutrient']
    nutrient_manager.update_nutrient_review(history_id, nutrient)
    return '', 204

@nutrients_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_nutrient_review(id):
    nutrient_manager.delete_nutrient(id)
    return '', 204

@nutrients_bp.route('/<ingredient_name>', methods=['POST'])
@login_required
def add_nutrient_review(ingredient_name):
    user_id = g.user['google_id']
    nutrient = request.get_json()['nutrient']
    nutrient_manager.add_nutrient_review(ingredient_name, user_id, nutrient)
    return '', 204