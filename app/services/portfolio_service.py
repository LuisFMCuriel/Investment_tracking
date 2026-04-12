from collections import defaultdict
from re import I

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.schemas.enums import TransactionType
from app.schemas.portfolio import PortfolioSummarySimple
from app.services.pnl_service import PNL_SERVICE

cash_only = ["BRICEKSP", "ICSUSSDP"]
class PortfolioService:
    def __init__(self):
        self.cache = None
        self.cache_timestamp = None
        self.ttl = timedelta(minutes=120)  # Cache time-to-live

    def get_portfolio_summary(self, db: Session) -> PortfolioSummarySimple:
        if self.cache and self.cache_timestamp and (datetime.utcnow() - self.cache_timestamp < self.ttl):
                return self.cache
        else:
            portfolio = {"Total_EUR": 0.0, "Total_USD": 0.0, "Total_invested_EUR": 0.0, "Total_invested_USD": 0.0, "pnl_usd": 0.0, "pnl_eur": 0.0}
            started_usd_with = 0.0
            started_eur_with = 0.0
            pnl_list = PNL_SERVICE.get_pnl(db)
            for pnl in pnl_list:
                if pnl.symbol not in cash_only:
                    if pnl.currency == "EUR":
                        portfolio["Total_EUR"] += pnl.market_value
                        portfolio["Total_invested_EUR"] += pnl.total_cost
                        portfolio["pnl_eur"] += pnl.unrealized_pnl or 0.0
                        started_eur_with += pnl.total_cost
                    elif pnl.currency == "USD":
                        portfolio["Total_USD"] += pnl.market_value
                        portfolio["Total_invested_USD"] += pnl.total_cost
                        portfolio["pnl_usd"] += pnl.unrealized_pnl or 0.0
                        started_usd_with += pnl.total_cost
                    else:
                        raise ValueError(f"Unsupported currency {pnl.currency} in PnL data")
                else:
                    if pnl.currency == "EUR":
                        portfolio["Total_EUR"] += pnl.total_cost
                        started_eur_with += pnl.total_cost
                    elif pnl.currency == "USD":
                        portfolio["Total_USD"] += pnl.total_cost
                        started_usd_with += pnl.total_cost
                    else:
                        raise ValueError(f"Unsupported currency {pnl.currency} in PnL data")
            percentage_usd = (portfolio["Total_USD"] - started_usd_with) / started_usd_with * 100 if started_usd_with > 0 else 0.0
            percentage_eur = (portfolio["Total_EUR"] - started_eur_with) / started_eur_with * 100 if started_eur_with > 0 else 0.0
            self.cache = PortfolioSummarySimple(
                Total_EUR = round(portfolio["Total_EUR"], 2),
                Total_USD = round(portfolio["Total_USD"], 2),
                Total_invested_EUR = round(portfolio["Total_invested_EUR"], 2),
                Total_invested_USD= round(portfolio["Total_invested_USD"], 2),
                Profit_EUR = round(portfolio["pnl_eur"], 2),
                Profit_USD= round(portfolio["pnl_usd"], 2),
                Percentage_profit_EUR = round(percentage_eur, 2),
                Percentage_profit_USD = round(percentage_usd, 2),
                )
            return self.cache

PORTFOLIO = PortfolioService()

"""
def get_portfolio_summary(db: Session) -> PortfolioSummary:
    cash_by_currency = defaultdict(float)

    transactions = (
        db.query(Transaction)
        .order_by(Transaction.transaction_date, Transaction.id)
        .all()
    )

    for tx in transactions:
        currency = tx.currency

        if tx.transaction_type == TransactionType.BUY:
            quantity = tx.quantity or 0.0
            price = tx.price or 0.0
            fees = tx.fees or 0.0
            cash_by_currency[currency] -= (quantity * price) + fees

        elif tx.transaction_type == TransactionType.SELL:
            quantity = tx.quantity or 0.0
            price = tx.price or 0.0
            fees = tx.fees or 0.0
            cash_by_currency[currency] += (quantity * price) - fees

        elif tx.transaction_type in {
            TransactionType.DEPOSIT,
            TransactionType.DIVIDEND,
            TransactionType.INTEREST,
            TransactionType.REWARD,
            TransactionType.DISTRIBUTION,
        }:
            cash_by_currency[currency] += tx.amount or 0.0

        elif tx.transaction_type == TransactionType.WITHDRAWAL:
            cash_by_currency[currency] -= tx.amount or 0.0

    pnl_positions = PNL_SERVICE.get_pnl(db)

    invested_value_by_currency = defaultdict(float)
    market_value_by_currency = defaultdict(float)
    unrealized_pnl_by_currency = defaultdict(float)
    priced_positions_count_by_currency = defaultdict(int)
    unpriced_positions_count_by_currency = defaultdict(int)

    for position in pnl_positions:
        currency = position.currency
        invested_value_by_currency[currency] += position.total_cost

        if position.price_available and position.market_value is not None and position.unrealized_pnl is not None:
            market_value_by_currency[currency] += position.market_value
            unrealized_pnl_by_currency[currency] += position.unrealized_pnl
            priced_positions_count_by_currency[currency] += 1
        else:
            unpriced_positions_count_by_currency[currency] += 1

    all_currencies = set(cash_by_currency.keys()) | set(invested_value_by_currency.keys())

    summaries = []
    for currency in sorted(all_currencies):
        priced_count = priced_positions_count_by_currency[currency]
        unpriced_count = unpriced_positions_count_by_currency[currency]

        market_value = market_value_by_currency[currency] if priced_count > 0 else None
        unrealized_pnl = unrealized_pnl_by_currency[currency] if priced_count > 0 else None

        summaries.append(
            PortfolioCurrencySummary(
                currency=currency,
                cash=round(cash_by_currency[currency], 2),
                invested_value=round(invested_value_by_currency[currency], 2),
                market_value=round(market_value, 2) if market_value is not None else None,
                unrealized_pnl=round(unrealized_pnl, 2) if unrealized_pnl is not None else None,
                priced_positions_count=priced_count,
                unpriced_positions_count=unpriced_count,
            )
        )

    return PortfolioSummary(by_currency=summaries)
"""