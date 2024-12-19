from flask import Blueprint, render_template, session
from config.db import db
from models.dishes import DishManager
from models.price import PriceManager
from models.users import UserManager
from models.userSelections import UserSelectionManager
from firebase_admin import firestore

home_bp = Blueprint('home', __name__)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)
dish_manager = DishManager(db)
price_manager = PriceManager(db, firestore)

@home_bp.route('/')
def home():
    user = user_manager.getUserBySession(session)
    total_price_length = price_manager.total_review_len()
    adjectives, spiciness, dietary, ingredients = dish_manager.filter_criteria()
    dishes = dish_manager.get_all_dishes()
    average_ratings, selection_counts, average_spiciness, average_sweetness, average_texture, average_healthiness, average_sourness = selection_manager.get_dish_statistics()
    return render_template(
        'home.html',
        user=user,
        dishes=dishes,
        adjectives=adjectives,
        spiciness=spiciness,
        dietary=dietary,
        ingredients=ingredients,
        total_price_length=total_price_length,
        selection_counts=selection_counts,
    )