"""Export service for business logic."""
import threading
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import logging

from app.repositories import MusicRepository
from app.utils import formatters

logger = logging.getLogger(__name__)


class ExportService:
    """Service for handling music export operations."""
    
    def __init__(self):
        """Initialize export service with thread-safe state."""
        self.lock = threading.Lock()
        self.status: Dict[str, Any] = {
            "running": False,
            "progress": 0,
            "total": 0,
            "message": "Aguardando início"
        }
        self.repository: Optional[MusicRepository] = None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current export status (thread-safe)."""
        with self.lock:
            return self.status.copy()
    
    def is_running(self) -> bool:
        """Check if export is currently running."""
        with self.lock:
            return self.status["running"]
    
    def start_export(
        self, 
        db_path: str, 
        output_dir: Optional[Path] = None,
        callback: Optional[Callable[[int, int], None]] = None
    ) -> None:
        """
        Start export process in background thread.
        
        Args:
            db_path: Path to database file
            output_dir: Output directory for exported files
            callback: Optional progress callback function
        """
        if self.is_running():
            raise ValueError("Export already running")
        
        with self.lock:
            self.status["running"] = True
            self.status["progress"] = 0
            self.status["total"] = 0
            self.status["message"] = "Iniciando exportação..."
        
        # Start export in background thread
        thread = threading.Thread(
            target=self._run_export,
            args=(db_path, output_dir, callback),
            daemon=True,
            name="ExportThread"
        )
        thread.start()
    
    def cancel_export(self) -> bool:
        """
        Cancel running export.
        
        Returns:
            True if cancel request was sent, False if nothing was running
        """
        with self.lock:
            if not self.status["running"]:
                return False
            self.status["running"] = False
            self.status["message"] = "Cancelando exportação..."
        return True
    
    def _should_cancel(self) -> bool:
        """Check if export should be cancelled (internal)."""
        with self.lock:
            return not self.status["running"]
    
    def _update_progress(self, current: int, total: int) -> None:
        """Update progress (thread-safe, internal)."""
        with self.lock:
            self.status["progress"] = current
            self.status["total"] = total
            self.status["message"] = f"Exportando música {current} de {total}..."
    
    def _run_export(
        self, 
        db_path: str, 
        output_dir: Optional[Path],
        callback: Optional[Callable[[int, int], None]]
    ) -> None:
        """
        Internal method to run export process.
        
        Args:
            db_path: Database path
            output_dir: Output directory
            callback: Progress callback
        """
        try:
            logger.info(f"Starting export from: {db_path}")
            
            # Initialize repository
            self.repository = MusicRepository(db_path)
            
            # Get all musics
            musics = self.repository.get_all_musics()
            total_musics = len(musics)
            
            if total_musics == 0:
                self._set_final_status("⚠️ Nenhuma música encontrada na view LISTA_MUSICAS.")
                return
            
            # Create output directory
            if output_dir is None:
                output_dir = Path("musicas_txt_formatadas")
            output_dir.mkdir(exist_ok=True)
            
            logger.info(f"Exporting {total_musics} musics to {output_dir}")
            
            # Export each music
            for idx, (nome_com, nome_album, nome, faixa, id_music) in enumerate(musics, 1):
                # Check for cancellation
                if self._should_cancel():
                    self._set_final_status("❌ Exportação cancelada pelo usuário.")
                    return
                
                # Update progress
                self._update_progress(idx, total_musics)
                if callback:
                    callback(idx, total_musics)
                
                # Get lyrics
                lyrics = self.repository.get_lyrics_by_music_id(id_music)
                
                # Generate filename
                song_name = nome_com or nome or 'Sem_título'
                
                if nome_album and "Hinário Adventista" in nome_album:
                    filename_base = f"{song_name} (Hinario Adventista) - {id_music}"
                else:
                    filename_base = f"{song_name} - {id_music}"
                
                filename = formatters.sanitize_filename(filename_base)
                file_path = output_dir / f"{filename}.txt"
                
                # Format and write lyrics
                formatted_lyrics = formatters.formatar_letra(lyrics)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Título: {nome or 'Sem título'}\n")
                    f.write(f"Artista: {nome_album or 'Sem álbum'}\n\n")
                    f.write(formatted_lyrics)
                
                logger.debug(f"Exported: {filename}")
            
            # Success
            self._set_final_status(f"✅ Exportação finalizada com sucesso! {total_musics} músicas exportadas.")
            logger.info(f"Export completed successfully: {total_musics} musics")
            
        except Exception as e:
            error_msg = f"Erro durante exportação: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self._set_final_status(f"❌ {error_msg}")
    
    def _set_final_status(self, message: str) -> None:
        """
        Set final status message and mark as not running.
        
        Args:
            message: Final status message
        """
        with self.lock:
            self.status["running"] = False
            self.status["message"] = message


# Global service instance
export_service = ExportService()
