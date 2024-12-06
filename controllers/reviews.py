from flask import Blueprint, render_template, session
from config.db import db
from models.dishes import DishManager
from models.userSelections import UserSelectionManager
from models.users import UserManager

reviews_bp = Blueprint('reviews', __name__)
manager = DishManager(db)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db)

@reviews_bp.route('/<name>', methods=['POST'])
def reviewController(name=None):
    user = user_manager.getUserBySession(session)
    dish = manager.get_dish_instance(name)
    return render_template('review.html', user=user, dish=dish)