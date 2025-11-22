from flask import Blueprint, redirect, request, url_for
from ..models.requestModel import RequestManager
from ..models.userModel import UserManager
from firebase_admin import firestore

request_bp = Blueprint('request', __name__)
request_manager = RequestManager(firestore)
user_manager = UserManager()

@request_bp.route('/submit-request', methods=['POST'])
def submit_request():
    name = request.form.get('name')
    description = request.form.get('description')
    request_manager.add_food_request(name, description)
    return redirect(url_for('home.home'))