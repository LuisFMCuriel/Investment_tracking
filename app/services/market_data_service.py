from pydoc import resolve
from app.services.providers.twelve_data_provider import TwelveDataProvider
from app.services.providers.yahoo_finance_provider import YahooFinanceProvider
from app.schemas.market_data import MarketQuote
from datetime import datetime, timedelta


SYMBOL_PROVIDER_MAP = {
    "VUAA.MI": "yahoo",
    "IWDA.AS": "yahoo",
}

SYMBOL_MAP = {
    # Lightyear/local symbol : Twelve Data symbol
    "BRICEKSP": None,
    "COST": "COST",
    "MELI": "MELI",
    "ICSUSSDP": None,
    "HOOD": "HOOD",
    "DIS": "DIS",
    "BABA": "BABA",
    "NVDA": "NVDA",
    "BRK.B": "BRKB",
    "NFLX": "NFLX",
    "VUAA": "VUAA.DE",
    "TSLA": "TSLA",
    "GOOGL": "GOOGl",
    "EQQQ": "EQQQ.MI",

}

class MarketDataService:
    def __init__(self) -> None:
        self.twelve_data = TwelveDataProvider()
        self.yahoo = YahooFinanceProvider()
        self._cache: dict[str, tuple[datetime, MarketQuote]] = {}
        self.ttl = timedelta(minutes=120)  # Cache time-to-live
    
    def resolve_symbol(symbol: str) -> str | None:
        if symbol in SYMBOL_MAP:
            return SYMBOL_MAP[symbol]
        return symbol

    def get_current_quote(self, symbol: str, currency: str) -> MarketQuote:
        resolved_symbol = self.resolve_symbol(symbol)
        if resolved_symbol is None:
            raise ValueError(f"No market-data mapping for symbol: {symbol}")
        now = datetime.utcnow()
        cached = self._cache.get(symbol)

        if cached:
            cached_at, quote = cached
            if now - cached_at < self.ttl:
                return quote  # Return cached quote if still valid

        if currency == "EUR":
            quote = self.yahoo.get_price(resolved_symbol)
        elif currency == "USD":
            quote = self.twelve_data.get_price(resolved_symbol)
        else:
            print("There is a problem resolving {} with currency {}".format(symbol, currency))
            return MarketQuote(
                symbol =symbol,
                price=None,
                currency=currency,
                exchange=None,
                as_of =now,
                provider=None,
                price_available=False,
                )

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