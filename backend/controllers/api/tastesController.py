from flask import Blueprint, g, request
from backend.utils.login import login_required
from ...services.managers import taste_manager, aggregate_manager, taste_similarity_service

tastes_bp = Blueprint('tastes', __name__, url_prefix='/api/tastes')

@tastes_bp.route('/similar/<dish_name>', methods=['GET'])
def get_similar_taste_dishes(dish_name):
    similar_dishes = taste_similarity_service.find_similar_dishes(dish_name, 5)
    return similar_dishes, 200

@tastes_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_taste_review(id):
    dish_review = taste_manager.get_dish_review_by_id(id)
    taste_manager.delete_history(id)
    aggregate_manager.delete_aggregate(dish_review)
    return '', 204

@tastes_bp.route('/<dish_name>', methods=['POST'])
@login_required
def add_taste_review(dish_name):
    user_id = g.user['google_id']
    spiciness = request.get_json()['spiciness']
    sweetness = request.get_json()['sweetness']
    sourness = request.get_json()['sourness']
    texture = request.get_json()['texture']
    temperature = request.get_json()['temperature']
    healthiness = request.get_json()['healthiness']
    rating = request.get_json()['rating']
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
    return '', 204

@tastes_bp.route('/', methods=['PUT'])
@login_required
def update_taste_review():
    data = request.get_json()
    dish_review = taste_manager.get_dish_review_by_id(data['history_id'])
    aggregate_manager.update_aggregate(dish_review['dish_name'], {
        "spiciness": int(dish_review['spiciness']),
        "sweetness": int(dish_review['sweetness']),
        "sourness": int(dish_review['sourness']),
        "temperature": int(dish_review['temperature']),
        "texture": int(dish_review['texture']),
        "rating": int(dish_review['rating']),
        "healthiness": int(dish_review['healthiness'])
    }, {
        "spiciness": int(data['spiciness']),
        "sweetness": int(data['sweetness']),
        "sourness": int(data['sourness']),
        "temperature": int(data['temperature']),
        "texture": int(data['texture']),
        "rating": int(data['rating']),
        "healthiness": int(data['healthiness'])
    })

    taste_manager.update_review(
        data['history_id'], 
        data['spiciness'], 
        data['sweetness'], 
        data['sourness'], 
        data['texture'], 
        data['temperature'], 
        data['healthiness'], 
        data['rating']
    )

    return '', 204