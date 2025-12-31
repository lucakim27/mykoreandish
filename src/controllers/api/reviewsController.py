from flask import Blueprint, request, redirect
from ...services.managers import aggregate_manager, dietary_manager, ingredient_manager, taste_manager, price_manager

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@reviews_bp.route('/get_total_reviews', methods=['GET'])
def get_review_count():
    return {"total_reviews": aggregate_manager.get_total_reviews()}

@reviews_bp.route('/add_dietary_review/<dish_name>/<user_id>', methods=['POST'])
def add_dietary_review(dish_name, user_id):
    dietary_selection = request.form.get('dietary')
    dietary_manager.add_dietary_review(dish_name, user_id, dietary_selection)
    aggregate_manager.add_dietary_aggregate(dish_name, dietary_selection)
    return redirect('/dishes/' + dish_name)

@reviews_bp.route('/add_ingredient_review/<dish_name>/<user_id>', methods=['POST'])
def add_ingredient_review(dish_name, user_id):
    ingredient_selection = request.form.get('ingredient')
    ingredient_manager.add_ingredient_review(dish_name, user_id, ingredient_selection)
    aggregate_manager.add_ingredient_aggregate(dish_name, ingredient_selection)
    return redirect('/dishes/' + dish_name)

@reviews_bp.route('/add_taste_review/<dish_name>/<user_id>', methods=['POST'])
def add_taste_review(dish_name, user_id):
    spiciness = request.form.get('spiciness')
    sweetness = request.form.get('sweetness')
    sourness = request.form.get('sourness')
    texture = request.form.get('texture')
    temperature = request.form.get('temperature')
    healthiness = request.form.get('healthiness')
    rating = request.form.get('rating')
    taste_manager.add_taste_review(
        user_id,
        dish_name,
        spiciness,
        sweetness,
        sourness,
        texture,
        temperature,
        healthiness,
        rating
    )
    aggregate_manager.add_aggregate(dish_name, {
        "spiciness": int(spiciness),
        "sweetness": int(sweetness),
        "sourness": int(sourness),
        "temperature": int(temperature),
        "texture": int(texture),
        "rating": int(rating),
        "healthiness": int(healthiness)
    })
    return redirect('/dishes/' + dish_name)

@reviews_bp.route('/add_price_review/<dish_name>/<user_id>', methods=['POST'])
def add_price_review(dish_name, user_id):
    price = request.form.get('price')
    country = request.form.get('country')
    city = request.form.get('city')
    price_manager.add_price_review(dish_name, user_id, price, country, city)
    return redirect('/dishes/' + dish_name)