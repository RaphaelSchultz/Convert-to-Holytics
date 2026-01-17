@echo off
echo ========================================
echo   Convert-to-Holytics - Build EXE
echo ========================================
echo.

echo [1/3] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [2/3] Instalando PyInstaller (se necessario)...
pip install pyinstaller

echo.
echo [3/3] Gerando executavel...
pyinstaller Convert-to-Holytics.spec

echo.
echo ========================================
echo   Build Concluido!
echo ========================================
echo.
echo Arquivo gerado em: dist\Convert-to-Holytics.exe
echo.
echo Pressione qualquer tecla para executar...
pause >nul
start dist\Convert-to-Holytics.exe
