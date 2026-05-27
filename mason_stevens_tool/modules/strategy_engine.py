"""
Strategic recommendations engine.
Generates targeted strategies to exploit Mason Stevens' weaknesses,
leverage their strengths, and capitalise on market opportunities.
"""

from typing import Any


EXPLOIT_WEAKNESSES = [
    {
        "weakness": "No proprietary AI/ML analytics layer",
        "strategy": "Build and demonstrate an AI-powered portfolio analytics and attribution tool that Mason Stevens cannot currently offer clients or advisers. Show real-time factor analysis, drawdown forecasting, and natural-language portfolio Q&A.",
        "proof_point": "Deploy this tool. Track how it surfaces insights faster than manual adviser analysis.",
        "pitch": "Your platform charges HNW clients 65–110 bps but can't answer 'why did my portfolio underperform last month?' in natural language. This closes that gap.",
        "effort": "high",
        "impact": "very_high",
    },
    {
        "weakness": "No direct-to-client digital channel (100% adviser-dependent)",
        "strategy": "Demonstrate a self-directed HNW investment dashboard that bypasses the adviser layer for informed investors — or offer it as a white-label module Mason Stevens could bolt onto their platform.",
        "proof_point": "Operate your own portfolio through it profitably. Show the cost saving vs using a platform + adviser.",
        "pitch": "A $100B+ segment of Australian HNW investors would use self-directed if the platform offered institutional-grade tools. You're leaving this segment entirely to Stockspot and Vanguard Personal Investor.",
        "effort": "high",
        "impact": "high",
    },
    {
        "weakness": "Platform functionality score 84.3% (lowest of 5 major platforms)",
        "strategy": "Map exactly which features account for the gap vs Hub24/Netwealth. Build the top 3 missing modules as open, demonstrable prototypes. Use Investment Trends benchmarking criteria as a checklist.",
        "proof_point": "Publish a gap analysis with live demos. Offer to integrate as freelance product or consultant.",
        "pitch": "You're 8 percentage points behind the leader on functionality. Here's exactly which features cause that, and here's a working prototype of two of them.",
        "effort": "medium",
        "impact": "high",
    },
    {
        "weakness": "Nascent data analytics and reporting capability",
        "strategy": "Build a client-facing performance attribution and portfolio reporting module with visualisation quality matching private banking standards (think Blackrock Aladdin Wealth, simplified). Offer as SaaS overlay or acquisition target.",
        "proof_point": "Use it on your own portfolio. Generate a sample report that looks better than Mason Stevens' current output.",
        "pitch": "Your HNW clients expect Goldman Sachs-quality reporting. This is what they're actually getting — and this is what they could get.",
        "effort": "high",
        "impact": "very_high",
    },
    {
        "weakness": "Small AUM ($8.5B) — limited scale",
        "strategy": "Develop an AUM growth intelligence tool: identify which adviser practices are underserved, which are growing, which are likely to switch platforms. Offer this as a distribution intelligence product.",
        "proof_point": "Map the adviser landscape using ASIC register data (public). Identify 20 target practices. Present as a BD tool.",
        "pitch": "You're 6x smaller than Hub24. Here's exactly which adviser practices you should target next — and why they're likely to move.",
        "effort": "medium",
        "impact": "high",
    },
]

LEVERAGE_STRENGTHS = [
    {
        "strength": "Multi-asset, multi-currency breadth (rarest capability in Australian platforms)",
        "strategy": "Build a cross-asset portfolio optimiser that specifically showcases fixed income, FX, and alternatives allocation — the exact assets Mason Stevens can access but clients rarely get optimal exposure to.",
        "opportunity": "Position yourself as the person who maximises the platform's unique capability for adviser clients.",
        "pitch": "Most advisers on your platform are only using 30% of its capability — they're not touching direct fixed income or FX overlays. Here's a tool that changes that.",
    },
    {
        "strength": "Outsourced CIO capability",
        "strategy": "Build a shadow CIO decision log: model their published model portfolios, track their allocation shifts, publish analysis of their investment calls. Use this to demonstrate a superior investment process.",
        "opportunity": "Either challenge their CIO thinking with data, or demonstrate you can do the same analysis independently.",
        "pitch": "I've been shadowing and stress-testing your model portfolios for 12 months. Here's what I found — and here's where I outperformed.",
    },
    {
        "strength": "PE backing (Adamantem Capital) — M&A war chest",
        "strategy": "Identify acquisition targets Adamantem should buy: small fintech/wealthtech companies with complementary capabilities. Present a strategic M&A shortlist.",
        "opportunity": "Demonstrates strategic thinking at the level Adamantem capital is thinking at.",
        "pitch": "You have capital to deploy. Here are 5 acquisition targets that would close your technology gaps and accelerate AUM growth — with rough valuations.",
    },
    {
        "strength": "HNW specialist positioning",
        "strategy": "Build a HNW investor behavioural analytics tool: track how HNW portfolios actually perform vs their stated objectives, what mistakes they make, and how an adviser could intervene earlier.",
        "opportunity": "Unique insight into a segment Mason Stevens claims to specialise in.",
        "pitch": "You say you're HNW specialists — but you have no data on how your clients' portfolios actually behave vs their goals. This closes that gap.",
    },
]

