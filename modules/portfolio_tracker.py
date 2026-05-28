"""
Portfolio tracker — pure functions, no file I/O.
State is managed by the caller (st.session_state in app.py).
"""

from datetime import datetime
import pandas as pd
import yfinance as yf


def empty_portfolio(name: str = "My Portfolio") -> dict:
    return {"trades": [], "cash": 0.0, "name": name, "inception_date": None}


def sample_portfolio() -> dict:
    return {
        "name": "Demo Portfolio",
        "inception_date": "2023-01-01",
        "cash": 15_000.0,
        "trades": [
            {"id": 1, "ticker": "BHP.AX",  "action": "buy", "quantity": 100, "price": 42.50,  "value": 4_250.0,  "date": "2023-01-15", "currency": "AUD", "notes": "Resources exposure"},
            {"id": 2, "ticker": "CBA.AX",  "action": "buy", "quantity": 30,  "price": 98.00,  "value": 2_940.0,  "date": "2023-02-01", "currency": "AUD", "notes": "Big 4 banking yield"},
            {"id": 3, "ticker": "CSL.AX",  "action": "buy", "quantity": 15,  "price": 280.00, "value": 4_200.0,  "date": "2023-03-10", "currency": "AUD", "notes": "Healthcare quality"},
            {"id": 4, "ticker": "NDQ.AX",  "action": "buy", "quantity": 200, "price": 28.50,  "value": 5_700.0,  "date": "2023-04-05", "currency": "AUD", "notes": "Global tech ETF"},
            {"id": 5, "ticker": "VGS.AX",  "action": "buy", "quantity": 100, "price": 95.00,  "value": 9_500.0,  "date": "2023-05-20", "currency": "AUD", "notes": "International diversification"},
            {"id": 6, "ticker": "WDS.AX",  "action": "buy", "quantity": 80,  "price": 35.00,  "value": 2_800.0,  "date": "2023-07-15", "currency": "AUD", "notes": "Energy"},
            {"id": 7, "ticker": "APX.AX",  "action": "buy", "quantity": 50,  "price": 14.00,  "value": 700.0,    "date": "2023-08-01", "currency": "AUD", "notes": "Fintech"},
        ],
    }


def add_trade(
    portfolio: dict,
    ticker: str,
    action: str,
    quantity: float,
    price: float,
    trade_date: str,
    currency: str = "AUD",
    notes: str = "",
) -> tuple[dict, dict]:
    import copy
    p = copy.deepcopy(portfolio)
    if p["inception_date"] is None:
        p["inception_date"] = trade_date
    trade = {
        "id": len(p["trades"]) + 1,
        "ticker": ticker.upper(),
        "action": action.lower(),
        "quantity": quantity,
        "price": price,
        "value": round(quantity * price, 2),
        "date": trade_date,
        "currency": currency,
        "notes": notes,
    }
    p["cash"] = p["cash"] - trade["value"] if action == "buy" else p["cash"] + trade["value"]
    p["trades"].append(trade)
    return p, trade


def delete_trade(portfolio: dict, trade_id: int) -> dict:
    import copy
    p = copy.deepcopy(portfolio)
    p["trades"] = [t for t in p["trades"] if t["id"] != trade_id]
    return p


def get_holdings(portfolio: dict) -> pd.DataFrame:
    trades = portfolio.get("trades", [])
    if not trades:
        return pd.DataFrame(columns=["ticker", "quantity", "avg_cost", "total_cost"])
    holdings: dict[str, dict] = {}
    for t in trades:
        tk = t["ticker"]
        if tk not in holdings:
            holdings[tk] = {"quantity": 0.0, "total_cost": 0.0}
        if t["action"] == "buy":
            holdings[tk]["quantity"] += t["quantity"]
            holdings[tk]["total_cost"] += t["value"]
        else:
            if holdings[tk]["quantity"] > 0:
                avg = holdings[tk]["total_cost"] / holdings[tk]["quantity"]
                holdings[tk]["quantity"] -= t["quantity"]
                holdings[tk]["total_cost"] -= avg * t["quantity"]
    rows = [
        {
            "ticker": tk,
            "quantity": round(h["quantity"], 4),
            "avg_cost": round(h["total_cost"] / h["quantity"], 4) if h["quantity"] > 0 else 0,
            "total_cost": round(h["total_cost"], 2),
        }
        for tk, h in holdings.items()
        if h["quantity"] > 0.001
    ]
    return pd.DataFrame(rows)


def enrich_with_prices(holdings: pd.DataFrame) -> pd.DataFrame:
    if holdings.empty:
        return holdings
    rows = []
    for _, row in holdings.iterrows():
        try:
            info = yf.Ticker(row["ticker"]).fast_info
            current_price = float(info.last_price or info.previous_close or row["avg_cost"])
        except Exception:
            current_price = float(row["avg_cost"])
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


def portfolio_summary(portfolio: dict) -> dict:
    holdings = get_holdings(portfolio)
    cash = portfolio.get("cash", 0.0)
    if holdings.empty:
        return {
            "name": portfolio.get("name", "My Portfolio"),
            "inception_date": portfolio.get("inception_date"),
            "num_positions": 0,
            "cash": cash,
            "total_cost": 0,
            "market_value": cash,
            "unrealised_pnl": 0,
            "total_pct_return": 0.0,
        }
    enriched = enrich_with_prices(holdings)
    total_cost = enriched["total_cost"].sum()
    market_value = enriched["market_value"].sum() + cash
    unrealised_pnl = enriched["unrealised_pnl"].sum()
    total_pct_return = round((unrealised_pnl / total_cost) * 100, 2) if total_cost else 0.0
    return {
        "name": portfolio.get("name", "My Portfolio"),
        "inception_date": portfolio.get("inception_date"),
        "num_positions": len(enriched),
        "cash": cash,
        "total_cost": round(float(total_cost), 2),
        "market_value": round(float(market_value), 2),
        "unrealised_pnl": round(float(unrealised_pnl), 2),
        "total_pct_return": total_pct_return,
    }
