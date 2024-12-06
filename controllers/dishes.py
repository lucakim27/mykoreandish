from flask import Blueprint, render_template, request, redirect, session, url_for
from controllers.auth import login_required
from models.dishes import DishManager
from models.users import UserManager
from models.userSelections import UserSelectionManager
from config.db import db
from utils.filters import format_time_ago

dishes_bp = Blueprint('dishes', __name__)
manager = DishManager(db)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db)

@dishes_bp.route('/', methods=['POST'])
def recommendation():
    user = user_manager.getUserBySession(session)
    description = request.form.get('description')
    adjectives = request.form.get('adjectives')
    spiciness = request.form.get('spiciness')
    dietary = request.form.get('dietary')
    ingredients = request.form.get('ingredients')
    recommendation = manager.make_recommendation(description, adjectives, spiciness, dietary, ingredients)
    return render_template('recommendation.html', user=user, recommendation=recommendation)

@dishes_bp.route('/<name>', methods=['POST'])
def food(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    average_ratings, average_prices, selection_counts = selection_manager.get_dish_statistics()
    return render_template('food.html', user=user, dish=dish, average_ratings=average_ratings, average_prices=average_prices, selection_counts=selection_counts)

@dishes_bp.route('/select/<name>', methods=['POST'])
@login_required
def select_food(name=None):
    price = request.form.get('price')
    rating = request.form.get('rating')
    restaurant = request.form.get('restaurant')
    selection_manager.add_selection(session.get('google_id'), name, price, rating, restaurant)
    return redirect(url_for('home.home'))

@dishes_bp.route('/rate_dish', methods=['POST'])
def rate_dish():
    history_id = request.form.get('history_id')
    rating = request.form.get('rating')
    price = request.form.get('price')
    restaurant = request.form.get('restaurant')
    selection_manager.update_review(history_id, rating, price, restaurant)
    return redirect(url_for('users.history'))

@dishes_bp.app_template_filter('time_ago')
def time_ago_filter(timestamp):
    return format_time_ago(timestamp)