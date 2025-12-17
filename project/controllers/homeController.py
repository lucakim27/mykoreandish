from flask import Blueprint, g, render_template
from ..services.managers import (
    dish_manager,
    dietary_manager,
    ingredient_manager,
    aggregate_manager,
    nutrient_manager,
    user_manager
)

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/api/home')
def home_api():
    dishes = dish_manager.get_all_dishes_in_dictionary()
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    dietary_total, ingredient_total, total_reviews, price_reviews, nutrients_reviews = aggregate_manager.get_all_stats()
    nutrients_count = nutrient_manager.get_nutrients_count()
    total_users = user_manager.get_total_users()
    return {
        "user": g.user,
        "dishes": dishes,
        "ingredients": ingredients,
        "dietaries": dietaries,
        "total_reviews": total_reviews,
        "dietary_total": dietary_total,
        "ingredient_total": ingredient_total,
        "nutrients_count": nutrients_count,
        "total_users": total_users,
        "price_reviews": price_reviews,
        "nutrients_reviews": nutrients_reviews
    }