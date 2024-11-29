from flask import Blueprint, redirect, render_template, request, session, url_for
from models.dishes import DishManager
from models.users import delete_history_function, getUserById
from config.db import db

users_bp = Blueprint('users', __name__)

dishes_ref = db.collection('Dishes')
users_ref = db.collection('Users')
user_selections_ref = db.collection('UserSelections')

manager = DishManager(dishes_ref, users_ref, user_selections_ref)

@users_bp.route('/')
def history():
    user = getUserById(db)
    if 'google_id' not in session:
        return redirect(url_for('login'))
    google_id = session['google_id']
    user_history = manager.get_user_history(google_id)
    history_data = [{
        'id': selection.get('id'), 
        'dish_name': selection.get('dish_name'), 
        'timestamp': selection.get('timestamp'), 
        'rating': selection.get('rating')
    } for selection in user_history]
    print(user)
    if user:
        return render_template('history.html', user=user, items=history_data)
    else:
        return render_template('history.html', items=history_data)

@users_bp.route('/delete-history', methods=['POST'])
def delete_history():
    history_id = request.form.get('history_id')
    if history_id:
        if delete_history_function(db, history_id):
            return redirect(url_for('users.history'))
    return redirect(url_for('users.history'))

@users_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
