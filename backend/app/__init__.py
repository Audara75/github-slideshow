from flask import Flask
from app.data_ingestion import data_ingestion_bp

def create_app():
    """Initializes and registers blueprints"""
    app = Flask(__name__)
    app.register_blueprint(data_ingestion_bp)
    return app
