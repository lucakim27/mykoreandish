from flask import Blueprint, request, redirect
from backend.utils.login import login_required
from ...services.managers import ingredient_manager, aggregate_manager, nutrient_manager

ingredients_bp = Blueprint('ingredients', __name__, url_prefix='/api/ingredients')

@ingredients_bp.route('/get_all_ingredients', methods=['GET'])
def get_all_ingredients():
    return ingredient_manager.get_all_ingredients()

@ingredients_bp.route('/get_top_ingredients', methods=['GET'])
def get_top_ingredients():
    return aggregate_manager.get_top_ingredients()

@ingredients_bp.route('/get_ingredient_instance/<ingredient_name>', methods=['GET'])
def get_ingredient_instance(ingredient_name):
    return ingredient_manager.get_ingredient_instance(ingredient_name)

@ingredients_bp.route('/add_nutrient_review/<ingredient_name>/<user_id>', methods=['POST'])
@login_required
def add_nutrient_review(ingredient_name, user_id):
    nutrient = request.form.get('nutrient')
    nutrient_manager.add_nutrient_review(ingredient_name, user_id, nutrient)
    return redirect('/ingredients/' + ingredient_name)

@ingredients_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_ingredient_review(id):
    ingredient = ingredient_manager.get_ingredient_review_by_id(id)
    ingredient_manager.delete_ingredient(id)
    aggregate_manager.delete_ingredient_aggregate(ingredient)
    return '', 204