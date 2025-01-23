from flask import Blueprint, render_template, session
from config.db import db
from models.dietaryModel import DietaryManager
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
from models.priceModel import PriceManager
from models.tasteModel import TasteManager
from models.userModel import UserManager
from firebase_admin import firestore

reviews_bp = Blueprint('reviews', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = TasteManager(db, firestore)
price_manager = PriceManager(db, firestore)
ingredient_manager = IngredientManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)

@reviews_bp.route('/<name>', methods=['POST'])
def reviewController(name=None):
    user = user_manager.get_user_by_session(session)
    dish = manager.get_dish_instance(name)
    return render_template('review.html', user=user, dish=dish)

# @reviews_bp.route('/price/<name>', methods=['POST'])
# def priceController(name=None):
#     user = user_manager.get_user_by_session(session)
#     dish = manager.get_dish_instance(name)
#     currency = price_manager.get_all_currency()
#     return render_template('price.html', user=user, dish=dish, currency=currency)

# @reviews_bp.route('/shop/<name>', methods=['POST'])
# def shopController(name=None):
#     user = user_manager.get_user_by_session(session)
#     dish = manager.get_dish_instance(name)
#     return render_template('shop.html', user=user, dish=dish)

@reviews_bp.route('/dietary/<name>', methods=['POST'])
def dietaryController(name=None):
    user = user_manager.get_user_by_session(session)
    dish = manager.get_dish_instance(name)
    dietaries = dietary_manager.get_all_dietaries()
    return render_template('dietary.html', user=user, dish=dish, dietaries=dietaries)

@reviews_bp.route('/ingredient/<name>', methods=['POST'])
def drinkController(name=None):
    user = user_manager.get_user_by_session(session)
    dish = manager.get_dish_instance(name)
    ingredients = ingredient_manager.get_all_ingredients()
    return render_template('ingredient.html', user=user, dish=dish, ingredients=ingredients)