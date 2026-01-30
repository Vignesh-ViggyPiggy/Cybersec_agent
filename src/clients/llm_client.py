# LLM Client for Ollama
from typing import Optional
from langchain_ollama import OllamaLLM
from langchain_core.language_models.llms import BaseLLM
from loguru import logger


class LLMClient:
    """Client for interacting with Ollama LLM"""
    
    def __init__(self, base_url: str, model: str, temperature: float = 0.7):
        """
        Initialize LLM client
        
        Args:
            base_url: Ollama base URL (e.g., http://localhost:11434)
            model: Model name (e.g., llama3.2)
            temperature: Sampling temperature (0.0 to 1.0)
        """
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        
        logger.info(f"Initializing LLM client: {base_url}, model={model}")
        
        self.llm = OllamaLLM(
            base_url=base_url,
            model=model,
            temperature=temperature
        )
    
    def get_llm(self) -> BaseLLM:
        """Get the LangChain LLM instance"""
        return self.llm
    
    def invoke(self, prompt: str) -> str:
        """
        Invoke the LLM with a prompt
        
        Args:
            prompt: The prompt text
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Invoking LLM with prompt length: {len(prompt)} chars")
            response = self.llm.invoke(prompt)
            logger.debug(f"LLM response length: {len(response)} chars")
            return response
        except Exception as e:
            error_msg = f"LLM invocation failed: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"


# Example usage
if __name__ == "__main__":
    from ..config import settings
    
    client = LLMClient(
        base_url=settings.llm_base_url,
        model=settings.llm_model
    )
    
    test_prompt = "What are the top 3 indicators of a brute force attack?"
    response = client.invoke(test_prompt)
    print(f"Prompt: {test_prompt}")
    print(f"Response: {response}")
