from .reviewsController import reviews_bp
from .dishesController import dishes_bp
from .ingredientsController import ingredients_bp
from .dietariesController import dietaries_bp
from .nutrientsController import nutrients_bp
from .usersController import users_api_bp
from .pricesController import prices_bp
from .notesController import notes_bp
from .favoritesController import favorites_bp
from .historiesController import histories_bp
from .tastesController import tastes_bp

def register_api_blueprints(app):
    app.register_blueprint(reviews_bp)
    app.register_blueprint(dishes_bp)
    app.register_blueprint(ingredients_bp)
    app.register_blueprint(dietaries_bp)
    app.register_blueprint(nutrients_bp)
    app.register_blueprint(users_api_bp)
    app.register_blueprint(prices_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(histories_bp)
    app.register_blueprint(tastes_bp)