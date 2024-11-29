from flask import Blueprint, redirect, render_template, request, url_for
from config.db import db
from models.requests import Requests
from models.users import getUserById
from firebase_admin import firestore

request_bp = Blueprint('request', __name__)

requests_ref = db.collection('Requests')

@request_bp.route('/')
def request_page():
    user = getUserById(db)
    if user:
        return render_template('request.html', user=user)
    else:
        return render_template('request.html')

@request_bp.route('/submit-request', methods=['POST'])
def submit_request():
    name = request.form.get('name')
    description = request.form.get('description')
    adjectives = request.form.get('adjective')
    Requests(name, description, adjectives, requests_ref, firestore).add_food_request()
    return redirect(url_for('index'))