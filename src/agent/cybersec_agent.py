# CyberSec Agent - Main Agent Implementation
import re
from typing import Dict, Any, Optional, List
from loguru import logger

from ..clients.llm_client import LLMClient
from ..tools.bert_tool import BertAnomalyTool
from ..tools.brave_search_tool import BraveSearchTool
from ..tools.duckduckgo_search_tool import DuckDuckGoSearchTool
from .prompts import SYSTEM_PROMPT, get_analysis_prompt
from ..config import settings


class CyberSecAgent:
    """
    Cybersecurity Log Analysis Agent using LangChain
    
    Orchestrates BERT anomaly detection and Brave Search to provide
    comprehensive threat analysis of security logs.
    """
    
    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        verbose: bool = True
    ):
        """
        Initialize CyberSec Agent
        
        Args:
            llm_client: Optional LLM client (creates default if not provided)
            verbose: Whether to show detailed agent execution logs
        """
        logger.info("Initializing CyberSec Agent")
        
        # Initialize LLM
        if llm_client is None:
            self.llm_client = LLMClient(
                base_url=settings.llm_base_url,
                model=settings.llm_model,
                temperature=0.7
            )
        else:
            self.llm_client = llm_client
        
        # Initialize tools
        self.bert_tool = BertAnomalyTool()
        
        # Initialize search tool based on configuration
        if settings.search_provider.lower() == "brave":
            self.search_tool = BraveSearchTool()
            logger.info("Using Brave Search for threat intelligence")
        else:
            self.search_tool = DuckDuckGoSearchTool()
            logger.info("Using DuckDuckGo Search (free) for threat intelligence")
        
        self.verbose = verbose
        
        # Store tools for agent use
        self.tools_map = {
            'bert_anomaly_detector': self.bert_tool,
            'brave_threat_intelligence' if settings.search_provider.lower() == 'brave' else 'duckduckgo_threat_intelligence': self.search_tool
        }
        
        logger.info("CyberSec Agent initialized successfully")
    
    def analyze_log(
        self,
        log_text: str,
        use_brave_search: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze a security log
        
        Args:
            log_text: The log content to analyze
            use_brave_search: Whether to use Brave Search (default: True)
            
        Returns:
            Dictionary containing structured analysis results
        """
        logger.info(f"Analyzing log (length: {len(log_text)} chars)")
        
        # Truncate if too long
        if len(log_text) > settings.max_log_length:
            log_text = log_text[:settings.max_log_length]
            logger.warning(f"Log truncated to {settings.max_log_length} characters")
        
        try:
            # Step 1: Run BERT anomaly detection
            if self.verbose:
                print("\n[1/5] Running BERT anomaly detection...")
            
            bert_result = self.bert_tool._run(log_text)
            bert_data = self.bert_tool.get_detection_data(log_text)
            
            # Step 2: Quick LLM analysis to identify threats for search
            threat_intel = ""
            search_sources = []
            search_query = None
            
            if use_brave_search:
                if self.verbose:
                    print("\n[2/5] Analyzing log to identify specific threats...")
                
                # Use LLM to extract specific threats from the log
                keywords = self._extract_threat_keywords(log_text, bert_result)
                
                if keywords:
                    if self.verbose:
                        print(f"\n[3/5] Searching threat intelligence for: {keywords}")
                    
                    search_query = keywords
                    threat_intel = self.search_tool._run(keywords)
                    search_sources = self.search_tool.get_search_results(keywords)
                    
                    if self.verbose:
                        print(f"Found {len(search_sources)} threat intelligence sources")
            
            # Step 4: Generate comprehensive analysis with LLM
            if self.verbose:
                print("\n[4/5] Generating comprehensive analysis...")
            
            analysis_prompt = f"""{SYSTEM_PROMPT}

Analyze the following security log:

LOG CONTENT:
{log_text}

BERT ANOMALY DETECTION RESULTS:
{bert_result}

{f"THREAT INTELLIGENCE:{threat_intel}" if threat_intel else ""}

Provide your structured analysis following this format:

**THREAT TYPE**: [specific threat type]

**SEVERITY LEVEL**: [CRITICAL/HIGH/MEDIUM/LOW/INFO]

**CONFIDENCE SCORE**: [0.0 to 1.0]

**DETAILED EXPLANATION**: 
[Your detailed analysis]

**INDICATORS OF COMPROMISE** (if applicable):
- [IOC 1]
- [IOC 2]

**RECOMMENDED ACTIONS**:
1. [Action 1]
2. [Action 2]
"""
            
            raw_output = self.llm_client.invoke(analysis_prompt)
            
            # Parse the structured output
            parsed_result = self._parse_analysis(raw_output)
            
            # Add metadata
            parsed_result["raw_analysis"] = raw_output
            parsed_result["log_text"] = log_text
            parsed_result["bert_data"] = bert_data
            parsed_result["search_sources"] = search_sources
            parsed_result["search_query"] = search_query
            
            # Step 5: Final LangChain agent summarization and autonomous tool calling
            if self.verbose:
                print("\n[5/5] Running final LangChain agent for summarization and additional investigation...")
            
            agent_result = self._run_final_agent_analysis(parsed_result, log_text)
            
            if agent_result:
                parsed_result["agent_summary"] = agent_result.get("output", "")
                
                # Convert agent actions to serializable format
                agent_actions = []
                for action_info, observation in agent_result.get("intermediate_steps", []):
                    if isinstance(action_info, dict):
                        agent_actions.append({
                            "tool": action_info.get("tool", "unknown"),
                            "tool_input": str(action_info.get("tool_input", "")),
                            "observation": str(observation)
                        })
                    else:
                        # Handle tuple format from some LangChain versions
                        agent_actions.append({
                            "tool": getattr(action_info, 'tool', str(action_info)),
                            "tool_input": str(getattr(action_info, 'tool_input', '')),
                            "observation": str(observation)
                        })
                parsed_result["agent_actions"] = agent_actions
            
            logger.info(f"Analysis complete: {parsed_result.get('threat_type', 'Unknown')}, Severity: {parsed_result.get('severity', 'Unknown')}")
            
            return parsed_result
            
        except Exception as e:
            logger.error(f"Error during log analysis: {e}")
            return {
                "threat_type": "Analysis Error",
                "severity": "UNKNOWN",
                "confidence_score": 0.0,
                "explanation": f"Error during analysis: {str(e)}",
                "recommended_actions": ["Review error logs", "Retry analysis"],
                "error": str(e)
            }
    
    def _run_final_agent_analysis(self, initial_analysis: Dict[str, Any], log_text: str) -> Dict[str, Any]:
        """
        Run final agent to summarize and optionally investigate further using LangChain tools
        
        Args:
            initial_analysis: Results from the initial 4-step analysis
            log_text: Original log text
            
        Returns:
            Agent execution result with summary and any additional tool calls
        """
        try:
            # Build context for the agent
            tool_descriptions = "\n".join([
                f"- {name}: {tool.description}" 
                for name, tool in self.tools_map.items()
            ])
            
            context = f"""You have completed an initial security log analysis. Here are the results:

**Threat Type**: {initial_analysis.get('threat_type', 'Unknown')}
**Severity**: {initial_analysis.get('severity', 'Unknown')}
**Confidence**: {initial_analysis.get('confidence_score', 0.0)}

**Explanation**: {initial_analysis.get('explanation', 'N/A')[:500]}

**Recommended Actions**:
{chr(10).join(f"- {action}" for action in initial_analysis.get('recommended_actions', [])[:3])}

**Original Log** (first 300 chars):
{log_text[:300]}

Your task:
1. Provide a concise executive summary (2-3 sentences) of the threat and its implications
2. If you need additional information, you can use these tools:
{tool_descriptions}

Format your response as:
SUMMARY: [your 2-3 sentence executive summary]
TOOL_CALLS: [any tool calls you want to make, or "NONE"]

If you want to call a tool, use this format:
TOOL: tool_name
INPUT: tool input
---"""

            # Get LLM response
            agent_response = self.llm_client.invoke(context)
            
            # Parse response
            summary_match = re.search(r'SUMMARY:\s*(.+?)(?=TOOL_CALLS:|$)', agent_response, re.DOTALL | re.IGNORECASE)
            summary = summary_match.group(1).strip() if summary_match else agent_response[:500]
            
            # Check for tool calls
            tool_calls = []
            tool_matches = re.finditer(r'TOOL:\s*(\w+)\s+INPUT:\s*(.+?)(?=TOOL:|$|---)', agent_response, re.DOTALL | re.IGNORECASE)
            
            for match in tool_matches:
                tool_name = match.group(1).strip()
                tool_input = match.group(2).strip()
                
                if tool_name in self.tools_map:
                    if self.verbose:
                        print(f"\nAgent calling tool: {tool_name}")
                        print(f"Input: {tool_input[:100]}...")
                    
                    try:
                        tool = self.tools_map[tool_name]
                        observation = tool._run(tool_input)
                        tool_calls.append({
                            "tool": tool_name,
                            "tool_input": tool_input,
                            "observation": observation
                        })
                        
                        if self.verbose:
                            print(f"Observation: {observation[:150]}...")
                    except Exception as e:
                        logger.warning(f"Tool call failed: {e}")
                        tool_calls.append({
                            "tool": tool_name,
                            "tool_input": tool_input,
                            "observation": f"Error: {str(e)}"
                        })
            
            return {
                "output": summary,
                "intermediate_steps": [({"tool": tc["tool"], "tool_input": tc["tool_input"]}, tc["observation"]) for tc in tool_calls]
            }
            
        except Exception as e:
            logger.error(f"Error in final agent analysis: {e}")
            return {
                "output": f"Agent analysis skipped due to error: {str(e)}",
                "intermediate_steps": []
            }
    
    def _extract_threat_keywords(self, log_text: str, bert_result: str) -> str:
        """Use LLM to extract specific threat keywords from log for targeted search"""
        
        # Quick analysis to identify specific threats
        extraction_prompt = f"""Analyze this security log and identify the SPECIFIC threats or attack types present.
Provide 2-3 precise search keywords/phrases that would help find threat intelligence.

Log:
{log_text[:500]}

BERT Analysis:
{bert_result[:200]}

Provide ONLY the search keywords (e.g., "SSH brute force attack indicators", "CVE-2024-1234", "SQL injection attack patterns").
Be specific and technical. Focus on attack types, CVEs, malware names, or specific techniques.
Do NOT provide generic terms like "security log analysis".

Search keywords:"""
        
        try:
            keywords_output = self.llm_client.invoke(extraction_prompt)
            # Clean up the output
            keywords = keywords_output.strip().replace('\n', ' ').replace('  ', ' ')
            # Take first 100 chars to avoid overly long queries
            keywords = keywords[:100].strip()
            
            if len(keywords) > 10:  # Valid keywords found
                return keywords
        except Exception as e:
            logger.warning(f"Failed to extract keywords with LLM: {e}")
        
        # Fallback to basic extraction
        return self._extract_keywords_fallback(log_text)
    
    def _extract_keywords_fallback(self, log_text: str) -> str:
        """Fallback regex-based keyword extraction"""
        keywords = []
        
        patterns = [
            r'(SQL injection|XSS|command injection)',
            r'(brute force|password attack)',
            r'(ransomware|malware|trojan)',
            r'(CVE-\d{4}-\d{4,7})',
        ]
        
        text_lower = log_text.lower()
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            keywords.extend(matches)
        
        if not keywords:
            if 'failed' in text_lower and ('password' in text_lower or 'login' in text_lower):
                return 'SSH authentication failure brute force'
            elif 'unauthorized' in text_lower:
                return 'unauthorized access attempt'
            elif 'injection' in text_lower:
                return 'code injection attack'
        
        return ' '.join(keywords[:3]) if keywords else None
    
    def _parse_analysis(self, raw_output: str) -> Dict[str, Any]:
        """
        Parse the agent's structured output
        
        Args:
            raw_output: Raw text output from agent
            
        Returns:
            Structured dictionary
        """
        result = {
            "threat_type": "Unknown",
            "severity": "UNKNOWN",
            "confidence_score": 0.5,
            "explanation": raw_output,
            "indicators_of_compromise": [],
            "recommended_actions": []
        }
        
        try:
            # Extract threat type
            threat_match = re.search(r'\*\*THREAT TYPE\*\*:?\s*(.+?)(?:\n|$)', raw_output, re.IGNORECASE)
            if threat_match:
                result["threat_type"] = threat_match.group(1).strip()
            
            # Extract severity
            severity_match = re.search(r'\*\*SEVERITY LEVEL\*\*:?\s*(\w+)', raw_output, re.IGNORECASE)
            if severity_match:
                result["severity"] = severity_match.group(1).strip().upper()
            
            # Extract confidence
            confidence_match = re.search(r'\*\*CONFIDENCE SCORE\*\*:?\s*([\d.]+)', raw_output, re.IGNORECASE)
            if confidence_match:
                result["confidence_score"] = float(confidence_match.group(1))
            
            # Extract explanation
            explanation_match = re.search(
                r'\*\*DETAILED EXPLANATION\*\*:?\s*(.+?)(?:\*\*|$)',
                raw_output,
                re.IGNORECASE | re.DOTALL
            )
            if explanation_match:
                result["explanation"] = explanation_match.group(1).strip()
            
            # Extract IoCs
            ioc_match = re.search(
                r'\*\*INDICATORS OF COMPROMISE\*\*:?\s*(.+?)(?:\*\*|$)',
                raw_output,
                re.IGNORECASE | re.DOTALL
            )
            if ioc_match:
                ioc_text = ioc_match.group(1).strip()
                # Split by lines and clean
                iocs = [line.strip('- ').strip() for line in ioc_text.split('\n') if line.strip()]
                result["indicators_of_compromise"] = [ioc for ioc in iocs if ioc]
            
            # Extract recommended actions
            actions_match = re.search(
                r'\*\*RECOMMENDED ACTIONS\*\*:?\s*(.+?)(?:\*\*|$)',
                raw_output,
                re.IGNORECASE | re.DOTALL
            )
            if actions_match:
                actions_text = actions_match.group(1).strip()
                # Split by lines and clean
                actions = [re.sub(r'^\d+\.?\s*', '', line).strip('- ').strip() 
                          for line in actions_text.split('\n') if line.strip()]
                result["recommended_actions"] = [action for action in actions if action]
        
        except Exception as e:
            logger.warning(f"Error parsing analysis output: {e}")
        
        return result


# Example usage
if __name__ == "__main__":
    import sys
    
    # Initialize agent
    agent = CyberSecAgent(verbose=True)
    
    # Test logs
    test_logs = [
        "Failed password for admin from 203.0.113.42 port 55892 ssh2",
        "Successful login for user john.doe from 192.168.1.100",
        "CRITICAL: Buffer overflow detected in application XYZ, potential CVE-2024-1234 exploitation"
    ]
    
    if len(sys.argv) > 1:
        # Use command line argument
        log = " ".join(sys.argv[1:])
        result = agent.analyze_log(log)
    else:
        # Use first test log
        log = test_logs[0]
        result = agent.analyze_log(log)
    
    print("\n" + "="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    print(f"Threat Type: {result['threat_type']}")
    print(f"Severity: {result['severity']}")
    print(f"Confidence: {result['confidence_score']}")
    print(f"\nExplanation:\n{result['explanation']}")
    print(f"\nRecommended Actions:")
    for i, action in enumerate(result['recommended_actions'], 1):
        print(f"  {i}. {action}")
