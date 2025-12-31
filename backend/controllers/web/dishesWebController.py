from flask import Blueprint, render_template

dishes_web_bp = Blueprint('dishes_web', __name__, url_prefix='/dishes')

@dishes_web_bp.route('/')
def foodListPage():
    return render_template('foodList.html')

@dishes_web_bp.route('/<food_name>')
def foodPage(food_name):
    return render_template('food.html')