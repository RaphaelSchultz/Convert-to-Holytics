"""Launcher - Inicia Flask e abre navegador automaticamente"""
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

def open_browser():
    """Abre navegador após 2 segundos"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Entry point"""
    try:
        # Import Flask app
        from app import create_app
        
        print("========================================")
        print("Iniciando Convert-to-Holytics...")
        print("Versão: 2026-01-17 - SEM METADADOS (CLEAN)")
        print("========================================")
        print("Aguarde, abrindo navegador...")
        
        # Create app
        app = create_app()
        
        # Start browser in background
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Run Flask (sem debug e reloader para .exe)
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False
        )
        
    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)

if __name__ == '__main__':
    main()
