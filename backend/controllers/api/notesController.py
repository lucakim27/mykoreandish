from flask import Blueprint, request
from ...services.managers import note_manager
from ...utils.login import login_required

notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@notes_bp.route('/<dish_name>/<user_id>', methods=['GET'])
def get_notes_by_dish_and_user(dish_name, user_id):
    note = note_manager.get_note(dish_name, user_id)
    return note, 200

@notes_bp.route('/<name>/<user_id>', methods=['POST'])
@login_required
def add_note(name, user_id):
    data = request.get_json(silent=True) or {}
    note_content = data.get('note_content', '')

    if not note_content.strip():
        note_manager.delete_note(name, user_id)
    else:
        note_manager.add_note(name, user_id, note_content)

    return '', 204
