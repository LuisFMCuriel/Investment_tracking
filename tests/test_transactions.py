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