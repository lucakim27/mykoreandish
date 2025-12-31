from flask import Blueprint, redirect, url_for
from ...services.managers import favorite_manager, ingredient_manager
from ...utils.login import login_required

favorites_bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')

@favorites_bp.route('/get_favorite_dishes/<user_id>', methods=['GET'])
def get_favorite_dishes(user_id):
    return favorite_manager.get_all_favorites(user_id)

@favorites_bp.route('/is_dish_favorite/<dish_name>/<user_id>', methods=['GET'])
def is_dish_favorite(dish_name, user_id):
    return favorite_manager.is_dish_favorite(dish_name, user_id)

@favorites_bp.route('/add/dish/<dish_name>/<user_id>', methods=['POST'])
@login_required
def addDishFavoriteController(dish_name, user_id):
    favorite_manager.add_favorite(dish_name, user_id)
    return redirect('/dishes/' + dish_name)

@favorites_bp.route('/delete/dish/<dish_name>/<user_id>', methods=['POST'])
@login_required
def deleteDishFavoriteController(dish_name, user_id):
    favorite_manager.delete_favorite(dish_name, user_id)
    return redirect('/dishes/' + dish_name)

@favorites_bp.route('/add/ingredient/<ingredient_name>/<user_id>', methods=['POST'])
@login_required
def addIngredientFavoriteController(ingredient_name, user_id):
    ingredient = ingredient_manager.get_ingredient_instance(ingredient_name)
    favorite_manager.add_favorite(ingredient['ingredient'], user_id)
    return redirect('/ingredients/'+ ingredient_name)

@favorites_bp.route('/delete/ingredient/<ingredient_name>/<user_id>', methods=['POST'])
@login_required
def deleteIngredientFavoriteController(ingredient_name, user_id):
    ingredient = ingredient_manager.get_ingredient_instance(ingredient_name)
    favorite_manager.delete_favorite(ingredient['ingredient'], user_id)
    return redirect('/ingredients/'+ ingredient_name)

@favorites_bp.route('/is_ingredient_favorite/<ingredient_name>/<user_id>', methods=['GET'])
def is_ingredient_favorite(ingredient_name, user_id):
    return favorite_manager.is_ingredient_favorite(ingredient_name, user_id)