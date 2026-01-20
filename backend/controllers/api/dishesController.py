from flask import Blueprint
from ...services.managers import dish_manager, aggregate_manager, ingredient_manager

dishes_bp = Blueprint('dishes', __name__, url_prefix='/api/dishes')

@dishes_bp.route('/', methods=['GET'])
def get_all_dishes():
    all_dishes = dish_manager.get_all_dishes()
    return all_dishes, 200

@dishes_bp.route('/top', methods=['GET'])
def get_top_dishes():
    top_dishes = aggregate_manager.get_top_dishes()
    return top_dishes, 200

@dishes_bp.route('/dietary/<dietary>', methods=['GET'])
def get_dishes_by_dietary(dietary):
    dishes_name = aggregate_manager.get_dishes_by_dietary(dietary)
    dishes_instance = dish_manager.get_dishes_instance(dishes_name)
    return dishes_instance, 200

@dishes_bp.route('/ingredient/<ingredient>', methods=['GET'])
def get_dishes_by_ingredient(ingredient):
    dishes_name = aggregate_manager.get_dishes_by_ingredient(ingredient)
    dishes_instance = dish_manager.get_dishes_instance(dishes_name)
    return dishes_instance, 200

@dishes_bp.route('/<aspect>/<value>', methods=['GET'])
def get_dishes_by_aspect(aspect, value):
    dishes_name = aggregate_manager.get_dishes_by_aspect_range(aspect, value)
    dishes_instance = dish_manager.get_dishes_instance(dishes_name)
    return dishes_instance, 200

@dishes_bp.route('/<dish_name>', methods=['GET'])
def get_dish_instance(dish_name):
    dish_instance = dish_manager.get_dish_instance(dish_name)
    return dish_instance, 200

@dishes_bp.route('/aggregates/<dish_name>', methods=['GET'])
def get_dish_aggregate(dish_name):
    aggregate = aggregate_manager.get_dish_aggregate(dish_name)
    return aggregate, 200

@dishes_bp.route('/recommendation/<dish_name>', methods=['GET'])
def get_similar_dishes(dish_name):
    similar_dishes = ingredient_manager.get_similar_dishes(dish_name)
    return similar_dishes, 200