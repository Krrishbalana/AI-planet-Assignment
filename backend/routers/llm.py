"""
LLM integration endpoints
Interact with OpenAI, Gemini, and other LLM providers
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os

from services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: Optional[str] = None
    context: Optional[List[str]] = None

class LLMResponse(BaseModel):
    response: str
    model: str
    tokens_used: int

@router.post("/generate")
async def generate_response(request: LLMRequest) -> LLMResponse:
    """Generate a response from an LLM"""
    try:
        result = await llm_service.generate(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            system_prompt=request.system_prompt,
            context=request.context
        )
        
        return LLMResponse(
            response=result["response"],
            model=result["model"],
            tokens_used=result["tokens_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models():
    """List available LLM models"""
    return {
        "models": [
            {"id": "gpt-4", "name": "GPT-4", "provider": "OpenAI"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI"},
            {"id": "gemini-pro", "name": "Gemini Pro", "provider": "Google"},
        ]
    }
