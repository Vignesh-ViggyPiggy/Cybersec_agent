# FastAPI Server for CyberSec Agent
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import sys

from .schemas import LogAnalysisRequest, LogAnalysisResponse, HealthResponse
from ..agent.cybersec_agent import CyberSecAgent
from ..clients.bert_client import BertClient
from ..config import settings


# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)


# Initialize FastAPI app
app = FastAPI(
    title="CyberSec Agent API",
    description="AI-powered security log analysis using LangChain, BERT, and Brave Search",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize agent (lazy loading)
agent: CyberSecAgent = None


def get_agent() -> CyberSecAgent:
    """Get or create agent instance"""
    global agent
    if agent is None:
        logger.info("Initializing CyberSec Agent...")
        agent = CyberSecAgent(verbose=False)
    return agent


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting CyberSec Agent API")
    logger.info(f"LLM URL: {settings.llm_base_url}")
    logger.info(f"BERT API URL: {settings.bert_api_url}")
    logger.info(f"Search Provider: {settings.search_provider}")
    if settings.search_provider.lower() == "brave":
        logger.info(f"Brave API configured: {bool(settings.brave_api_key and settings.brave_api_key != 'your_brave_api_key_here')}")
    
    # Pre-initialize agent
    try:
        get_agent()
        logger.info("Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "service": "CyberSec Agent API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    
    # Check BERT API
    bert_client = BertClient(settings.bert_api_url)
    bert_healthy = bert_client.check_health()
    
    return HealthResponse(
        status="healthy" if bert_healthy else "degraded",
        llm_url=settings.llm_base_url,
        bert_url=settings.bert_api_url,
        bert_healthy=bert_healthy,
        search_provider=settings.search_provider
    )


@app.post("/api/analyze", response_model=LogAnalysisResponse)
async def analyze_log(request: LogAnalysisRequest):
    """
    Analyze a security log
    
    This endpoint uses a LangChain agent to orchestrate:
    1. BERT anomaly detection
    2. Brave Search threat intelligence
    3. LLM-powered analysis
    
    Returns structured threat analysis with severity, explanation, and recommendations.
    """
    try:
        logger.info(f"Received analysis request (log length: {len(request.log_text)} chars)")
        
        # Get agent
        agent_instance = get_agent()
        
        # Analyze log
        result = agent_instance.analyze_log(
            log_text=request.log_text,
            use_brave_search=request.use_brave_search
        )
        
        # Return response
        return LogAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"Error during log analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# Run server
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )
