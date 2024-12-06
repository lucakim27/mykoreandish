from flask import Blueprint, render_template, session
from config.db import db
from models.dishes import DishManager
from models.users import UserManager
from models.userSelections import UserSelectionManager

home_bp = Blueprint('home', __name__)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db)
dish_manager = DishManager(db)

@home_bp.route('/')
def home():
    user = user_manager.getUserBySession(session)
    adjectives, spiciness, dietary, ingredients = dish_manager.filter_criteria()
    average_ratings, average_prices, selection_counts = selection_manager.get_dish_statistics()
    return render_template(
        'home.html',
        user=user,
        adjectives=adjectives,
        spiciness=spiciness,
        dietary=dietary,
        ingredients=ingredients,
        average_ratings=average_ratings,
        selection_counts=selection_counts,
        average_prices=average_prices
    )