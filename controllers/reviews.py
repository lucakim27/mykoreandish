from flask import Blueprint, render_template, session
from config.db import db
from models.dishes import DishManager
from models.userSelections import UserSelectionManager
from models.users import UserManager
from utils.location import fetch_geoapify_data
from firebase_admin import firestore

reviews_bp = Blueprint('reviews', __name__)
manager = DishManager(db)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)

@reviews_bp.route('/<name>', methods=['POST'])
def reviewController(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    return render_template('review.html', user=user, dish=dish)

@reviews_bp.route('/price/<name>', methods=['POST'])
def priceController(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    region_text, price_placeholder = fetch_geoapify_data()
    return render_template('price.html', user=user, dish=dish, region_text=region_text, price_placeholder=price_placeholder)