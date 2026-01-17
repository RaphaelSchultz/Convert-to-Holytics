"""Tests for export service."""
import pytest
import time
from pathlib import Path

from app.services.export_service import ExportService


class TestExportService:
    """Tests for ExportService class."""
    
    def test_initial_status(self):
        """Test initial service status."""
        service = ExportService()
        status = service.get_status()
        
        assert status['running'] == False
        assert status['progress'] == 0
        assert status['total'] == 0
        assert 'message' in status
    
    def test_is_running_initially_false(self):
        """Test that service is not running initially."""
        service = ExportService()
        assert service.is_running() == False
    
    def test_cancel_when_not_running(self):
        """Test cancelling when nothing is running."""
        service = ExportService()
        assert service.cancel_export() == False
    
    def test_start_export_with_mock_db(self, mock_db):
        """Test starting export with mock database."""
        service = ExportService()
        output_dir = Path('/tmp/test_export_output')
        output_dir.mkdir(exist_ok=True)
        
        # Start export
        service.start_export(mock_db, output_dir)
        
        # Give it a moment to start
        time.sleep(0.1)
        
        # Check that it's running or has completed
        status = service.get_status()
        assert status['progress'] >= 0
        
        # Cleanup
        if output_dir.exists():
            for file in output_dir.glob('*.txt'):
                file.unlink()
            output_dir.rmdir()
    
    def test_cannot_start_twice(self, mock_db):
        """Test that can't start export when already running."""
        service = ExportService()
        output_dir = Path('/tmp/test_export_output2')
        output_dir.mkdir(exist_ok=True)
        
        # Start first export
        service.start_export(mock_db, output_dir)
        
        # Try to start again
        with pytest.raises(ValueError):
            service.start_export(mock_db, output_dir)
        
        # Cleanup
        time.sleep(1)  # Wait for completion
        if output_dir.exists():
            for file in output_dir.glob('*.txt'):
                file.unlink()
            output_dir.rmdir()
