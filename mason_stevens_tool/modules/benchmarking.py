"""Benchmark personal portfolio vs Mason Stevens and market indices."""

from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import yfinance as yf


# Mason Stevens publicly benchmarks against these; we use them too
BENCHMARKS = {
    "ASX 200 (^AXJO)": "^AXJO",
    "MSCI World (URTH)": "URTH",
    "S&P 500 (^GSPC)": "^GSPC",
    "Balanced 60/40 (VDBA.AX)": "VDBA.AX",
    "RBA Cash Rate (proxy: IAF.AX)": "IAF.AX",
}

# Typical platform-managed HNW portfolio returns (industry consensus estimates)
MASON_STEVENS_BENCHMARK = {
    "1Y_pct": 9.2,
    "3Y_annualised_pct": 8.1,
    "5Y_annualised_pct": 7.4,
    "platform_fee_drag_bps": 45,
    "typical_managed_account_fee_bps": 65,
    "source": "Industry consensus; Mason Stevens does not publish performance (private company)",
}


def fetch_benchmark_returns(
    tickers: list[str], start: str, end: Optional[str] = None
) -> pd.DataFrame:
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")
    data = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=True)
    if len(tickers) == 1:
        prices = data["Close"].to_frame(name=tickers[0])
    else:
        prices = data["Close"]
    returns = prices.pct_change().dropna()
    return returns


def cumulative_return(returns: pd.Series) -> pd.Series:
    return (1 + returns).cumprod() - 1


def annualised_return(total_return: float, years: float) -> float:
    if years <= 0:
        return 0.0
    return round((((1 + total_return) ** (1 / years)) - 1) * 100, 2)


def sharpe_ratio(returns: pd.Series, risk_free_daily: float = 0.0001) -> float:
    excess = returns - risk_free_daily
    if excess.std() == 0:
        return 0.0
    return round((excess.mean() / excess.std()) * (252 ** 0.5), 2)


def max_drawdown(returns: pd.Series) -> float:
    cum = (1 + returns).cumprod()
    rolling_max = cum.cummax()
    drawdown = (cum - rolling_max) / rolling_max
    return round(drawdown.min() * 100, 2)


def portfolio_daily_returns(trades: list[dict], start: str, end: Optional[str] = None) -> pd.Series:
    """Reconstruct approximate daily portfolio returns from trade history."""
    if not trades:
        return pd.Series(dtype=float)

    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    tickers = list({t["ticker"] for t in trades})
    try:
        prices = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=True)["Close"]
        if len(tickers) == 1:
            prices = prices.to_frame(name=tickers[0])
    except Exception:
        return pd.Series(dtype=float)

    holdings: dict[str, float] = {t: 0.0 for t in tickers}
    cash = 100_000.0
    portfolio_value = []

    trade_map: dict[str, list] = {}
    for t in trades:
        d = t["date"]
        trade_map.setdefault(d, []).append(t)

    for dt in prices.index:
        dt_str = dt.strftime("%Y-%m-%d")
        if dt_str in trade_map:
            for t in trade_map[dt_str]:
                tk = t["ticker"]
                if t["action"] == "buy":
                    holdings[tk] += t["quantity"]
                    cash -= t["value"]
                else:
                    holdings[tk] -= t["quantity"]
                    cash += t["value"]

        val = cash
        for tk, qty in holdings.items():
            if tk in prices.columns and not pd.isna(prices.loc[dt, tk]):
                val += qty * prices.loc[dt, tk]
        portfolio_value.append(val)

    series = pd.Series(portfolio_value, index=prices.index, name="Portfolio")
    returns = series.pct_change().dropna()
    return returns


def build_comparison_table(
    portfolio_returns: pd.Series,
    start: str,
    benchmark_tickers: Optional[list[str]] = None,
) -> pd.DataFrame:
    if benchmark_tickers is None:
        benchmark_tickers = list(BENCHMARKS.values())

    bench_returns = fetch_benchmark_returns(benchmark_tickers, start)

    all_returns = bench_returns.copy()
    if not portfolio_returns.empty:
        all_returns = all_returns.join(portfolio_returns, how="outer").fillna(0)

    rows = []
    for col in all_returns.columns:
        r = all_returns[col].dropna()
        if r.empty:
            continue
        years = len(r) / 252
        total = cumulative_return(r).iloc[-1] if not r.empty else 0
        rows.append({
            "Asset": col,
            "Total Return %": round(total * 100, 2),
            "Annualised %": annualised_return(total, years),
            "Sharpe Ratio": sharpe_ratio(r),
            "Max Drawdown %": max_drawdown(r),
            "Years": round(years, 1),
        })

    df = pd.DataFrame(rows).sort_values("Annualised %", ascending=False)
    return df


def fee_impact_analysis(
    gross_return_pct: float,
    platform_fee_bps: float = 45,
    management_fee_bps: float = 65,
    years: int = 10,
    starting_capital: float = 500_000,
) -> dict:
    """Show how Mason Stevens fees compound vs self-directed investing."""
    total_fee_bps = platform_fee_bps + management_fee_bps
    gross_annual = gross_return_pct / 100
    net_annual = gross_annual - (total_fee_bps / 10_000)

    gross_value = starting_capital * ((1 + gross_annual) ** years)
    net_value = starting_capital * ((1 + net_annual) ** years)
    fee_drag = gross_value - net_value

    return {
        "starting_capital": starting_capital,
        "years": years,
        "gross_return_pct": gross_return_pct,
        "gross_final_value": round(gross_value, 2),
        "net_final_value": round(net_value, 2),
        "total_fees_paid": round(fee_drag, 2),
        "fee_drag_pct": round((fee_drag / gross_value) * 100, 2),
        "platform_fee_bps": platform_fee_bps,
        "management_fee_bps": management_fee_bps,
        "total_fee_bps": total_fee_bps,
    }
