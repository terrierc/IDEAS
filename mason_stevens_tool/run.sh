#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Install dependencies if needed
if ! python -c "import streamlit, pandas, plotly, yfinance" 2>/dev/null; then
  echo "Installing dependencies..."
  pip install -r requirements.txt --quiet
fi

echo ""
echo "  Mason Stevens Intelligence Tool"
echo "  ================================"
echo "  Open your browser at: http://localhost:8501"
echo ""

streamlit run app.py
