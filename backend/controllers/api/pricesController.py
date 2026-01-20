from flask import Blueprint, redirect, request
from backend.utils.login import login_required
from ...services.managers import price_manager

prices_bp = Blueprint('prices', __name__, url_prefix='/api/prices')

@prices_bp.route('/<dish_name>', methods=['GET'])
def get_price_info(dish_name):
    price = price_manager.get_price_info(dish_name)
    return price, 200

@prices_bp.route('/update_price_review', methods=['POST'])
@login_required
def update_price_review():
    history_id = request.form.get('history_id')
    new_price = request.form.get('price')
    new_country = request.form.get('country')
    new_state = request.form.get('state')
    price_manager.update_price(history_id, new_price, new_country, new_state)
    return redirect('/users')

@prices_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_price_review(id):
    price_manager.delete_price(id)
    return '', 204

@prices_bp.route('/<dish_name>/<user_id>', methods=['POST'])
@login_required
def add_price_review(dish_name, user_id):
    price = request.form.get('price')
    country = request.form.get('country')
    price_manager.add_price_review(dish_name, user_id, price, country)
    return redirect('/dishes/' + dish_name)