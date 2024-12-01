from flask import Blueprint, redirect, render_template, request, session, url_for
from controllers.auth import login_required
from models.dishes import DishManager
from models.users import UserManager
from models.userSelections import UserSelectionManager
from config.db import db

users_bp = Blueprint('users', __name__)
manager = DishManager(db)
user_manager = UserManager(db)
selection_manager = UserSelectionManager(db)

@users_bp.route('/')
@login_required
def history():
    user = user_manager.getUserBySession(session)
    user_history = selection_manager.get_user_history(session['google_id'])
    return render_template('history.html', user=user, items=user_history)

@users_bp.route('/delete-history', methods=['POST'])
def deleteHistoryRoute():
    history_id = request.form.get('history_id')
    if history_id:
        if selection_manager.delete_history(history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))
