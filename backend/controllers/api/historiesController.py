from itertools import chain
from flask import Blueprint, g, jsonify
from ...services.managers import dietary_manager, ingredient_manager, taste_manager, nutrient_manager, price_manager

histories_bp = Blueprint('histories', __name__, url_prefix='/api/histories')

@histories_bp.route('/', methods=['GET'])
def get_history():
    user_id = g.user['google_id']
    return jsonify({
        "history": list(chain(
            taste_manager.get_user_history(user_id), 
            dietary_manager.get_dietary_history(user_id), 
            ingredient_manager.get_ingredient_history(user_id),
            nutrient_manager.get_nutrient_history(user_id),
            price_manager.get_price_history(user_id)
        ))
    }), 200