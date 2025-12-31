import os
from flask import Flask, g, session
from flask_dance.contrib.google import make_google_blueprint
from src.config.config import Config
from .services.managers import user_manager

def create_app(config_object=Config):
    app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
    app.config.from_object(config_object)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = app.config.get("OAUTHLIB_INSECURE_TRANSPORT", "1")

    @app.before_request
    def load_user():
        user_id = session.get("google_id")
        g.user = user_manager.get_user_by_id(user_id) if user_id else None

    google_bp = make_google_blueprint(
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        redirect_to='auth_bp.google_login'
    )
    app.register_blueprint(google_bp, url_prefix='/login')

    from .controllers.authController import auth_bp
    # from .controllers.dishesController import dishes_bp
    # from .controllers.ingredientsController import ingredients_bp
    # from .controllers.usersController import users_bp
    # from .controllers.web.homeController import home_bp
    from .controllers.errorHandlersController import error_bp
    # from .controllers.insightController import insight_bp
    # from .controllers.web.footerController import footer_bp
    # from .controllers.favoriteController import favorite_bp
    # from .controllers.noteController import note_bp

    from .controllers.web import register_web_blueprints
    from .controllers.api import register_api_blueprints

    register_web_blueprints(app)
    register_api_blueprints(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(dishes_bp, url_prefix='/dishes')
    # app.register_blueprint(ingredients_bp, url_prefix='/ingredients')
    # app.register_blueprint(users_bp, url_prefix='/users')
    # app.register_blueprint(footer_bp, url_prefix='/footer')
    # app.register_blueprint(favorite_bp, url_prefix='/favorite')
    # app.register_blueprint(insight_bp, url_prefix='/insight')
    # app.register_blueprint(note_bp, url_prefix='/note')
    # app.register_blueprint(home_bp)
    app.register_blueprint(error_bp)

    return app
