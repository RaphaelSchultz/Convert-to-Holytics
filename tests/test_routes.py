"""Tests for API routes."""
import pytest
import json


class TestHealthRoutes:
    """Tests for health check routes."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'convert-to-holytics'
    
    def test_index_route(self, client):
        """Test index endpoint."""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'name' in data
        assert 'version' in data
        assert 'endpoints' in data


class TestExportRoutes:
    """Tests for export routes."""
    
    def test_get_status_initial(self, client):
        """Test getting initial status."""
        response = client.get('/api/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'running' in data
        assert 'progress' in data
        assert 'total' in data
        assert 'message' in data
    
    def test_start_export_without_db_path(self, client):
        """Test starting export without providing database path."""
        response = client.post('/api/start',
                               data=json.dumps({}),
                               content_type='application/json')
        # Should fail validation or use default
        assert response.status_code in [400, 500]
    
    def test_start_export_with_invalid_path(self, client):
        """Test starting export with invalid database path."""
        response = client.post('/api/start',
                               data=json.dumps({'db_path': '/nonexistent/path.db'}),
                               content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_cancel_without_running_export(self, client):
        """Test cancelling when no export is running."""
        response = client.post('/api/cancel')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
