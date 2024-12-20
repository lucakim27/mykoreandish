from flask import Blueprint, redirect, render_template, request, session, url_for
from controllers.auth import login_required
from models.dishes import DishManager
from models.price import PriceManager
from models.users import UserManager
from models.userSelections import UserSelectionManager
from config.db import db
from firebase_admin import firestore

users_bp = Blueprint('users', __name__)
manager = DishManager(csv_file='csv/dishes.csv')
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db, firestore)
price_manager = PriceManager(db, firestore)

@users_bp.route('/')
@login_required
def history():
    user = user_manager.getUserBySession(session)
    price_history = price_manager.get_price_history(session['google_id'])
    user_history = selection_manager.get_user_history(session['google_id'])
    return render_template('history.html', user=user, items=user_history, price_history=price_history)

@users_bp.route('/delete-history', methods=['POST'])
def deleteHistoryRoute():
    history_id = request.form.get('history_id')
    if history_id:
        if selection_manager.delete_history(history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))

@users_bp.route('/delete-price', methods=['POST'])
def deletePriceRoute():
    history_id = request.form.get('history_id')
    if history_id:
        if price_manager.delete_price(history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))
