# CyberSec Agent - AI-Powered Log Analysis System

An intelligent cybersecurity log analysis system that combines LangChain, local LLM, BERT anomaly detection, and threat intelligence search to provide comprehensive security log analysis with autonomous agent capabilities.

## Architecture

- **Frontend**: React-based web UI with real-time analysis and network access support
- **Backend**: FastAPI server orchestrating the analysis pipeline
- **LLM & BERT Model**: Can be hosted locally (Ollama) or on remote machines
- **Analysis Pipeline**: 5-step workflow combining manual orchestration with autonomous LangChain agent

## 5-Step Analysis Workflow

1. **BERT Anomaly Detection**: ML-based log anomaly scoring with confidence metrics
2. **LLM Threat Extraction**: Intelligent identification of specific threats for targeted search
3. **Threat Intelligence Search**: DuckDuckGo or Brave Search with real source URLs
4. **Comprehensive Analysis**: Structured threat analysis with severity, IOCs, and recommendations
5. **LangChain Agent Summary**: Autonomous agent provides executive summary and can make additional tool calls if needed

## Features

- 🤖 **Hybrid LangChain Agent**: Reliable 4-step workflow + autonomous agent for final summary and verification
- 🔍 **BERT Anomaly Detection**: Visual display of anomaly scores, thresholds, status, and confidence
- 🌐 **Threat Intelligence Search**: DuckDuckGo (free, default) or Brave Search with clickable source links
- 📊 **Structured Analysis**: Threat type, severity, confidence scores, IOCs, and actionable recommendations
- 🎯 **Executive Summary**: LLM-powered final summary with optional autonomous tool calls
- 🔗 **Real Source URLs**: Clickable links to security blogs, documentation, and threat intelligence sources
- 🌐 **Network Access**: Automatic hostname detection for multi-device access on same network
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

**Access from other devices on same network:**
The frontend automatically detects your IP address, so you can access from any device on the same network:
- `http://<your-ip>:3000` (e.g., `http://192.168.1.100:3000`)

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
- Modern, dark-themed UI with gradient accents
- Real-time analysis with loading indicators
- Color-coded severity badges (CRITICAL, HIGH, MEDIUM, LOW, INFO)
- Visual confidence scores with progress bars
- **BERT Anomaly Detection Display**: 4-column grid showing anomaly score, threshold, status, and confidence
- **Clickable Threat Intelligence Sources**: Real URLs with titles, links, and snippets from security sources
- **LangChain Agent Summary**: Executive summary with optional additional tool calls displayed
- Quick sample logs for testing
- Responsive design
- **Network access**: Automatic IP detection for access from any device on same network

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

print(f"Threat: {result['threat_type']}")
print(f"Severity: {result['severity']}")
print(f"Confidence: {result['confidence_score']}")
print(f"\nExplanation: {result['explanation']}")

# BERT Detection Data
if result.get('bert_data'):
    print(f"\nBERT Anomaly Score: {result['bert_data']['anomaly_score']}")
    print(f"Is Anomalous: {result['bert_data']['is_anomaly']}")
    print(f"Confidence: {result['bert_data']['confidence']}%")

# Threat Intelligence Sources
if result.get('search_sources'):
    print(f"\nThreat Intelligence Sources ({len(result['search_sources'])}):")
    for source in result['search_sources']:
        print(f"  - {source['title']}: {source['url']}")

# LangChain Agent Summary
if result.get('agent_summary'):
    print(f"\nExecutive Summary: {result['agent_summary']}")
    if result.get('agent_actions'):
        print(f"Agent made {len(result['agent_actions'])} additional tool calls")

# Recommended Actions
print("\nRecommended Actions:")
for i, action in enumerate(result['recommended_actions'], 1):
    print(f"  {i}. {action}")
