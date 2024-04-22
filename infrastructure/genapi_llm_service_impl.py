from llm_service import LLMService  # Import the base class
from abc import ABC, abstractmethod
import requests  # Assuming interaction with AwesomeLLM uses HTTP requests
from example import Example  # Import Example class

class GenapiLlmService(LLMService):
  def __init__(self, api_key: str):
    self.api_key = api_key

  def make_prompt(self, action: str, examples: list[Example]) -> str:

    # Parse response (replace with actual data extraction)
    return "{}"