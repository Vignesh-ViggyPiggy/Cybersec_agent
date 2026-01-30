@echo off
REM CyberSec Agent - Unified Startup Script

echo ============================================================
echo          CyberSec Agent - Starting All Services
echo ============================================================
echo.

REM Check virtual environment
if not exist "..\venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found at ..\venv
    echo Please run: python -m venv ..\venv
    echo Then: ..\venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check .env file
if not exist ".env" (
    echo Warning: .env file not found!
    echo Creating from .env.example...
    copy .env.example .env
    echo Please edit .env file with your configuration.
    echo.
)

echo [1/4] Checking BERT API (Port 7000)...
timeout /t 1 /nobreak >nul
curl -s http://localhost:7000/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       BERT API already running
) else (
    echo       Starting BERT API...
    cd ..
    start /min cmd /c "..\venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 7000"
    cd cybersec_agent
    timeout /t 3 /nobreak >nul
)
echo.

echo [2/4] Checking Ollama (Port 11434)...
timeout /t 1 /nobreak >nul
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       Ollama already running
) else (
    echo       Warning: Ollama not running!
    echo       Please start Ollama manually: ollama serve
)
echo.

echo [3/4] Starting CyberSec Agent API (Port 8080)...
set PYTHONPATH=%cd%
start "CyberSec API" cmd /k "cd /d %cd% && ..\venv\Scripts\python.exe -m src.api.server"
timeout /t 3 /nobreak >nul
echo       API server starting at http://localhost:8080
echo       API docs available at http://localhost:8080/docs
echo.

echo [4/4] Starting Frontend (Port 3000)...
if not exist "frontend\node_modules" (
    echo       Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)
cd frontend
start "CyberSec Frontend" cmd /k "npm run dev"
cd ..
timeout /t 2 /nobreak >nul
echo       Frontend starting at http://localhost:3000
echo.

echo ============================================================
echo                  All Services Started!
echo ============================================================
echo.
echo Services:
echo   - BERT API:        http://localhost:7000/health
echo   - Ollama LLM:      http://localhost:11434
echo   - API Server:      http://localhost:8080/docs
echo   - Web Frontend:    http://localhost:3000
echo.
echo Press Ctrl+C in each window to stop services.
echo ============================================================
echo.
pause
