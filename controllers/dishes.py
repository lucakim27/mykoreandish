from flask import Blueprint, render_template, request, redirect, url_for
from models.dishes import DishManager
from models.users import get_logged_in_user, getUserById, login_required, rate_dish_function
from config.db import db

dishes_bp = Blueprint('dishes', __name__)

dishes_ref = db.collection('Dishes')
users_ref = db.collection('Users')
user_selections_ref = db.collection('UserSelections')

manager = DishManager(dishes_ref, users_ref, user_selections_ref)

@dishes_bp.route('/', methods=['POST'])
def recommendation():
    user = getUserById(db)
    print(user)
    description = request.form.get('description')
    recommendation = manager.make_recommendation(description)
    if user:
        return render_template('recommendation.html', user=user, recommendation=recommendation)
    else:
        return render_template('recommendation.html', recommendation=recommendation)

@dishes_bp.route('/<name>', methods=['POST'])
@login_required
def food(name=None):
    user = getUserById(db)
    print(user)
    dish = manager.get_food_by_name(name)
    if user:
        return render_template('food.html', user=user, dish=dish)
    else:
        return render_template('food.html', dish=dish)

@dishes_bp.route('/select/<name>', methods=['POST'])
@login_required
def select_food(name=None):
    manager.add_selection(get_logged_in_user(), name)
    return redirect(url_for('index'))

@dishes_bp.route('/rate_dish', methods=['POST'])
def rate_dish():
    history_id = request.form.get('history_id')
    rating = request.form.get('rating')

    if rate_dish_function(db, history_id, rating):
        return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))