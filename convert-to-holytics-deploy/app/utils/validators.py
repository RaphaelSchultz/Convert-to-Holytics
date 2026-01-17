"""Utility functions for validation."""
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


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
