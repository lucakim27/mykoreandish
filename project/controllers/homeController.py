from flask import Blueprint, g, render_template, session
from ..models.aggregateModel import AggregateManager
from ..models.dietaryModel import DietaryManager
from ..models.dishModel import DishManager
from ..models.ingredientModel import IngredientManager
from ..models.nutrientModel import NutrientManager
from ..models.userModel import UserManager
from ..models.tasteModel import TasteManager
from firebase_admin import firestore

home_bp = Blueprint('home', __name__)
user_manager = UserManager()
selection_manager = TasteManager(firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')
ingredient_manager = IngredientManager(firestore)
dietary_manager = DietaryManager(firestore)
aggregate_manager = AggregateManager()
nutrient_manager = NutrientManager(firestore)

@home_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

@home_bp.route('/')
def home():
    dishes = dish_manager.get_all_dishes_in_dictionary()
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    dietary_total, ingredient_total, total_reviews, price_reviews, nutrients_reviews = aggregate_manager.get_all_stats()
    nutrients_count = nutrient_manager.get_nutrients_count()
    total_users = user_manager.get_total_users()
    return render_template(
        'home.html',
        user=g.user,
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