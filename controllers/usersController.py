from itertools import chain
from flask import Blueprint, redirect, render_template, request, session, url_for
from controllers.authController import login_required
from models.dietaryModel import DietaryManager
from models.dishesModel import DishManager
from models.ingredientModel import IngredientManager
from models.priceModel import PriceManager
from models.usersModel import UserManager
from models.userSelectionsModel import UserSelectionManager
from config.db import db
from firebase_admin import firestore

users_bp = Blueprint('users', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)
price_manager = PriceManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)
ingredient_manager = IngredientManager(db, firestore)

@users_bp.route('/')
@login_required
def history():
    user = user_manager.get_user_by_session(session)
    currency = price_manager.get_all_currency()
    price_history = price_manager.get_price_history(session['google_id'])
    user_history = selection_manager.get_user_history(session['google_id'])
    dietary_history = dietary_manager.get_dietary_history(session['google_id'])
    ingredient_history = ingredient_manager.get_ingredient_history(session['google_id'])
     # Combine both histories into one list
    combined_history = list(chain(price_history, user_history, dietary_history, ingredient_history))

    # Sort by timestamp (assuming each entry has a 'timestamp' field)
    combined_history.sort(key=lambda x: x['timestamp'])
    return render_template('history.html', user=user, combined_history=combined_history, currency=currency)

@users_bp.route('/delete-history', methods=['POST'])
def deleteHistoryRoute():
    history_id = request.form.get('history_id')
    if history_id:
        if selection_manager.delete_history(history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))

@users_bp.route('/delete-price', methods=['POST'])
def deletePriceRoute():
    history_id = request.form.get('history_id')
    if history_id:
        if price_manager.delete_price(history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))

@users_bp.route('/delete-dietary', methods=['POST'])
def deleteDietaryRoute():
    history_id = request.form.get('history_id')
    if history_id:
        if dietary_manager.delete_dietary(history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))

@users_bp.route('/delete-ingredient', methods=['POST'])
def deleteIngredientRoute():
    history_id = request.form.get('history_id')
    if history_id:
        if ingredient_manager.delete_ingredient(history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))

@users_bp.route('/profile')
def profile():
    user = user_manager.get_user_by_session(session)
    return render_template('profile.html', user=user)