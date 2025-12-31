from flask import Blueprint, redirect, request
from ...services.managers import price_manager

prices_bp = Blueprint('prices', __name__, url_prefix='/api/prices')

@prices_bp.route('/get_all_locations', methods=['GET'])
def get_all_locations():
    return price_manager.get_all_locations()

@prices_bp.route('/get_price_info/<dish_name>', methods=['GET'])
def get_price_info(dish_name):
    return price_manager.get_price_info(dish_name)

@prices_bp.route('/update_price_review', methods=['POST'])
def update_price_review():
    history_id = request.form.get('history_id')
    new_price = request.form.get('price')
    new_country = request.form.get('country')
    new_state = request.form.get('state')
    price_manager.update_price(history_id, new_price, new_country, new_state)
    return redirect('/users')

@prices_bp.route('/delete_price_review', methods=['POST'])
def delete_price_review():
    history_id = request.form.get('history_id')
    price_manager.delete_price(history_id)
    return redirect('/users')