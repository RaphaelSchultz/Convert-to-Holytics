@echo off
echo ========================================
echo   Convert-to-Holytics - Build EXE
echo ========================================
echo.

echo [1/4] Fechando processos...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM Convert-to-Holytics.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2/4] Limpando builds anteriores...
if exist build rd /s /q build 2>nul
if exist dist rd /s /q dist 2>nul
timeout /t 1 /nobreak >nul

echo.
echo [3/4] Gerando executavel...
echo (Isso leva 1-2 minutos)
pyinstaller --onefile --noconsole --name="Convert-to-Holytics" --add-data="app;app" --add-data="static;static" --add-data="templates;templates" launcher.py

echo.
echo [4/4] Verificando...
if exist "dist\Convert-to-Holytics.exe" (
    echo.
    echo ========================================
    echo   SUCESSO! EXE Criado!
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
