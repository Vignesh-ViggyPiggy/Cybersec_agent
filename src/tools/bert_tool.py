# LangChain Tool for BERT Anomaly Detection
from typing import Type, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from loguru import logger

from ..clients.bert_client import BertClient
from ..config import settings


class BertAnomalyInput(BaseModel):
    """Input schema for BERT anomaly detection tool"""
    log_text: str = Field(description="The log text to analyze for anomalies")


class BertAnomalyTool(BaseTool):
    """LangChain tool for detecting anomalies in logs using BERT model"""
    
    name: str = "bert_anomaly_detector"
    description: str = """
    Detects anomalies in log text using a fine-tuned BERT model.
    Use this tool FIRST before any analysis to determine if the log is anomalous.
    
    Input: log_text (string) - The log entry or log file content to analyze
    
    Returns: A JSON string containing:
    - anomaly_score: Numerical score indicating anomaly level
    - is_anomaly: Boolean indicating if log is anomalous
    - confidence: Confidence percentage
    - interpretation: Human-readable interpretation of the score
    """
    args_schema: Type[BaseModel] = BertAnomalyInput
    
    bert_client: Optional[BertClient] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.bert_client is None:
            self.bert_client = BertClient(settings.bert_api_url)
    
    def get_detection_data(self, log_text: str) -> dict:
        """Get raw detection data for API response"""
        if len(log_text) > settings.max_log_length:
            log_text = log_text[:settings.max_log_length]
        
        result = self.bert_client.detect_anomaly(log_text)
        
        if result.get("error"):
            return None
        
        anomaly_score = result["anomaly_score"]
        threshold = result["threshold"]
        confidence = min(100.0, (anomaly_score / threshold) * 100)
        
        return {
            "anomaly_score": anomaly_score,
            "is_anomaly": result["is_anomaly"],
            "threshold": threshold,
            "confidence": confidence
        }
    
    def _run(self, log_text: str) -> str:
        """
        Execute BERT anomaly detection
        
        Args:
            log_text: The log text to analyze
            
        Returns:
            JSON string with detection results
        """
        logger.info("BERT Anomaly Tool: Analyzing log")
        
        # Truncate if too long
        if len(log_text) > settings.max_log_length:
            log_text = log_text[:settings.max_log_length]
            logger.warning(f"Log truncated to {settings.max_log_length} characters")
        
        result = self.bert_client.detect_anomaly(log_text)
        
        # Format result as structured text for LLM
        if result.get("error"):
            return f"""
BERT Anomaly Detection ERROR: {result['error']}
Unable to perform anomaly detection. Proceeding with manual analysis.
"""
        
        anomaly_score = result["anomaly_score"]
        is_anomaly = result["is_anomaly"]
        threshold = result["threshold"]
        
        # Calculate confidence percentage
        confidence = min(100.0, (anomaly_score / threshold) * 100)
        
        # Interpret the score
        if anomaly_score < threshold * 0.3:
            interpretation = "NORMAL - Log appears benign with typical patterns"
        elif anomaly_score < threshold * 0.7:
            interpretation = "SUSPICIOUS - Log shows minor deviations from normal"
        elif anomaly_score < threshold:
            interpretation = "CONCERNING - Log exhibits unusual patterns"
        else:
            interpretation = "ANOMALOUS - Log shows significant abnormal behavior"
        
        return f"""
BERT Anomaly Detection Results:
================================
Anomaly Score: {anomaly_score:.2f} (Threshold: {threshold:.2f})
Is Anomaly: {'YES' if is_anomaly else 'NO'}
Confidence: {confidence:.1f}%
Interpretation: {interpretation}

Analysis: {'This log exhibits anomalous behavior and requires deeper investigation.' if is_anomaly else 'This log appears normal but should still be analyzed for context.'}
"""
    
    async def _arun(self, log_text: str) -> str:
        """Async version (not implemented, falls back to sync)"""
        return self._run(log_text)


# Example usage
if __name__ == "__main__":
    tool = BertAnomalyTool()
    
    test_logs = [
        "User admin logged in successfully from 192.168.1.50",
        "Failed login attempt from 203.0.113.42 user: admin",
        "ALERT: Unauthorized access attempt detected on port 22 from 198.51.100.10"
    ]
    
    for log in test_logs:
        print(f"\n{'='*60}")
        print(f"Testing: {log}")
        print(f"{'='*60}")
        result = tool._run(log)
        print(result)
