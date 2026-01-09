from flask import Blueprint
from backend.utils.login import login_required
from ...services.managers import taste_manager, aggregate_manager

tastes_bp = Blueprint('tastes', __name__, url_prefix='/api/tastes')

@tastes_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_taste_review(id):
    dish_review = taste_manager.get_dish_review_by_id(id)
    taste_manager.delete_history(id)
    aggregate_manager.delete_aggregate(dish_review)
    return '', 204