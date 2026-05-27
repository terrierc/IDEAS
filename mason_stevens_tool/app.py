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
    get_top_weaknesses,
    get_top_opportunities,
    competitive_gap_analysis,
    business_model_canvas,
    strategic_gaps,
)
from modules.portfolio_tracker import (
    add_trade,
    get_holdings,
    enrich_with_prices,
    portfolio_summary,
    get_all_trades,
    set_portfolio_name,
    delete_trade,
    import_sample_portfolio,
    set_cash_balance,
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


st.set_page_config(
    page_title="Mason Stevens Intelligence Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.metric-card {
    background: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 16px;
    margin: 4px 0;
}
.positive { color: #a6e3a1; font-weight: bold; }
.negative { color: #f38ba8; font-weight: bold; }
.tag-high { background: #f38ba8; color: #1e1e2e; border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; }
.tag-medium { background: #fab387; color: #1e1e2e; border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; }
.tag-low { background: #a6e3a1; color: #1e1e2e; border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

profile = load_company_profile()
company = profile["company"]

with st.sidebar:
    st.title("📊 MS Intelligence")
    st.caption(f"Target: **{company['name']}**")
    st.caption(f"AUM: AUD ${company['aum_aud_billions']}B | Staff: {company['employees']}")
    st.divider()
    page = st.radio(
        "Navigate",
        [
            "Company Intelligence",
            "SWOT Analysis",
            "Competitive Landscape",
            "Strategy Engine",
            "My Portfolio",
            "Benchmarking",
            "The Pitch",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Built to outperform, then prove it.")


# ─── COMPANY INTELLIGENCE ────────────────────────────────────────────────────

if page == "Company Intelligence":
    st.title(f"Company Intelligence: {company['name']}")
    st.caption(f"Founded {company['founded']} · {company['headquarters']} · {company['ownership']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("AUM", f"A${company['aum_aud_billions']}B")
    col2.metric("Valuation", f"A${company['valuation_aud_millions']}M")
    col3.metric("Employees", company["employees"])
    col4.metric("Platform Score", "84.3%", delta="-8.3pp vs leader", delta_color="inverse")

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
        gaps = strategic_gaps(profile)
        for g in gaps:
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
            with st.container():
                st.markdown(f"**{item['point']}** `score {item['score']}/10`")
                st.caption(item["detail"])
                st.divider()

        st.subheader("Opportunities")
        for item in swot["opportunities"]:
            with st.container():
                st.markdown(f"**{item['point']}** `score {item['score']}/10`")
                st.caption(item["detail"])
                st.divider()

    with col2:
        st.subheader("Weaknesses")
        for item in swot["weaknesses"]:
            with st.container():
                st.markdown(f"**{item['point']}** `score {item['score']}/10`")
                st.caption(item["detail"])
                st.divider()

        st.subheader("Threats")
        for item in swot["threats"]:
            with st.container():
                st.markdown(f"**{item['point']}** `score {item['score']}/10`")
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
        title="AUM vs Platform Functionality (bubble size = employees)",
        height=500,
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Competitive Gap vs Mason Stevens")
    gaps = competitive_gap_analysis(profile)
    gap_df = pd.DataFrame(gaps)
    st.dataframe(
        gap_df.style.background_gradient(subset=["aum_gap_billions", "functionality_gap"], cmap="RdYlGn_r"),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Full Competitive Matrix")
    display_df = df[["name", "aum_billions", "functionality_score", "employees_approx", "listed", "differentiator"]].copy()
    display_df.columns = ["Platform", "AUM ($B)", "Functionality %", "~Employees", "Listed", "Differentiator"]
    ms_row = display_df[display_df["Platform"] == "Mason Stevens"].index
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Mason Stevens AUM", f"A${company['aum_aud_billions']}B", delta="vs Hub24: -A$46.5B", delta_color="inverse")
    col2.metric("Functionality Score", "84.3%", delta="vs leader: -8.3pp", delta_color="inverse")
    col3.metric("Market Position", "#5 of 6", delta="Fastest improving", delta_color="normal")


# ─── STRATEGY ENGINE ─────────────────────────────────────────────────────────

elif page == "Strategy Engine":
    st.title("Strategy Engine")
    st.caption("How to exploit their weaknesses, leverage their strengths, and capitalise on opportunities.")

    tab1, tab2, tab3 = st.tabs(["Exploit Weaknesses", "Leverage Strengths", "Capitalise Opportunities"])

    with tab1:
        st.subheader("Exploit Their Weaknesses")
        st.caption("Ranked by impact. Build these — then use them as proof of capability.")
        for i, item in enumerate(get_exploit_plan(), 1):
            impact_colour = {"very_high": "error", "high": "warning", "medium": "info"}.get(item["impact"], "info")
            with st.expander(f"#{i} — {item['weakness']}", expanded=(i == 1)):
                getattr(st, impact_colour)(f"Impact: {item['impact'].replace('_', ' ').title()} | Effort: {item['effort'].title()}")
                st.markdown(f"**Strategy:** {item['strategy']}")
                st.markdown(f"**Proof Point:** {item['proof_point']}")
                st.info(f"**Pitch Line:** {item['pitch']}")

    with tab2:
        st.subheader("Leverage Their Strengths")
        st.caption("Show you understand their best assets — and can help them extract more value from them.")
        for item in get_leverage_plan():
            with st.expander(f"Strength: {item['strength'][:60]}..."):
                st.markdown(f"**Strategy:** {item['strategy']}")
                st.markdown(f"**Opportunity:** {item['opportunity']}")
                st.success(f"**Pitch Line:** {item['pitch']}")

    with tab3:
        st.subheader("Capitalise on Market Opportunities")
        st.caption("Opportunities Mason Stevens is positioned for but not yet executing on.")
        for item in get_opportunity_plan():
            with st.expander(f"Opportunity: {item['opportunity'][:60]}..."):
                st.markdown(f"**Strategy:** {item['strategy']}")
                st.warning(f"**Timing:** {item['timing']}")
                st.success(f"**Pitch Line:** {item['pitch']}")


# ─── MY PORTFOLIO ────────────────────────────────────────────────────────────

elif page == "My Portfolio":
    st.title("My Portfolio")

    summary = portfolio_summary()
    holdings = get_holdings()
    trades = get_all_trades()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Positions", summary["num_positions"])
    col2.metric("Market Value", f"${summary['market_value']:,.0f}")
    col3.metric("Total Cost", f"${summary['total_cost']:,.0f}")
    pnl_colour = "normal" if summary["unrealised_pnl"] >= 0 else "inverse"
    col4.metric("Unrealised P&L", f"${summary['unrealised_pnl']:,.0f}", delta_color=pnl_colour)
    ret_colour = "normal" if summary["total_pct_return"] >= 0 else "inverse"
    col5.metric("Return", f"{summary['total_pct_return']:.2f}%", delta_color=ret_colour)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Holdings", "Add Trade", "Import / Reset"])

    with tab1:
        if holdings.empty:
            st.info("No holdings yet. Add trades in the 'Add Trade' tab, or import the sample portfolio.")
        else:
            enriched = enrich_with_prices(holdings)
            st.dataframe(
                enriched.style.applymap(
                    lambda v: "color: #a6e3a1" if isinstance(v, float) and v > 0 else "color: #f38ba8" if isinstance(v, float) and v < 0 else "",
                    subset=["unrealised_pnl", "pct_return"],
                ),
                use_container_width=True,
                hide_index=True,
            )

            if not enriched.empty:
                fig = px.pie(enriched, values="market_value", names="ticker", title="Portfolio Allocation by Market Value")
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        with st.form("add_trade"):
            col1, col2, col3 = st.columns(3)
            ticker = col1.text_input("Ticker (e.g. BHP.AX, AAPL)").upper()
            action = col2.selectbox("Action", ["buy", "sell"])
            currency = col3.selectbox("Currency", ["AUD", "USD", "GBP", "EUR"])

            col4, col5, col6 = st.columns(3)
            quantity = col4.number_input("Quantity", min_value=0.0001, value=100.0)
            price = col5.number_input("Price", min_value=0.0001, value=10.0)
            trade_date = col6.date_input("Date")

            notes = st.text_input("Notes (optional)")
            submitted = st.form_submit_button("Add Trade")

            if submitted and ticker:
                trade = add_trade(
                    ticker=ticker,
                    action=action,
                    quantity=quantity,
                    price=price,
                    trade_date=str(trade_date),
                    currency=currency,
                    notes=notes,
                )
                st.success(f"Added: {action.upper()} {quantity} x {ticker} @ ${price:.4f} = ${trade['value']:,.2f}")
                st.rerun()

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Import Sample Portfolio")
            st.caption("Loads a demo ASX portfolio for testing.")
            if st.button("Load Sample Portfolio"):
                import_sample_portfolio()
                st.success("Sample portfolio loaded.")
                st.rerun()
        with col2:
            st.subheader("Set Portfolio Name")
            new_name = st.text_input("Name", value=summary.get("name", "My Portfolio"))
            if st.button("Update Name"):
                set_portfolio_name(new_name)
                st.success("Name updated.")
                st.rerun()

    if trades:
        st.divider()
        st.subheader("Trade History")
        trades_df = pd.DataFrame(trades)
        st.dataframe(trades_df[["id", "date", "ticker", "action", "quantity", "price", "value", "currency", "notes"]], use_container_width=True, hide_index=True)

        del_id = st.number_input("Delete trade by ID", min_value=1, step=1)
        if st.button("Delete Trade"):
            if delete_trade(int(del_id)):
                st.success(f"Trade {del_id} deleted.")
                st.rerun()
            else:
                st.error("Trade not found.")


# ─── BENCHMARKING ────────────────────────────────────────────────────────────

elif page == "Benchmarking":
    st.title("Benchmarking")
    st.caption("How your portfolio compares vs market indices and Mason Stevens' benchmarks.")

    summary = portfolio_summary()
    trades = get_all_trades()

    st.subheader("Fee Impact Analysis")
    st.caption("How much Mason Stevens' fees cost a client vs self-directed investing over time.")

    col1, col2, col3 = st.columns(3)
    starting_capital = col1.number_input("Starting Capital ($)", value=500_000, step=50_000)
    gross_return = col2.number_input("Assumed Gross Return (%)", value=9.0, step=0.5)
    years = col3.slider("Years", min_value=1, max_value=30, value=10)

    fee_data = fee_impact_analysis(gross_return, years=years, starting_capital=starting_capital)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gross Final Value", f"${fee_data['gross_final_value']:,.0f}")
    col2.metric("Net After Fees", f"${fee_data['net_final_value']:,.0f}")
    col3.metric("Total Fees Paid", f"${fee_data['total_fees_paid']:,.0f}", delta_color="inverse")
    col4.metric("Fee Drag", f"{fee_data['fee_drag_pct']:.1f}%", delta_color="inverse")

    years_list = list(range(1, years + 1))
    gross_vals = [starting_capital * ((1 + gross_return / 100) ** y) for y in years_list]
    net_rate = gross_return / 100 - fee_data["total_fee_bps"] / 10_000
    net_vals = [starting_capital * ((1 + net_rate) ** y) for y in years_list]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years_list, y=gross_vals, name="Self-Directed (0 bps)", line=dict(color="#a6e3a1", width=2)))
    fig.add_trace(go.Scatter(x=years_list, y=net_vals, name=f"Mason Stevens (~{fee_data['total_fee_bps']}bps fees)", line=dict(color="#f38ba8", width=2, dash="dash")))
    fig.update_layout(title="Compounding Fee Drag Over Time", xaxis_title="Years", yaxis_title="Portfolio Value ($)", height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Mason Stevens Benchmark Reference")
    ms_bench = MASON_STEVENS_BENCHMARK
    col1, col2, col3 = st.columns(3)
    col1.metric("1Y Benchmark Return", f"{ms_bench['1Y_pct']}%", help=ms_bench["source"])
    col2.metric("3Y Annualised", f"{ms_bench['3Y_annualised_pct']}%")
    col3.metric("5Y Annualised", f"{ms_bench['5Y_annualised_pct']}%")
    st.caption(f"Source: {ms_bench['source']}")

    if trades and summary["inception_date"]:
        st.divider()
        st.subheader("Portfolio vs Benchmarks")
        st.caption("Compares your portfolio performance vs market indices from your portfolio inception date.")
        if st.button("Run Comparison (fetches live market data)"):
            with st.spinner("Fetching market data..."):
                port_returns = portfolio_daily_returns(trades, summary["inception_date"])
                bench_tickers = [v for k, v in list(BENCHMARKS.items())[:3]]
                try:
                    comparison = build_comparison_table(port_returns, summary["inception_date"], bench_tickers)
                    st.dataframe(
                        comparison.style.background_gradient(subset=["Annualised %", "Sharpe Ratio"], cmap="RdYlGn"),
                        use_container_width=True,
                        hide_index=True,
                    )
                except Exception as e:
                    st.warning(f"Could not fetch live data: {e}. Add trades and ensure internet access.")
    else:
        st.info("Add trades in 'My Portfolio' to enable live benchmarking.")


# ─── THE PITCH ───────────────────────────────────────────────────────────────

elif page == "The Pitch":
    st.title("The Pitch")
    st.caption("Use this to structure your approach: sell the technology, land a job, or start a conversation.")

    summary = portfolio_summary()

    col1, col2 = st.columns(2)
    personal_return = col1.number_input("Your Portfolio Return (%)", value=summary.get("total_pct_return", 12.0), step=0.5)
    benchmark_return = col2.number_input("Mason Stevens Benchmark Return (%)", value=9.2, step=0.5)

    outperformance = personal_return - benchmark_return
    colour = "normal" if outperformance > 0 else "inverse"
    st.metric("Outperformance vs Mason Stevens Benchmark", f"{outperformance:+.2f}pp", delta_color=colour)

    st.divider()
    narrative = generate_pitch_narrative(personal_return, benchmark_return)
    st.markdown(narrative)

    st.divider()
    st.subheader("Priority Actions — What to Build Next")
    report = full_strategy_report(profile, personal_return, benchmark_return)
    for i, action in enumerate(report["top_3_priority_actions"], 1):
        st.info(f"**#{i}:** {action}")

    st.divider()
    st.subheader("Approach Options")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Option A: Sell the Tech")
        st.markdown("""
- Build 1-2 working prototypes from the strategy list
- Request a product demo with their CTO/CPO
- Price as SaaS overlay: $50K–$200K AUD setup + monthly per-adviser fee
- Reference: ATHENA deal = they buy fintech. You have a precedent.
        """)
    with col2:
        st.subheader("Option B: Get Hired")
        st.markdown("""
- Apply directly to investment or product roles
- Lead with quantified outperformance + the analytical toolset you built
- Target: Investment Analyst, Product Manager (Platform), Data/Quant roles
- New PE owner = growth hiring cycle = open positions likely
        """)
    with col3:
        st.subheader("Option C: Strategic Consulting")
        st.markdown("""
- Offer a 30-day strategy engagement: platform gap analysis + M&A target shortlist
- Entry fee: $10K–$20K AUD
- Outcome: credibility + recurring relationship
- Reference: the gap analysis in this tool as your deliverable sample
        """)

    st.divider()
    st.subheader("Contact Points at Mason Stevens")
    st.markdown("""
| Name | Role | Relevance |
|------|------|-----------|
| CEO | Platform leadership, PE strategy | Decision maker for tech acquisition / senior hire |
| CTO/CPO | Technology platform | Prototype demo |
| Peter Mermolas | Family Office / UHNW | Your family office dashboard pitch |
| Investment/Portfolio team | CIO function | Investment process + performance discussion |

*Note: LinkedIn search 'Mason Stevens' for current leadership. Post-Adamantem acquisition, new executives likely hired.*
    """)
