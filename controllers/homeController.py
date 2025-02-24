from flask import Blueprint, render_template, session
from config.db import db
# from models.aggregateModel import AggregateManager
from models.dietaryModel import DietaryManager
from models.dishModel import DishManager
from models.ingredientModel import IngredientManager
from models.userModel import UserManager
from models.tasteModel import TasteManager
from firebase_admin import firestore
# from controllers.dishesController import cache_manager

home_bp = Blueprint('home', __name__)
user_manager = UserManager(db)
selection_manager = TasteManager(db, firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')
ingredient_manager = IngredientManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)
# aggregate_manager = AggregateManager(db)

@home_bp.route('/')
def home():
    user = user_manager.get_user_by_session(session)
    dishes = dish_manager.get_all_dishes()
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    # top_aspects = aggregate_manager.get_top_n_by_aspect(top_n=3)
    return render_template(
        'home.html',
        user=user,
        dishes=dishes,
        ingredients=ingredients,
        dietaries=dietaries
        # top_dishes=top_aspects.get('total_reviews', []),
        # top_spicy=top_aspects.get('spiciness', []),
        # top_sweet=top_aspects.get('sweetness', []),
        # top_sour=top_aspects.get('sourness', []),
        # top_healthy=top_aspects.get('healthiness', []),
        # top_temperature=top_aspects.get('temperature', []),
        # top_rating=top_aspects.get('rating', []),
        # top_texture=top_aspects.get('texture', [])
    )