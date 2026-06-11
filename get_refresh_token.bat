@echo off
chcp 65001 >nul
title Hermes Notifier — Obtener Refresh Token

echo.
echo  Abriendo navegador para autenticación de Gmail...
echo  Inicia sesión y acepta los permisos cuando se pida.
echo.

call .venv\Scripts\activate.bat
python get_refresh_token.py

echo.
echo  Copia el GMAIL_REFRESH_TOKEN al archivo .env
echo.
pause
