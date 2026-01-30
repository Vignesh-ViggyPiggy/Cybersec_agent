#!/bin/bash
# CyberSec Agent - Unified Startup Script

echo "============================================================"
echo "          CyberSec Agent - Starting All Services"
echo "============================================================"
echo

# Check virtual environment
if [ ! -d "../venv" ]; then
    echo "Error: Virtual environment not found at ../venv"
    echo "Please run: python -m venv ../venv"
    echo "Then: source ../venv/bin/activate"
    echo "Then: pip install -r requirements.txt"
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration."
    echo
fi

echo "[1/4] Checking BERT API (Port 7000)..."
sleep 1
if curl -s http://localhost:7000/health > /dev/null 2>&1; then
    echo "      ✓ BERT API already running"
else
    echo "      Starting BERT API..."
    cd ..
    ../venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 7000 > /dev/null 2>&1 &
    cd cybersec_agent
    sleep 3
fi
echo

echo "[2/4] Checking Ollama (Port 11434)..."
sleep 1
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "      ✓ Ollama already running"
else
    echo "      Warning: Ollama not running!"
    echo "      Please start Ollama manually: ollama serve"
fi
echo

echo "[3/4] Starting CyberSec Agent API (Port 8080)..."
export PYTHONPATH=$(pwd)
../venv/bin/python -m src.api.server > api.log 2>&1 &
API_PID=$!
sleep 3
echo "      ✓ API server starting at http://localhost:8080"
echo "      API docs available at http://localhost:8080/docs"
echo "      (PID: $API_PID, logs: api.log)"
echo

echo "[4/4] Starting Frontend (Port 3000)..."
if [ ! -d "frontend/node_modules" ]; then
    echo "      Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 2
echo "      ✓ Frontend starting at http://localhost:3000"
echo "      (PID: $FRONTEND_PID, logs: frontend.log)"
echo

echo "============================================================"
echo "                  All Services Started!"
echo "============================================================"
echo
echo "Services:"
echo "  - BERT API:        http://localhost:7000/health"
echo "  - Ollama LLM:      http://localhost:11434"
echo "  - API Server:      http://localhost:8080/docs"
echo "  - Web Frontend:    http://localhost:3000"
echo
echo "To stop all services:"
echo "  kill $API_PID $FRONTEND_PID"
echo
echo "Logs:"
echo "  - API: api.log"
echo "  - Frontend: frontend.log"
echo "============================================================"
