from flask import Blueprint, redirect, request, url_for
from config.db import db
from models.requestModel import RequestManager
from models.userModel import UserManager
from firebase_admin import firestore

request_bp = Blueprint('request', __name__)
request_manager = RequestManager(db, firestore)
user_manager = UserManager(db)

@request_bp.route('/submit-request', methods=['POST'])
def submit_request():
    name = request.form.get('name')
    description = request.form.get('description')
    request_manager.add_food_request(name, description)
    return redirect(url_for('home.home'))