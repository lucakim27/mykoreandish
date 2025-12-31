from flask import Blueprint, g, render_template, request, redirect, url_for
from ..utils.login import login_required
from ..services.managers import (
    dish_manager,
    selection_manager,
    dietary_manager,
    ingredient_manager,
    favorite_manager,
    aggregate_manager,
    price_manager,
    note_manager
)

dishes_bp = Blueprint('dishes', __name__)

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
        g.user['google_id'], 
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
    dietary_manager.add_dietary(name, g.user['google_id'], dietary)
    aggregate_manager.add_dietary_aggregate(name, dietary)
    return redirect(url_for('dishes.food', name=name))

@dishes_bp.route('/ingredient_review/<name>', methods=['POST'])
@login_required
def ingredientReviewRoute(name=None):
    ingredient = request.form.get('ingredient')
    ingredient_manager.add_ingredient(name, g.user['google_id'], ingredient)
    aggregate_manager.add_ingredient_aggregate(name, ingredient)
    return redirect(url_for('dishes.food', name=name))


@dishes_bp.route('/price_review/<name>', methods=['POST'])
@login_required
def priceReviewRoute(name=None):
    price = request.form.get('price')
    country = request.form.get('country')
    city = request.form.get('city')
    price_manager.add_price(name, g.user['google_id'], price, country, city)
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
