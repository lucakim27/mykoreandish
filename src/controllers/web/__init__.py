from .homeController import home_bp
from .insightController import insight_bp
from .footerController import footer_bp
from .usersController import users_web_bp
from .dishesWebController import dishes_web_bp
from .ingredientsWebController import ingredients_web_bp

def register_web_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(insight_bp)
    app.register_blueprint(footer_bp)
    app.register_blueprint(users_web_bp)
    app.register_blueprint(dishes_web_bp)
    app.register_blueprint(ingredients_web_bp)
