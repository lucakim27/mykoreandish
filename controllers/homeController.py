from flask import Blueprint, render_template, session
from config.db import db
from models.dietaryModel import DietaryManager
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
from models.userModel import UserManager
from models.tasteModel import TasteManager
from firebase_admin import firestore
from controllers.dishesController import cache_manager

home_bp = Blueprint('home', __name__)
user_manager = UserManager(db)
selection_manager = TasteManager(db, firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')
ingredient_manager = IngredientManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)

@home_bp.route('/')
def home():
    user = user_manager.get_user_by_session(session)
    dishes = dish_manager.get_all_dishes()
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    top_spicy = cache_manager.get_top_spicy(3)  # Get top 3 spicy dishes
    top_sweet = cache_manager.get_top_sweet(3)  # Get top 3 sweet dishes
    top_sour = cache_manager.get_top_sour(3)    # Get top 3 sour dishes
    top_healthy = cache_manager.get_top_healthy(3)  # Get top 3 healthy dishes
    top_temperature = cache_manager.get_top_temperature(3)  # Get top 3 temperature dishes
    top_rating = cache_manager.get_top_rating(3)  # Get top 3 rated dishes
    top_texture = cache_manager.get_top_texture(3)  # Get top 3 texture dishes
    return render_template(
        'home.html',
        user=user,
        dishes=dishes,
        ingredients=ingredients,
        dietaries=dietaries,
        top_spicy=top_spicy,
        top_sweet=top_sweet,
        top_sour=top_sour,
        top_healthy=top_healthy,
        top_temperature=top_temperature,
        top_rating=top_rating,
        top_texture=top_texture
    )