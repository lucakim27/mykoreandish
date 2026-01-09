from backend.utils.login import login_required
from flask import Blueprint, request, redirect
from ...services.managers import dietary_manager, aggregate_manager

dietaries_bp = Blueprint('dietaries', __name__, url_prefix='/api/dietaries')

@dietaries_bp.route('/', methods=['GET'])
def get_all_dietaries():
    return dietary_manager.get_all_dietaries()

@dietaries_bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_dietary_review(id):
    dietary = dietary_manager.get_dietary_review_by_id(id)
    dietary_manager.delete_dietary(id)
    aggregate_manager.delete_dietary_aggregate(dietary)
    return '', 204