# CyberSec Agent - AI-Powered Log Analysis System

An intelligent cybersecurity log analysis system that combines LangChain, local LLM, BERT anomaly detection, and Brave Search API to provide comprehensive threat analysis.

## Architecture

- **Frontend/CLI**: Runs locally on user's machine
- **LLM & BERT Model**: Can be hosted locally or on remote machines
- **Analysis Pipeline**: LangChain agent orchestrates tools for comprehensive analysis

## Features

- 🤖 **LangChain Agent**: Intelligent orchestration of analysis tools
- 🔍 **BERT Anomaly Detection**: ML-based log anomaly scoring
- 🌐 **Threat Intelligence Search**: DuckDuckGo (free, no API key) or Brave Search API
- 📊 **Structured Analysis**: Threat type, severity, explanation, and recommendations
- 🔌 **Flexible Deployment**: Local or remote hosting for models

## Installation

1. Clone and navigate to the directory:
```bash
cd cybersec_agent
```

2. Create virtual environment (or use parent venv):
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Quick Start

Start all services with one command:
```bash
# Windows
.\start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

Then open your browser to `http://localhost:3000`
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Quick Start

Start all services with one command:
```bash
# Windows
.\start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

Then open your browser to `http://localhost:3000`

## Configuration

Edit `.env` file:

```env
# Local LLM (Ollama)
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2

# Remote LLM example
# LLM_BASE_URL=http://remote-server:11434

# BERT API (local or remote)
BERT_API_URL=http://localhost:7000

# Search Provider (FREE option available!)
SEARCH_PROVIDER=duckduckgo  # Options: 'duckduckgo' (free) or 'brave'

# Brave Search API Key (only needed if using SEARCH_PROVIDER=brave)
BRAVE_API_KEY=your_api_key_here
```

**Search Options:**
- **DuckDuckGo** (default): FREE, no API key required
- **Brave**: Requires API key from https://brave.com/search/api/

## Usage

### Quick Start - All Services

Start everything with one command:
```bash
# Windows
.\start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

This will start:
1. BERT API (Port 7000) - if not already running
2. Ollama check (Port 11434)
3. CyberSec Agent API (Port 8080)
4. Web Frontend (Port 3000)

Then open your browser to `http://localhost:3000`

**Web Frontend Features:**
- Modern, dark-themed UI
- Real-time analysis with loading indicators
- Color-coded severity badges
- Visual confidence scores
- Quick sample logs for testing
- Responsive design

### Individual Services (Advanced)

**API Server Only:**
```bash
cd cybersec_agent
python -m src.api.server
```
Access at `http://localhost:8080/docs`

**CLI Interface Only:**
```bash
python -m src.cli.main
```
Interactive terminal mode

**API Endpoint Example:**
```bash
POST http://localhost:8080/api/analyze
Content-Type: application/json

{
  "log_text": "Failed login attempt from 192.168.1.100",
  "use_brave_search": true
}
```

### Example Usage

```python
from src.agent.cybersec_agent import CyberSecAgent

agent = CyberSecAgent()
result = agent.analyze_log("Suspicious network traffic detected on port 445")

print(result["threat_type"])
print(result["severity"])
print(result["explanation"])
print(result["recommended_actions"])
```

## Project Structure

```
cybersec_agent/
├── src/
│   ├── agent/              # LangChain agent implementation
│   │   ├── cybersec_agent.py
│   │   └── prompts.py
│   ├── tools/              # LangChain tools
│   │   ├── bert_tool.py
│   │   └── brave_search_tool.py
│   ├── clients/            # API clients
│   │   ├── bert_client.py
│   │   └── llm_client.py
│   ├── api/                # FastAPI server
│   │   ├── server.py
│   │   └── schemas.py
│   ├── cli/                # Command-line interface
│   │   └── main.py
│   └── config.py           # Configuration management
├── frontend/               # React web interface
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api.js          # API client
│   │   └── App.jsx         # Main app
│   ├── package.json
│   └── vite.config.js
├── docker/                 # Docker configurations
├── examples/               # Sample logs
├── requirements.txt
├── .env.example
└── README.md
```

## Dependencies

### Running BERT Model (if local)

Start the BERT anomaly detection server:
```bash
cd ../
uvicorn app:app --host 0.0.0.0 --port 7000
```

### Running Ollama (if local)

```bash
ollama serve
ollama pull llama3.2
```

## Response Schema

```json
{
  "threat_type": "Brute Force Attack",
  "severity": "HIGH",
  "confidence_score": 0.87,
  "explanation": "Multiple failed login attempts detected...",
  "recommended_actions": [
    "Implement account lockout policy",
    "Enable multi-factor authentication",
    "Review authentication logs"
  ],
  "bert_anomaly_score": 8.5,
  "is_anomaly": true,
  "threat_intelligence": [
    {
      "source": "example.com",
      "title": "Brute Force Attack Patterns",
      "url": "https://..."
    }
  ]
}
```

## License

MIT
