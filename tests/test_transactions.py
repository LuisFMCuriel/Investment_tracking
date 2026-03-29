from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transaction() -> None:
    payload = {
        "symbol": "AAPL",
        "transaction_type": "buy",
        "quantity": 10,
        "price": 150.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-01"
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["symbol"] == "AAPL"
    assert data["transaction_type"] == "buy"
    assert data["quantity"] == 10
    assert data["price"] == 150.0
    assert data["currency"] == "USD"
    assert data["fees"] == 1.0
    assert data["transaction_date"] == "2024-01-01"

def test_read_transactions() -> None:
    response = client.get("/transactions")
    payload1 = {
        "symbol": "AAPL",
        "transaction_type": "buy",
        "quantity": 10,
        "price": 150.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-01"
    }
    payload2 = {
        "symbol": "GOOGL",
        "transaction_type": "sell",
        "quantity": 5,
        "price": 2000.0,
        "currency": "USD",
        "fees": 2.0,
        "transaction_date": "2024-01-02"
    }
    client.post("/transactions", json=payload1)
    client.post("/transactions", json=payload2)
    response = client.get("/transactions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert "id" in data[0]
    assert "symbol" in data[0]
    assert "transaction_type" in data[0]
    assert "quantity" in data[0]
    assert "price" in data[0]
    assert "currency" in data[0]
    assert "fees" in data[0]
    assert "transaction_date" in data[0]