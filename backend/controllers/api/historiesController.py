from itertools import chain
from flask import Blueprint, jsonify
from ...services.managers import dietary_manager, ingredient_manager, taste_manager, nutrient_manager, price_manager
from ...utils.login import login_required

histories_bp = Blueprint('histories', __name__, url_prefix='/api/histories')

@histories_bp.route('/get_user_history/<user_id>', methods=['GET'])
@login_required
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