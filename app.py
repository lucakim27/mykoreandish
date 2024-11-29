from flask import Flask, render_template, request, redirect, url_for, session
from utils.dishes import DishManager
from utils.users import get_dish_statistics, getUserById, logout_user, get_logged_in_user, delete_history_function, login_required, rate_dish_function, store_google_user
import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from utils.requests import Requests
import nltk
nltk.download('stopwords')

cred = credentials.Certificate("/etc/secrets/credentials.json") # production
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0' # production

# cred = credentials.Certificate('credentials.json') # local environment
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # local environment

firebase_admin.initialize_app(cred)
db = firestore.client()

dishes_ref = db.collection('Dishes')
users_ref = db.collection('Users')
user_selections_ref = db.collection('UserSelections')
requests_ref = db.collection('Requests')

manager = DishManager(dishes_ref, users_ref, user_selections_ref)

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to='google_login'
)
app.register_blueprint(google_blueprint, url_prefix='/login')

@app.route('/')
def index():
    average_ratings, selection_counts = get_dish_statistics(db)
    user = getUserById(db)
    if user:
        return render_template('index.html', user=user, average_ratings=average_ratings, selection_counts=selection_counts)
    else:
        return render_template('index.html', average_ratings=average_ratings, selection_counts=selection_counts)

@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/oauth2/v1/userinfo')
    assert resp.ok, resp.text
    user_info = resp.json()

    store_google_user(db, user_info)
    session['google_id'] = user_info.get('id')

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/recommendation', methods=['POST'])
def recommendation():
    user = getUserById(db)
    description = request.form.get('description')
    recommendation = manager.make_recommendation(description)
    if user:
        return render_template('recommendation.html', user=user, recommendation=recommendation)
    else:
        return render_template('recommendation.html', recommendation=recommendation)

@app.route('/food/<name>', methods=['GET', 'POST'])
def food(name=None):
    user = getUserById(db)
    dish = manager.get_food_by_name(name)
    if user:
        return render_template('food.html', user=user, dish=dish)
    else:
        return render_template('food.html', dish=dish)

@app.route('/select/<name>', methods=['POST'])
@login_required
def select_food(name=None):
    manager.add_selection(get_logged_in_user(), name)
    return redirect(url_for('index'))

@app.route('/history')
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
    if user:
        return render_template('history.html', user=user, items=history_data)
    else:
        return render_template('history.html', items=history_data)
    
@app.route('/delete_history', methods=['POST'])
def delete_history():
    history_id = request.form.get('history_id')
    if history_id:
        if delete_history_function(db, history_id):
            return redirect(url_for('history'))
    return redirect(url_for('history'))

@app.route('/rate_dish', methods=['POST'])
def rate_dish():
    history_id = request.form.get('history_id')
    rating = request.form.get('rating')

    if rate_dish_function(db, history_id, rating):
        return redirect(url_for('history'))
    return redirect(url_for('history'))

@app.route('/request')
def request_page():
    user = getUserById(db)
    if user:
        return render_template('request.html', user=user)
    else:
        return render_template('request.html')
    
@app.route('/submit-request', methods=['POST'])
def submit_request():
    name = request.form.get('name')
    description = request.form.get('description')
    adjectives = request.form.get('adjective')
    Requests(name, description, adjectives, requests_ref, firestore).add_food_request()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    user = getUserById(db)
    if not user.get('admin', False):  # Ensure the user is an admin
        return "Access Denied", 403

    # Fetch user requests from Firestore
    requests = []
    requests_ref = db.collection('Requests').stream()
    for req in requests_ref:
        req_data = req.to_dict()
        req_data['id'] = req.id  # Add Firestore document ID for deletion
        requests.append(req_data)

    return render_template('admin.html', user=user, requests=requests)

@app.route('/admin/add-food', methods=['POST'])
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


@app.route('/admin/delete-request', methods=['POST'])
def delete_request():
    request_id = request.form.get('id')  # Get the Firestore document ID

    if not request_id:
        # flash('Invalid request ID.', 'error')
        return redirect('/admin')

    # Delete the request from Firestore
    db.collection('Requests').document(request_id).delete()
    # flash('Request deleted successfully!', 'success')
    return redirect('/admin')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)