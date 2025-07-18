from flask import Blueprint, render_template, session
from config.db import db
from models.aggregateModel import AggregateManager
from models.dietaryModel import DietaryManager
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
from models.nutrientModel import NutrientManager
from models.userModel import UserManager
from models.tasteModel import TasteManager
from firebase_admin import firestore

home_bp = Blueprint('home', __name__)
user_manager = UserManager(db)
selection_manager = TasteManager(db, firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')
ingredient_manager = IngredientManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)
aggregate_manager = AggregateManager(db)
nutrient_manager = NutrientManager(db, firestore)

@home_bp.route('/')
def home():
    user = user_manager.get_user_by_session(session)
    dishes = dish_manager.get_all_dishes_in_dictionary()
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    dietary_total, ingredient_total, total_reviews, price_reviews, nutrients_reviews = aggregate_manager.get_all_stats()
    nutrients_count = nutrient_manager.get_nutrients_count()
    total_users = user_manager.get_total_users()
    return render_template(
        'home.html',
        user=user,
        dishes=dishes,
        ingredients=ingredients,
        dietaries=dietaries,
        total_reviews=total_reviews,
        dietary_total=dietary_total,
        ingredient_total=ingredient_total,
        nutrients_count=nutrients_count,
        total_users=total_users,
        price_reviews=price_reviews,
        nutrients_reviews=nutrients_reviews
    )