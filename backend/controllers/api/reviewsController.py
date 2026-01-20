from flask import Blueprint, jsonify
from ...services.managers import aggregate_manager

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@reviews_bp.route('/', methods=['GET'])
def get_review_count():
    total_reviews = aggregate_manager.get_total_reviews()
    return jsonify(total_reviews), 200