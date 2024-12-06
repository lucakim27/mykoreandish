from flask import Flask
import os
from flask_dance.contrib.google import make_google_blueprint
from controllers.auth import auth_bp
from controllers.dishes import dishes_bp
from controllers.users import users_bp
from controllers.admin import admin_bp
from controllers.request import request_bp
from controllers.home import home_bp
from controllers.reviews import reviews_bp
from controllers.error_handlers import error_bp
from config.nltk_config import initialize_nltk
from config.config import Config

initialize_nltk()
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = Config.OAUTHLIB_INSECURE_TRANSPORT
google_blueprint = make_google_blueprint(
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    redirect_to='auth_bp.google_login'
)

app.register_blueprint(google_blueprint, url_prefix='/login')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dishes_bp, url_prefix='/dishes')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(request_bp, url_prefix='/request')
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(home_bp)
app.register_blueprint(error_bp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)