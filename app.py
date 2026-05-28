"""
Mason Stevens Competitive Intelligence & Portfolio Benchmarking Tool
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from modules.company_analysis import (
    load_company_profile,
    get_swot_summary,
    competitive_gap_analysis,
    business_model_canvas,
    strategic_gaps,
)
from modules.portfolio_tracker import (
    sample_portfolio,
    empty_portfolio,
    add_trade,
    delete_trade,
    get_holdings,
    enrich_with_prices,
    portfolio_summary,
)
from modules.benchmarking import (
    BENCHMARKS,
    MASON_STEVENS_BENCHMARK,
    portfolio_daily_returns,
    build_comparison_table,
    fee_impact_analysis,
)
from modules.strategy_engine import (
    get_exploit_plan,
    get_leverage_plan,
    get_opportunity_plan,
    generate_pitch_narrative,
    full_strategy_report,
)

# ── Session state init ────────────────────────────────────────────────────────
if "portfolio" not in st.session_state:
    st.session_state.portfolio = sample_portfolio()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mason Stevens Intelligence Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { min-width: 220px; max-width: 220px; }
.block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

profile = load_company_profile()
company = profile["company"]

PAGES = [
    "Company Intelligence",
    "SWOT Analysis",
    "Competitive Landscape",
    "Strategy Engine",
    "My Portfolio",
    "Benchmarking",
    "The Pitch",
]

with st.sidebar:
    st.markdown("### 📊 MS Intelligence")
    st.caption(f"**{company['name']}**  \nAUM A${company['aum_aud_billions']}B · {company['employees']} staff")
    st.divider()
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.divider()
    st.caption("Built to outperform, then prove it.")


# ─── COMPANY INTELLIGENCE ────────────────────────────────────────────────────

if page == "Company Intelligence":
    st.title(f"Company Intelligence: {company['name']}")
    st.caption(f"Founded {company['founded']} · {company['headquarters']} · {company['ownership']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AUM", f"A${company['aum_aud_billions']}B")
    c2.metric("Valuation", f"A${company['valuation_aud_millions']}M")
    c3.metric("Employees", company["employees"])
    c4.metric("Platform Score", "84.3%", delta="-8.3pp vs leader", delta_color="inverse")

    st.divider()
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("Business Model Canvas")
        bmc = business_model_canvas(profile)
        with st.expander("Value Proposition", expanded=True):
            st.write(bmc["value_proposition"])
        with st.expander("Revenue Streams"):
            for r in bmc["revenue_streams"]:
                st.write(f"• {r}")
        with st.expander("Customer Segments"):
            for s in bmc["customer_segments"]:
                st.write(f"• {s}")
        with st.expander("Key Resources"):
            for r in bmc["key_resources"]:
                st.write(f"• {r}")
        with st.expander("Key Activities"):
            for a in bmc["key_activities"]:
                st.write(f"• {a}")
        with st.expander("Cost Structure"):
            for c in bmc["cost_structure"]:
                st.write(f"• {c}")

    with col_right:
        st.subheader("Strategic Gaps")
        for g in strategic_gaps(profile):
            st.error(f"⚠ {g}")

        st.subheader("Investment Philosophy")
        inv = profile["investment_philosophy"]
        st.write(f"**Approach:** {inv['approach']}")
        st.write("**Asset classes:** " + ", ".join(inv["asset_classes"][:6]) + "...")
        st.write(f"**Outsourced CIO:** {'Yes' if inv['outsourced_cio'] else 'No'}")
        st.write(f"**ESG:** {inv['esg_capability']}")


# ─── SWOT ANALYSIS ───────────────────────────────────────────────────────────

elif page == "SWOT Analysis":
    st.title("SWOT Analysis — Mason Stevens")

    swot = get_swot_summary(profile)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Strengths")
        for item in swot["strengths"]:
            st.markdown(f"**{item['point']}** `{item['score']}/10`")
            st.caption(item["detail"])
            st.divider()

        st.subheader("Opportunities")
        for item in swot["opportunities"]:
            st.markdown(f"**{item['point']}** `{item['score']}/10`")
            st.caption(item["detail"])
            st.divider()

    with col2:
        st.subheader("Weaknesses")
        for item in swot["weaknesses"]:
            st.markdown(f"**{item['point']}** `{item['score']}/10`")
            st.caption(item["detail"])
            st.divider()

        st.subheader("Threats")
        for item in swot["threats"]:
            st.markdown(f"**{item['point']}** `{item['score']}/10`")
            st.caption(item["detail"])
            st.divider()

    st.divider()
    st.subheader("SWOT Score Summary")
    categories = ["strengths", "weaknesses", "opportunities", "threats"]
    avg_scores = {cat: sum(i["score"] for i in swot[cat]) / len(swot[cat]) for cat in categories}
    fig = go.Figure(go.Bar(
        x=list(avg_scores.keys()),
        y=list(avg_scores.values()),
        marker_color=["#a6e3a1", "#f38ba8", "#89dceb", "#fab387"],
        text=[f"{v:.1f}" for v in avg_scores.values()],
        textposition="outside",
    ))
    fig.update_layout(
        title="Average SWOT Score by Category (10 = most impactful)",
        yaxis=dict(range=[0, 10]),
        showlegend=False,
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True)


# ─── COMPETITIVE LANDSCAPE ───────────────────────────────────────────────────

elif page == "Competitive Landscape":
    st.title("Competitive Landscape")

    competitors = profile["competitive_landscape"]["direct_competitors"]
    df = pd.DataFrame(competitors)

    st.subheader("Platform Positioning Map")
    fig = px.scatter(
        df,
        x="aum_billions",
        y="functionality_score",
        size="employees_approx",
        color="name",
        text="name",
        labels={"aum_billions": "AUM (A$ Billions)", "functionality_score": "Platform Functionality Score (%)"},
        title="AUM vs Platform Functionality  (bubble size = employees)",
        height=500,
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Competitive Gap vs Mason Stevens")
    gap_df = pd.DataFrame(competitive_gap_analysis(profile))
    st.dataframe(
        gap_df.style.background_gradient(subset=["aum_gap_billions", "functionality_gap"], cmap="RdYlGn_r"),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Full Competitive Matrix")
    display_df = df[["name", "aum_billions", "functionality_score", "employees_approx", "listed", "differentiator"]].copy()
    display_df.columns = ["Platform", "AUM ($B)", "Functionality %", "~Employees", "Listed", "Differentiator"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Mason Stevens AUM", f"A${company['aum_aud_billions']}B", delta="vs Hub24: -A$46.5B", delta_color="inverse")
    c2.metric("Functionality Score", "84.3%", delta="vs leader: -8.3pp", delta_color="inverse")
    c3.metric("Market Position", "#5 of 6", delta="Fastest improving", delta_color="normal")


# ─── STRATEGY ENGINE ─────────────────────────────────────────────────────────

elif page == "Strategy Engine":
    st.title("Strategy Engine")
    st.caption("How to exploit their weaknesses, leverage their strengths, and capitalise on opportunities.")

    tab1, tab2, tab3 = st.tabs(["Exploit Weaknesses", "Leverage Strengths", "Capitalise Opportunities"])

    with tab1:
        st.subheader("Exploit Their Weaknesses")
        st.caption("Ranked by impact. Build these — then use them as proof of capability.")
        for i, item in enumerate(get_exploit_plan(), 1):
            impact_fn = {"very_high": st.error, "high": st.warning, "medium": st.info}.get(item["impact"], st.info)
            with st.expander(f"#{i} — {item['weakness']}", expanded=(i == 1)):
                impact_fn(f"Impact: {item['impact'].replace('_', ' ').title()} | Effort: {item['effort'].title()}")
                st.markdown(f"**Strategy:** {item['strategy']}")
                st.markdown(f"**Proof Point:** {item['proof_point']}")
                st.info(f"**Pitch Line:** {item['pitch']}")

    with tab2:
        st.subheader("Leverage Their Strengths")
        st.caption("Show you understand their best assets — and can help them extract more value from them.")
        for item in get_leverage_plan():
            with st.expander(f"Strength: {item['strength'][:70]}"):
                st.markdown(f"**Strategy:** {item['strategy']}")
                st.markdown(f"**Opportunity:** {item['opportunity']}")
                st.success(f"**Pitch Line:** {item['pitch']}")

    with tab3:
        st.subheader("Capitalise on Market Opportunities")
        st.caption("Opportunities Mason Stevens is positioned for but not yet executing on.")
        for item in get_opportunity_plan():
            with st.expander(f"Opportunity: {item['opportunity'][:70]}"):
                st.markdown(f"**Strategy:** {item['strategy']}")
                st.warning(f"**Timing:** {item['timing']}")
                st.success(f"**Pitch Line:** {item['pitch']}")


# ─── MY PORTFOLIO ────────────────────────────────────────────────────────────

elif page == "My Portfolio":
    st.title("My Portfolio")

    port = st.session_state.portfolio
    summary = portfolio_summary(port)
    holdings = get_holdings(port)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Positions", summary["num_positions"])
    c2.metric("Market Value", f"${summary['market_value']:,.0f}")
    c3.metric("Total Cost", f"${summary['total_cost']:,.0f}")
    c4.metric("Unrealised P&L", f"${summary['unrealised_pnl']:,.0f}")
    c5.metric("Return", f"{summary['total_pct_return']:.2f}%")

    st.divider()
    tab1, tab2, tab3 = st.tabs(["Holdings", "Add Trade", "Manage"])

    with tab1:
        enriched = enrich_with_prices(holdings)
        if enriched.empty:
            st.info("No holdings. Add trades in the **Add Trade** tab.")
        else:
            def _colour_pnl(val):
                if not isinstance(val, (int, float)):
                    return ""
                return "color: #a6e3a1" if val > 0 else "color: #f38ba8" if val < 0 else ""

            st.dataframe(
                enriched.style.map(_colour_pnl, subset=["unrealised_pnl", "pct_return"]),
                use_container_width=True,
                hide_index=True,
            )
            fig = px.pie(enriched, values="market_value", names="ticker", title="Portfolio Allocation by Market Value")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        with st.form("add_trade"):
            c1, c2, c3 = st.columns(3)
            ticker = c1.text_input("Ticker  (e.g. BHP.AX, AAPL)").strip().upper()
            action = c2.selectbox("Action", ["buy", "sell"])
            currency = c3.selectbox("Currency", ["AUD", "USD", "GBP", "EUR"])

            c4, c5, c6 = st.columns(3)
            quantity = c4.number_input("Quantity", min_value=0.0001, value=100.0)
            price = c5.number_input("Price per share ($)", min_value=0.0001, value=10.0)
            trade_date = c6.date_input("Trade Date")

            notes = st.text_input("Notes (optional)")
            if st.form_submit_button("Add Trade", type="primary"):
                if not ticker:
                    st.error("Enter a ticker symbol.")
                else:
                    st.session_state.portfolio, trade = add_trade(
                        st.session_state.portfolio,
                        ticker=ticker,
                        action=action,
                        quantity=quantity,
                        price=price,
                        trade_date=str(trade_date),
                        currency=currency,
                        notes=notes,
                    )
                    st.success(f"Added: {action.upper()} {quantity:,.4g} × {ticker} @ ${price:.4f} = ${trade['value']:,.2f}")
                    st.rerun()

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Reset to Sample Portfolio")
            st.caption("Replaces all trades with the demo ASX portfolio.")
            if st.button("Load Sample Portfolio"):
                st.session_state.portfolio = sample_portfolio()
                st.success("Sample portfolio loaded.")
                st.rerun()
        with c2:
            st.subheader("Clear All Trades")
            st.caption("Start fresh with a blank portfolio.")
            if st.button("Clear Portfolio", type="secondary"):
                st.session_state.portfolio = empty_portfolio()
                st.success("Portfolio cleared.")
                st.rerun()

        trades = port.get("trades", [])
        if trades:
            st.divider()
            st.subheader("Trade History")
            trades_df = pd.DataFrame(trades)[["id", "date", "ticker", "action", "quantity", "price", "value", "currency", "notes"]]
            st.dataframe(trades_df, use_container_width=True, hide_index=True)

            with st.form("delete_trade"):
                del_id = st.number_input("Delete trade by ID", min_value=1, step=1, value=1)
                if st.form_submit_button("Delete", type="secondary"):
                    st.session_state.portfolio = delete_trade(st.session_state.portfolio, int(del_id))
                    st.success(f"Trade {del_id} deleted.")
                    st.rerun()


# ─── BENCHMARKING ────────────────────────────────────────────────────────────

elif page == "Benchmarking":
    st.title("Benchmarking")
    st.caption("How your portfolio compares vs market indices and Mason Stevens' benchmarks.")

    st.subheader("Fee Impact Analysis")
    st.caption("The real cost of paying Mason Stevens platform + management fees vs self-directed investing.")

    c1, c2, c3 = st.columns(3)
    starting_capital = c1.number_input("Starting Capital ($)", value=500_000, step=50_000)
    gross_return = c2.number_input("Assumed Gross Return (%/yr)", value=9.0, step=0.5)
    years = c3.slider("Years", min_value=1, max_value=30, value=10)

    fee_data = fee_impact_analysis(gross_return, years=years, starting_capital=starting_capital)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gross Final Value", f"${fee_data['gross_final_value']:,.0f}")
    c2.metric("Net After Fees", f"${fee_data['net_final_value']:,.0f}")
    c3.metric("Total Fees Paid", f"${fee_data['total_fees_paid']:,.0f}", delta_color="inverse")
    c4.metric("Fee Drag", f"{fee_data['fee_drag_pct']:.1f}%", delta_color="inverse")

    years_list = list(range(1, years + 1))
    gross_vals = [starting_capital * ((1 + gross_return / 100) ** y) for y in years_list]
    net_rate = gross_return / 100 - fee_data["total_fee_bps"] / 10_000
    net_vals = [starting_capital * ((1 + net_rate) ** y) for y in years_list]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years_list, y=gross_vals, name="Self-Directed (no platform fees)", line=dict(color="#a6e3a1", width=2)))
    fig.add_trace(go.Scatter(x=years_list, y=net_vals, name=f"Mason Stevens (~{fee_data['total_fee_bps']} bps fees)", line=dict(color="#f38ba8", width=2, dash="dash")))
    fig.update_layout(title="Compounding Fee Drag Over Time", xaxis_title="Years", yaxis_title="Portfolio Value ($)", height=360)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Mason Stevens Benchmark Reference")
    ms = MASON_STEVENS_BENCHMARK
    c1, c2, c3 = st.columns(3)
    c1.metric("1Y Benchmark Return", f"{ms['1Y_pct']}%")
    c2.metric("3Y Annualised", f"{ms['3Y_annualised_pct']}%")
    c3.metric("5Y Annualised", f"{ms['5Y_annualised_pct']}%")
    st.caption(f"Source: {ms['source']}")

    port = st.session_state.portfolio
    trades = port.get("trades", [])
    inception = port.get("inception_date")

    if trades and inception:
        st.divider()
        st.subheader("Live Portfolio vs Benchmarks")
        st.caption("Fetches live market data and compares your portfolio from inception date. Takes ~10 seconds.")
        if st.button("Run Comparison", type="primary"):
            with st.spinner("Fetching market data..."):
                try:
                    port_returns = portfolio_daily_returns(trades, inception)
                    bench_tickers = list(BENCHMARKS.values())[:3]
                    comparison = build_comparison_table(port_returns, inception, bench_tickers)
                    st.dataframe(
                        comparison.style.background_gradient(subset=["Annualised %", "Sharpe Ratio"], cmap="RdYlGn"),
                        use_container_width=True,
                        hide_index=True,
                    )
                except Exception as e:
                    st.warning(f"Could not fetch live data: {e}")
    else:
        st.info("Add your own trades in **My Portfolio** to enable live benchmarking.")


# ─── THE PITCH ───────────────────────────────────────────────────────────────

elif page == "The Pitch":
    st.title("The Pitch")
    st.caption("Structure your approach: sell the technology, land a job, or open a consulting conversation.")

    port = st.session_state.portfolio
    summary = portfolio_summary(port)
    default_return = float(summary.get("total_pct_return") or 12.0)

    c1, c2 = st.columns(2)
    personal_return = c1.number_input("Your Portfolio Return (%)", value=default_return, step=0.5)
    benchmark_return = c2.number_input("Mason Stevens Benchmark Return (%)", value=9.2, step=0.5)

    outperformance = personal_return - benchmark_return
    st.metric(
        "Outperformance vs Mason Stevens Benchmark",
        f"{outperformance:+.2f} percentage points",
        delta_color="normal" if outperformance > 0 else "inverse",
    )

    st.divider()
    st.markdown(generate_pitch_narrative(personal_return, benchmark_return))

    st.divider()
    st.subheader("Top 3 Priority Actions — Build These First")
    report = full_strategy_report(profile, personal_return, benchmark_return)
    for i, action in enumerate(report["top_3_priority_actions"], 1):
        st.info(f"**#{i}** {action}")

    st.divider()
    st.subheader("How to Approach Them")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Option A — Sell the Tech**")
        st.markdown("""
