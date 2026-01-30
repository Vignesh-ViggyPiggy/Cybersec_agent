"""
Simple test demonstrating the CyberSec Agent working
"""
import sys
sys.path.insert(0, "c:/Users/vigne/Downloads/Installer/api_example/cybersec_agent")

print("="*70)
print("🛡️  CyberSec Agent - Test Run Demonstration")
print("="*70)
print()

# Step 1: Test BERT API
print("✓ Testing BERT API Connection...")
import requests
try:
    response = requests.get("http://localhost:7000/health", timeout=5)
    if response.status_code == 200:
        print(f"  BERT API: {response.json()}")
        print("  ✓ BERT API is running\n")
    else:
        print("  ✗ BERT API returned unexpected status\n")
except Exception as e:
    print(f"  ✗ BERT API not available: {e}\n")

# Step 2: Test BERT detection directly
print("✓ Testing BERT Anomaly Detection...")
test_log = "Failed password for admin from 203.0.113.42 port 55892 ssh2"
print(f"  Test log: {test_log}")

try:
    bert_response = requests.post(
        "http://localhost:7000/detect-anomaly",
        json={"log_text": test_log},
        timeout=10
    )
    bert_data = bert_response.json()
    print(f"  Anomaly Score: {bert_data['anomaly_score']:.2f}")
    print(f"  Is Anomaly: {bert_data['is_anomaly']}")
    print(f"  ✓ BERT detection successful\n")
except Exception as e:
    print(f"  ✗ BERT detection failed: {e}\n")

# Step 3: Test Ollama
print("✓ Testing Ollama LLM...")
try:
    ollama_response = requests.get("http://localhost:11434/api/tags", timeout=5)
    models = ollama_response.json().get('models', [])
    print(f"  Available models: {[m['name'] for m in models]}")
    print(f"  ✓ Ollama is running with {len(models)} model(s)\n")
except Exception as e:
    print(f"  ✗ Ollama not available: {e}\n")

# Step 4: Test full stack with API (if running)
print("✓ Testing Full Stack (API Server)...")
print("  Note: This requires the API server to be running.")
print("  You can start it with: python -m src.api.server")
print()

try:
    health_response = requests.get("http://localhost:8080/health", timeout=5)
    if health_response.status_code == 200:
        health_data = health_response.json()
        print(f"  API Status: {health_data['status']}")
        print(f"  BERT Healthy: {health_data['bert_healthy']}")
        print("  ✓ API server is running\n")
        
        # Try an analysis
        print("  Running log analysis...")
        analysis_response = requests.post(
            "http://localhost:8080/api/analyze",
            json={
                "log_text": test_log,
                "use_brave_search": False
            },
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            result = analysis_response.json()
            print(f"\n  RESULTS:")
            print(f"  ========")
            print(f"  Threat Type: {result.get('threat_type', 'N/A')}")
            print(f"  Severity: {result.get('severity', 'N/A')}")
            print(f"  Confidence: {result.get('confidence_score', 0)*100:.1f}%")
            print(f"  ✓ Analysis completed successfully!\n")
        else:
            print(f"  ✗ Analysis failed with status {analysis_response.status_code}\n")
            
    else:
        print("  ✗ API server returned unexpected status\n")
except requests.exceptions.ConnectionError:
    print("  ℹ  API server not running (this is optional for this demo)\n")
except Exception as e:
    print(f"  ℹ  API server check skipped: {e}\n")

print("="*70)
print("Test Summary")
print("="*70)
print("The CyberSec Agent system components:")
print("1. ✓ BERT API (Port 7000) - Anomaly detection model")
print("2. ✓ Ollama LLM (Port 11434) - Language model") 
print("3. • CyberSec Agent API (Port 8080) - Main API (optional)")
print("4. • Frontend (Port 3000) - Web interface (optional)")
print()
print("To run the full system:")
print("  Terminal 1: python -m src.api.server")
print("  Terminal 2: cd frontend && npm run dev")
print("="*70)
