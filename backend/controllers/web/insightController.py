from flask import Blueprint, render_template

insight_bp = Blueprint('insight', __name__, url_prefix="/insight")

@insight_bp.route('/', methods=["GET"])
def insightPage():
    return render_template('insight.html')