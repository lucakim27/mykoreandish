from flask import session, flash

users = {"admin": "123"}

def login_user(username, password):
    if username in users and users[username] == password:
        session['username'] = username
        flash('Login successful!', 'success')
        return True
    flash('Invalid username or password.', 'error')
    return False

def register_user(username, password):
    if username in users:
        flash('Username already exists. Please choose another one.', 'error')
        return False
    users[username] = password
    flash('Registration successful! You can now log in.', 'success')
    return True

def logout_user():
    session.pop('username', None)
    flash('You have been logged out.', 'info')

def get_logged_in_user():
    return session.get('username')

def fetch_user_history(username):
    return username