from flask import Blueprint, g, render_template, session
from config.db import db
from models.aggregateModel import AggregateManager
from models.userModel import UserManager
from models.ingredientModel import IngredientManager
from firebase_admin import firestore as firestore_module
from models.dishModel import DishManager

insight_bp = Blueprint('insight', __name__)
user_manager = UserManager(db)
aggregate_manager = AggregateManager(db)
ingredient_manager = IngredientManager(db, firestore_module)
dish_manager = DishManager(csv_file='csv/dishes.csv')

@insight_bp.before_request
def load_user():
    user_id = session.get('google_id')
    g.user = user_manager.get_user_by_id(user_id) if user_id else None

@insight_bp.route('/', methods=['POST'])
def insight_page():
    top_five = aggregate_manager.get_top_five()
    return render_template('insight.html', user=g.user, top_ingredients=top_five['top_ingredients'], top_dishes=top_five['top_dishes'])