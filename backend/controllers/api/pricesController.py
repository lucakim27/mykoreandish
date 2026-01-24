from flask import Blueprint, g, request
from backend.utils.login import login_required
from ...services.managers import price_manager

prices_bp = Blueprint('prices', __name__, url_prefix='/api/prices')

@prices_bp.route('/<dish_name>', methods=['GET'])
def get_price_info(dish_name):
    price = price_manager.get_price_info(dish_name)
    return price, 200

@prices_bp.route('/', methods=['PUT'])
@login_required
def update_price_review():
    data = request.get_json()
    history_id = data['history_id']
    new_price = data['price']
    new_country = data['country']
    price_manager.update_price(history_id, new_price, new_country)
    return '', 204

@prices_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_price_review(id):
    price_manager.delete_price(id)
    return '', 204

@prices_bp.route('/<dish_name>', methods=['POST'])
@login_required
def add_price_review(dish_name):
    user_id = g.user['google_id']
    price = request.get_json()['price']
    country = request.get_json()['country']
    price_manager.add_price_review(dish_name, user_id, price, country)
    return '', 204