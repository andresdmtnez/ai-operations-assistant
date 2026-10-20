import httpx
import os
from typing import Optional, Any
from app.agent.core.model import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(
        self,
        base_url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434"),
        model: str = os.getenv("MODEL_NAME", "qwen3:8b")
    ):
        self.base_url = base_url
        self.model = model

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    **kwargs
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]
