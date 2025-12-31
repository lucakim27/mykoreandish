from flask import Blueprint, redirect, url_for, request
from ...services.managers import note_manager, ingredient_manager
from ...utils.login import login_required

notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@notes_bp.route('/get_note/<dish_name>/<user_id>', methods=['GET'])
def get_notes_by_dish_and_user(dish_name, user_id):
    return note_manager.get_note(dish_name, user_id)

@notes_bp.route('/add/<name>/<user_id>', methods=['POST'])
@login_required
def add_note(name, user_id):
    note_content = request.form.get('note_content')
    note_manager.add_note(name, user_id, note_content)
    ingredients = ingredient_manager.get_all_ingredients()
    for ingredient in ingredients:
        if ingredient['ingredient'] == name:
            return redirect('/ingredients/' + name)
    else:
        return redirect('/dishes/' + name)
