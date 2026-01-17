"""Application entry point."""
import os
import logging

from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    config = app.config
    host = config.get('HOST', '0.0.0.0')
    port = config.get('PORT', 5000)
    debug = config.get('DEBUG', False)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    
    app.run(host=host, port=port, debug=debug)
