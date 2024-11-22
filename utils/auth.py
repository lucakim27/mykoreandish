import sqlite3
from flask import session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os

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