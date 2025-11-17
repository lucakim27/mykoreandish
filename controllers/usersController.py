from itertools import chain
from flask import Blueprint, redirect, render_template, request, session, url_for
from models.aggregateModel import AggregateManager
from models.nutrientModel import NutrientManager
from models.priceModel import PriceManager
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
price_manager = PriceManager('csv/locations.csv', db, firestore)

@users_bp.route('/')
@login_required
def history():
    user = user_manager.get_user_by_session(session)
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    nutrients = nutrient_manager.get_all_nutrients()
    locations = price_manager.get_all_locations()
    combined_history = list(chain(
        selection_manager.get_user_history(session['google_id']), 
        dietary_manager.get_dietary_history(session['google_id']), 
        ingredient_manager.get_ingredient_history(session['google_id']),
        nutrient_manager.get_nutrient_history(session['google_id']),
        price_manager.get_price_history(session['google_id'])
    ))
    return render_template(
        'history.html', 
        user=user,
        combined_history=combined_history,
        ingredients=ingredients,
        dietaries=dietaries,
        nutrients=nutrients,
        locations=locations
    )

@users_bp.route('/delete-history', methods=['POST'])
def deleteHistoryRoute():
    history_id = request.form.get('history_id')
    dish_review = selection_manager.get_dish_review_by_id(history_id)
    selection_manager.delete_history(history_id)
    aggregate_manager.delete_aggregate(dish_review)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-dietary', methods=['POST'])
def deleteDietaryRoute():
    history_id = request.form.get('history_id')
    dietary = dietary_manager.get_dietary_review_by_id(history_id)
    dietary_manager.delete_dietary(history_id)
    aggregate_manager.delete_dietary_aggregate(dietary)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-ingredient', methods=['POST'])
def deleteIngredientRoute():
    history_id = request.form.get('history_id')
    ingredient = ingredient_manager.get_ingredient_review_by_id(history_id)
    ingredient_manager.delete_ingredient(history_id)
    aggregate_manager.delete_ingredient_aggregate(ingredient)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-nutrient', methods=['POST'])
def deleteNutrientRoute():
    history_id = request.form.get('history_id')
    nutrient_manager.delete_nutrient(history_id)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-price', methods=['POST'])
def deletePriceRoute():
    history_id = request.form.get('history_id')
    price_manager.delete_price(history_id)
    return redirect(url_for('users.history'))

@users_bp.route('/profile')
def profile():
    user = user_manager.get_user_by_session(session)
    dietaries = dietary_manager.get_all_dietaries()
    return render_template('profile.html', user=user, dietaries=dietaries)

@users_bp.route('/update-dietary', methods=['POST'])
def updateDietaryPrefernece():
    user = user_manager.get_user_by_session(session)
    dietary_preference = request.form.get('dietary_preference')
    user_manager.update_dietary_preference(user, dietary_preference)
    return redirect(url_for('users.profile'))

@users_bp.route('/list', methods=['POST'])
def userList():
    user = user_manager.get_user_by_session(session)
    users = user_manager.get_all_users()
    return render_template('userList.html', user=user, users=users)

@users_bp.route('/user/<user_id>', methods=['GET'])
def userProfileController(user_id):
    user = user_manager.get_user_by_session(session)
    profile_user = user_manager.get_user_by_id(user_id)
    if profile_user is None:
        return redirect(url_for('users.userList'))
    return render_template('userProfile.html', user=user, profile_user=profile_user)

@users_bp.route('/updateDietaryPreference', methods=['POST'])
def updateDietaryPreference():
    user = user_manager.get_user_by_session(session)
    dietary_preference = request.form.get('dietary_preference')
    user_manager.update_dietary(user, dietary_preference)
    return redirect(url_for('users.profile'))