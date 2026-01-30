# API Schemas
from typing import List, Optional
from pydantic import BaseModel, Field


class SearchSource(BaseModel):
    """Search result source"""
    title: str = Field(description="Title of the source")
    url: str = Field(description="URL of the source")
    snippet: str = Field(description="Brief description or snippet")


class AgentAction(BaseModel):
    """Action taken by the LangChain agent"""
    tool: str = Field(description="Name of the tool used")
    tool_input: str = Field(description="Input provided to the tool")
    observation: str = Field(description="Result from the tool")


class BertAnomalyData(BaseModel):
    """BERT anomaly detection results"""
    anomaly_score: float = Field(description="Anomaly score from BERT model")
    is_anomaly: bool = Field(description="Whether log is classified as anomalous")
    threshold: float = Field(description="Anomaly detection threshold")
    confidence: float = Field(description="Confidence percentage")


class LogAnalysisRequest(BaseModel):
    """Request schema for log analysis"""
    log_text: str = Field(
        ...,
        description="The log content to analyze",
        min_length=1,
        max_length=50000
    )
    use_brave_search: bool = Field(
        default=True,
        description="Whether to use Brave Search for threat intelligence"
    )


class LogAnalysisResponse(BaseModel):
    """Response schema for log analysis"""
    threat_type: str = Field(description="Type of threat identified")
    severity: str = Field(description="Severity level: CRITICAL, HIGH, MEDIUM, LOW, INFO")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0")
    explanation: str = Field(description="Detailed explanation of the analysis")
    indicators_of_compromise: List[str] = Field(
        default=[],
        description="List of indicators of compromise found"
    )
    recommended_actions: List[str] = Field(
        default=[],
        description="Recommended actions to take"
    )
    raw_analysis: Optional[str] = Field(
        default=None,
        description="Raw analysis output from the agent"
    )
    bert_data: Optional[BertAnomalyData] = Field(
        default=None,
        description="BERT anomaly detection data"
    )
    search_sources: List[SearchSource] = Field(
        default=[],
        description="List of search sources used for threat intelligence"
    )
    search_query: Optional[str] = Field(
        default=None,
        description="Query used for threat intelligence search"
    )
    agent_summary: Optional[str] = Field(
        default=None,
        description="Final summary from LangChain agent"
    )
    agent_actions: List[AgentAction] = Field(
        default=[],
        description="Additional tool calls made by the autonomous agent"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if analysis failed"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    llm_url: str
    bert_url: str
    bert_healthy: bool
    search_provider: str
    version: str = "1.0.0"