- Build 1–2 working prototypes from the Strategy Engine list
- Request a product demo with their CTO / CPO
- Price as SaaS overlay: $50K–$200K setup + per-adviser monthly fee
- Precedent: their ATHENA deal proves they buy fintech
        """)
    with c2:
        st.markdown("**Option B — Get Hired**")
        st.markdown("""
- Apply to Investment Analyst, Product Manager, or Data/Quant roles
- Lead with your quantified outperformance + this toolset
- New PE owner = active growth hiring cycle
- Ask for a technical interview, not just a resume screen
        """)
    with c3:
        st.markdown("**Option C — Consulting Entry**")
        st.markdown("""
- Offer a 30-day engagement: platform gap analysis + M&A shortlist
- Price: $10K–$20K AUD
- Deliverable: this tool's output, packaged as a report
- Outcome: credibility, access, and a recurring relationship
        """)

    st.divider()
    st.subheader("Who to Contact at Mason Stevens")
    st.markdown("""
| Role | Why | How to reach |
|------|-----|-------------|
| CEO | Tech acquisition / senior hire decision | LinkedIn · Direct email via website |
| CTO / CPO | Platform prototype demo | LinkedIn |
| Peter Mermolas (Family Office) | Your family office dashboard pitch aligns directly to his brief | LinkedIn |
| Investment / Portfolio team | Investment process & performance conversation | LinkedIn · IMAP events |

*Post-Adamantem acquisition (April 2025) there will be new hires — check LinkedIn for current leadership.*
    """)
