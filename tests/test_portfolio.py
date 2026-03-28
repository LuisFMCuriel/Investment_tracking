from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_read_portfolio():
    response = client.get("/portfolio")
    assert response.status_code == 200
    assert response.json() == {
        "total_value": 100000.0,
        "cash": 20000.0,
        "invested_value": 80000.0,
        "unrealized_pln": 5000.0,
        "currency": "EUR"
    }
