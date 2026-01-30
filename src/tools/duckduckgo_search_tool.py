# LangChain Tool for DuckDuckGo Search (Free Alternative)
from typing import Type, Optional, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ddgs import DDGS
from loguru import logger


class DuckDuckGoSearchInput(BaseModel):
    """Input schema for DuckDuckGo Search tool"""
    query: str = Field(description="The search query for cybersecurity threat intelligence")


class DuckDuckGoSearchTool(BaseTool):
    """LangChain tool for searching cybersecurity threat intelligence using DuckDuckGo (Free, No API Key)"""
    
    name: str = "duckduckgo_threat_intelligence"
    description: str = """
    Searches for real-time cybersecurity threat intelligence, CVE information, 
    attack patterns, and security advisories using DuckDuckGo search.
    
    This is a FREE alternative that requires NO API key.
    
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
    args_schema: Type[BaseModel] = DuckDuckGoSearchInput
    
    def get_search_results(self, query: str) -> List[dict]:
        """Get raw search results for API response"""
        logger.info(f"DuckDuckGo: Fetching results for '{query}'")
        
        try:
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=5))
            
            results = []
            for r in search_results:
                results.append({
                    "title": r.get("title", "No title"),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "No description available")
                })
            
            if not results:
                logger.warning(f"No results found for: {query}")
            
            return results
        except Exception as e:
            logger.error(f"Error fetching search results: {e}")
            return []
    
    def _run(self, query: str) -> str:
        """
        Execute DuckDuckGo Search for threat intelligence
        
        Args:
            query: Search query
            
        Returns:
            Formatted search results
        """
        logger.info(f"DuckDuckGo Search Tool: Searching for '{query}'")
        
        try:
            # Use DuckDuckGo Instant Answer API
            api_url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
            
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # Get related topics
            related_topics = data.get("RelatedTopics", [])
            for topic in related_topics[:5]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "url": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", "")
                    })
            
            # Add abstract if available
            if data.get("Abstract"):
                results.insert(0, {
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("Abstract", "")
                })
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=5))
            
            if not search_results:
                return f"No specific threat intelligence found for query: {query}"
            
            # Format results for LLM consumption
            formatted_results = f"""
DuckDuckGo Threat Intelligence Results for: "{query}"
{'='*70}

Found {len(search_results)} relevant sources:

"""
            for i, result in enumerate(search_results, 1):
                formatted_results += f"""
[{i}] {result.get('title', 'No title')}
    URL: {result.get('href', '')}
    Summary: {result.get('body', 'No description')[:300]}

"""
            
            formatted_results += f"""
{'='*70}
Use this threat intelligence to enhance your analysis of the log.
"""
            
            logger.info(f"DuckDuckGo Search: Found {len(search_results)} results")
            return formatted_results
            
        except Exception as e:
            error_msg = f"DuckDuckGo search error: {str(e)}"
            logger.error(error_msg)
            return f"Error retrieving threat intelligence: {error_msg}. Proceeding with available information."