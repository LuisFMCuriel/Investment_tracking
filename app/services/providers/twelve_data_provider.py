from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import requests

from app.core.config import settings
from app.schemas.market_data import MarketQuote


class TwelveDataProvider:
    BASE_URL = "https://api.twelvedata.com"

    def __init__(self, api_key: str | None = None, timeout: int = 10) -> None:
        self.api_key = api_key or settings.twelve_data_api_key
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"apikey {self.api_key}",
        }

    def _get_json(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        response = requests.get(
            f"{self.BASE_URL}/{endpoint}",
            params=params,
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and data.get("status") == "error":
            message = data.get("message", "Unknown Twelve Data error")
            raise ValueError(message)

        return data

    def get_price(self, symbol: str) -> MarketQuote:
        quote_data = self._get_json("quote", {"symbol": symbol})

        raw_price = quote_data.get("close") or quote_data.get("price")
        price = float(raw_price) if raw_price not in (None, "") else None

        return MarketQuote(
            symbol=symbol,
            price=price,
            currency=quote_data.get("currency"),
            exchange=quote_data.get("exchange"),
            as_of=datetime.now(timezone.utc),
            provider="twelve_data",
            price_available=price is not None,
        )