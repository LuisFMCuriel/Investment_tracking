# 422 for schema validation errors from Pydantic/FastAPI for example missing quantity for BUY
# 400 for business-rule errors raised by your service and converted in the route for example oversell or duplicate transaction
# 201 for successful creation of a resource
# 200 for successful retrieval of resources
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from app.db.base import Base
from app.models.transaction import Transaction
from app.db.session import engine

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)

def clear_transactions():
    db = SessionLocal()
    try:
        db.query(Transaction).delete()
        db.commit()
    finally:
        db.close()

def test_create_buy_transaction() -> None:
    clear_transactions()
    payload = {
        "symbol": "AAPL",
        "transaction_type": "BUY",
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
    assert data["transaction_type"] == "BUY"
    assert data["quantity"] == 10
    assert data["price"] == 150.0
    assert data["currency"] == "USD"
    assert data["fees"] == 1.0
    assert data["transaction_date"] == "2024-01-01"



def test_create_sell_transaction_when_enough_shares_exist() -> None:
    clear_transactions()
    buy_payload = {
        "symbol": "MSFT",
        "transaction_type": "BUY",
        "quantity": 10,
        "price": 300.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-03"
    }
    sell_payload = {
        "symbol": "MSFT",
        "transaction_type": "SELL",
        "quantity": 4,
        "price": 320.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-04"
    }

    buy_response = client.post("/transactions", json=buy_payload)
    assert buy_response.status_code == 201

    sell_response = client.post("/transactions", json=sell_payload)
    assert sell_response.status_code == 201

    data = sell_response.json()
    assert data["symbol"] == "MSFT"
    assert data["transaction_type"] == "SELL"
    assert data["quantity"] == 4


def test_reject_oversell_transaction() -> None:
    clear_transactions()
    buy_payload = {
        "symbol": "TSLA",
        "transaction_type": "BUY",
        "quantity": 2,
        "price": 250.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-05"
    }
    sell_payload = {
        "symbol": "TSLA",
        "transaction_type": "SELL",
        "quantity": 5,
        "price": 260.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-06"
    }

    buy_response = client.post("/transactions", json=buy_payload)
    assert buy_response.status_code == 201

    sell_response = client.post("/transactions", json=sell_payload)
    assert sell_response.status_code == 400
    assert "only" in sell_response.json()["detail"]


def test_reject_duplicate_transaction() -> None:
    clear_transactions()
    payload = {
        "symbol": "NVDA",
        "transaction_type": "BUY",
        "quantity": 3,
        "price": 800.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-07"
    }

    first_response = client.post("/transactions", json=payload)
    second_response = client.post("/transactions", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "This transaction already exists"


def test_create_deposit_transaction() -> None:
    clear_transactions()
    payload = {
        "transaction_type": "DEPOSIT",
        "amount": 1000.0,
        "currency": "USD",
        "fees": 0.0,
        "transaction_date": "2024-01-08"
    }

    response = client.post("/transactions", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["transaction_type"] == "DEPOSIT"
    assert data["amount"] == 1000.0
    assert data["symbol"] is None
    assert data["quantity"] is None
    assert data["price"] is None


def test_reject_buy_without_quantity() -> None:
    clear_transactions()
    payload = {
        "symbol": "AMZN",
        "transaction_type": "BUY",
        "price": 150.0,
        "currency": "USD",
        "fees": 1.0,
        "transaction_date": "2024-01-09"
    }

    response = client.post("/transactions", json=payload)

    assert response.status_code == 422


def test_reject_deposit_with_quantity() -> None:
    clear_transactions()
    payload = {
        "transaction_type": "DEPOSIT",
        "amount": 500.0,
        "quantity": 3,
        "currency": "USD",
        "fees": 0.0,
        "transaction_date": "2024-01-10"
    }

    response = client.post("/transactions", json=payload)

    assert response.status_code == 422


def test_read_transactions_returns_list() -> None:
    clear_transactions()
    response = client.get("/transactions")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "id" in data[0]
        assert "symbol" in data[0]
        assert "transaction_type" in data[0]
        assert "quantity" in data[0]
        assert "price" in data[0]
        assert "amount" in data[0]
        assert "currency" in data[0]
        assert "fees" in data[0]
        assert "transaction_date" in data[0]