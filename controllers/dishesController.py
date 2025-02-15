from flask import Blueprint, render_template, request, redirect, session, url_for
from utils.login import login_required
from models.dietaryModel import DietaryManager
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
# from models.priceModel import PriceManager
# from models.shopModel import ShopManager
from models.userModel import UserManager
from models.tasteModel import TasteManager
from config.db import db
from utils.time import format_time_ago
from firebase_admin import firestore

dishes_bp = Blueprint('dishes', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = TasteManager(db, firestore)
# price_manager = PriceManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)
ingredient_manager = IngredientManager(db, firestore)
# shop_manager = ShopManager(db, firestore)

@dishes_bp.route('/', methods=['POST'])
def explore():
    user = user_manager.get_user_by_session(session)
    dishes = manager.all_search()
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'search.html', 
        user=user,
        ingredients=ingredients,
        recommendation=dishes,
        dietaries=dietaries
    )

@dishes_bp.route('/dietary', methods=['POST'])
def dietaryFilter():
    user = user_manager.get_user_by_session(session)
    dietary = request.form.get('dietary')
    dish_names = dietary_manager.get_dishes_by_ingredient(dietary)
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'search.html', 
        user=user, 
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/ingredient', methods=['POST'])
def ingredientFilter():
    user = user_manager.get_user_by_session(session)
    ingredient = request.form.get('ingredient')
    dish_names = ingredient_manager.get_dishes_by_ingredient(ingredient)
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'search.html', 
        user=user, 
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

# @dishes_bp.route('/description', methods=['POST'])
# def description():
#     user = user_manager.get_user_by_session(session)
#     description = request.form.get('description')
#     dishes = manager.description_search(description)
#     return render_template(
#         'search.html', 
#         user=user, 
#         recommendation=dishes
#     )

@dishes_bp.route('/<name>', methods=['GET', 'POST'])
def food(name=None):
    user = user_manager.get_user_by_session(session)
    dish = manager.get_dish_instance(name)
    # prices = price_manager.get_price(name)
    # shops = shop_manager.get_shop(name)
    dietaries = dietary_manager.get_dietary(name)
    ingredients = ingredient_manager.get_ingredient(name)
    tastes = selection_manager.get_dish_rating(name)
    return render_template(
        'food.html', 
        # prices=prices, 
        # shops=shops,
        user=user, 
        dish=dish,
        dietaries=dietaries,
        ingredients=ingredients,
        tastes=tastes
    )

@dishes_bp.route('/select/<name>', methods=['POST'])
@login_required
def select_food(name=None):
    spiciness = request.form.get('spiciness')
    sweetness = request.form.get('sweetness')
    sourness = request.form.get('sourness')
    texture = request.form.get('texture')
    temperature = request.form.get('temperature')
    healthiness = request.form.get('healthiness')
    rating = request.form.get('rating')
    selection_manager.add_selection(
        session.get('google_id'), 
        name, 
        spiciness, 
        sweetness, 
        sourness, 
        texture, 
        temperature, 
        healthiness, 
        rating
    )
    return redirect(url_for('dishes.food', name=name))

# @dishes_bp.route('/price_review/<name>', methods=['POST'])
# @login_required
# def priceReviewRoute(name=None):
#     price = request.form.get('price')
#     currency = request.form.get('currency')
#     price_manager.add_price(session.get('google_id'), name, price, currency)
#     return redirect(url_for('dishes.food', name=name))

@dishes_bp.route('/dietary_review/<name>', methods=['POST'])
@login_required
def dietaryReviewRoute(name=None):
    dietary = request.form.get('dietary')
    dietary_manager.add_dietary(name, session.get('google_id'), dietary)
    return redirect(url_for('dishes.food', name=name))

@dishes_bp.route('/ingredient_review/<name>', methods=['POST'])
@login_required
def ingredientReviewRoute(name=None):
    ingredient = request.form.get('ingredient')
    ingredient_manager.add_ingredient(name, session.get('google_id'), ingredient)
    return redirect(url_for('dishes.food', name=name))

# @dishes_bp.route('/shop_review/<name>', methods=['POST'])
# @login_required
# def shopReviewRoute(name=None):
#     shop = request.form.get('shop')
#     shop_manager.add_shop(session.get('google_id'), name, shop)
#     return redirect(url_for('dishes.food', name=name))

@dishes_bp.route('/rate_dish', methods=['POST'])
def rate_dish():
    history_id = request.form.get('history_id')
    spiciness = request.form.get('spiciness')
    sweetness = request.form.get('sweetness')
    sourness = request.form.get('sourness')
    texture = request.form.get('texture')
    temperature = request.form.get('temperature')
    healthiness = request.form.get('healthiness')
    rating = request.form.get('rating')
    selection_manager.update_review(
        history_id, 
        spiciness, 
        sweetness, 
        sourness, 
        texture, 
        temperature, 
        healthiness, 
        rating
    )
    return redirect(url_for('users.history'))

# @dishes_bp.route('/update_price', methods=['POST'])
# def update_price():
#     history_id = request.form.get('history_id')
#     price = request.form.get('price')
#     currency = request.form.get('currency')
#     price_manager.update_price(history_id, price, currency)
#     return redirect(url_for('users.history'))

# @dishes_bp.route('/update_shop', methods=['POST'])
# def update_shop():
#     history_id = request.form.get('history_id')
#     link = request.form.get('link')
#     shop_manager.update_shop(history_id, link)
#     return redirect(url_for('users.history'))

@dishes_bp.route('/update_dietary', methods=['POST'])
def update_dietary():
    history_id = request.form.get('history_id')
    dietary = request.form.get('dietary')
    dietary_manager.update_dietary(history_id, dietary)
    return redirect(url_for('users.history'))

@dishes_bp.route('/update_ingredient', methods=['POST'])
def update_ingredient():
    history_id = request.form.get('history_id')
    ingredient = request.form.get('ingredient')
    ingredient_manager.update_ingredient(history_id, ingredient)
    return redirect(url_for('users.history'))

@dishes_bp.app_template_filter('time_ago')
def time_ago_filter(timestamp):
    return format_time_ago(timestamp)