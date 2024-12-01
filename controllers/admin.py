from flask import Blueprint, render_template, request, redirect, session
from config.db import db
from models.dishes import DishManager
from models.requests import RequestsManager
from models.users import UserManager
from firebase_admin import firestore

admin_bp = Blueprint('admin', __name__)
request_manager = RequestsManager(db, firestore)
user_manager = UserManager(db)
dish_manager = DishManager(db)

@admin_bp.route('/')
def admin_panel():
    user = user_manager.getUserBySession(session)
    requests = request_manager.get_food_request(user)
    return render_template('admin.html', user=user, requests=requests)

@admin_bp.route('/add-food', methods=['POST'])
def add_food():
    dish_name = request.form.get('dish_name')
    description = request.form.get('description')
    adjectives = request.form.getlist('adjectives[]')
    dish_manager.add_dish(dish_name, description, adjectives)
    return redirect('/admin')

@admin_bp.route('/delete-request', methods=['POST'])
def delete_request():
    request_id = request.form.get('id')  # Get the Firestore document ID
    request_manager.delete_request(request_id)
    return redirect('/admin')
