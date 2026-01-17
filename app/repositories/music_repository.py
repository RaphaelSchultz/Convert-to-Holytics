"""Music repository for database operations."""
import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class MusicRepository:
    """Repository for accessing music data from Louvor JA database."""
    
    def __init__(self, db_path: str):
        """
        Initialize repository with database path.
        
        Args:
            db_path: Path to the Louvor JA database file
        """
        self.db_path = db_path
    
    def get_all_musics(self) -> List[Tuple]:
        """
        Get all music records from database.
        
        Returns:
            List of tuples containing music metadata
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
                SELECT NOME_COM, NOME_ALBUM, NOME, FAIXA, ID
                FROM LISTA_MUSICAS
            """
            cursor.execute(query)
            return cursor.fetchall()
    
    def get_lyrics_by_music_id(self, music_id: int) -> List[Tuple[Optional[str]]]:
        """
        Get lyrics for a specific music.
        
        Args:
            music_id: Music ID
            
        Returns:
            List of tuples containing lyric stanzas
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
                SELECT lyric 
                FROM lyrics 
                WHERE id_music = ?
            """
            cursor.execute(query, (music_id,))
            return cursor.fetchall()
    
    def count_musics(self) -> int:
        """
        Count total number of music records.
        
        Returns:
            Total count of music records
        """
        try:
            musics = self.get_all_musics()
            return len(musics)
        except Exception as e:
            logger.error(f"Error counting musics: {e}")
            return 0
