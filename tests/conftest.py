"""Pytest configuration and fixtures."""
import pytest
import tempfile
import sqlite3
from pathlib import Path

from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_db():
    """Create a mock SQLite database for testing."""
    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / 'test_database.db'
    
    # Create database with test data
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE LISTA_MUSICAS (
            ID INTEGER PRIMARY KEY,
            NOME TEXT,
            NOME_COM TEXT,
            NOME_ALBUM TEXT,
            FAIXA INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE lyrics (
            id INTEGER PRIMARY KEY,
            id_music INTEGER,
            lyric TEXT,
            FOREIGN KEY (id_music) REFERENCES LISTA_MUSICAS(ID)
        )
    """)
    
    # Insert test data
    cursor.execute("""
        INSERT INTO LISTA_MUSICAS (ID, NOME, NOME_COM, NOME_ALBUM, FAIXA)
        VALUES (1, 'Musica Teste', 'Musica Teste Completa', 'Album Teste', 1)
    """)
    
    cursor.execute("""
        INSERT INTO lyrics (id_music, lyric)
        VALUES (1, 'Estrofe 1\nLinha 1\nLinha 2')
    """)
    
    cursor.execute("""
        INSERT INTO lyrics (id_music, lyric)
        VALUES (1, 'Estrofe 2\nLinha 3\nLinha 4')
    """)
    
    conn.commit()
    conn.close()
    
    yield str(db_path)
    
    # Cleanup
    db_path.unlink()
    Path(temp_dir).rmdir()
