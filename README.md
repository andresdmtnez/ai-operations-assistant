# AI Operations Assistant – Backend API

## Overview

This repository contains the **FastAPI** backend for the AI Operations Assistant portfolio project. It provides a small set of operational endpoints that read data from a PostgreSQL database using **SQLAlchemy**.

- **Health** – `GET /health` – simple health‑check (verifies that the API can start and that a lightweight DB query succeeds).
- **Customers** – `GET /customers` – list all customers.
- **Orders** – `GET /orders` – list orders, optionally filtered by `status` and/or `customer_id`.
- **Tickets** – `GET /tickets` – list all support tickets.

All data is fetched directly from PostgreSQL; there is **no hard‑coded data**.

## Prerequisites

- **Python 3.12+** (the environment used for development).
- **PostgreSQL 17** running locally (default connection string in `apps/api/app/database.py`):
  ```
  postgresql+psycopg://aiassistant:aiassistant_dev@127.0.0.1:5432/ai_operations
  ```
  Adjust the URL or provide environment variables if you use a different instance.
- `make` is not required; the commands are simple `pip`/`uvicorn` calls.

## Setup

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r apps/api/requirements.txt

# 3. Ensure the PostgreSQL database exists and the tables are created.
#    The first start of the API will automatically create the tables.
```

## Running the API

```bash
uvicorn apps.api.app.main:app --reload --host 0.0.0.0 --port 8000
```

- The `--reload` flag enables hot‑reloading during development.
- Open a browser at <http://127.0.0.1:8000/docs> to view the automatically generated Swagger UI.

## Endpoints

| Method | Path | Description | Query parameters |
|--------|------|-------------|------------------|
| `GET` | `/health` | Returns `{"status": "ok"}` if the service is up (and can execute a lightweight DB query). | – |
| `GET` | `/customers` | List all customers. | – |
| `GET` | `/customers/{customer_id}` | Retrieve a single customer or `404` if not found. | – |
| `GET` | `/orders` | List orders; can filter by `status` and/or `customer_id`. | `status` (string), `customer_id` (int) |
| `GET` | `/orders/{order_id}` | Retrieve a single order or `404`. | – |
| `GET` | `/tickets` | List all tickets. | – |
| `GET` | `/tickets/{ticket_id}` | Retrieve a single ticket or `404`. | – |

## Testing

```bash
pytest -q
```
All tests should pass (`7 passed`). The test suite uses FastAPI’s `TestClient` and does not require a live PostgreSQL instance because the tables are created automatically and the queries return empty lists when no data is present.

## Future Work (Day 5+)

- Populate the database with seed data.
- Add create / update / delete endpoints with human‑in‑the‑loop approval.
- Integrate the AI agent, tools, and RAG components.
- Connect the Next.js frontend.

---
*Generated on Day 4 – API operational and verified.*
