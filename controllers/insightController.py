from flask import Blueprint, render_template, session
from config.db import db
from models.aggregateModel import AggregateManager
from models.userModel import UserManager

insight_bp = Blueprint('insight', __name__)
user_manager = UserManager(db)
aggregate_manager = AggregateManager(db)

@insight_bp.route('/', methods=['POST'])
def insight_page():
    user = user_manager.get_user_by_session(session)
    aggregates = aggregate_manager.get_overall_aggregates()
    return render_template('insight.html', user=user, aggregates=aggregates)