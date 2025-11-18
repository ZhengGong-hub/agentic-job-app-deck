"""OpenAI LLM adapter with JSON-only helpers."""
import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(dotenv_path=".apikey")


class OpenAIClient:
    """Thin wrapper for OpenAI chat completion."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.1):
        """
        Initialize OpenAI client.
        
        Args:
            model_name: Model name (e.g., "gpt-4o-mini")
            temperature: Temperature for sampling (0-0.2 recommended)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
    
    def chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Make a chat completion request.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            response_format: Optional response format (e.g., {"type": "json_object"})
            
        Returns:
            Response content as string
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    
    def chat_completion_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> Dict[str, Any]:
        """
        Make a chat completion request with JSON response.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt (should mention JSON output)
            
        Returns:
            Parsed JSON response
        """
        response = self.chat_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format={"type": "json_object"},
        )
        return json.loads(response)

