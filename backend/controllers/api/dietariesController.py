from flask import Blueprint
from ...services.managers import dietary_manager

dietaries_bp = Blueprint('dietaries', __name__, url_prefix='/api/dietaries')

@dietaries_bp.route('/get_all_dietaries', methods=['GET'])
def get_all_dietaries():
    return dietary_manager.get_all_dietaries()