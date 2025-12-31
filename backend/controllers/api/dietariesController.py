from backend.utils.login import login_required
from flask import Blueprint, request, redirect
from ...services.managers import dietary_manager, aggregate_manager

dietaries_bp = Blueprint('dietaries', __name__, url_prefix='/api/dietaries')

@dietaries_bp.route('/get_all_dietaries', methods=['GET'])
def get_all_dietaries():
    return dietary_manager.get_all_dietaries()

@dietaries_bp.route('/delete_dietary_review', methods=['POST'])
@login_required
def delete_dietary_review():
    history_id = request.form.get('history_id')
    dietary = dietary_manager.get_dietary_review_by_id(history_id)
    dietary_manager.delete_dietary(history_id)
    aggregate_manager.delete_dietary_aggregate(dietary)
    return redirect('/users')