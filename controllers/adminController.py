from flask import Blueprint, render_template, request, redirect, session
from config.db import db
from models.dishModel import DishManager
from models.requestModel import RequestManager
from models.userModel import UserManager
from firebase_admin import firestore

admin_bp = Blueprint('admin', __name__)
request_manager = RequestManager(db, firestore)
user_manager = UserManager(db)
dish_manager = DishManager(csv_file='csv/dishes.csv')

@admin_bp.route('/')
def admin_panel():
    user = user_manager.get_user_by_session(session)
    if not user or not user.get('admin', False):
            return "Access Denied", 403
    requests = request_manager.get_food_request()
    return render_template('admin.html', user=user, requests=requests)

@admin_bp.route('/add-food', methods=['POST'])
def add_food():
    user = user_manager.get_user_by_session(session)
    if not user or not user.get('admin', False):
            return "Access Denied", 403
    dish_name = request.form.get('dish_name')
    description = request.form.get('description')
    korean_name = request.form.getlist('korean_name')
    dish_manager.add_dish(dish_name, description, korean_name)
    return redirect('/admin')

@admin_bp.route('/delete-request', methods=['POST'])
def delete_request():
    user = user_manager.get_user_by_session(session)
    if not user or not user.get('admin', False):
            return "Access Denied", 403
    request_id = request.form.get('id')
    request_manager.delete_request(request_id)
    return redirect('/admin')
