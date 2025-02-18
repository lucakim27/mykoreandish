from flask import Blueprint, redirect, render_template, request, session, url_for
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
from config.db import db
from firebase_admin import firestore
from models.nutrientModel import NutrientManager
from models.userModel import UserManager
from utils.login import login_required

ingredients_bp = Blueprint('ingredients', __name__)
ingredient_manager = IngredientManager(db, firestore)
user_manager = UserManager(db)
nutrient_manager = NutrientManager(db, firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')

@ingredients_bp.route('/', methods=['POST'])
def ingredientsController():
    user = user_manager.get_user_by_session(session)
    ingredients = ingredient_manager.get_all_ingredients()
    nutrients = nutrient_manager.get_all_nutrients()
    dishes = dish_manager.get_all_dishes()
    return render_template(
        'ingredientSearch.html', 
        user=user,
        nutrients=nutrients,
        dishes=dishes,
        recommendation=ingredients
    )

@ingredients_bp.route('/nutrient', methods=['POST'])
def nutrientFilterController():
    user = user_manager.get_user_by_session(session)
    nutrient = request.form.get('nutrient')
    ingredients_name = nutrient_manager.get_ingredients_by_nutrient(nutrient)
    ingredients = ingredient_manager.get_ingredients_instance(ingredients_name)
    nutrients = nutrient_manager.get_all_nutrients()
    dishes = dish_manager.get_all_dishes()
    return render_template(
        'ingredientSearch.html', 
        user=user, 
        dishes=dishes,
        nutrients=nutrients,
        recommendation=ingredients
    )

@ingredients_bp.route('/dish', methods=['POST'])
def ingredientFilterController():
    user = user_manager.get_user_by_session(session)
    dish = request.form.get('dish')
    ingredients_name = ingredient_manager.get_ingredients_by_dish(dish)
    ingredients = ingredient_manager.get_ingredients_instance(ingredients_name)
    nutrients = nutrient_manager.get_all_nutrients()
    dishes = dish_manager.get_all_dishes()
    return render_template(
        'ingredientSearch.html', 
        user=user, 
        dishes=dishes,
        nutrients=nutrients,
        recommendation=ingredients
    )

@ingredients_bp.route('/<name>', methods=['GET', 'POST'])
def ingredientsListController(name=None):
    user = user_manager.get_user_by_session(session)
    ingredient = ingredient_manager.get_ingredient_instance(name)
    nutrient = nutrient_manager.get_nutrient(name)
    dishes = ingredient_manager.get_dishes_by_ingredient(name)
    nutrients = nutrient_manager.get_all_nutrients()
    return render_template(
        'ingredientDetail.html',
        user=user,
        dishes=dishes,
        ingredient=ingredient,
        nutrient=nutrient,
        nutrients=nutrients
    )

@ingredients_bp.route('/nutrient_review/<name>', methods=['POST'])
@login_required
def nutrientReviewRoute(name=None):
    nutrient = request.form.get('nutrient')
    nutrient_manager.add_nutrient(name, session.get('google_id'), nutrient)
    return redirect(url_for('ingredients.ingredientsListController', name=name))

@ingredients_bp.route('/update_nutrient', methods=['POST'])
def update_nutrient():
    history_id = request.form.get('history_id')
    nutrient = request.form.get('nutrient')
    nutrient_manager.update_nutrient(history_id, nutrient)
    return redirect(url_for('users.history'))