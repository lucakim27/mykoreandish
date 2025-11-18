from functools import wraps
from flask import session
from models.userModel import UserManager
from config.db import db

user_manager = UserManager(db)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = user_manager.get_user_by_id(session.get('google_id'))
        if not user or not user.get("admin", False):
            return "Access Denied", 403
        return f(*args, **kwargs)
    return decorated_function
