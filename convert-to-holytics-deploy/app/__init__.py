"""Flask application factory."""
from flask import Flask
from flask_cors import CORS
import logging
import os

from app.config import get_config
from app.routes import export_bp, health_bp


def setup_logging(config):
    """Configure application logging."""
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )


def create_app(config_name=None):
    """
    Flask application factory.
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(config_class)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting app with {config_name} configuration")
    
    # Setup CORS
    CORS(app, origins=config_class.CORS_ORIGINS)
    logger.info(f"CORS enabled for origins: {config_class.CORS_ORIGINS}")
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(export_bp, url_prefix='/api')
    logger.info("Blueprints registered")
    
    return app
