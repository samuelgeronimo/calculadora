@echo off
echo ========================================
echo  Iniciando Extrator de Produtos
echo ========================================
echo.
echo Matando processos Python anteriores...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Iniciando servidor...
python app.py

pause
