@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" home.py
) else if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" home.py
) else (
    python home.py
)
if errorlevel 1 (
    echo.
    echo Nao foi possivel iniciar. Envie uma captura do erro para verificarmos.
    pause
)
