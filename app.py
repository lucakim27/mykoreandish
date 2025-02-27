from flask import Flask
import os
from flask_dance.contrib.google import make_google_blueprint
from controllers.authController import auth_bp
from controllers.dishesController import dishes_bp
from controllers.ingredientsController import ingredients_bp
from controllers.usersController import users_bp
from controllers.adminController import admin_bp
from controllers.requestController import request_bp
from controllers.homeController import home_bp
from controllers.errorHandlersController import error_bp
from config.config import Config
from controllers.footerController import footer_bp
from controllers.favoriteController import favorite_bp

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
app.register_blueprint(ingredients_bp, url_prefix='/ingredients')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(request_bp, url_prefix='/request')
app.register_blueprint(footer_bp, url_prefix='/footer')
app.register_blueprint(favorite_bp, url_prefix='/favorite')
app.register_blueprint(home_bp)
app.register_blueprint(error_bp)

if __name__ == '__main__':
    # set port to 10000 for Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)