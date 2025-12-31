import os
from flask import Flask, g, session
from flask_dance.contrib.google import make_google_blueprint
from backend.config.config import Config
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
    from .controllers.errorHandlersController import error_bp

    from .controllers.web import register_web_blueprints
    from .controllers.api import register_api_blueprints

    register_web_blueprints(app)
    register_api_blueprints(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(error_bp)

    return app
