from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_positions() -> None:
    response = client.get("/positions")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0] == {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "quantity": 10,
        "average_cost": 150.00,
        "current_price": 170.00,
        "unrealized_pln": 200.00,
        "currency": "USD"
    }