@echo off
title Flask Server - Compras Paraguai
cd /d "%~dp0"
echo.
echo ====================================================================
echo   SERVIDOR FLASK - COMPRAS PARAGUAI
echo ====================================================================
echo.
echo   Iniciando servidor...
echo.
"C:\Program Files\Python312\python.exe" app.py
echo.
echo   Servidor encerrado.
echo   Pressione qualquer tecla para fechar...
pause > nul
