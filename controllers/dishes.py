from flask import Blueprint, render_template, request, redirect, session, url_for
from controllers.auth import login_required
from models.dietary import DietaryManager
from models.dishes import DishManager
from models.price import PriceManager
from models.users import UserManager
from models.userSelections import UserSelectionManager
from config.db import db
from utils.filters import format_time_ago
from firebase_admin import firestore

dishes_bp = Blueprint('dishes', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)
price_manager = PriceManager(db, firestore)
dietary_manager = DietaryManager(db, firestore)

@dishes_bp.route('/', methods=['POST'])
def recommendation():
    user = user_manager.getUserBySession(session)
    description = request.form.get('description')
    recommendation = manager.make_recommendation(description)
    return render_template(
        'recommendation.html', 
        user=user, 
        recommendation=recommendation
    )

@dishes_bp.route('/filter', methods=['POST'])
def filtering():
    user = user_manager.getUserBySession(session)
    recommendation = manager.filter_recommendation()
    return render_template(
        'recommendation.html', 
        user=user, 
        recommendation=recommendation
    )

@dishes_bp.route('/<name>', methods=['POST'])
def food(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    prices = price_manager.get_price(name)
    dietaries = dietary_manager.getDietary(name)
    average_ratings, selection_counts, average_spiciness, average_sweetness, average_texture, average_healthiness, average_sourness, average_temperature = selection_manager.get_dish_statistics()
    return render_template(
        'food.html', 
        prices=prices, 
        user=user, 
        dish=dish, 
        average_ratings=average_ratings, 
        selection_counts=selection_counts, 
        average_spiciness=average_spiciness, 
        average_sweetness=average_sweetness, 
        average_texture=average_texture, 
        average_healthiness=average_healthiness, 
        average_sourness=average_sourness,
        dietaries=dietaries,
        average_temperature=average_temperature
    )

@dishes_bp.route('/select/<name>', methods=['POST'])
@login_required
def select_food(name=None):
    spiciness = request.form.get('spiciness')
    sweetness = request.form.get('sweetness')
    sourness = request.form.get('sourness')
    texture = request.form.get('texture')
    temperature = request.form.get('temperature')
    healthiness = request.form.get('healthiness')
    rating = request.form.get('rating')
    selection_manager.add_selection(session.get('google_id'), name, spiciness, sweetness, sourness, texture, temperature, healthiness, rating)
    return redirect(url_for('home.home'))

@dishes_bp.route('/price_review/<name>', methods=['POST'])
@login_required
def priceReviewRoute(name=None):
    price = request.form.get('price')
    currency = request.form.get('currency')
    price_manager.add_price(session.get('google_id'), name, price, currency)
    return redirect(url_for('home.home'))

@dishes_bp.route('/dietary_review/<name>', methods=['POST'])
@login_required
def dietaryReviewRoute(name=None):
    dietary = request.form.get('dietary')
    dietary_manager.addDietary(name, session.get('google_id'), dietary)
    return redirect(url_for('home.home'))

@dishes_bp.route('/rate_dish', methods=['POST'])
def rate_dish():
    history_id = request.form.get('history_id')
    spiciness = request.form.get('spiciness')
    sweetness = request.form.get('sweetness')
    sourness = request.form.get('sourness')
    texture = request.form.get('texture')
    temperature = request.form.get('temperature')
    healthiness = request.form.get('healthiness')
    rating = request.form.get('rating')
    selection_manager.update_review(history_id, spiciness, sweetness, sourness, texture, temperature, healthiness, rating)
    return redirect(url_for('users.history'))

@dishes_bp.route('/update_price', methods=['POST'])
def update_price():
    history_id = request.form.get('history_id')
    price = request.form.get('price')
    currency = request.form.get('currency')
    price_manager.update_price(history_id, price, currency)
    return redirect(url_for('users.history'))

@dishes_bp.route('/update_dietary', methods=['POST'])
def update_dietary():
    history_id = request.form.get('history_id')
    dietary = request.form.get('dietary')
    dietary_manager.update_dietary(history_id, dietary)
    return redirect(url_for('users.history'))

@dishes_bp.app_template_filter('time_ago')
def time_ago_filter(timestamp):
    return format_time_ago(timestamp)