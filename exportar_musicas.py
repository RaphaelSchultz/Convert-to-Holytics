import sqlite3
from pathlib import Path
import unicodedata
from typing import Optional, Callable, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def formatar_letra(estrofes: List[Tuple[Optional[str]]]) -> str:
    """
    Formata as estrofes da música em blocos de texto.
    
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
        
        texto = normalize_unicode(texto)
        texto = texto.strip('\n')
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        if linhas:
            blocos.append('\n'.join(linhas))
    
    return '\n\n'.join(blocos)


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


def exportar_musicas(
    db_path: str, 
    callback: Optional[Callable[[int, int], None]] = None, 
    cancel_check: Optional[Callable[[], bool]] = None
) -> str:
    """
    Exporta músicas do banco de dados Louvor JA para arquivos .txt formatados.
    
    Args:
        db_path: Caminho para o arquivo database.db do Louvor JA
        callback: Função opcional para reportar progresso (idx, total)
        cancel_check: Função opcional que retorna True se deve cancelar
        
    Returns:
        Mensagem de status da operação
    """
    try:
        # Usar context manager para garantir que a conexão seja fechada
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            query_musicas = """
            SELECT NOME_COM, NOME_ALBUM, NOME, FAIXA, ID
            FROM LISTA_MUSICAS
            """
            cursor.execute(query_musicas)
            musicas = cursor.fetchall()

            total_musicas = len(musicas)
            if total_musicas == 0:
                logger.warning("Nenhuma música encontrada na view LISTA_MUSICAS")
                return "⚠️ Nenhuma música encontrada na view LISTA_MUSICAS."

            output_dir = Path("musicas_txt_formatadas")
            output_dir.mkdir(exist_ok=True)
            logger.info(f"Iniciando exportação de {total_musicas} músicas para {output_dir}")

            for idx, (nome_com, nome_album, nome, faixa, id_music) in enumerate(musicas, 1):
                # Verificar se foi solicitado cancelamento
                if cancel_check and cancel_check():
                    logger.info("Exportação cancelada pelo usuário")
                    return "❌ Exportação cancelada pelo usuário."
                
                # Reportar progresso
                if callback:
                    callback(idx, total_musicas)

                # Buscar letras da música
                query_letras = """
                SELECT lyric 
                FROM lyrics 
                WHERE id_music = ?
                """
                cursor.execute(query_letras, (id_music,))
                estrofes = cursor.fetchall()

                # Determinar nome do arquivo
                if nome_album and "Hinário Adventista" in nome_album:
                    nome_arquivo_base = f"{nome_com or nome or 'Sem_título'} (Hinario Adventista)"
                else:
                    nome_arquivo_base = f"{nome_com or nome or 'Sem_título'}{id_music}"
                
                nome_arquivo = sanitize_filename(nome_arquivo_base)
                caminho_txt = output_dir / f"{nome_arquivo}.txt"

                # Formatar e salvar letra
                letra_formatada = formatar_letra(estrofes)

                with open(caminho_txt, 'w', encoding='utf-8') as f:
                    f.write(f"Título: {nome or 'Sem título'}\n")
                    f.write(f"Artista: {nome_album or 'Sem álbum'}\n\n")
                    f.write(letra_formatada)
                
                logger.debug(f"Exportada música {idx}/{total_musicas}: {nome_arquivo}")

            logger.info(f"Exportação finalizada com sucesso! {total_musicas} músicas exportadas")
            return "✅ Exportação finalizada com sucesso!"

    except sqlite3.Error as e:
        error_msg = f"Erro ao acessar o banco de dados: {e}"
        logger.error(error_msg)
        return f"❌ {error_msg}"
    except Exception as e:
        error_msg = f"Erro inesperado durante exportação: {e}"
        logger.error(error_msg)
        return f"❌ {error_msg}"
