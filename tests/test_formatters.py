"""Tests for formatters utility module."""
import pytest
from app.utils.formatters import normalize_unicode, sanitize_filename, formatar_letra


class TestNormalizeUnicode:
    """Tests for normalize_unicode function."""
    
    def test_removes_accents(self):
        """Test que remove acentos."""
        assert normalize_unicode("São Paulo") == "Sao Paulo"
        assert normalize_unicode("México") == "Mexico"
        assert normalize_unicode("Coração") == "Coracao"
    
    def test_handles_empty_string(self):
        """Test com string vazia."""
        assert normalize_unicode("") == ""
    
    def test_handles_none(self):
        """Test com None."""
        assert normalize_unicode(None) == ""  # type: ignore
    
    def test_preserves_regular_text(self):
        """Test que preserva texto sem acentos."""
        assert normalize_unicode("Hello World") == "Hello World"


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""
    
    def test_removes_invalid_chars(self):
        """Test que remove caracteres inválidos."""
        assert sanitize_filename("file:name") == "filename"
        assert sanitize_filename("file/name") == "filename"
        assert sanitize_filename("file\\name") == "filename"
        assert sanitize_filename("file*name") == "filename"
    
    def test_handles_empty_string(self):
        """Test com string vazia."""
        assert sanitize_filename("") == "musica_sem_nome"
    
    def test_removes_accents(self):
        """Test que remove acentos."""
        result = sanitize_filename("Canção de Natal")
        assert result == "Cancao de Natal"
    
    def test_preserves_spaces(self):
        """Test que preserva espaços."""
        assert sanitize_filename("My File Name") == "My File Name"


class TestFormatarLetra:
    """Tests for formatar_letra function."""
    
    def test_formats_single_stanza(self):
        """Test formatação de uma estrofe."""
        estrofes = [("Linha 1\nLinha 2",)]
        result = formatar_letra(estrofes)
        assert "Linha 1" in result
        assert "Linha 2" in result
    
    def test_formats_multiple_stanzas(self):
        """Test formatação de múltiplas estrofes."""
        estrofes = [
            ("Estrofe 1\nLinha 1",),
            ("Estrofe 2\nLinha 2",)
        ]
        result = formatar_letra(estrofes)
        assert "Estrofe 1" in result
        assert "Estrofe 2" in result
        assert "\n\n" in result  # Double newline between stanzas
    
    def test_handles_empty_lyrics(self):
        """Test com letras vazias."""
        assert formatar_letra([]) == "Letra não disponível"
        assert formatar_letra([(None,)]) == "Letra não disponível"
    
    def test_removes_accents_in_lyrics(self):
        """Test que remove acentos das letras."""
        estrofes = [("São José",)]
        result = formatar_letra(estrofes)
        assert "Sao Jose" in result
