#!/usr/bin/env python3
"""Validate normalized data, references, links, depth and visual coverage."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def load(path: str) -> dict:
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        ERRORS.append(f"{path}: cannot parse JSON-compatible YAML: {exc}")
        return {}


def require(record: dict, fields: list[str], context: str) -> None:
    for field in fields:
        if field not in record or record[field] in ("", None, []):
            ERRORS.append(f"{context}: missing required field `{field}`")


def words(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return len(re.findall(r"\b[\w'-]+\b", text))


def check_links() -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for target in pattern.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                WARNINGS.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                ERRORS.append(f"{path.relative_to(ROOT)}: broken link `{target}`")


def check_claim_citations() -> None:
    scoped = list((ROOT / "reports").glob("*.md")) + list((ROOT / "technologies").glob("*.md")) + list((ROOT / "vendors").glob("*.md"))
    for path in scoped:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for number, paragraph in enumerate(re.split(r"\n\s*\n", text), 1):
            if len(re.findall(r"\b[\w'-]+\b", paragraph)) < 55:
                continue
            if paragraph.startswith((">", "|", "```", "-", "#")) or re.match(r"^\d+\.", paragraph):
                continue
            if "SRC-" not in paragraph:
                WARNINGS.append(f"{path.relative_to(ROOT)} paragraph {number}: long analytical paragraph has no inline source ID")


def main() -> int:
    source_data = load("data/source_database.yaml")
    tech_data = load("data/technology_taxonomy.yaml")
    vendor_data = load("data/vendor_roadmaps.yaml")
    figure_data = load("data/figure_registry.yaml")
    benchmark_data = load("data/benchmark_database.yaml")

    sources = source_data.get("sources", [])
    technologies = tech_data.get("technologies", [])
    vendors = vendor_data.get("vendors", [])
    roadmaps = vendor_data.get("roadmap_items", [])
    figures = figure_data.get("figures", [])
    benchmarks = benchmark_data.get("benchmarks", [])

    dashboard_files = [
        "dashboard/index.html",
        "dashboard/styles.css",
        "dashboard/app.js",
        "dashboard/dashboard_data.js",
        "dashboard/README.md",
        "scripts/build_dashboard.py",
        "scripts/serve_dashboard.py",
    ]
    for relative in dashboard_files:
        if not (ROOT / relative).exists():
            ERRORS.append(f"dashboard: missing required file {relative}")

    dashboard_data_path = ROOT / "dashboard/dashboard_data.js"
    if dashboard_data_path.exists():
        prefix = "window.DASHBOARD_DATA = "
        raw = dashboard_data_path.read_text(encoding="utf-8")
        if not raw.startswith(prefix) or not raw.rstrip().endswith(";"):
            ERRORS.append("dashboard/dashboard_data.js: invalid data bundle wrapper")
        else:
            try:
                dashboard_data = json.loads(raw[len(prefix):].strip().removesuffix(";"))
                expected_counts = {
                    "technologies": len(technologies),
                    "vendors": len(vendors),
                    "roadmap_items": len(roadmaps),
                    "benchmarks": len(benchmarks),
                }
                for key, expected in expected_counts.items():
                    actual = len(dashboard_data.get(key, []))
                    if actual != expected:
                        ERRORS.append(f"dashboard data: {key} has {actual} records; expected {expected}")
            except json.JSONDecodeError as exc:
                ERRORS.append(f"dashboard/dashboard_data.js: invalid JSON payload: {exc}")
    dashboard_app_path = ROOT / "dashboard/app.js"
    if dashboard_app_path.exists():
        dashboard_app = dashboard_app_path.read_text(encoding="utf-8")
        for feature in ["saveSession", "exportSession", "exportCsv", "togglePresentation", "roadmapChart", "scatterChart"]:
            if feature not in dashboard_app:
                ERRORS.append(f"dashboard/app.js: missing required dashboard function `{feature}`")

    source_ids = {item.get("source_id") for item in sources}
    figure_ids = {item.get("figure_id") for item in figures}

    source_fields = ["source_id", "title", "publisher", "author", "date_published", "date_accessed", "url", "source_type", "credibility_tier", "relevant_technologies", "summary", "key_extracted_facts", "limitations_or_caveats"]
    tech_fields = ["technology_id", "name", "category", "description", "maturity_level", "key_vendors", "relevant_applications", "technical_metrics", "business_metrics", "roadmap", "advantages", "limitations", "bottlenecks", "Marvell_relevance_score", "competitive_threat_score", "partnership_potential_score", "acquisition_relevance_score", "source_ids", "figure_ids", "last_refreshed", "next_suggested_refresh", "confidence_level", "open_questions"]
    vendor_fields = ["vendor_id", "name", "category", "packaging_technologies", "roadmap_claims", "customers_public", "Marvell_relationship", "Marvell_relevance", "competitive_threat", "partnership_potential", "acquisition_relevance", "key_sources", "key_figures", "last_refreshed", "next_suggested_refresh", "confidence_level", "open_questions"]
    figure_fields = ["figure_id", "title", "figure_type", "source_type", "original_source", "local_path", "license_or_usage_note", "date_accessed", "related_technologies", "related_vendors", "caption", "source_ids", "caveats"]

    for item in sources:
        require(item, source_fields, f"source {item.get('source_id', '?')}")
    for item in technologies:
        require(item, tech_fields, f"technology {item.get('technology_id', '?')}")
        for source_id in item.get("source_ids", []):
            if source_id not in source_ids:
                ERRORS.append(f"technology {item.get('technology_id')}: missing source ID {source_id}")
        for figure_id in item.get("figure_ids", []):
            if figure_id not in figure_ids:
                ERRORS.append(f"technology {item.get('technology_id')}: missing figure ID {figure_id}")
        profile = ROOT / item.get("profile_path", "")
        if not profile.exists():
            ERRORS.append(f"technology {item.get('technology_id')}: missing profile {item.get('profile_path')}")
    for item in vendors:
        require(item, vendor_fields, f"vendor {item.get('vendor_id', '?')}")
        for source_id in item.get("key_sources", []):
            if source_id not in source_ids:
                ERRORS.append(f"vendor {item.get('vendor_id')}: missing source ID {source_id}")
        for figure_id in item.get("key_figures", []):
            if figure_id not in figure_ids:
                ERRORS.append(f"vendor {item.get('vendor_id')}: missing figure ID {figure_id}")
    for item in roadmaps:
        require(item, ["year", "technology", "vendor", "claimed_capability", "status", "evidence_source", "confidence_level", "Marvell_relevance", "key_risk"], f"roadmap {item.get('year', '?')} {item.get('technology', '?')}")
        if item.get("evidence_source") not in source_ids:
            ERRORS.append(f"roadmap {item.get('technology')}: missing evidence source {item.get('evidence_source')}")
    for item in figures:
        require(item, figure_fields, f"figure {item.get('figure_id', '?')}")
        if item.get("source_type") != "author-created schematic" and not item.get("URL"):
            ERRORS.append(f"figure {item.get('figure_id')}: external figure lacks URL")
        if not (ROOT / item.get("local_path", "")).exists():
            ERRORS.append(f"figure {item.get('figure_id')}: missing local path {item.get('local_path')}")
        for source_id in item.get("source_ids", []):
            if source_id not in source_ids:
                ERRORS.append(f"figure {item.get('figure_id')}: missing source ID {source_id}")
    for item in benchmarks:
        require(item, ["benchmark_id", "technology", "metric", "value", "unit", "condition", "source_id", "confidence_level", "comparable_to", "caveat"], f"benchmark {item.get('benchmark_id', '?')}")
        if item.get("source_id") not in source_ids:
            ERRORS.append(f"benchmark {item.get('benchmark_id')}: missing source ID {item.get('source_id')}")

    thresholds = {
        "reports/advanced_packaging_main_report.md": 30000,
        "reports/executive_summary_for_marvell_leadership.md": 2000,
        "reports/marvell_xpu_implications.md": 4000,
        "reports/corp_dev_and_partnership_watchlist.md": 3000,
    }
    for relative, minimum in thresholds.items():
        path = ROOT / relative
        if not path.exists():
            ERRORS.append(f"missing major report {relative}")
            continue
        count = words(path)
        if count < minimum:
            ERRORS.append(f"{relative}: {count} words; expected at least {minimum}")
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "```mermaid" not in text and "FIG-" not in text:
            ERRORS.append(f"{relative}: no visual")

    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
    prompt_names = [
        "Future Refresh Prompts",
        "Full database refresh prompt",
        "Section-specific refresh prompt",
        "Marvell-specific refresh prompt",
        "HBM roadmap refresh prompt",
        "CPO and optical I/O refresh prompt",
        "Corporate development watchlist refresh prompt",
        "Figure and visual refresh prompt",
    ]
    for name in prompt_names:
        if name not in readme:
            ERRORS.append(f"README.md: missing refresh prompt `{name}`")
    if "Executive presentation dashboard" not in readme or "scripts/build_dashboard.py" not in readme:
        ERRORS.append("README.md: missing dashboard navigation or build instructions")

    check_links()
    check_claim_citations()

    print(f"Validated {len(sources)} sources, {len(technologies)} technologies, {len(vendors)} vendors, {len(roadmaps)} roadmap items, {len(figures)} figures and {len(benchmarks)} benchmarks.")
    print(f"Errors: {len(ERRORS)}")
    for item in ERRORS:
        print(f"ERROR: {item}")
    print(f"Warnings: {len(WARNINGS)}")
    for item in WARNINGS[:50]:
        print(f"WARNING: {item}")
    if len(WARNINGS) > 50:
        print(f"WARNING: {len(WARNINGS) - 50} additional warnings suppressed")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
