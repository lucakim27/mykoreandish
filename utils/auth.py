import sqlite3
from flask import redirect, session, flash, url_for
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

            cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.execute('''
                    UPDATE users
                    SET name = ?, email = ?
                    WHERE google_id = ?
                ''', (name, email, google_id))
            else:
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

def get_dish_average_ratings():
    query = '''
    SELECT Dishes.dish_name, AVG(UserSelections.rating) as average_rating
    FROM UserSelections
    JOIN Dishes ON UserSelections.dish_id = Dishes.id
    GROUP BY UserSelections.dish_id
    ORDER BY average_rating DESC
    '''

    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row  # Use Row factory for dict-like access
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            average_ratings = {row["dish_name"]: row["average_rating"] for row in results}
            return average_ratings
    except sqlite3.Error as e:
        print(f"Error fetching average ratings: {e}")
        return {}

def get_dish_counts():
    query = '''
    SELECT Dishes.dish_name, COUNT(UserSelections.dish_id) as selection_count
    FROM UserSelections
    JOIN Dishes ON UserSelections.dish_id = Dishes.id
    GROUP BY UserSelections.dish_id
    ORDER BY selection_count DESC
    '''

    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row  # Use Row factory for dict-like access
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            dish_counts = {row["dish_name"]: row["selection_count"] for row in results}
            return dish_counts
    except sqlite3.Error as e:
        print(f"Error fetching dish counts: {e}")
        return {}

