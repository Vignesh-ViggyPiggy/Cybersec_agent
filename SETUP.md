# Setup and Installation Guide

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and configure:
# - LLM_BASE_URL (Ollama endpoint)
# - BERT_API_URL (BERT model endpoint)
# - BRAVE_API_KEY (from https://brave.com/search/api/)
```

### 3. Start Required Services

#### Option A: Local Setup

**Start BERT API (in separate terminal):**
```bash
cd ..
uvicorn app:app --host 0.0.0.0 --port 7000
```

**Start Ollama (in separate terminal):**
```bash
ollama serve
ollama pull llama3.2
```

#### Option B: Docker Setup

```bash
docker-compose up -d
```

### 4. Run CyberSec Agent

**Start Everything (Recommended):**
```bash
# Windows:
.\start.bat

# Linux/Mac:
chmod +x start.sh
./start.sh
```

This starts all services and opens the web interface at `http://localhost:3000`

**Or start individual components:**

**API Server Only:**
```bash
python -m src.api.server
```

**CLI Interface Only:**
```bash
python -m src.cli.main
```

## Usage Examples

### CLI Usage

**Interactive mode:**
```bash
python -m src.cli.main
```

**Analyze log text:**
```bash
python -m src.cli.main "Failed login attempt from 192.168.1.100"
```

**Analyze log file:**
```bash
python -m src.cli.main -f /path/to/logfile.log
```

### API Usage

**Using curl:**
```bash
curl -X POST http://localhost:8080/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"log_text": "Failed login from 192.168.1.100", "use_brave_search": true}'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8080/api/analyze",
    json={
        "log_text": "Suspicious network traffic on port 445",
        "use_brave_search": True
    }
)

result = response.json()
print(f"Threat: {result['threat_type']}")
print(f"Severity: {result['severity']}")
print(f"Actions: {result['recommended_actions']}")
```

## Configuration Options

### Remote vs Local Deployment

#### Local LLM and BERT
```env
LLM_BASE_URL=http://localhost:11434
BERT_API_URL=http://localhost:7000
```

#### Remote LLM and Local BERT
```env
LLM_BASE_URL=http://remote-server:11434
BERT_API_URL=http://localhost:7000
```

#### Both Remote
```env
LLM_BASE_URL=http://llm-server:11434
BERT_API_URL=http://bert-server:7000
```

## Troubleshooting

### "Connection refused" errors

1. Check BERT API is running:
```bash
curl http://localhost:7000/health
```

2. Check Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

### "BERT API not configured" warning

Update `.env` with correct BERT API URL:
```env
BERT_API_URL=http://localhost:7000
```

### "Brave API key not configured"

Get API key from https://brave.com/search/api/ and add to `.env`:
```env
BRAVE_API_KEY=your_actual_api_key_here
```

## Development

### Running Tests
```bash
# Install dev dependencies
pip install pytest pytest-asyncio

# Run tests (when implemented)
pytest tests/
```

### Project Structure
```
cybersec_agent/
├── src/
│   ├── agent/          # LangChain agent
│   ├── tools/          # BERT and Brave Search tools
│   ├── clients/        # API clients
│   ├── api/            # FastAPI server
│   └── cli/            # Command-line interface
├── docker/             # Docker configurations
├── requirements.txt    # Python dependencies
└── .env               # Configuration
```
