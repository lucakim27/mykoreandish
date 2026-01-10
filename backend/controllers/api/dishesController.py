from flask import Blueprint, redirect, request
from backend.utils.login import login_required
from ...services.managers import dish_manager, aggregate_manager, ingredient_manager, dietary_manager

dishes_bp = Blueprint('dishes', __name__, url_prefix='/api/dishes')

@dishes_bp.route('/get_all_dishes', methods=['GET'])
def get_all_dishes():
    return dish_manager.get_all_dishes_in_dictionary()

@dishes_bp.route('/get_top_dishes', methods=['GET'])
def get_top_dishes():
    return aggregate_manager.get_top_dishes()

@dishes_bp.route('/get_dishes_by_dietary/<dietary>', methods=['GET'])
def get_dishes_by_dietary(dietary):
    dishes_name = aggregate_manager.get_dishes_by_dietary(dietary)
    return dish_manager.get_dishes_instance(dishes_name)

@dishes_bp.route('/get_dishes_by_ingredient/<path:ingredient>', methods=['GET'])
def get_dishes_by_ingredient(ingredient):
    dishes_name = aggregate_manager.get_dishes_by_ingredient(ingredient)
    return dish_manager.get_dishes_instance(dishes_name)

@dishes_bp.route('/get_dishes_by_aspect/<aspect>/<value>', methods=['GET'])
def get_dishes_by_aspect(aspect, value):
    dishes_name = aggregate_manager.get_dishes_by_aspect_range(aspect, value)
    return dish_manager.get_dishes_instance(dishes_name)

@dishes_bp.route('/get_dish_instance/<dish_name>', methods=['GET'])
def get_dish_instance(dish_name):
    return dish_manager.get_dish_instance(dish_name)

@dishes_bp.route('/get_dish_aggregate/<dish_name>', methods=['GET'])
def get_dish_aggregate(dish_name):
    return aggregate_manager.get_dish_aggregate(dish_name)

@dishes_bp.route('/get_similar_dishes/<dish_name>', methods=['GET'])
def get_similar_dishes(dish_name):
    return ingredient_manager.get_similar_dishes(dish_name)

@dishes_bp.route('/get_dish_aggregates/<dish_name>', methods=['GET'])
def get_dish_aggregates(dish_name):
    return aggregate_manager.get_dish_aggregate(dish_name)

@dishes_bp.route('/update_dietary_review', methods=['POST'])
@login_required
def update_dietary_review():
    history_id = request.form.get('history_id')
    new_dietary = request.form.get('dietary')
    dietary_review = dietary_manager.get_dietary_review_by_id(history_id)
    aggregate_manager.update_dietary_aggregate(
        dietary_review.get('dish_name', 0), 
        dietary_review.get('dietary', 0), 
        new_dietary
    )
    dietary_manager.update_dietary(history_id, new_dietary)
    return redirect('/users')