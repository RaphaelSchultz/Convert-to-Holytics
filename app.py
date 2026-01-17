from flask import Flask, request, jsonify
from flask_cors import CORS
import exportar_musicas
import threading
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)

# CORS configuration
cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, origins=cors_origins)

# Thread-safe state management
export_lock = threading.Lock()
export_status: Dict[str, Any] = {
    "running": False, 
    "progress": 0, 
    "total": 0, 
    "message": "Aguardando início"
}


def validate_db_path(db_path: str) -> tuple[bool, str]:
    """
    Valida o caminho do banco de dados para prevenir path traversal.
    
    Args:
        db_path: Caminho do banco de dados
        
    Returns:
        Tupla (válido, mensagem_erro)
    """
    try:
        path = Path(db_path).resolve()
        
        # Verificar se o arquivo existe
        if not path.exists():
            return False, f"Arquivo não encontrado: {db_path}"
        
        # Verificar se é um arquivo (não diretório)
        if not path.is_file():
            return False, "O caminho deve apontar para um arquivo"
        
        # Verificar extensão
        if path.suffix.lower() not in ['.db', '.sqlite', '.sqlite3']:
            return False, "Arquivo deve ter extensão .db, .sqlite ou .sqlite3"
        
        # Verificar se o caminho não contém tentativas de path traversal
        if '..' in db_path:
            return False, "Caminho inválido: caracteres '..' não são permitidos"
        
        logger.info(f"Caminho validado com sucesso: {path}")
        return True, ""
        
    except Exception as e:
        logger.error(f"Erro na validação do caminho: {e}")
        return False, f"Erro ao validar caminho: {str(e)}"


def callback(idx: int, total: int) -> None:
    """Atualiza o progresso da exportação de forma thread-safe."""
    with export_lock:
        export_status["progress"] = idx
        export_status["total"] = total
        export_status["message"] = f"Exportando música {idx} de {total}..."


def cancel_check() -> bool:
    """Verifica se a exportação deve ser cancelada."""
    with export_lock:
        return not export_status["running"]


def run_export(db_path: str) -> None:
    """Executa a exportação em thread separada."""
    try:
        logger.info(f"Iniciando exportação do banco: {db_path}")
        result = exportar_musicas.exportar_musicas(db_path, callback, cancel_check)
        
        with export_lock:
            export_status["running"] = False
            export_status["message"] = result
        
        logger.info(f"Exportação concluída: {result}")
        
    except Exception as e:
        error_msg = f"Erro durante exportação: {str(e)}"
        logger.error(error_msg)
        
        with export_lock:
            export_status["running"] = False
            export_status["message"] = f"❌ {error_msg}"


@app.route('/start', methods=['POST'])
def start_export():
    """Inicia o processo de exportação."""
    with export_lock:
        if export_status["running"]:
            logger.warning("Tentativa de iniciar exportação já em andamento")
            return jsonify({"error": "Exportação já em andamento"}), 400

    # Obter caminho do banco de dados
    data = request.get_json() or {}
    db_path = data.get('db_path', os.getenv('DEFAULT_DB_PATH', ''))
    
    if not db_path:
        logger.error("Caminho do banco de dados não fornecido")
        return jsonify({
            "error": "Caminho do banco de dados não fornecido",
            "hint": "Envie 'db_path' no corpo da requisição"
        }), 400
    
    # Validar caminho do banco de dados
    is_valid, error_message = validate_db_path(db_path)
    if not is_valid:
        logger.error(f"Validação falhou: {error_message}")
        return jsonify({"error": error_message}), 400

    # Iniciar exportação
    with export_lock:
        export_status["running"] = True
        export_status["progress"] = 0
        export_status["total"] = 0
        export_status["message"] = "Iniciando exportação..."

    export_thread = threading.Thread(
        target=run_export, 
        args=(db_path,), 
        daemon=True,
        name="ExportThread"
    )
    export_thread.start()
    
    logger.info(f"Thread de exportação iniciada para: {db_path}")
    
    with export_lock:
        status_copy = export_status.copy()
    
    return jsonify({
        "message": "Exportação iniciada", 
        "status": status_copy
    }), 200


@app.route('/status', methods=['GET'])
def get_status():
    """Retorna o status atual da exportação."""
    with export_lock:
        status_copy = export_status.copy()
    
    return jsonify(status_copy), 200


@app.route('/cancel', methods=['POST'])
def cancel_export():
    """Cancela a exportação em andamento."""
    with export_lock:
        if not export_status["running"]:
            logger.warning("Tentativa de cancelar exportação inexistente")
            return jsonify({"error": "Nenhuma exportação em andamento"}), 400
        
        export_status["running"] = False
        export_status["message"] = "Cancelando exportação..."
    
    logger.info("Exportação cancelada pelo usuário")
    
    with export_lock:
        status_copy = export_status.copy()
    
    return jsonify({
        "message": "Solicitação de cancelamento enviada", 
        "status": status_copy
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para monitoramento."""
    return jsonify({
        "status": "healthy",
        "service": "convert-to-holytics",
        "version": "1.0.0"
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Endpoint raiz com informações da API."""
    return jsonify({
        "name": "Convert to Holytics API",
        "version": "1.0.0",
        "description": "API para exportar músicas do Louvor JA para arquivos .txt formatados",
        "endpoints": {
            "POST /start": "Iniciar exportação (requer db_path no body)",
            "GET /status": "Obter status da exportação",
            "POST /cancel": "Cancelar exportação em andamento",
            "GET /health": "Health check"
        }
    }), 200


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando servidor em {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)
