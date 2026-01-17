"""Health check and utility routes."""
from flask import Blueprint, jsonify, render_template

# Create Blueprint
health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        JSON with health status
    """
    return jsonify({
        "status": "healthy",
        "service": "convert-to-holytics",
        "version": "1.0.0"
    }), 200


@health_bp.route('/', methods=['GET'])
def index():
    """
    Render web interface.
    
    Returns:
        HTML template
    """
    return render_template('index.html')


@health_bp.route('/api', methods=['GET'])
def api_info():
    """
    API information endpoint.
    
    Returns:
        JSON with API documentation
    """
    return jsonify({
        "name": "Convert to Holytics API",
        "version": "1.0.0",
        "description": "API para exportar músicas do Louvor JA para arquivos .txt formatados",
        "endpoints": {
            "POST /api/start": "Iniciar exportação (requer db_path no body)",
            "GET /api/status": "Obter status da exportação",
            "POST /api/cancel": "Cancelar exportação em andamento",
            "GET /health": "Health check",
            "GET /": "Web interface",
            "GET /api": "API information"
        },
        "documentation": "https://github.com/RaphaelSchultz/Convert-to-Holytics"
    }), 200
