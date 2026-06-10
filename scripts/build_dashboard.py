#!/usr/bin/env python3
"""Build the browser dashboard data bundle from repository databases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dashboard" / "dashboard_data.js"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    vendor_data = load("data/vendor_roadmaps.yaml")
    technologies = load("data/technology_taxonomy.yaml")["technologies"]
    payload = {
        "generated_at": max(item["last_refreshed"] for item in technologies),
        "technologies": technologies,
        "vendors": vendor_data["vendors"],
        "roadmap_items": vendor_data["roadmap_items"],
        "benchmarks": load("data/benchmark_database.yaml")["benchmarks"],
        "companies": load("data/company_database.yaml")["companies"],
        "sources": load("data/source_database.yaml")["sources"],
        "figures": load("data/figure_registry.yaml")["figures"],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "window.DASHBOARD_DATA = "
        + json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(
        "Built dashboard data with "
        f"{len(payload['technologies'])} technologies, "
        f"{len(payload['vendors'])} vendors, "
        f"{len(payload['roadmap_items'])} roadmap items and "
        f"{len(payload['companies'])} watchlist companies."
    )


if __name__ == "__main__":
    main()
