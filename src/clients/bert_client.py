# BERT Anomaly Detection Client
import requests
from typing import Dict, Any, Optional
from loguru import logger


class BertClient:
    """Client for communicating with BERT anomaly detection API"""
    
    def __init__(self, api_url: str, timeout: int = 30):
        """
        Initialize BERT client
        
        Args:
            api_url: Base URL of BERT API (e.g., http://localhost:7000)
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.health_endpoint = f"{self.api_url}/health"
        self.detect_endpoint = f"{self.api_url}/detect-anomaly"
        
    def check_health(self) -> bool:
        """Check if BERT API is available"""
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"BERT API health check failed: {e}")
            return False
    
    def detect_anomaly(self, log_text: str) -> Dict[str, Any]:
        """
        Detect anomalies in log text using BERT model
        
        Args:
            log_text: The log text to analyze
            
        Returns:
            Dict containing:
                - anomaly_score: float
                - is_anomaly: bool
                - threshold: float
                - error: Optional[str]
        """
        try:
            logger.debug(f"Sending log to BERT API: {log_text[:100]}...")
            
            response = requests.post(
                self.detect_endpoint,
                json={"log_text": log_text},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"BERT anomaly detection: score={data.get('anomaly_score')}, is_anomaly={data.get('is_anomaly')}")
            
            return {
                "anomaly_score": data.get("anomaly_score", 0.0),
                "is_anomaly": data.get("is_anomaly", False),
                "threshold": data.get("threshold", 10.5),
                "error": None
            }
            
        except requests.exceptions.Timeout:
            error_msg = "BERT API request timed out"
            logger.error(error_msg)
            return {
                "anomaly_score": 0.0,
                "is_anomaly": False,
                "threshold": 10.5,
                "error": error_msg
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"BERT API request failed: {str(e)}"
            logger.error(error_msg)
            return {
                "anomaly_score": 0.0,
                "is_anomaly": False,
                "threshold": 10.5,
                "error": error_msg
            }
            
        except Exception as e:
            error_msg = f"Unexpected error during BERT detection: {str(e)}"
            logger.error(error_msg)
            return {
                "anomaly_score": 0.0,
                "is_anomaly": False,
                "threshold": 10.5,
                "error": error_msg
            }


# Example usage
if __name__ == "__main__":
    from ..config import settings
    
    client = BertClient(settings.bert_api_url)
    
    # Check health
    if client.check_health():
        print("✓ BERT API is healthy")
    else:
        print("✗ BERT API is not available")
    
    # Test detection
    test_log = "Failed login attempt from 192.168.1.100 with user admin"
    result = client.detect_anomaly(test_log)
    print(f"\nTest log: {test_log}")
    print(f"Result: {result}")
