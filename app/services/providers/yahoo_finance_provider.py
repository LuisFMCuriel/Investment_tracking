from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import yfinance as yf

from app.schemas.market_data import MarketQuote


class YahooFinanceProvider:
    def get_price(self, symbol: str) -> MarketQuote:
        ticker = yf.Ticker(symbol)

        info: dict[str, Any] = ticker.fast_info or {}
        history = ticker.history(period="2d", interval="1d", auto_adjust=False)

        current_price = info.get("lastPrice")
        currency = info.get("currency")
        exchange = info.get("exchange")

        previous_close = info.get("previousClose")
        open_price = info.get("open")
        day_high = info.get("dayHigh")
        day_low = info.get("dayLow")
        volume = info.get("lastVolume")

        if history is not None and not history.empty:
            last_row = history.iloc[-1]

            if current_price is None:
                current_price = float(last_row["Close"])

            if open_price is None and "Open" in history.columns:
                open_price = float(last_row["Open"])

            if day_high is None and "High" in history.columns:
                day_high = float(last_row["High"])

            if day_low is None and "Low" in history.columns:
                day_low = float(last_row["Low"])

            if volume is None and "Volume" in history.columns:
                volume = float(last_row["Volume"])

            if previous_close is None and len(history) >= 2:
                previous_close = float(history.iloc[-2]["Close"])

        if current_price is None:
            raise ValueError(f"Could not retrieve price for symbol: {symbol}")
        
        return MarketQuote(
            symbol=symbol,
            price=float(current_price),
            currency=currency,
            exchange = exchange,
            as_of=datetime.now(timezone.utc),
            provider = "yahoo_finance",
            price_available= True if current_price is not None else False,
        )
        