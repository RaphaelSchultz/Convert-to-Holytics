"""Utility functions for text formatting."""
import unicodedata
from typing import List, Tuple, Optional


def normalize_unicode(text: str) -> str:
    """
    Remove acentos e caracteres especiais Unicode.
    
    Args:
        text: Texto a ser normalizado
        
    Returns:
        Texto sem acentos
    """
    if not text:
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text) 
        if unicodedata.category(c) != 'Mn'
    )


def sanitize_filename(name: str) -> str:
    """
    Remove caracteres inválidos do nome de arquivo.
    
    Args:
        name: Nome a ser sanitizado
        
    Returns:
        Nome limpo e seguro para usar como nome de arquivo
    """
    if not name:
        return "musica_sem_nome"
    
    # Remove acentos e caracteres especiais do sistema de arquivos
    name = normalize_unicode(name)
    # Remove caracteres proibidos em nomes de arquivo
    invalid_chars = r'\/:*?"<>|#'
    name = ''.join(c for c in name if c not in invalid_chars)
    
    return name.strip()


def formatar_letra(estrofes: List[Tuple[Optional[str]]]) -> str:
    """
    Formata as estrofes da música em blocos de texto.
    PRESERVA acentuação original do conteúdo.
    
    Args:
        estrofes: Lista de tuplas contendo o texto das estrofes
        
    Returns:
        Letra formatada em blocos separados por linhas vazias
    """
    if not estrofes or all(estrofe[0] is None for estrofe in estrofes):
        return "Letra não disponível"
    
    blocos = []
    for estrofe in estrofes:
        texto = estrofe[0]
        if not texto:
            continue
        
        # NÃO normalizar unicode aqui - preservar acentos!
        texto = texto.strip('\n')
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        
        # SAFETY FILTER: Remover metadados se existirem no texto original do banco
        linhas = [
            l for l in linhas 
            if not l.lstrip().lower().startswith(('título:', 'titulo:', 'artista:', 'artist:'))
        ]
        
        if linhas:
            blocos.append('\n'.join(linhas))
    
    return '\n\n'.join(blocos)
