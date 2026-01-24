from flask import Blueprint, g, request
from backend.utils.login import login_required
from ...services.managers import ingredient_manager, aggregate_manager

ingredients_bp = Blueprint('ingredients', __name__, url_prefix='/api/ingredients')

@ingredients_bp.route('/', methods=['GET'])
def get_all_ingredients():
    all_ingredients = ingredient_manager.get_all_ingredients()
    return all_ingredients, 200

@ingredients_bp.route('/top', methods=['GET'])
def get_top_ingredients():
    top_ingredients = aggregate_manager.get_top_ingredients()
    return top_ingredients, 200

@ingredients_bp.route('/<ingredient_name>', methods=['GET'])
def get_ingredient_instance(ingredient_name):
    ingredient_instance = ingredient_manager.get_ingredient_instance(ingredient_name)
    return ingredient_instance, 200

@ingredients_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_ingredient_review(id):
    dish_name, ingredient = ingredient_manager.get_ingredient_review_by_id(id)
    ingredient_manager.delete_ingredient(id)
    aggregate_manager.delete_ingredient_aggregate(dish_name, ingredient)
    return '', 204

@ingredients_bp.route('/', methods=['PUT'])
@login_required
def update_ingredient_review():
    new_ingredient = request.get_json()['ingredient']
    history_id = request.get_json()['history_id']
    dish_name, old_ingredient  = ingredient_manager.get_ingredient_review_by_id(history_id)
    ingredient_manager.update_ingredient_review(history_id, new_ingredient)
    aggregate_manager.update_ingredient_aggregate(dish_name, old_ingredient, new_ingredient)
    return '', 204

@ingredients_bp.route('/<dish_name>', methods=['POST'])
@login_required
def add_ingredient_review(dish_name):
    user_id = g.user['google_id']
    ingredient = request.get_json()['ingredient']
    ingredient_manager.add_ingredient_review(dish_name, user_id, ingredient)
    aggregate_manager.add_ingredient_aggregate(dish_name, ingredient)
    return '', 204