
import asyncio
import json
from unittest.mock import patch

import httpx

from app.agent.providers.ollama import OllamaProvider


def test_ollama_provider_generate_response():
    captured = {}

    def mock_ollama(request):
        captured["url"] = str(request.url)
        captured["body"] = json.loads(
            request.content
        )

        return httpx.Response(
            200,
            json={
                "message": {
                    "content": "Respuesta de prueba"
                }
            }
        )

    original_client = httpx.AsyncClient

    def mock_client():
        return original_client(
            transport=httpx.MockTransport(
                mock_ollama
            )
        )

    provider = OllamaProvider(
        base_url="http://127.0.0.1:11434",
        model="qwen3:8b"
    )

    with patch(
        "app.agent.providers.ollama.httpx.AsyncClient",
        new=mock_client
    ):
        result = asyncio.run(
            provider.generate_response(
                prompt="Hola",
                system_prompt="Responde en español"
            )
        )

    assert result == "Respuesta de prueba"

    assert captured["url"] == (
        "http://127.0.0.1:11434/api/chat"
    )

    assert captured["body"]["model"] == "qwen3:8b"
    assert captured["body"]["stream"] is False

    assert captured["body"]["messages"] == [
        {
            "role": "system",
            "content": "Responde en español"
        },
        {
            "role": "user",
            "content": "Hola"
        }
    ]
