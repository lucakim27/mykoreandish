from flask import Blueprint, render_template, session
from models.ingredientModel import IngredientManager
from config.db import db
from firebase_admin import firestore
from models.userModel import UserManager

ingredients_bp = Blueprint('ingredients', __name__)
ingredient_manager = IngredientManager(db, firestore)
user_manager = UserManager(db)

@ingredients_bp.route('/', methods=['POST'])
def ingredientsController():
    user = user_manager.get_user_by_session(session)
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template(
        'ingredientSearch.html', 
        user=user, 
        recommendation=ingredients
    )

@ingredients_bp.route('/<name>', methods=['GET', 'POST'])
def ingredientsListController(name=None):
    user = user_manager.get_user_by_session(session)
    ingredient = ingredient_manager.get_ingredient_instance(name)
    # nutrients = nutrients_manager.get_dish_rating(name)
    return render_template(
        'ingredientDetail.html',
        user=user, 
        ingredient=ingredient,
    )