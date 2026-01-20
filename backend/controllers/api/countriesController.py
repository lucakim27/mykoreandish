from flask import Blueprint
from ...services.managers import price_manager

countries_bp = Blueprint('countries', __name__, url_prefix='/api/countries')

@countries_bp.route('/', methods=['GET'])
def get_all_countries():
    all_countries = price_manager.get_all_countries()
    return all_countries, 200