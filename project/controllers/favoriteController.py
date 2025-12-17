from flask import Blueprint, g, redirect, url_for
from ..utils.login import login_required
from ..services.managers import (
    dish_manager,
    favorite_manager,
    ingredient_manager
)

favorite_bp = Blueprint('favorite', __name__)

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