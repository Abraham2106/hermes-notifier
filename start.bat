@echo off
chcp 65001 >nul
title Hermes Notifier — Corriendo

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║        Hermes Notifier — Iniciando       ║
echo  ╚══════════════════════════════════════════╝
echo.
echo  Presiona Ctrl+C para detener el bot.
echo.

call .venv\Scripts\activate.bat
python gmail_monitor.py

pause
