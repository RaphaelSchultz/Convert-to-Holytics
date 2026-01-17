"""Export routes for music export operations."""
from flask import Blueprint, request, jsonify, send_file
from pathlib import Path
import logging
import os
import zipfile
import io
from werkzeug.utils import secure_filename

from app.services import export_service
from app.utils.validators import validate_db_path
from app.config import get_config

logger = logging.getLogger(__name__)

# Create Blueprint
export_bp = Blueprint('export', __name__)
config = get_config()

# Upload configuration
UPLOAD_FOLDER = Path('temp_uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'db', 'sqlite', 'sqlite3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@export_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload database file.
    
    Returns:
        JSON with uploaded file path
    """
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = UPLOAD_FOLDER / filename
        file.save(str(filepath))
        logger.info(f"File uploaded: {filepath}")
        return jsonify({
            "message": "Arquivo enviado com sucesso",
            "filepath": str(filepath)
        }), 200
    
    return jsonify({"error": "Tipo de arquivo não permitido"}), 400


@export_bp.route('/start', methods=['POST'])
def start_export():
    """
    Start music export process.
    
    Request JSON:
        {
            "db_path": "path/to/database.db"  // or uploaded file path
        }
    
    Returns:
        JSON response with status
    """
    # Check if already running
    if export_service.is_running():
        logger.warning("Attempt to start export while already running")
        return jsonify({"error": "Exportação já em andamento"}), 400
    
    # Get database path from request
    data = request.get_json() or {}
    db_path = data.get('db_path', config.DEFAULT_DB_PATH)
    
    if not db_path:
        logger.error("Database path not provided")
        return jsonify({
            "error": "Caminho do banco de dados não fornecido",
            "hint": "Envie 'db_path' no corpo da requisição"
        }), 400
    
    # Validate path
    is_valid, error_message = validate_db_path(db_path)
    if not is_valid:
        logger.error(f"Path validation failed: {error_message}")
        return jsonify({"error": error_message}), 400
    
    # Start export
    try:
        output_dir = Path(config.OUTPUT_DIR)
        export_service.start_export(db_path, output_dir)
        logger.info(f"Export started for: {db_path}")
        
        return jsonify({
            "message": "Exportação iniciada",
            "status": export_service.get_status()
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error starting export: {e}", exc_info=True)
        return jsonify({"error": f"Erro ao iniciar exportação: {str(e)}"}), 500


@export_bp.route('/status', methods=['GET'])
def get_status():
    """
    Get current export status.
    
    Returns:
        JSON with progress information
    """
    return jsonify(export_service.get_status()), 200


@export_bp.route('/cancel', methods=['POST'])
def cancel_export():
    """
    Cancel running export.
    
    Returns:
        JSON response confirming cancellation
    """
    if not export_service.cancel_export():
        logger.warning("Attempt to cancel non-existent export")
        return jsonify({"error": "Nenhuma exportação em andamento"}), 400
    
    logger.info("Export cancellation requested")
    
    return jsonify({
        "message": "Solicitação de cancelamento enviada",
        "status": export_service.get_status()
    }), 200


@export_bp.route('/download', methods=['GET'])
def download_results():
    """
    Download exported files as a ZIP archive.
    
    Returns:
        ZIP file containing all exported music files
    """
    try:
        output_dir = Path(config.OUTPUT_DIR)
        
        if not output_dir.exists() or not any(output_dir.glob('*.txt')):
            return jsonify({
                "error": "Nenhum arquivo exportado encontrado"
            }), 404
        
        # Create ZIP file in memory
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for txt_file in output_dir.glob('*.txt'):
                zf.write(txt_file, txt_file.name)
        
        memory_file.seek(0)
        
        logger.info("ZIP file created and ready for download")
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='musicas_exportadas.zip'
        )
        
    except Exception as e:
        logger.error(f"Error creating ZIP: {e}", exc_info=True)
        return jsonify({
            "error": f"Erro ao criar arquivo ZIP: {str(e)}"
        }), 500
