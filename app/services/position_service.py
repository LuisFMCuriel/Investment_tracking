from app.schemas.position import Position

def get_positions() -> list[Position]:
    # This is a placeholder implementation. In a real application, you would fetch this data from a database or an external API.
    return [
        Position(
            symbol="AAPL",
            name="Apple Inc.",
            quantity=10,
            average_cost=150.00,
            current_price=170.00,
            unrealized_pln=200.00,
            currency="USD"
        ),
        Position(
            symbol="GOOGL",
            name="Alphabet Inc.",
            quantity=5,
            average_cost=2500.00,
            current_price=2800.00,
            unrealized_pln=1500.00,
            currency="USD"
        ),
        Position(
            symbol="VWCE",
            name="Vanguard FTSE All-World UCITS ETF",
            quantity=8,
            average_cost=600.00,
            current_price=700.00,
            unrealized_pln=800.00,
            currency="EUR"
        )
    ]