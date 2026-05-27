"""Personal portfolio tracker with real market data via yfinance."""

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf


PORTFOLIO_FILE = Path(__file__).parent.parent / "data" / "portfolio.json"


def _load_portfolio() -> dict:
    if PORTFOLIO_FILE.exists():
        with open(PORTFOLIO_FILE) as f:
            return json.load(f)
    return {"trades": [], "cash": 0.0, "name": "My Portfolio", "inception_date": None}


def _save_portfolio(data: dict) -> None:
    PORTFOLIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def add_trade(
    ticker: str,
    action: str,  # "buy" or "sell"
    quantity: float,
    price: float,
    trade_date: str,
    currency: str = "AUD",
    notes: str = "",
) -> dict:
    data = _load_portfolio()
    if data["inception_date"] is None:
        data["inception_date"] = trade_date
    trade = {
        "id": len(data["trades"]) + 1,
        "ticker": ticker.upper(),
        "action": action.lower(),
        "quantity": quantity,
        "price": price,
        "value": round(quantity * price, 2),
        "date": trade_date,
        "currency": currency,
        "notes": notes,
        "timestamp": datetime.now().isoformat(),
    }
    if action.lower() == "buy":
        data["cash"] -= trade["value"]
    else:
        data["cash"] += trade["value"]
    data["trades"].append(trade)
    _save_portfolio(data)
    return trade


def set_cash_balance(amount: float) -> None:
    data = _load_portfolio()
    data["cash"] = amount
    _save_portfolio(data)


def get_holdings() -> pd.DataFrame:
    data = _load_portfolio()
    if not data["trades"]:
        return pd.DataFrame(columns=["ticker", "quantity", "avg_cost", "total_cost"])

    holdings: dict[str, dict] = {}
    for t in data["trades"]:
        ticker = t["ticker"]
        if ticker not in holdings:
            holdings[ticker] = {"quantity": 0.0, "total_cost": 0.0, "trades": 0}
        if t["action"] == "buy":
            holdings[ticker]["quantity"] += t["quantity"]
            holdings[ticker]["total_cost"] += t["value"]
            holdings[ticker]["trades"] += 1
        else:
            if holdings[ticker]["quantity"] > 0:
                avg_cost = holdings[ticker]["total_cost"] / holdings[ticker]["quantity"]
                holdings[ticker]["quantity"] -= t["quantity"]
                holdings[ticker]["total_cost"] -= avg_cost * t["quantity"]

    rows = []
    for ticker, h in holdings.items():
        if h["quantity"] > 0.001:
            rows.append({
                "ticker": ticker,
                "quantity": round(h["quantity"], 4),
                "avg_cost": round(h["total_cost"] / h["quantity"], 4) if h["quantity"] > 0 else 0,
                "total_cost": round(h["total_cost"], 2),
            })
    return pd.DataFrame(rows)


def enrich_with_prices(holdings: pd.DataFrame) -> pd.DataFrame:
    if holdings.empty:
        return holdings
    rows = []
    for _, row in holdings.iterrows():
        ticker = row["ticker"]
        try:
            info = yf.Ticker(ticker).fast_info
            current_price = info.last_price or info.previous_close
        except Exception:
            current_price = row["avg_cost"]

        market_value = round(row["quantity"] * current_price, 2)
        unrealised_pnl = round(market_value - row["total_cost"], 2)
        pct_return = round((unrealised_pnl / row["total_cost"]) * 100, 2) if row["total_cost"] else 0

        rows.append({
            **row.to_dict(),
            "current_price": round(current_price, 4),
            "market_value": market_value,
            "unrealised_pnl": unrealised_pnl,
            "pct_return": pct_return,
        })
    return pd.DataFrame(rows)


