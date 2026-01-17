"""Application configuration classes."""
import os
from pathlib import Path
from dotenv import load_dotenv
import platform

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # Export
    OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', 'musicas_txt_formatadas'))
    
    # Database
    @staticmethod
    def get_default_db_path():
        """Get default database path based on OS."""
        system = platform.system()
        
        if system == 'Windows':
            return r'C:\Program Files (x86)\Louvor JA\config\database.db'
        elif system == 'Darwin':  # macOS
            return str(Path.home() / 'Library' / 'Application Support' / 'Louvor JA' / 'database.db')
        else:  # Linux
            return str(Path.home() / '.louvor-ja' / 'database.db')
    
    DEFAULT_DB_PATH = os.getenv('DEFAULT_DB_PATH', get_default_db_path.__func__())


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Production should have a secure secret key (will warn if not set)
    if not os.getenv('SECRET_KEY'):
        import warnings
        warnings.warn("SECRET_KEY not set. Using default key. This is INSECURE for production!")


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    
    # Use temp directory for testing
    OUTPUT_DIR = Path('/tmp/test_musicas')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
