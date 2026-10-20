
from importlib import import_module
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
chat_module = import_module("app.api.chat")


@pytest.fixture
def llm_mock(monkeypatch):
    generate = AsyncMock(
        return_value="Respuesta simulada de Qwen3"
    )

    provider = SimpleNamespace(
        generate_response=generate
    )

    monkeypatch.setattr(
        chat_module,
        "llm_provider",
        provider
    )

    return generate


@pytest.mark.parametrize(
    "endpoint",
    ["/chat/", "/chat/llm"]
)
def test_chat_success(endpoint, llm_mock):
    response = client.post(
        endpoint,
        json={"message": "Hola"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "reply": "Respuesta simulada de Qwen3"
    }

    llm_mock.assert_awaited_once_with(
        prompt="Hola",
        system_prompt=chat_module.SYSTEM_PROMPT
    )


@pytest.mark.parametrize(
    "error_type",
    [httpx.ConnectError, httpx.ReadTimeout]
)
def test_chat_provider_error(error_type, llm_mock):
    llm_mock.side_effect = error_type(
        "Error simulado"
    )

    response = client.post(
        "/chat/llm",
        json={"message": "Hola"}
    )

    assert response.status_code == 502
    assert "detail" in response.json()


@pytest.mark.parametrize(
    "endpoint",
    ["/chat/", "/chat/llm"]
)
@pytest.mark.parametrize(
    "message",
    ["", "x" * 2001]
)
def test_chat_invalid_message(
    endpoint,
    message,
    llm_mock
):
    response = client.post(
        endpoint,
        json={"message": message}
    )

    assert response.status_code == 422
    llm_mock.assert_not_awaited()
