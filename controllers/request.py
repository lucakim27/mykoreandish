from flask import Blueprint, redirect, render_template, request, session, url_for
from config.db import db
from models.requests import RequestsManager
from models.users import UserManager
from firebase_admin import firestore

request_bp = Blueprint('request', __name__)
manager = RequestsManager(db, firestore)
user_manager = UserManager(db)

@request_bp.route('/')
def request_page():
    user = user_manager.getUserBySession(session)
    return render_template('request.html', user=user)

@request_bp.route('/submit-request', methods=['POST'])
def submit_request():
    name = request.form.get('name')
    description = request.form.get('description')
    adjectives = request.form.get('adjective')
    manager.add_food_request(name, description, adjectives)
    return redirect(url_for('home.home'))