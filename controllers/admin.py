from flask import Blueprint, render_template, request, redirect
from config.db import db
from models.users import getUserById

admin_bp = Blueprint('admin', __name__)
requests_ref = db.collection('Requests')

@admin_bp.route('/')
def admin_panel():
    user = getUserById(db)
    print(user)
    if not user.get('admin', False):
        return "Access Denied", 403

    requests = []
    requests_ref = db.collection('Requests').stream()
    for req in requests_ref:
        req_data = req.to_dict()
        req_data['id'] = req.id
        requests.append(req_data)

    return render_template('admin.html', user=user, requests=requests)

@admin_bp.route('/add-food', methods=['POST'])
def add_food():
    # Retrieve data from the form
    dish_name = request.form.get('dish_name')
    description = request.form.get('description')
    adjectives = request.form.getlist('adjectives[]')  # This retrieves all adjectives as a list

    # Validate the inputs
    if not dish_name or not description or not adjectives:
        # flash('All fields are required!', 'error')
        return redirect('/admin')

    # Add the food item to the Firestore 'foods' collection
    db.collection('Dishes').add({
        'dish_name': dish_name,
        'description': description,
        'adjectives': adjectives  # Store adjectives as a list
    })

    # flash('Food added successfully!', 'success')
    return redirect('/admin')

@admin_bp.route('/delete-request', methods=['POST'])
def delete_request():
    request_id = request.form.get('id')  # Get the Firestore document ID

    if not request_id:
        # flash('Invalid request ID.', 'error')
        return redirect('/admin')

    # Delete the request from Firestore
    db.collection('Requests').document(request_id).delete()
    # flash('Request deleted successfully!', 'success')
    return redirect('/admin')
