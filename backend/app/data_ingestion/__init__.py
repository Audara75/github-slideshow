from flask import Blueprint

data_ingestion_bp = Blueprint('data_ingestion_bp', __name__, url_prefix='/api/ingestion')

from . import routes
