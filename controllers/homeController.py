from flask import Blueprint, render_template, session
from config.db import db
from models.dietaryModel import DietaryManager
from models.dishesModel import DishManager
from models.ingredientModel import IngredientManager
from models.priceModel import PriceManager
from models.usersModel import UserManager
from models.userSelectionsModel import UserSelectionManager
from firebase_admin import firestore

home_bp = Blueprint('home', __name__)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')
price_manager = PriceManager(db, firestore)
ingredient_manager = IngredientManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)

@home_bp.route('/')
def home():
    user = user_manager.get_user_by_session(session)
    dishes = dish_manager.get_all_dishes()
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    return render_template(
        'home.html',
        user=user,
        dishes=dishes,
        ingredients=ingredients,
        dietaries=dietaries
    )