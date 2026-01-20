from backend.utils.login import login_required
from flask import Blueprint, redirect, request
from ...services.managers import dietary_manager, aggregate_manager

dietaries_bp = Blueprint('dietaries', __name__, url_prefix='/api/dietaries')

@dietaries_bp.route('/', methods=['GET'])
def get_all_dietaries():
    dietaries = dietary_manager.get_all_dietaries()
    return dietaries, 200

@dietaries_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_dietary_review(id):
    dietary = dietary_manager.get_dietary_review_by_id(id)
    dietary_manager.delete_dietary(id)
    aggregate_manager.delete_dietary_aggregate(dietary)
    return '', 204

@dietaries_bp.route('/', methods=['POST'])
@login_required
def update_dietary_review():
    history_id = request.form.get('history_id')
    new_dietary = request.form.get('dietary')
    dietary_review = dietary_manager.get_dietary_review_by_id(history_id)
    aggregate_manager.update_dietary_aggregate(
        dietary_review.get('dish_name', 0), 
        dietary_review.get('dietary', 0), 
        new_dietary
    )
    dietary_manager.update_dietary(history_id, new_dietary)
    return redirect('/users')

@dietaries_bp.route('/<dish_name>/<user_id>', methods=['POST'])
def add_dietary_review(dish_name, user_id):
    dietary_selection = request.form.get('dietary')
    dietary_manager.add_dietary_review(dish_name, user_id, dietary_selection)
    aggregate_manager.add_dietary_aggregate(dish_name, dietary_selection)
    return redirect('/dishes/' + dish_name)