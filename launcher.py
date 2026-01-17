"""Launcher script for standalone executable."""
import os
import sys
import logging
import webbrowser
import threading
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def open_browser():
    """Open browser after short delay."""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Main entry point for standalone executable."""
    try:
        # Import Flask app
        from app import create_app
        
        logger.info("Iniciando Convert-to-Holytics...")
        logger.info("Criando aplicação Flask...")
        
        # Create app
        app = create_app()
        
        # Start browser in background
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        logger.info("Abrindo navegador em http://127.0.0.1:5000")
        logger.info("Pressione Ctrl+C para encerrar")
        
        # Run Flask app
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False
        )
        
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {e}", exc_info=True)
        input("Pressione Enter para sair...")
        sys.exit(1)

if __name__ == '__main__':
    main()
