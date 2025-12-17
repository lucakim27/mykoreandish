from flask import Blueprint, g, render_template
from ..services.managers import aggregate_manager

insight_bp = Blueprint('insight', __name__)

@insight_bp.route('/', methods=['POST'])
def insight_page():
    return render_template('insight.html')

@insight_bp.route('/api/getStats', methods=['POST'])
def insight_api():
    top_five = aggregate_manager.get_top_five()
    return {
        "user": g.user,
        "top_ingredients": top_five['top_ingredients'],
        "top_dishes": top_five['top_dishes']
    }