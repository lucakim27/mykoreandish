from flask import Blueprint, g, redirect, request, url_for
from ..utils.login import login_required
from ..services.managers import (
    note_manager,
    ingredient_manager
)

note_bp = Blueprint('note', __name__)

@note_bp.route('/add/<name>', methods=['POST'])
@login_required
def add_note(name):
    note_content = request.form.get('note_content')
    note_manager.add_note(name, g.user['google_id'], note_content)
    ingredients = ingredient_manager.get_all_ingredients()
    for ingredient in ingredients:
        if ingredient['ingredient'] == name:
            return redirect(url_for('ingredients.ingredientsListController', name=name))
    else:
        return redirect(url_for('dishes.food', name=name))
