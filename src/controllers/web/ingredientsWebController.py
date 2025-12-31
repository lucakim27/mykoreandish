from flask import Blueprint, render_template

ingredients_web_bp = Blueprint('ingredients_web', __name__, url_prefix='/ingredients')

@ingredients_web_bp.route('/<ingredient_name>')
def ingredientPage(ingredient_name):
    return render_template('ingredient.html')