from itertools import chain
from flask import Blueprint, redirect, render_template, request, session, url_for
from models.aggregateModel import AggregateManager
from models.nutrientModel import NutrientManager
from utils.login import login_required
from models.dietaryModel import DietaryManager
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
from models.userModel import UserManager
from models.tasteModel import TasteManager
from config.db import db
from firebase_admin import firestore

users_bp = Blueprint('users', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = TasteManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)
ingredient_manager = IngredientManager(db, firestore)
nutrient_manager = NutrientManager(db, firestore)
aggregate_manager = AggregateManager(db)

@users_bp.route('/')
@login_required
def history():
    user = user_manager.get_user_by_session(session)
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    nutrients = nutrient_manager.get_all_nutrients()
    combined_history = list(chain(
        selection_manager.get_user_history(session['google_id']), 
        dietary_manager.get_dietary_history(session['google_id']), 
        ingredient_manager.get_ingredient_history(session['google_id']),
        nutrient_manager.get_nutrient_history(session['google_id'])
    ))
    return render_template(
        'history.html', 
        user=user, 
        combined_history=combined_history, 
        ingredients=ingredients, 
        dietaries=dietaries, 
        nutrients=nutrients
    )

@users_bp.route('/delete-history', methods=['POST'])
def deleteHistoryRoute():
    history_id = request.form.get('history_id')
    dish_review = selection_manager.get_dish_review_by_id(history_id)
    selection_manager.delete_history(history_id)
    aggregate_manager.delete_aggregate(dish_review['dish_name'], {
        "spiciness": int(dish_review['spiciness']),
        "sweetness": int(dish_review['sweetness']),
        "sourness": int(dish_review['sourness']),
        "temperature": int(dish_review['temperature']),
        "texture": int(dish_review['texture']),
        "rating": int(dish_review['rating']),
        "healthiness": int(dish_review['healthiness'])
    })
    return redirect(url_for('users.history'))

@users_bp.route('/delete-dietary', methods=['POST'])
def deleteDietaryRoute():
    history_id = request.form.get('history_id')
    dietary = dietary_manager.get_dietary_review_by_id(history_id)
    dietary_manager.delete_dietary(history_id)
    aggregate_manager.delete_dietary_aggregate(dietary['dish_name'], dietary['dietary'])
    return redirect(url_for('users.history'))

@users_bp.route('/delete-ingredient', methods=['POST'])
def deleteIngredientRoute():
    history_id = request.form.get('history_id')
    ingredient = ingredient_manager.get_ingredient_review_by_id(history_id)
    ingredient_manager.delete_ingredient(history_id)
    aggregate_manager.delete_ingredient_aggregate(ingredient['dish_name'], ingredient['ingredient'])
    return redirect(url_for('users.history'))

@users_bp.route('/delete-nutrient', methods=['POST'])
def deleteNutrientRoute():
    history_id = request.form.get('history_id')
    nutrient_manager.delete_nutrient(history_id)
    return redirect(url_for('users.history'))

@users_bp.route('/profile')
def profile():
    user = user_manager.get_user_by_session(session)
    return render_template('profile.html', user=user)