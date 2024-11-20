from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.filter import DishManager

manager = DishManager('csv/dishes.csv')

app = Flask(__name__)

app.secret_key = "your_secret_key"  # Replace with a strong random key

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

users = {"testuser": "password123"}  # Example user credentials (username: password)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password are correct
        if username in users and users[username] == password:
            session['username'] = username  # Store the username in the session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('register'))
        
        users[username] = password  # Add new user to the "database"
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Recommendation route
@app.route('/recommendation', methods=['POST'])
def recommendation():
    criteria = {key: value.lower() for key, value in request.form.items()}
    recommendation = manager.make_recommendation(**criteria)
    return render_template('recommendation.html', recommendation=recommendation)

# 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
