from flask import Blueprint, redirect, request
from backend.utils.login import login_required
from ...services.managers import nutrient_manager

nutrients_bp = Blueprint('nutrients', __name__, url_prefix='/api/nutrients')

@nutrients_bp.route('/get_all_nutrients', methods=['GET'])
def get_all_nutrients():
    return nutrient_manager.get_all_nutrients()

@nutrients_bp.route('/get_ingredient_nutrients/<ingredient_name>', methods=['GET'])
def get_ingredient_nutrients(ingredient_name):
    return nutrient_manager.get_ingredient_nutrients(ingredient_name)

@nutrients_bp.route('/update_nutrient_review', methods=['POST'])
@login_required
def update_nutrient_review():
    history_id = request.form.get('history_id')
    nutrient = request.form.get('nutrient')
    nutrient_manager.update_nutrient_review(history_id, nutrient)
    return redirect('/users')

@nutrients_bp.route('/delete_nutrient_review', methods=['POST'])
@login_required
def delete_nutrient_review():
    history_id = request.form.get('history_id')
    nutrient_manager.delete_nutrient(history_id)
    return redirect('/users')