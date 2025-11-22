from flask import Blueprint, g, render_template, request, redirect, session, url_for
from ..models.aggregateModel import AggregateManager
from ..models.favoriteModel import FavoriteManager
from ..models.noteModel import NoteManager
from ..models.priceModel import PriceManager
from ..utils.login import login_required
from ..models.dietaryModel import DietaryManager
from ..models.dishModel import DishManager
from ..models.ingredientModel import IngredientManager
from ..models.userModel import UserManager
from ..models.tasteModel import TasteManager
from ..utils.time import format_time_ago
from firebase_admin import firestore

dishes_bp = Blueprint('dishes', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager()
selection_manager = TasteManager(firestore)
dietary_manager = DietaryManager(firestore)
ingredient_manager = IngredientManager(firestore)
favorite_manager = FavoriteManager(firestore)
aggregate_manager = AggregateManager()
price_manager = PriceManager('csv/locations.csv',firestore)
note_manager = NoteManager(firestore)

@dishes_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

@dishes_bp.route('/', methods=['POST'])
def explore():
    dishes = manager.all_search()
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(g.user)
    return render_template(
        'foodList.html', 
        user=g.user,
        ingredients=ingredients,
        recommendation=dishes,
        dietaries=dietaries,
        favorites=favorites
    )

@dishes_bp.route('/dietary', methods=['POST'])
def dietaryFilter():
    dietary = request.form.get('dietary')
    dish_names = dietary_manager.get_dishes_by_ingredient(dietary)
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(g.user)
    return render_template(
        'foodList.html', 
        user=g.user, 
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients,
        favorites=favorites
    )

@dishes_bp.route('/ingredient', methods=['POST'])
def ingredientFilter():
    ingredient = request.form.get('ingredient')
    dish_names = ingredient_manager.get_dishes_by_ingredient(ingredient)
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(g.user)
    return render_template(
        'foodList.html', 
        user=g.user, 
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients,
        favorites=favorites
    )

@dishes_bp.route('/spiciness', methods=['POST'])
def spicinessFilter():
    spiciness = request.form.get('spiciness')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('spiciness', int(spiciness))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=g.user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/sweetness', methods=['POST'])
def sweetnessFilter():
    sweetness = request.form.get('sweetness')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('sweetness', int(sweetness))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=g.user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/sourness', methods=['POST'])
def sournessFilter():
    sourness = request.form.get('sourness')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('sourness', int(sourness))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=g.user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/texture', methods=['POST'])
def textureFilter():
    texture = request.form.get('texture')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('texture', int(texture))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=g.user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/temperature', methods=['POST'])
def temperatureFilter():
    temperature = request.form.get('temperature')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('temperature', int(temperature))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=g.user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/healthiness', methods=['POST'])
def healthinessFilter():
    user = user_manager.get_user_by_id(session.get('google_id'))
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
    rating = request.form.get('rating')
    dish_names = aggregate_manager.get_dishes_by_aspect_range('rating', int(rating))
    dishes = manager.get_dish_instances(dish_names)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'foodList.html', 
        user=g.user,
        recommendation=dishes,
        dietaries=dietaries,
        ingredients=ingredients
    )

@dishes_bp.route('/<name>', methods=['GET', 'POST'])
def food(name=None):
    dish = manager.get_dish_instance(name)
    aggregates = aggregate_manager.get_dish_aggregate(name)
    dietaries = dietary_manager.get_all_dietaries()
    ingredients = ingredient_manager.get_all_ingredients()
    favorites = favorite_manager.get_all_favorites(g.user)
    similar_dishes = ingredient_manager.get_similar_dishes(name)
    locations = price_manager.get_all_locations()
    price_info = price_manager.get_price_info(dish["dish_name"])
    note = note_manager.get_note_by_dish_and_user(dish["dish_name"], g.user['google_id']) if g.user else None
    return render_template(
        'food.html',
        user=g.user, 
        dish=dish,
        aggregates=aggregates,
        dietaries=dietaries,
        ingredients=ingredients,
        favorites=favorites,
        similar_dishes=similar_dishes,
        locations=locations,
        price_info=price_info,
        note=note
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


@dishes_bp.route('/price_review/<name>', methods=['POST'])
@login_required
def priceReviewRoute(name=None):
    price = request.form.get('price')
    country = request.form.get('country')
    city = request.form.get('city')
    price_manager.add_price(name, session.get('google_id'), price, country, city)
    # aggregate_manager.add_price_aggregate(name, price, country, city)
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

@dishes_bp.route('/update_price', methods=['POST'])
def update_price():
    history_id = request.form.get('history_id')
    new_price = request.form.get('price')
    new_country = request.form.get('country')
    new_state = request.form.get('state')
    # ingredient_review = ingredient_manager.get_ingredient_review_by_id(history_id)
    # aggregate_manager.update_ingredient_aggregate(
    #     ingredient_review.get('dish_name', 0), 
    #     ingredient_review.get('ingredient', 0), 
    #     new_ingredient
    # )
    price_manager.update_price(history_id, new_price, new_country, new_state)
    return redirect(url_for('users.history'))

@dishes_bp.app_template_filter('time_ago')
def time_ago_filter(timestamp):
    return format_time_ago(timestamp)