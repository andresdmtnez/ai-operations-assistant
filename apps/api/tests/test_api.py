from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_customers():
    response = client.get("/customers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_orders():
    response = client.get("/orders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_tickets():
    response = client.get("/tickets/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_customer_not_found():
    response = client.get("/customers/999999")

    assert response.status_code == 404


def test_order_not_found():
    response = client.get("/orders/999999")

    assert response.status_code == 404


def test_ticket_not_found():
    response = client.get("/tickets/999999")

    assert response.status_code == 404


def test_chat_valid_message():
    response = client.post("/chat/", json={"message": "Hola"})

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)
    assert len(data["reply"]) > 0


def test_chat_empty_message():
    response = client.post("/chat/", json={"message": ""})

    assert response.status_code == 422


def test_chat_message_too_long():
    long_message = "x" * 2001
    response = client.post("/chat/", json={"message": long_message})

    assert response.status_code == 422

