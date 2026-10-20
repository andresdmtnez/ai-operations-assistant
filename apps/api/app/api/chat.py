import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.agent.providers.ollama import OllamaProvider

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

class ChatResponse(BaseModel):
    reply: str

# Initialize provider
llm_provider = OllamaProvider()

SYSTEM_PROMPT = (
    "Eres un asistente de operaciones empresariales. "
    "Responde en español de manera clara, precisa y profesional. "
    "No inventes datos sobre clientes, pedidos ni tickets. "
    "Si no tienes acceso a información real, indícalo. "
    "No afirmes haber ejecutado operaciones que no se realizaron."
)

@router.post("/", response_model=ChatResponse)
async def chat_simple(request: ChatRequest):
    """
    Deterministic endpoint used by frontend initially.
    Now redirects to LLM provider for Day 12.
    """
    return await chat_llm(request)

@router.post("/llm", response_model=ChatResponse)
async def chat_llm(request: ChatRequest):
    try:
        reply = await llm_provider.generate_response(
            prompt=request.message,
            system_prompt=SYSTEM_PROMPT
        )
        return ChatResponse(reply=reply)
    except Exception as e:
        # Check for connection errors specifically if needed, 
        # but the provider raises for status or generic Exception
        raise HTTPException(status_code=502, detail=f"Error al procesar solicitud con el LLM: {str(e)}")
