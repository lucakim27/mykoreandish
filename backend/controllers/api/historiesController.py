from itertools import chain
from flask import Blueprint, jsonify, redirect, request
from ...services.managers import dietary_manager, ingredient_manager, taste_manager, nutrient_manager, price_manager, aggregate_manager
from ...utils.login import login_required

histories_bp = Blueprint('histories', __name__, url_prefix='/api/histories')

@histories_bp.route('/get_user_history/<user_id>', methods=['GET'])
def get_history(user_id):
    combined_history = list(chain(
        taste_manager.get_user_history(user_id), 
        dietary_manager.get_dietary_history(user_id), 
        ingredient_manager.get_ingredient_history(user_id),
        nutrient_manager.get_nutrient_history(user_id),
        price_manager.get_price_history(user_id)
    ))

    return jsonify({
        "history": combined_history
    })

@histories_bp.route('/get_history_meta', methods=['GET'])
@login_required
def get_history_meta():
    return jsonify({
        "ingredients": ingredient_manager.get_all_ingredients(),
        "dietaries": dietary_manager.get_all_dietaries(),
        "nutrients": nutrient_manager.get_all_nutrients(),
        "locations": price_manager.get_all_locations()
    })

@histories_bp.route('/update_taste_review', methods=['POST'])
def update_taste_review():
    history_id = request.form.get('history_id')
    spiciness = request.form.get('spiciness')
    sweetness = request.form.get('sweetness')
    sourness = request.form.get('sourness')
    texture = request.form.get('texture')
    temperature = request.form.get('temperature')
    healthiness = request.form.get('healthiness')
    rating = request.form.get('rating')
    dish_review = taste_manager.get_dish_review_by_id(history_id)
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
    taste_manager.update_review(
        history_id, 
        spiciness, 
        sweetness, 
        sourness, 
        texture, 
        temperature, 
        healthiness, 
        rating
    )
    return redirect('/users')