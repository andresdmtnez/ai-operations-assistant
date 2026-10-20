from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="Mensaje del usuario")


class ChatResponse(BaseModel):
    reply: str


@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Endpoint temporal de chat para validar el flujo frontend-backend.
    
    No integra ningún modelo de IA real aún.
    """
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="El mensaje no puede estar vacío",
        )

    # Respuesta determinista temporal
    reply = (
        "Mensaje recibido correctamente. "
        "El agente de IA todavía no está conectado."
    )

    return ChatResponse(reply=reply)