from flask import Blueprint, render_template, session
from config.db import db
from models.dishes import DishManager
from models.price import PriceManager
from models.users import UserManager
from models.userSelections import UserSelectionManager
from firebase_admin import firestore

home_bp = Blueprint('home', __name__)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)
dish_manager = DishManager(csv_file='csv/dishes.csv')
price_manager = PriceManager(db, firestore)

@home_bp.route('/')
def home():
    user = user_manager.getUserBySession(session)
    dishes = dish_manager.get_all_dishes()
    return render_template(
        'home.html',
        user=user,
        dishes=dishes
    )