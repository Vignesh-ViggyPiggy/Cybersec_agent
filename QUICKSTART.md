# 🛡️ CyberSec Agent - Quick Start Guide

## One-Command Startup

Simply run:
```bash
# Windows
.\start.bat

# Linux/Mac
./start.sh
```

This automatically starts:
- ✓ BERT API (Port 7000) - ML anomaly detection
- ✓ Ollama LLM (Port 11434) - Language model
- ✓ API Server (Port 8080) - Backend API
- ✓ Web Frontend (Port 3000) - User interface

Then open: **http://localhost:3000**

## Services Overview

| Service | Port | URL |
|---------|------|-----|
| **Web UI** | 3000 | http://localhost:3000 |
| **API Docs** | 8080 | http://localhost:8080/docs |
| **BERT Health** | 7000 | http://localhost:7000/health |
| **Ollama** | 11434 | http://localhost:11434 |

## Alternative: Individual Services

**CLI Only:**
```bash
python -m src.cli.main
```

**API Only:**
```bash
python -m src.api.server
```

## Stopping Services

Press `Ctrl+C` in each terminal window, or:
- Close the terminal windows
- On Linux/Mac: Check `api.log` and `frontend.log` for process IDs

## First Time Setup

1. Ensure Python virtual environment is created:
   ```bash
   cd ..
   python -m venv venv
   ```

2. Activate and install dependencies:
   ```bash
   # Windows
   ..\venv\Scripts\activate
   # Linux/Mac
   source ../venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. Configure environment (if needed):
   ```bash
   # Edit .env file
   notepad .env  # Windows
   nano .env     # Linux/Mac
   ```

4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. Start everything:
   ```bash
   .\start.bat  # Windows
   ./start.sh   # Linux/Mac
   ```

## Troubleshooting

**Port already in use:**
- Check if services are already running
- Kill existing processes on those ports

**BERT API not starting:**
- Manually start: `cd .. && python -m uvicorn app:app --port 7000`

**Ollama not found:**
- Install Ollama: https://ollama.ai
- Start service: `ollama serve`
- Pull model: `ollama pull seneca` or `ollama pull llama3.2`

**Frontend dependencies error:**
- Install Node.js: https://nodejs.org
- Run: `cd frontend && npm install`

## Documentation

- Full README: [README.md](README.md)
- Setup Guide: [SETUP.md](SETUP.md)
- Test Results: [TEST_RESULTS.md](TEST_RESULTS.md)
- Demo Script: `python demo_test.py`
