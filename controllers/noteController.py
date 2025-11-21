from flask import Blueprint, g, redirect, request, session, url_for
from config.db import db
from models.ingredientModel import IngredientManager
from models.noteModel import NoteManager
from models.userModel import UserManager
from firebase_admin import firestore as firestore_module
from utils.login import login_required

note_bp = Blueprint('note', __name__)
user_manager = UserManager(db)
note_manager = NoteManager(db, firestore_module)
ingredient_manager = IngredientManager(db, firestore_module)

@note_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

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
