@echo off
echo ========================================
echo   Convert-to-Holytics - Build Limpo
echo ========================================
echo.

echo [1/5] Fechando processos Python...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
taskkill /F /IM Convert-to-Holytics.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2/5] Limpando build antigo...
if exist build (
    rd /s /q build 2>nul
    timeout /t 1 /nobreak >nul
)
if exist dist (
    rd /s /q dist 2>nul
    timeout /t 1 /nobreak >nul
)
del /f /q *.spec 2>nul

echo.
echo [3/5] Instalando dependencias...
pip install -q pyinstaller pillow

echo.
echo [4/5] Gerando executavel GUI...
echo (Isso pode levar 1-2 minutos)
pyinstaller --onefile --windowed --icon=icon.ico --add-data "app;app" --name="Convert-to-Holytics" gui_app.py

echo.
echo [5/5] Verificando resultado...
if exist "dist\Convert-to-Holytics.exe" (
    echo.
    echo ========================================
    echo   SUCESSO! EXE Gerado!
    echo ========================================
    echo.
    echo Local: dist\Convert-to-Holytics.exe
    echo.
    echo Deseja testar agora? (S/N)
    choice /c SN /n /m "Pressione S para Sim ou N para Nao: "
    if errorlevel 2 goto :fim
    if errorlevel 1 goto :executar
) else (
    echo.
    echo ========================================
    echo   ERRO! EXE nao foi gerado!
    echo ========================================
    echo.
    echo Verifique os erros acima.
    pause
    goto :fim
)

:executar
echo.
echo Executando Convert-to-Holytics.exe...
start "" "dist\Convert-to-Holytics.exe"
goto :fim

:fim
echo.
echo Processo finalizado!
pause
