"""
LLM service for interacting with OpenAI, Gemini, and other providers
"""
import os
from typing import List, Optional, Dict, Any
from openai import AsyncOpenAI
# import google.generativeai as genai  # Uncomment when using Gemini

class LLMService:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_client = AsyncOpenAI(api_key=self.openai_key) if self.openai_key else None
    
    async def generate(
        self,
        prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate a response from an LLM"""
        
        if model.startswith("gpt"):
            return await self._generate_openai(
                prompt, model, temperature, max_tokens, system_prompt, context
            )
        elif model.startswith("gemini"):
            return await self._generate_gemini(
                prompt, model, temperature, max_tokens, system_prompt, context
            )
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    async def _generate_openai(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str],
        context: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if context:
            context_text = "\n\n".join(context)
            messages.append({
                "role": "system",
                "content": f"Context:\n{context_text}"
            })
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "response": response.choices[0].message.content,
            "model": model,
            "tokens_used": response.usage.total_tokens
        }
    
    async def _generate_gemini(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str],
        context: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate response using Google Gemini"""
        # Implement Gemini integration
        # genai.configure(api_key=self.gemini_key)
        # model = genai.GenerativeModel(model)
        # ...
        
        raise NotImplementedError("Gemini integration not yet implemented")