CAPITALISE_OPPORTUNITIES = [
    {
        "opportunity": "AI-powered portfolio analytics — no Australian platform has differentiated here yet",
        "strategy": "Build the first AI portfolio assistant for Australian advisers: natural language querying of client portfolios, automatic rebalancing recommendations, risk factor explanations. Demo it on real data.",
        "timing": "First-mover window: 12–18 months before Hub24/Netwealth deploy something similar.",
        "pitch": "First Australian wealth platform to launch AI-native portfolio analytics wins the next wave of adviser adoption. Here's a working prototype.",
    },
    {
        "opportunity": "UHNW/Family Office expansion (Peter Mermolas hire signals intent)",
        "strategy": "Build a family office dashboard: consolidated reporting across multiple entities (trusts, companies, individuals, super), multi-currency, private market exposure tracking, tax optimisation overlays.",
        "timing": "Mason Stevens is hiring for this now. Get in front of them as the tech that powers it.",
        "pitch": "Your family office push needs family office-grade technology. Here's a prototype — and I built it in 3 months.",
    },
    {
        "opportunity": "Private markets/alternatives demand from HNW clients",
        "strategy": "Build an alternatives deal-flow and portfolio tracker: private equity, private credit, real estate — with valuation, J-curve tracking, IRR calculation, and integration into the overall portfolio view.",
        "timing": "Alternatives AUM growing 15%+ pa globally; no adviser platform in Australia has solved this cleanly.",
        "pitch": "Your clients want alternatives exposure. Here's what a proper private markets portfolio overlay looks like.",
    },
    {
        "opportunity": "ESG/impact overlay (Adamantem is impact-focused PE)",
        "strategy": "Build an ESG analytics and portfolio screening tool aligned to the PE owner's values. Automated ESG scoring, controversy monitoring, carbon footprint attribution, impact reporting.",
        "timing": "Adamantem's impact mandate means this is strategically aligned to the new owners.",
        "pitch": "Your PE owner is an impact investor. Your platform has no ESG capability. Here's how to close that gap quickly.",
    },
]


def get_exploit_plan() -> list[dict]:
    return sorted(EXPLOIT_WEAKNESSES, key=lambda x: {"very_high": 4, "high": 3, "medium": 2, "low": 1}.get(x["impact"], 0), reverse=True)


def get_leverage_plan() -> list[dict]:
    return LEVERAGE_STRENGTHS


def get_opportunity_plan() -> list[dict]:
    return CAPITALISE_OPPORTUNITIES


def generate_pitch_narrative(personal_return_pct: float, benchmark_return_pct: float) -> str:
    outperformance = round(personal_return_pct - benchmark_return_pct, 2)
    alpha_descriptor = "significantly" if outperformance > 5 else "consistently" if outperformance > 2 else "marginally"

    return f"""
## The Pitch: Why Mason Stevens Should Work With You

### The Performance Proof
Using a systematic, data-driven investment process built independently — without a platform,
without an adviser, and without paying {benchmark_return_pct}+ bps in fees — this portfolio
has returned **{personal_return_pct:.1f}%** vs the Mason Stevens benchmark of **{benchmark_return_pct:.1f}%**.

That's **{outperformance:+.1f} percentage points** of outperformance, {alpha_descriptor} exceeding
what clients receive after paying platform and management fees.

### What This Proves
1. **The investment process works** — independent of institutional infrastructure
2. **The analytical tools built to support it are the edge** — not the platform
3. **The fee drag is real and significant** — clients are paying for a capability gap

### What Mason Stevens Gets
- A proprietary AI-powered analytics layer (prototype ready)
- A direct-to-client digital channel strategy (reducing adviser dependency risk)
- A family office dashboard built for the UHNW push they've just started
- A private markets tracking module their advisers are asking for
- A strategist who has beaten their benchmark independently

### The Offer
Three options for Mason Stevens to capture this:
1. **Acquire the technology** — white-label the toolset as a platform feature upgrade
2. **Hire the builder** — bring the investment + technology capability in-house
3. **Strategic partnership** — integrate as a product overlay for adviser clients

The alternative is watching Hub24 or Netwealth build this first.
"""


def full_strategy_report(profile: dict, personal_return_pct: float = 0.0, benchmark_return_pct: float = 9.2) -> dict:
    return {
        "company": profile["company"]["name"],
        "generated": __import__("datetime").datetime.now().isoformat(),
        "exploit_weaknesses": get_exploit_plan(),
        "leverage_strengths": get_leverage_plan(),
        "capitalise_opportunities": get_opportunity_plan(),
        "pitch_narrative": generate_pitch_narrative(personal_return_pct, benchmark_return_pct),
        "top_3_priority_actions": [
            get_exploit_plan()[0]["strategy"],
            get_opportunity_plan()[0]["strategy"],
            get_leverage_plan()[0]["strategy"],
        ],
    }