def portfolio_summary() -> dict:
    data = _load_portfolio()
    holdings = get_holdings()
    if holdings.empty:
        return {
            "name": data.get("name", "My Portfolio"),
            "inception_date": data.get("inception_date"),
            "num_positions": 0,
            "cash": data["cash"],
            "total_cost": 0,
            "market_value": 0,
            "unrealised_pnl": 0,
            "total_pct_return": 0,
        }
    enriched = enrich_with_prices(holdings)
    total_cost = enriched["total_cost"].sum()
    market_value = enriched["market_value"].sum() + data["cash"]
    unrealised_pnl = enriched["unrealised_pnl"].sum()
    total_pct_return = round((unrealised_pnl / total_cost) * 100, 2) if total_cost else 0
    return {
        "name": data.get("name", "My Portfolio"),
        "inception_date": data.get("inception_date"),
        "num_positions": len(enriched),
        "cash": data["cash"],
        "total_cost": round(total_cost, 2),
        "market_value": round(market_value, 2),
        "unrealised_pnl": round(unrealised_pnl, 2),
        "total_pct_return": total_pct_return,
    }


def get_all_trades() -> list[dict]:
    return _load_portfolio()["trades"]


def set_portfolio_name(name: str) -> None:
    data = _load_portfolio()
    data["name"] = name
    _save_portfolio(data)


def delete_trade(trade_id: int) -> bool:
    data = _load_portfolio()
    original_len = len(data["trades"])
    data["trades"] = [t for t in data["trades"] if t["id"] != trade_id]
    _save_portfolio(data)
    return len(data["trades"]) < original_len


def import_sample_portfolio() -> None:
    """Loads a sample high-performing portfolio for demo purposes."""
    data = _load_portfolio()
    data["name"] = "Demo Portfolio"
    data["inception_date"] = "2023-01-01"
    data["cash"] = 15000.0
    data["trades"] = [
        {"id": 1, "ticker": "BHP.AX", "action": "buy", "quantity": 100, "price": 42.50, "value": 4250.0, "date": "2023-01-15", "currency": "AUD", "notes": "Resources exposure", "timestamp": "2023-01-15T10:00:00"},
        {"id": 2, "ticker": "CBA.AX", "action": "buy", "quantity": 30, "price": 98.00, "value": 2940.0, "date": "2023-02-01", "currency": "AUD", "notes": "Big 4 banking yield", "timestamp": "2023-02-01T10:00:00"},
        {"id": 3, "ticker": "CSL.AX", "action": "buy", "quantity": 15, "price": 280.00, "value": 4200.0, "date": "2023-03-10", "currency": "AUD", "notes": "Healthcare quality", "timestamp": "2023-03-10T10:00:00"},
        {"id": 4, "ticker": "NDQ.AX", "action": "buy", "quantity": 200, "price": 28.50, "value": 5700.0, "date": "2023-04-05", "currency": "AUD", "notes": "Global tech exposure via ETF", "timestamp": "2023-04-05T10:00:00"},
        {"id": 5, "ticker": "VGS.AX", "action": "buy", "quantity": 100, "price": 95.00, "value": 9500.0, "date": "2023-05-20", "currency": "AUD", "notes": "International diversification", "timestamp": "2023-05-20T10:00:00"},
        {"id": 6, "ticker": "NXL.AX", "action": "buy", "quantity": 500, "price": 1.20, "value": 600.0, "date": "2023-06-01", "currency": "AUD", "notes": "Small cap speculative", "timestamp": "2023-06-01T10:00:00"},
        {"id": 7, "ticker": "WDS.AX", "action": "buy", "quantity": 80, "price": 35.00, "value": 2800.0, "date": "2023-07-15", "currency": "AUD", "notes": "Energy transition play", "timestamp": "2023-07-15T10:00:00"},
        {"id": 8, "ticker": "APX.AX", "action": "buy", "quantity": 50, "price": 14.00, "value": 700.0, "date": "2023-08-01", "currency": "AUD", "notes": "Fintech exposure", "timestamp": "2023-08-01T10:00:00"},
    ]
    _save_portfolio(data)
