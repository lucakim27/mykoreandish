from flask import Blueprint, g, request
from ...services.managers import note_manager
from ...utils.login import login_required

notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@notes_bp.route('/<dish_name>', methods=['GET'])
@login_required
def get_notes_by_dish_and_user(dish_name):
    user_id = g.user['google_id']
    note = note_manager.get_note(dish_name, user_id)
    return note, 200

@notes_bp.route('/<name>', methods=['POST'])
@login_required
def add_note(name):
    user_id = g.user['google_id']
    note_content = request.get_json()['note_content']
    note_manager.add_note(name, user_id, note_content)
    return '', 204

@notes_bp.route('/<name>', methods=['PUT'])
@login_required
def update_note(name):
    user_id = g.user['google_id']
    note_content = request.get_json()['note_content']
    note_manager.update_note(name, user_id, note_content)
    return '', 204

@notes_bp.route('/<name>', methods=['DELETE'])
@login_required
def delete_note(name):
    user_id = g.user['google_id']
    note_manager.delete_note(name, user_id)
    return '', 204