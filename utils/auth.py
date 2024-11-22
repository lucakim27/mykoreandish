import sqlite3
from flask import redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data', 'app.db')

def login_user(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result and check_password_hash(result[0], password):
        session['username'] = username
        flash('Login successful!', 'success')
        return True
    flash('Invalid username or password.', 'error')
    return False

def register_user(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        flash('Registration successful! You can now log in.', 'success')
        return True
    except sqlite3.IntegrityError:
        flash('Username already exists. Please choose another one.', 'error')
        return False
    finally:
        conn.close()

def logout_user():
    session.pop('username', None)
    flash('You have been logged out.', 'info')

def get_logged_in_user():
    return session.get('username')

def delete_history_function(history_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM UserSelections WHERE id = ?", (history_id,))
        conn.commit()
        flash('History item deleted successfully.', 'success')
        return True
    except sqlite3.Error as e:
        flash('An error occurred while deleting the history item.', 'error')
        print(f"SQLite error: {e}")
        return False
    finally:
        conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def rate_dish_function(history_id, rating):
    if not history_id or not rating:
        flash('Invalid input for rating.', 'error')
        return False

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE UserSelections
                SET rating = ?
                WHERE id = ?
            ''', (rating, history_id))
            conn.commit()
            flash('Rating saved successfully!', 'success')
            return True
    except sqlite3.Error as e:
        flash(f'Error saving rating: {e}', 'error')
        return False