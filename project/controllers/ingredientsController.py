from flask import Blueprint, g, redirect, render_template, request, session, url_for
from ..models.dishModel import DishManager
from ..models.favoriteModel import FavoriteManager
from ..models.ingredientModel import IngredientManager
from firebase_admin import firestore
from ..models.noteModel import NoteManager
from ..models.nutrientModel import NutrientManager
from ..models.userModel import UserManager
from ..utils.login import login_required

ingredients_bp = Blueprint('ingredients', __name__)
ingredient_manager = IngredientManager(firestore)
user_manager = UserManager()
nutrient_manager = NutrientManager(firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')
favorite_manager = FavoriteManager(firestore)
note_manager = NoteManager(firestore)

@ingredients_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

@ingredients_bp.route('/<name>', methods=['GET', 'POST'])
def ingredientsListController(name=None):
    ingredient = ingredient_manager.get_ingredient_instance(name)
    nutrient = nutrient_manager.get_nutrient(name)
    dishes = ingredient_manager.get_dishes_by_ingredient(name)
    nutrients = nutrient_manager.get_all_nutrients()
    favorites = favorite_manager.get_all_favorites(g.user)
    note = note_manager.get_note_by_dish_and_user(name, g.user["google_id"]) if g.user else None
    return render_template(
        'ingredient.html',
        user=g.user,
        dishes=dishes,
        ingredient=ingredient,
        nutrient=nutrient,
        nutrients=nutrients,
        favorites=favorites,
        note=note
    )

@ingredients_bp.route('/nutrient_review/<name>', methods=['POST'])
@login_required
def nutrientReviewRoute(name=None):
    nutrient = request.form.get('nutrient')
    nutrient_manager.add_nutrient(name, g.user["google_id"], nutrient)
    return redirect(url_for('ingredients.ingredientsListController', name=name))

@ingredients_bp.route('/update_nutrient', methods=['POST'])
@login_required
def update_nutrient():
    history_id = request.form.get('history_id')
    nutrient = request.form.get('nutrient')
    nutrient_manager.update_nutrient(history_id, nutrient)
    return redirect(url_for('users.history'))