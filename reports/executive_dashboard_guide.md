# Executive Dashboard and Presentation Builder

> **Section metadata**
> - **Section title:** Executive Dashboard and Presentation Builder
> - **Owner placeholder:** Advanced Packaging Intelligence Owner
> - **Last refreshed date:** 2026-06-10
> - **Refresh status:** Current
> - **Source count:** Inherits all normalized repository sources
> - **Confidence level:** Dashboard reflects database confidence labels without changing them
> - **Key changes since last refresh:** Initial interactive dashboard implementation
> - **Open questions:** Leadership presentation templates and Marvell brand-system alignment
> - **Links to related sections:** [Dashboard](../dashboard/index.html), [Executive summary](executive_summary_for_marvell_leadership.md), [Generated index](../index.md)
> - **Figures included:** Interactive SVG charts
> - **Tables included:** Filtered technology, vendor, roadmap, benchmark, watchlist, and diligence tables
> - **Next suggested refresh date:** 2026-09-10

## Purpose

The dashboard converts the indexed research database into a configurable executive presentation. It does not create new factual claims. It filters, ranks, charts, and formats the normalized technology, vendor, roadmap, benchmark, source, and corporate-development records already stored in the repository.

## Presentation workflow

1. Run `python3 scripts/serve_dashboard.py`.
2. Open `http://localhost:8000/dashboard/`.
3. Choose a leadership, engineering, strategy, or corporate-development preset.
4. Apply technology category, vendor category, relevance, search, and roadmap-year filters.
5. Select the modules that should appear in the briefing.
6. Save the session or export its configuration as JSON.
7. Select **Present** for a distraction-free screen view.
8. Select **Print / PDF** for an executive handout.

## Available modules

| Module | Executive use |
|---|---|
| Executive scorecard | Headline counts for priority technologies, vendors, roadmap events, sources, and watchlist assets |
| Strategic takeaways | Build, partner, acquire/invest, monitor, differentiation, and risk messages |
| Technology priority matrix | Relevance versus partnership potential, with threat represented by bubble size |
| Vendor landscape | Competitive threat, relevance, portfolio, evidence confidence, and partnership potential |
| Roadmap | 2024-2030 stacked evidence-status chart and detailed roadmap table |
| Corporate-development watchlist | Capability concentration and target-level posture |
| Technical benchmarks | Conditioned quantitative metrics with source IDs and caveats |
| Leadership diligence | Presentation-ready questions and review triggers |

## Output discipline

- Scores are directional strategy assessments, not precise financial or engineering measurements.
- Roadmap status remains visibly separated into confirmed/qualified, announced/ramping, expected, and speculative.
- Tables link back to technology and vendor profiles where available.
- Charts use native SVG and remain sharp in PDF output.
- External chart libraries and network calls are not used.
- Saved sessions remain in browser local storage; exported JSON files can be shared or archived.

## Dashboard refresh

The data bundle must be rebuilt whenever a normalized database changes:

```bash
python3 scripts/build_dashboard.py
python3 scripts/validate_database.py
python3 scripts/build_index.py
```

Validation checks that the dashboard bundle contains the same technology, vendor, roadmap, and benchmark record counts as the source databases.
