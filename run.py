"""Application entry point."""
import logging
from app import create_app
from app.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create app instance (for Vercel)
app = create_app()

if __name__ == '__main__':
    config = get_config()
    logger.info(f"Starting server on {config.HOST}:{config.PORT} (debug={config.DEBUG})")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
