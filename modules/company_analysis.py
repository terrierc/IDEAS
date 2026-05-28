"""Company intelligence and SWOT analysis engine."""

import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).parent.parent / "data"


def load_company_profile(company_key: str = "mason_stevens") -> dict[str, Any]:
    path = DATA_DIR / f"{company_key}.json"
    with open(path) as f:
        return json.load(f)


def get_swot_summary(profile: dict) -> dict:
    swot = profile["swot"]
    return {
        category: sorted(items, key=lambda x: x["score"], reverse=True)
        for category, items in swot.items()
    }


def get_top_weaknesses(profile: dict, n: int = 5) -> list[dict]:
    return sorted(profile["swot"]["weaknesses"], key=lambda x: x["score"], reverse=True)[:n]


def get_top_opportunities(profile: dict, n: int = 5) -> list[dict]:
    return sorted(profile["swot"]["opportunities"], key=lambda x: x["score"], reverse=True)[:n]


def competitive_gap_analysis(profile: dict) -> list[dict]:
    """Returns how Mason Stevens compares vs each competitor on key metrics."""
    ms = next(
        c for c in profile["competitive_landscape"]["direct_competitors"]
        if c["name"] == "Mason Stevens"
    )
    peers = [
        c for c in profile["competitive_landscape"]["direct_competitors"]
        if c["name"] != "Mason Stevens"
    ]
    gaps = []
    for peer in peers:
        gaps.append({
            "competitor": peer["name"],
            "aum_gap_billions": round(peer["aum_billions"] - ms["aum_billions"], 1),
            "functionality_gap": round(peer["functionality_score"] - ms["functionality_score"], 1),
            "aum_ratio": round(peer["aum_billions"] / ms["aum_billions"], 1),
            "differentiator": peer["differentiator"],
        })
    return sorted(gaps, key=lambda x: x["aum_ratio"], reverse=True)


def business_model_canvas(profile: dict) -> dict:
    bm = profile["business_model"]
    company = profile["company"]
    return {
        "company": company["name"],
        "value_proposition": bm["value_proposition"],
        "customer_segments": [s["segment"] for s in bm["customer_segments"]],
        "key_resources": bm["key_resources"],
        "key_activities": bm["key_activities"],
        "revenue_streams": [
            f"{r['name']} ({r['type']}, importance: {r['importance']})"
            for r in bm["revenue_streams"]
        ],
        "cost_structure": bm["cost_structure"],
    }


def strategic_gaps(profile: dict) -> list[str]:
    return profile.get("strategic_gaps", [])
