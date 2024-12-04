from flask import Blueprint, render_template, request, redirect, session, url_for
from controllers.auth import login_required
from models.dishes import DishManager
from models.users import UserManager
from models.userSelections import UserSelectionManager
from config.db import db

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
    return render_template('food.html', user=user, dish=dish)

@dishes_bp.route('/select/<name>', methods=['POST'])
@login_required
def select_food(name=None):
    selection_manager.add_selection(session.get('google_id'), name)
    return redirect(url_for('home.home'))

@dishes_bp.route('/rate_dish', methods=['POST'])
def rate_dish():
    history_id = request.form.get('history_id')
    rating = request.form.get('rating')
    selection_manager.rate_dish(history_id, rating)
    return redirect(url_for('users.history'))