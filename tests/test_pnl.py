from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_pnl():
    response = client.get("/pnl")
    assert response.status_code == 200
    assert response.json() == {
        "unrealized_pnl": 240.00,
        "daily_pnl": 35.50,
        "total_return_pct": 4.12,
        "currency": "EUR"
    }