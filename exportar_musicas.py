import sqlite3
from pathlib import Path
import re
import unicodedata

def formatar_letra(estrofes):
    if not estrofes or all(estrofe[0] is None for estrofe in estrofes):
        return "Letra não disponível"
    
    blocos = []
    for estrofe in estrofes:
        texto = estrofe[0]
        if not texto:
            continue
        
        texto = ''.join(c for c in unicodedata.normalize('NFKD', texto) 
                       if unicodedata.category(c) != 'Mn')
        texto = texto.strip('\n')
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        if linhas:
            blocos.append('\n'.join(linhas))
    
    return '\n\n'.join(blocos)

def sanitize_filename(name: str) -> str:
    if not name:
        return "musica_sem_nome"
    name = ''.join(c for c in unicodedata.normalize('NFKD', name) 
                  if unicodedata.category(c) != 'Mn' and c not in r'\/:*?"<>|#')
    return name.strip()

def exportar_musicas(db_path, callback=None, cancel_check=None):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query_musicas = """
        SELECT NOME_COM, NOME_ALBUM, NOME, FAIXA, ID
        FROM LISTA_MUSICAS
        """
        cursor.execute(query_musicas)
        musicas = cursor.fetchall()

        total_musicas = len(musicas)
        if total_musicas == 0:
            return "⚠️ Nenhuma música encontrada na view LISTA_MUSICAS."

        output_dir = Path("musicas_txt_formatadas")
        output_dir.mkdir(exist_ok=True)

        for idx, (nome_com, nome_album, nome, faixa, id_music) in enumerate(musicas, 1):
            if cancel_check and cancel_check():
                return "❌ Exportação cancelada pelo usuário."
            
            if callback:
                callback(idx, total_musicas)

            query_letras = """
            SELECT lyric 
            FROM lyrics 
            WHERE id_music = ?
            """
            cursor.execute(query_letras, (id_music,))
            estrofes = cursor.fetchall()

            if nome_album and "Hinário Adventista" in nome_album:
                nome_arquivo_base = f"{nome_com or nome or 'Sem_título'} (Hinario Adventista)"
            else:
                nome_arquivo_base = f"{nome_com or nome or 'Sem_título'}{id_music}"
            
            nome_arquivo = sanitize_filename(nome_arquivo_base)
            caminho_txt = output_dir / f"{nome_arquivo}.txt"

            letra_formatada = formatar_letra(estrofes)

            with open(caminho_txt, 'w', encoding='utf-8') as f:
                f.write(f"Título: {nome or 'Sem título'}\n")
                f.write(f"Artista: {nome_album or 'Sem álbum'}\n\n")
                f.write(letra_formatada)

        return "✅ Exportação finalizada com sucesso!"

    except sqlite3.Error as e:
        return f"❌ Erro ao acessar o banco de dados: {e}"
    finally:
        conn.close()