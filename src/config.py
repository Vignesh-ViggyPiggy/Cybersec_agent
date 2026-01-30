# Configuration Management
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # LLM Configuration
    llm_base_url: str = Field(default="http://localhost:11434", description="Ollama or LLM API base URL")
    llm_model: str = Field(default="llama3.2", description="LLM model name")
    
    # BERT Anomaly Detection
    bert_api_url: str = Field(default="http://localhost:7000", description="BERT API endpoint")
    
    # Search API Configuration
    search_provider: str = Field(default="duckduckgo", description="Search provider: 'duckduckgo' (free) or 'brave'")
    brave_api_key: str = Field(default="", description="Brave Search API key (only needed if search_provider='brave')")
    
    # Application Settings
    log_level: str = Field(default="INFO", description="Logging level")
    max_log_length: int = Field(default=10000, description="Maximum log text length")
    
    # Server Configuration
    api_host: str = Field(default="0.0.0.0", description="API server host")
    api_port: int = Field(default=8080, description="API server port")
    
    # Analysis Configuration
    bert_anomaly_threshold: float = Field(default=10.5, description="BERT anomaly threshold")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