```

## Project Structure

```
cybersec_agent/
├── src/
│   ├── agent/              # LangChain agent implementation
│   │   ├── cybersec_agent.py   # Main agent with 5-step workflow
│   │   └── prompts.py          # System prompts
│   ├── tools/              # LangChain BaseTool implementations
│   │   ├── bert_tool.py            # BERT anomaly detection tool
│   │   ├── brave_search_tool.py    # Brave Search API tool
│   │   └── duckduckgo_search_tool.py  # DuckDuckGo search tool (free)
│   ├── clients/            # API clients
│   │   ├── bert_client.py      # BERT API client
│   │   └── llm_client.py       # Ollama LLM client
│   ├── api/                # FastAPI server
│   │   ├── server.py           # Main API server
│   │   └── schemas.py          # Pydantic models
│   ├── cli/                # Command-line interface
│   │   └── main.py
│   └── config.py           # Configuration management
├── frontend/               # React web interface
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── LogUploader.jsx    # Log input component
│   │   │   └── ResultViewer.jsx   # Results display (BERT, sources, summary)
│   │   ├── api.js          # API client with auto hostname detection
│   │   ├── App.jsx         # Main app
│   │   └── App.css         # Styles
│   ├── package.json
│   └── vite.config.js
├── docker/                 # Docker configurations
├── examples/               # Sample logs
├── test_agent_workflow.py  # Test script
├── requirements.txt
├── .env.example
├── start.bat              # Windows startup script
├── start.sh               # Linux/Mac startup script
└── README.md
```

## Dependencies

### Python Backend
- **LangChain 0.3.x**: Agent framework and tool orchestration
- **FastAPI 0.109.0**: High-performance API server
- **Ollama**: Local LLM inference
- **ddgs 9.10.0**: DuckDuckGo search integration (free)
- **Pydantic 2.5.3**: Data validation
- **Loguru**: Logging

### Frontend
- **React 18.2.0**: UI framework
- **Vite**: Fast build tool
- **Axios**: HTTP client

### Running BERT Model (if local)

Start the BERT anomaly detection server:
```bash
cd ../
uvicorn app:app --host 0.0.0.0 --port 7000
```

### Running Ollama (if local)

```bash
ollama serve
ollama pull seneca  # or llama3.2, mistral, etc.
```

## Testing

Run the comprehensive test:
```bash
python test_agent_workflow.py
```

This will test the full 5-step workflow and show:
- BERT anomaly detection
- Threat keyword extraction
- Threat intelligence search
- Comprehensive analysis
- LangChain agent summary and autonomous tool calls

## How It Works

1. **User submits log** → Frontend sends to FastAPI backend
2. **BERT Analysis** → ML model scores log for anomalies
3. **Threat Extraction** → LLM identifies specific threats (e.g., "SSH brute force")
4. **Intelligence Search** → DuckDuckGo/Brave searches for threat-specific information
5. **LLM Analysis** → Generates structured threat report with IOCs and recommendations
6. **Agent Summary** → LangChain agent provides executive summary and can make additional tool calls if needed
7. **Results Display** → Frontend shows all data with visual components

## API Endpoints

- `GET /` - Root endpoint with service info
- `GET /health` - Health check for all services
- `POST /api/analyze` - Analyze security log
- `GET /docs` - Interactive API documentation (Swagger UI)

## Response Schema

```json
{
  "threat_type": "Brute Force Attack",
  "severity": "HIGH",
  "confidence_score": 0.92,
  "explanation": "Multiple failed SSH login attempts detected from 203.0.113.42...",
  "indicators_of_compromise": [
    "IP: 203.0.113.42",
    "Failed login attempts: 5",
    "Targeted accounts: admin, root"
  ],
  "recommended_actions": [
    "Block suspicious IP 203.0.113.42",
    "Enable SSH key authentication",
    "Implement rate limiting on SSH"
  ],
  "bert_data": {
    "anomaly_score": 10.46,
    "is_anomaly": false,
    "threshold": 11.5,
    "confidence": 99.6
  },
  "search_query": "SSH brute force attack indicators",
  "search_sources": [
    {
      "title": "SSH Brute Force Attack Detection and Prevention",
      "url": "https://example.com/ssh-security",
      "snippet": "Learn how to detect and prevent SSH brute force attacks..."
    }
  ],
  "agent_summary": "The network is under high-risk brute-force attack as multiple failed SSH login attempts target privileged accounts. This pattern aligns with distributed attacks and could lead to system compromise.",
  "agent_actions": [
    {
      "tool": "duckduckgo_threat_intelligence",
      "tool_input": "CVE-2024-1234 exploitation",
      "observation": "Found 5 threat intelligence sources..."
    }
  ],
  "raw_analysis": "Full LLM analysis text..."
}
```

## License

MIT
