from flask import Flask, render_template
from models.users import get_dish_statistics, getUserById
import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint
from controllers.auth import auth_bp
from controllers.dishes import dishes_bp
from controllers.users import users_bp
from controllers.admin import admin_bp
from controllers.request import request_bp
from config.db import db
import nltk
nltk.download('stopwords')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0' # production
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # local environment

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to='auth_bp.google_login'
)
app.register_blueprint(google_blueprint, url_prefix='/login')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dishes_bp, url_prefix='/dishes')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(request_bp, url_prefix='/request')

@app.route('/')
def index():
    user = getUserById(db)
    print(user)
    average_ratings, selection_counts = get_dish_statistics(db)
    if user:
        return render_template('index.html', user=user, average_ratings=average_ratings, selection_counts=selection_counts)
    else:
        return render_template('index.html', average_ratings=average_ratings, selection_counts=selection_counts)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)