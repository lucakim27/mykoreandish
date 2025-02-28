from flask import Blueprint, render_template, request, redirect, session, url_for
from models.aggregateModel import AggregateManager
from models.favoriteModel import FavoriteManager
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
favorite_manager = FavoriteManager(db, firestore)
aggregate_manager = AggregateManager(db)

@dishes_bp.route('/', methods=['POST'])
def explore():
    user = user_manager.get_user_by_session(session)
    dishes = manager.all_search()
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(user)
    return render_template(
        'foodList.html', 
        user=user,
        ingredients=ingredients,
        recommendation=dishes,
        dietaries=dietaries,
        favorites=favorites
    )

@dishes_bp.route('/dietary', methods=['POST'])
def dietaryFilter():
    user = user_manager.get_user_by_session(session)
    dietary = request.form.get('dietary')
    dish_names = dietary_manager.get_dishes_by_ingredient(dietary)
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(user)
    return render_template(
        'foodList.html', 
        user=user, 
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients,
        favorites=favorites
    )

@dishes_bp.route('/ingredient', methods=['POST'])
def ingredientFilter():
    user = user_manager.get_user_by_session(session)
    ingredient = request.form.get('ingredient')
    dish_names = ingredient_manager.get_dishes_by_ingredient(ingredient)
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(user)
    return render_template(
        'foodList.html', 
        user=user, 
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients,
        favorites=favorites
    )

@dishes_bp.route('/spiciness', methods=['POST'])
def spicinessFilter():
    user = user_manager.get_user_by_session(session)
    spiciness = request.form.get('spiciness')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('spiciness', int(spiciness))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/sweetness', methods=['POST'])
def sweetnessFilter():
    user = user_manager.get_user_by_session(session)
    sweetness = request.form.get('sweetness')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('sweetness', int(sweetness))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/sourness', methods=['POST'])
def sournessFilter():
    user = user_manager.get_user_by_session(session)
    sourness = request.form.get('sourness')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('sourness', int(sourness))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/texture', methods=['POST'])
def textureFilter():
    user = user_manager.get_user_by_session(session)
    texture = request.form.get('texture')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('texture', int(texture))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/temperature', methods=['POST'])
def temperatureFilter():
    user = user_manager.get_user_by_session(session)
    temperature = request.form.get('temperature')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('temperature', int(temperature))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/healthiness', methods=['POST'])
def healthinessFilter():
    user = user_manager.get_user_by_session(session)
    healthiness = request.form.get('healthiness')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('healthiness', int(healthiness))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/rating', methods=['POST'])
def ratingFilter():
    user = user_manager.get_user_by_session(session)
    rating = request.form.get('rating')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('rating', int(rating))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/<name>', methods=['GET', 'POST'])
def food(name=None):
    user = user_manager.get_user_by_session(session)
    dish = manager.get_dish_instance(name)
    aggregates = aggregate_manager.get_dish_aggregate(name)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(user)
    return render_template(
        'food.html',
        user=user, 
        dish=dish,
        aggregates=aggregates,
        dietaries=dietaries,
        ingredients=ingredients,
        favorites=favorites
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
    aggregate_manager.add_aggregate(name, {
        "spiciness": int(spiciness),
        "sweetness": int(sweetness),
        "sourness": int(sourness),
        "temperature": int(temperature),
        "texture": int(texture),
        "rating": int(rating),
        "healthiness": int(healthiness)
    })
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
    aggregate_manager.add_dietary_aggregate(name, dietary)
    return redirect(url_for('dishes.food', name=name))

@dishes_bp.route('/ingredient_review/<name>', methods=['POST'])
@login_required
def ingredientReviewRoute(name=None):
    ingredient = request.form.get('ingredient')
    ingredient_manager.add_ingredient(name, session.get('google_id'), ingredient)
    aggregate_manager.add_ingredient_aggregate(name, ingredient)
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
    dish_review = selection_manager.get_dish_review_by_id(history_id)
    aggregate_manager.update_aggregate(dish_review['dish_name'], {
        "spiciness": int(dish_review['spiciness']),
        "sweetness": int(dish_review['sweetness']),
        "sourness": int(dish_review['sourness']),
        "temperature": int(dish_review['temperature']),
        "texture": int(dish_review['texture']),
        "rating": int(dish_review['rating']),
        "healthiness": int(dish_review['healthiness'])
    }, {
        "spiciness": int(spiciness),
        "sweetness": int(sweetness),
        "sourness": int(sourness),
        "temperature": int(temperature),
        "texture": int(texture),
        "rating": int(rating),
        "healthiness": int(healthiness)
    })
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
    new_dietary = request.form.get('dietary')
    dietary_review = dietary_manager.get_dietary_review_by_id(history_id)
    aggregate_manager.update_dietary_aggregate(
        dietary_review.get('dish_name', 0), 
        dietary_review.get('dietary', 0), 
        new_dietary
    )
    dietary_manager.update_dietary(history_id, new_dietary)
    return redirect(url_for('users.history'))

@dishes_bp.route('/update_ingredient', methods=['POST'])
def update_ingredient():
    history_id = request.form.get('history_id')
    new_ingredient = request.form.get('ingredient')
    ingredient_review = ingredient_manager.get_ingredient_review_by_id(history_id)
    aggregate_manager.update_ingredient_aggregate(
        ingredient_review.get('dish_name', 0), 
        ingredient_review.get('ingredient', 0), 
        new_ingredient
    )
    ingredient_manager.update_ingredient(history_id, new_ingredient)
    return redirect(url_for('users.history'))

@dishes_bp.app_template_filter('time_ago')
def time_ago_filter(timestamp):
    return format_time_ago(timestamp)