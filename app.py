from flask import Flask, render_template, request, redirect, url_for, session
from utils.dish import DishManager
from utils.auth import login_user, register_user, logout_user, get_logged_in_user
from utils.db import create_tables
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
manager = DishManager()

@app.route('/')
def index():
    username = get_logged_in_user()
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect(url_for('login'))
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/recommendation', methods=['POST'])
def recommendation():
    criteria = {key: value.lower() for key, value in request.form.items()}
    recommendation = manager.make_recommendation(**criteria)
    return render_template('recommendation.html', recommendation=recommendation)

@app.route('/food/<name>', methods=['POST'])
def food(name=None):
    dish = manager.get_food_by_name(name)  # Fetch dish by name from database
    manager.add_selection(get_logged_in_user(), name)
    return render_template('food.html', dish=dish)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_history = manager.get_user_history(username)

    history_data = [{'dish_name': record[0], 'timestamp': record[1]} for record in user_history]
    return render_template('history.html', items=history_data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '_main_':
    create_tables()
    app.run(host='0.0.0.0', port=80)