@echo off
setlocal
cd /d "%~dp0"
title PrintMaster - Print Preview and Printing

echo =======================================================
echo    PrintMaster - Windows and Mac Print Tool
echo =======================================================

:: 1. Check Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found in system PATH.
    echo Please install Python 3 from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: 2. Check dependencies in current Python
python -c "import PyQt6, pymupdf, PIL" >nul 2>nul
if %ERRORLEVEL% equ 0 (
    goto :LAUNCH
)

:: 3. If missing, check or create venv
if not exist ".venv" (
    echo [1/2] Creating virtual environment (.venv)...
    python -m venv .venv
)

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: 4. Install dependencies
echo [2/2] Installing required packages (PyQt6, pymupdf, Pillow)...
python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Package installation failed. Please check internet connection.
    pause
    exit /b 1
)

:LAUNCH
echo Starting PrintMaster...
python main.py %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo Application exited with error code: %ERRORLEVEL%
    pause
)
endlocal
