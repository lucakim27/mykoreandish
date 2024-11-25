from flask import Flask, render_template, request, redirect, url_for, session
from utils.dish import DishManager
from utils.user import get_dish_statistics, get_username, logout_user, get_logged_in_user, delete_history_function, login_required, rate_dish_function, store_google_user
import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/etc/secrets/credentials.json") # production
# cred = credentials.Certificate('credentials.json') # local environment

firebase_admin.initialize_app(cred)
db = firestore.client()

dishes_ref = db.collection('Dishes')
users_ref = db.collection('Users')
user_selections_ref = db.collection('UserSelections')

manager = DishManager(dishes_ref, users_ref, user_selections_ref)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0' # production
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # local environment

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
    username = get_username(db)
    return render_template('index.html', username=username, average_ratings=average_ratings, selection_counts=selection_counts)

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
    username = get_username(db)
    criteria = {key: value.lower() for key, value in request.form.items()}
    recommendation = manager.make_recommendation(**criteria)
    return render_template('recommendation.html', username=username, recommendation=recommendation)

@app.route('/food/<name>', methods=['GET', 'POST'])
@login_required
def food(name=None):
    username = get_username(db)
    dish = manager.get_food_by_name(name)
    manager.add_selection(get_logged_in_user(), name)
    return render_template('food.html', username=username, dish=dish)

@app.route('/history')
def history():
    username = get_username(db)
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
    return render_template('history.html', username=username, items=history_data)

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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)