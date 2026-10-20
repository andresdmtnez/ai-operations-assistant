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


def test_create_ticket():
    # Assumes at least one customer exists (from seed data)
    response = client.post(
        "/tickets/",
        json={
            "customer_id": 1,
            "subject": "Test ticket",
            "description": "This is a test ticket"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["subject"] == "Test ticket"
    assert data["description"] == "This is a test ticket"
    assert data["status"] == "open"
    assert "id" in data
    assert isinstance(data["id"], int)
    assert "created_at" in data


def test_create_ticket_nonexistent_customer():
    response = client.post(
        "/tickets/",
        json={
            "customer_id": 99999,  # Non-existent customer
            "subject": "Test ticket",
            "description": "This should fail"
        }
    )
    
    assert response.status_code == 404


def test_create_ticket_missing_fields():
    # Missing customer_id
    response = client.post(
        "/tickets/",
        json={
            "subject": "Test ticket"
        }
    )
    
    assert response.status_code == 422
    
    # Missing subject
    response = client.post(
        "/tickets/",
        json={
            "customer_id": 1
        }
    )
    
    assert response.status_code == 422


def test_update_ticket_status():
    # First create a ticket
    create_response = client.post(
        "/tickets/",
        json={
            "customer_id": 1,
            "subject": "Ticket to update",
            "description": "Will update status"
        }
    )
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]
    
    # Update to in_progress
    response = client.patch(
        f"/tickets/{ticket_id}",
        json={"status": "in_progress"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["id"] == ticket_id
    
    # Update to closed
    response = client.patch(
        f"/tickets/{ticket_id}",
        json={"status": "closed"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "closed"
    assert data["id"] == ticket_id


def test_update_ticket_invalid_status():
    # Create a ticket first
    create_response = client.post(
        "/tickets/",
        json={
            "customer_id": 1,
            "subject": "Ticket for invalid status",
            "description": "Testing invalid status"
        }
    )
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]
    
    # Try invalid status
    response = client.patch(
        f"/tickets/{ticket_id}",
        json={"status": "invalid_status"}
    )
    
    assert response.status_code == 422


def test_update_ticket_not_found():
    response = client.patch(
        "/tickets/999999",
        json={"status": "closed"}
    )
    
    assert response.status_code == 404
