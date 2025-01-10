from flask import Blueprint, redirect, render_template, request, session, url_for
from config.db import db
from models.requestsModel import RequestsManager
from models.usersModel import UserManager
from firebase_admin import firestore

request_bp = Blueprint('request', __name__)
request_manager = RequestsManager(db, firestore)
user_manager = UserManager(db)

@request_bp.route('/')
def request_page():
    user = user_manager.get_user_by_session(session)
    return render_template('request.html', user=user)

@request_bp.route('/submit-request', methods=['POST'])
def submit_request():
    name = request.form.get('name')
    description = request.form.get('description')
    request_manager.add_food_request(name, description)
    return redirect(url_for('home.home'))