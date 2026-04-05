from app.services.providers.twelve_data_provider import TwelveDataProvider
from app.schemas.market_data import MarketQuote
from datetime import datetime, timedelta

class MarketDataService:
    def __init__(self) -> None:
        self.provider = TwelveDataProvider()
        self._cache: dict[str, tuple[datetime, MarketQuote]] = {}
        self.ttl = timedelta(minutes=120)  # Cache time-to-live

    def get_current_quote(self, symbol: str) -> MarketQuote:
        now = datetime.utcnow()
        cached = self._cache.get(symbol)
        if cached:
            cached_at, quote = cached
            if now - cached_at < self.ttl:
                return quote  # Return cached quote if still valid
        quote = self.provider.get_price(symbol)
        self._cache[symbol] = (now, quote)  # Cache the new quote
        return quote


def get_current_price(symbol: str) -> float:
    # Placeholder implementation - replace with actual logic to fetch current price
    # For example, you could integrate with a market data API like Alpha Vantage, Yahoo Finance, etc.
    mock_prices = {
        "AAPL": 150.00,
        "GOOGL": 2800.00,
        "MSFT": 300.00,
        "AMZN": 3500.00,
        "TSLA": 700.00,
        "EQQQ": 3500.00,
        "VUAA": 700.00,
        "BRICEKSP": 100.00,
        "COST": 400.00,
        "MELI": 233.00,
        "ICSUSSDP": 100.00,
        "HOOD": 30.00,
        "DIS": 180.00,
        "ICSUSSDP": 100.00,
        "BABA": 200.00,
        "NVDA": 220.00,
        "BRK.B": 300.00,
        "MELI": 219.00,
        "IWDA": 80.00,

    }
    return mock_prices.get(symbol.upper(), 100.00)  # Default to 100 if symbol not found)


market_data_service = MarketDataService()