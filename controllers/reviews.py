from flask import Blueprint, render_template, session
from config.db import db
from models.dishes import DishManager
from models.userSelections import UserSelectionManager
from models.users import UserManager
from firebase_admin import firestore

reviews_bp = Blueprint('reviews', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)

@reviews_bp.route('/<name>', methods=['POST'])
def reviewController(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    return render_template('review.html', user=user, dish=dish)

@reviews_bp.route('/price/<name>', methods=['POST'])
def priceController(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    return render_template('price.html', user=user, dish=dish)

@reviews_bp.route('/dietary/<name>', methods=['POST'])
def dietaryController(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    return render_template('dietary.html', user=user, dish=dish)

@reviews_bp.route('/ingredient/<name>', methods=['POST'])
def drinkController(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    return render_template('ingredient.html', user=user, dish=dish)