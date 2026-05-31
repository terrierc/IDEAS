# Mason Stevens Intelligence Tool

Competitive intelligence and portfolio benchmarking tool for analysing Mason Stevens and the Australian wealth platform market.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=terrierc/IDEAS&branch=main&mainModule=app.py)

## What it does

| Page | Purpose |
|------|---------|
| **Company Intelligence** | Business model canvas, revenue streams, strategic gaps |
| **SWOT Analysis** | Scored strengths, weaknesses, opportunities, threats with visual summary |
| **Competitive Landscape** | Positioning map vs Hub24, Netwealth, Praemium, BT Panorama |
| **Strategy Engine** | Ranked plays to exploit weaknesses, leverage strengths, capitalise on opportunities |
| **My Portfolio** | Trade log with live pricing via yfinance, P&L, allocation chart |
| **Benchmarking** | Fee drag analysis, portfolio vs ASX200 / MSCI World / S&P500 |
| **The Pitch** | Outperformance narrative generator + approach playbook |

## Deploy instantly (Streamlit Cloud — free)

1. Fork or push this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub → **New app** → select this repo → main file: `app.py` → **Deploy**

No configuration required. Streamlit reads `requirements.txt` and installs everything automatically.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

## Project structure

```
app.py                  # Main Streamlit app
requirements.txt        # Python dependencies
.streamlit/
  config.toml           # Disables email prompt, sets dark theme
data/
  mason_stevens.json    # Company profile, SWOT, competitive data
modules/
  company_analysis.py   # SWOT, business model canvas, gap analysis
  portfolio_tracker.py  # Trade log, holdings, P&L (session_state based)
  benchmarking.py       # Fee drag, returns comparison, Sharpe ratio
  strategy_engine.py    # Strategic recommendations and pitch generator
```
