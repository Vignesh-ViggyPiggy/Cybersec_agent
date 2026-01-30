# LangChain Tool for Brave Search API
from typing import Type, Optional, List, Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from loguru import logger

from ..config import settings


class BraveSearchInput(BaseModel):
    """Input schema for Brave Search tool"""
    query: str = Field(description="The search query for cybersecurity threat intelligence")


class BraveSearchTool(BaseTool):
    """LangChain tool for searching cybersecurity threat intelligence using Brave Search API"""
    
    name: str = "brave_threat_intelligence"
    description: str = """
    Searches for real-time cybersecurity threat intelligence, CVE information, 
    attack patterns, and security advisories using Brave Search API.
    
    Use this tool to:
    - Look up CVE details and exploit information
    - Find information about specific attack types (e.g., "SQL injection patterns")
    - Research malware families and techniques
    - Get latest security advisories and patches
    
    Input: query (string) - Search query related to the threat or log content
    
    Returns: Formatted search results with titles, URLs, and descriptions from 
    trusted security sources.
    
    Example queries:
    - "CVE-2024-1234 exploitation details"
    - "SSH brute force attack indicators"
    - "ransomware lateral movement techniques"
    """
    args_schema: Type[BaseModel] = BraveSearchInput
    
    api_key: str = ""
    base_url: str = "https://api.search.brave.com/res/v1/web/search"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.api_key:
            self.api_key = settings.brave_api_key
    
    def get_search_results(self, query: str) -> List[dict]:
        """Get raw search results for API response"""
        logger.info(f"Brave Search: Fetching results for '{query}'")
        
        if not self.api_key or self.api_key == "your_brave_api_key_here":
            return []
        
        try:
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.api_key
            }
            params = {"q": query, "count": 5}
            
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get("web", {}).get("results", [])
            
            return [
                {
                    "title": r.get("title", "No title"),
                    "url": r.get("url", ""),
                    "snippet": r.get("description", "No description")
                }
                for r in results[:5]
            ]
        except Exception as e:
            logger.error(f"Error fetching Brave search results: {e}")
            return []
    
    def _run(self, query: str) -> str:
        """
        Execute Brave Search for threat intelligence
        
        Args:
            query: Search query
            
        Returns:
            Formatted search results
        """
        logger.info(f"Brave Search Tool: Searching for '{query}'")
        
        if not self.api_key or self.api_key == "your_brave_api_key_here":
            logger.warning("Brave API key not configured")
            return """
Brave Search API Error: API key not configured.
Please set BRAVE_API_KEY in your .env file.

To get an API key:
1. Visit https://brave.com/search/api/
2. Sign up for an API key
3. Add it to your .env file: BRAVE_API_KEY=your_key_here
"""
        
        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key
            }
            
            params = {
                "q": query,
                "count": 5,  # Number of results
                "safesearch": "off",
                "text_decorations": False,
                "search_lang": "en"
            }
            
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("web", {}).get("results", [])
            
            if not results:
                return f"No threat intelligence found for query: {query}"
            
            # Format results for LLM consumption
            formatted_results = f"""
Brave Search Threat Intelligence Results for: "{query}"
{'='*70}

Found {len(results)} relevant sources:

"""
            for i, result in enumerate(results[:5], 1):
                title = result.get("title", "No title")
                url = result.get("url", "")
                description = result.get("description", "No description available")
                
                formatted_results += f"""
[{i}] {title}
    URL: {url}
    Summary: {description}

"""
            
            formatted_results += f"""
{'='*70}
Use this threat intelligence to enhance your analysis of the log.
"""
            
            logger.info(f"Brave Search: Found {len(results)} results")
            return formatted_results
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Brave Search API error: {str(e)}"
            logger.error(error_msg)
            return f"Error retrieving threat intelligence: {error_msg}"
        
        except Exception as e:
            error_msg = f"Unexpected error during search: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    
    async def _arun(self, query: str) -> str:
        """Async version (not implemented, falls back to sync)"""
        return self._run(query)


# Example usage
if __name__ == "__main__":
    tool = BraveSearchTool()
    
    test_queries = [
        "SSH brute force attack detection",
        "CVE-2024-1234",
        "ransomware indicators of compromise"
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Testing: {query}")
        print(f"{'='*70}")
        result = tool._run(query)
        print(result)
