from flask import Blueprint, render_template, request, redirect, session
from config.db import db
from models.aggregateModel import AggregateManager
from models.dishModel import DishManager
from models.requestModel import RequestManager
from models.userModel import UserManager
from firebase_admin import firestore
from utils.admin import admin_required

admin_bp = Blueprint('admin', __name__)
request_manager = RequestManager(db, firestore)
user_manager = UserManager(db)
dish_manager = DishManager(csv_file='csv/dishes.csv')
aggregate_manager = AggregateManager(db)

@admin_bp.route('/')
@admin_required
def admin_panel():
    user = user_manager.get_user_by_session(session)
    requests = request_manager.get_food_request()
    return render_template('admin.html', user=user, requests=requests)

@admin_bp.route('/delete-request', methods=['POST'])
@admin_required
def delete_request():
    request_id = request.form.get('id')
    request_manager.delete_request(request_id)
    return redirect('/admin')