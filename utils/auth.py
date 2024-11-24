import sqlite3
from flask import redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data', 'app.db')

def store_google_user(google_user_data):
    google_id = google_user_data.get('id')
    name = google_user_data.get('name')
    email = google_user_data.get('email')

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Check if the user already exists
            cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                # If user exists, update their info (if necessary)
                cursor.execute('''
                    UPDATE users
                    SET name = ?, email = ?
                    WHERE google_id = ?
                ''', (name, email, google_id))
            else:
                # If user doesn't exist, insert new user
                cursor.execute('''
                    INSERT INTO users (username, google_id, email, name)
                    VALUES (?, ?, ?, ?)
                ''', (name, google_id, email, name))

            conn.commit()

    except sqlite3.Error as e:
        print(f"Error storing user: {e}")

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
            return redirect(url_for('google.login'))
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