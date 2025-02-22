from flask import Blueprint, render_template, request, redirect, session, url_for
from models.cacheModel import CacheManager
from utils.login import login_required
from models.dietaryModel import DietaryManager
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
from models.userModel import UserManager
from models.tasteModel import TasteManager
from config.db import db
from utils.time import format_time_ago
from firebase_admin import firestore

dishes_bp = Blueprint('dishes', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = TasteManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)
ingredient_manager = IngredientManager(db, firestore)
cache_manager = CacheManager(db)

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

@dishes_bp.route('/spiciness', methods=['POST'])
def spicinessFilter():
    user = user_manager.get_user_by_session(session)
    spiciness = request.form.get('spiciness')
    dish_names = cache_manager.get_dishes_by_spiciness(spiciness)
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

@dishes_bp.route('/sweetness', methods=['POST'])
def sweetnessFilter():
    user = user_manager.get_user_by_session(session)
    sweetness = request.form.get('sweetness')
    dish_names = cache_manager.get_dishes_by_sweetness(sweetness)
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

@dishes_bp.route('/sourness', methods=['POST'])
def sournessFilter():
    user = user_manager.get_user_by_session(session)
    sourness = request.form.get('sourness')
    dish_names = cache_manager.get_dishes_by_sourness(sourness)
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

@dishes_bp.route('/texture', methods=['POST'])
def textureFilter():
    user = user_manager.get_user_by_session(session)
    texture = request.form.get('texture')
    dish_names = cache_manager.get_dishes_by_texture(texture)
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

@dishes_bp.route('/temperature', methods=['POST'])
def temperatureFilter():
    user = user_manager.get_user_by_session(session)
    temperature = request.form.get('temperature')
    dish_names = cache_manager.get_dishes_by_temperature(temperature)
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

@dishes_bp.route('/healthiness', methods=['POST'])
def healthinessFilter():
    user = user_manager.get_user_by_session(session)
    healthiness = request.form.get('healthiness')
    dish_names = cache_manager.get_dishes_by_healthiness(healthiness)
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

@dishes_bp.route('/rating', methods=['POST'])
def ratingFilter():
    user = user_manager.get_user_by_session(session)
    rating = request.form.get('rating')
    dish_names = cache_manager.get_dishes_by_rating(rating)
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

@dishes_bp.route('/<name>', methods=['GET', 'POST'])
def food(name=None):
    user = user_manager.get_user_by_session(session)
    dish = manager.get_dish_instance(name)
    dietary = dietary_manager.get_dietary(name)
    ingredient = ingredient_manager.get_ingredient(name)
    tastes = selection_manager.get_dish_rating(name)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'food.html',
        user=user, 
        dish=dish,
        dietary=dietary,
        ingredient=ingredient,
        tastes=tastes,
        dietaries=dietaries,
        ingredients=ingredients
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