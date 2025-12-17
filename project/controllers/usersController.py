from itertools import chain
from ..utils.login import login_required
from flask import Blueprint, g, redirect, render_template, request, url_for
from ..services.managers import (
    selection_manager,
    dietary_manager,
    ingredient_manager,
    aggregate_manager,
    price_manager,
    nutrient_manager,
    user_manager
)


users_bp = Blueprint('users', __name__)

@users_bp.route('/')
@login_required
def history():
    ingredients = ingredient_manager.get_all_ingredients()
    dietaries = dietary_manager.get_all_dietaries()
    nutrients = nutrient_manager.get_all_nutrients()
    locations = price_manager.get_all_locations()
    combined_history = list(chain(
        selection_manager.get_user_history(g.user["google_id"]), 
        dietary_manager.get_dietary_history(g.user["google_id"]), 
        ingredient_manager.get_ingredient_history(g.user["google_id"]),
        nutrient_manager.get_nutrient_history(g.user["google_id"]),
        price_manager.get_price_history(g.user["google_id"])
    ))
    return render_template(
        'history.html', 
        user=g.user,
        combined_history=combined_history,
        ingredients=ingredients,
        dietaries=dietaries,
        nutrients=nutrients,
        locations=locations
    )

@users_bp.route('/delete-history', methods=['POST'])
@login_required
def deleteHistoryRoute():
    history_id = request.form.get('history_id')
    dish_review = selection_manager.get_dish_review_by_id(history_id)
    selection_manager.delete_history(history_id)
    aggregate_manager.delete_aggregate(dish_review)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-dietary', methods=['POST'])
@login_required
def deleteDietaryRoute():
    history_id = request.form.get('history_id')
    dietary = dietary_manager.get_dietary_review_by_id(history_id)
    dietary_manager.delete_dietary(history_id)
    aggregate_manager.delete_dietary_aggregate(dietary)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-ingredient', methods=['POST'])
@login_required
def deleteIngredientRoute():
    history_id = request.form.get('history_id')
    ingredient = ingredient_manager.get_ingredient_review_by_id(history_id)
    ingredient_manager.delete_ingredient(history_id)
    aggregate_manager.delete_ingredient_aggregate(ingredient)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-nutrient', methods=['POST'])
@login_required
def deleteNutrientRoute():
    history_id = request.form.get('history_id')
    nutrient_manager.delete_nutrient(history_id)
    return redirect(url_for('users.history'))

@users_bp.route('/delete-price', methods=['POST'])
@login_required
def deletePriceRoute():
    history_id = request.form.get('history_id')
    price_manager.delete_price(history_id)
    return redirect(url_for('users.history'))

@users_bp.route('/profile')
def profile():
    dietaries = dietary_manager.get_all_dietaries()
    return render_template('profile.html', user=g.user, dietaries=dietaries)

@users_bp.route('/list', methods=['POST'])
def userList():
    users = user_manager.get_all_users()
    return render_template('userList.html', user=g.user, users=users)

@users_bp.route('/user/<user_id>', methods=['GET'])
def userProfileController(user_id):
    profile_user = user_manager.get_user_by_id(user_id)
    if profile_user is None:
        return redirect(url_for('users.userList'))
    return render_template('userProfile.html', user=g.user, profile_user=profile_user)

@users_bp.route('/updateDietaryPreference', methods=['POST'])
@login_required
def updateDietaryPreference():
    dietary_preference = request.form.get('dietary_preference')
    user_manager.update_dietary(g.user, dietary_preference)
    return redirect(url_for('users.profile'))