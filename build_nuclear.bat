@echo off
echo ========================================
echo   Convert-to-Holytics - NUCLEAR BUILD
echo ========================================
echo.

echo [1/5] Matando processos...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM Convert-to-Holytics.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2/5] DELETANDO TUDO (Builds e Caches)...
if exist build rd /s /q build 2>nul
if exist dist rd /s /q dist 2>nul
if exist __pycache__ rd /s /q __pycache__ 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /f /s /q *.pyc 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [3/5] Gerando executavel (CLEAN BUILD)...
echo (Isso leva 1-2 minutos)
pyinstaller --clean --onefile --noconsole --name="Convert-to-Holytics" --add-data="app;app" --add-data="static;static" --add-data="templates;templates" launcher.py

echo.
echo [4/5] Verificando...
if exist "dist\Convert-to-Holytics.exe" (
    echo.
    echo ========================================
    echo   SUCESSO! NOVO EXE CRIADO!
    echo ========================================
    echo.
    echo Local: dist\Convert-to-Holytics.exe
    echo.
    echo Testar agora? (S/N)
    choice /c SN /n
    if errorlevel 2 goto fim
    if errorlevel 1 start "" "dist\Convert-to-Holytics.exe"
) else (
    echo.
    echo ========================================
    echo   ERRO! Veja mensagens acima
    echo ========================================
)

:fim
echo.
pause
