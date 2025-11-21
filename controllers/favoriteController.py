from flask import Blueprint, g, redirect, session, url_for
from config.db import db
from models.dishModel import DishManager
from models.favoriteModel import FavoriteManager
from models.ingredientModel import IngredientManager
from models.userModel import UserManager
from utils.login import login_required
from firebase_admin import firestore

favorite_bp = Blueprint('favorite', __name__)
user_manager = UserManager(db)
dish_manager = DishManager(csv_file='csv/dishes.csv')
favorite_manager = FavoriteManager(db, firestore)
ingredient_manager = IngredientManager(db, firestore)

@favorite_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

@favorite_bp.route('/add/dish/<name>', methods=['POST'])
@login_required
def addDishFavoriteController(name=None):
    dish = dish_manager.get_dish_instance(name)
    favorite_manager.add_favorite(dish['dish_name'], g.user['google_id'])
    return redirect(url_for('dishes.food', name=name))

@favorite_bp.route('/delete/dish/<name>', methods=['POST'])
@login_required
def deleteDishFavoriteController(name=None):
    dish = dish_manager.get_dish_instance(name)
    favorite_manager.delete_favorite(dish['dish_name'], g.user['google_id'])
    return redirect(url_for('dishes.food', name=name))

@favorite_bp.route('/add/ingredient/<name>', methods=['POST'])
@login_required
def addIngredientFavoriteController(name=None):
    ingredient = ingredient_manager.get_ingredient_instance(name)
    favorite_manager.add_favorite(ingredient['ingredient'], g.user['google_id'])
    return redirect(url_for('ingredients.ingredientsListController', name=name))

@favorite_bp.route('/delete/ingredient/<name>', methods=['POST'])
@login_required
def deleteIngredientFavoriteController(name=None):
    ingredient = ingredient_manager.get_ingredient_instance(name)
    favorite_manager.delete_favorite(ingredient['ingredient'], g.user['google_id'])
    return redirect(url_for('ingredients.ingredientsListController', name=name))