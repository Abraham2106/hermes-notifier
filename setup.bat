@echo off
chcp 65001 >nul
title Hermes Notifier — Setup

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║        Hermes Notifier — Setup           ║
echo  ╚══════════════════════════════════════════╝
echo.

:: ── Verificar Python ──────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instálalo desde https://python.org
    pause
    exit /b 1
)
echo [OK] Python encontrado.

:: ── Crear entorno virtual ─────────────────────
if not exist ".venv" (
    echo [..] Creando entorno virtual...
    python -m venv .venv
    echo [OK] Entorno virtual creado.
) else (
    echo [OK] Entorno virtual ya existe.
)

:: ── Activar e instalar dependencias ──────────
echo [..] Instalando dependencias...
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo [OK] Dependencias instaladas.

:: ── Verificar .env ────────────────────────────
if not exist ".env" (
    echo.
    echo [!] No se encontró el archivo .env
    echo     Copiando .env.example a .env...
    copy .env.example .env >nul
    echo.
    echo  ┌─────────────────────────────────────────────┐
    echo  │  ACCIÓN REQUERIDA:                          │
    echo  │  Abre el archivo .env y rellena los valores │
    echo  │  antes de continuar.                        │
    echo  └─────────────────────────────────────────────┘
    echo.
    echo  Presiona cualquier tecla para abrir .env en el editor...
    pause >nul
    notepad .env
) else (
    echo [OK] Archivo .env encontrado.
)

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║  Setup completo. Próximos pasos:         ║
echo  ║                                          ║
echo  ║  1. Asegúrate de tener el .env listo     ║
echo  ║  2. Corre: get_refresh_token.bat         ║
echo  ║     para obtener tu GMAIL_REFRESH_TOKEN  ║
echo  ║  3. Corre: start.bat para iniciar el bot ║
echo  ╚══════════════════════════════════════════╝
echo.
pause
