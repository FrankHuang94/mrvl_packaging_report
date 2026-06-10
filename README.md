# Marvell Advanced Packaging Intelligence Database

An indexed, source-backed knowledge base and executive report on advanced semiconductor packaging for AI infrastructure, focused on Marvell's hyperscaler custom XPU opportunity.

**Baseline refresh:** 2026-06-10  
**Evidence cutoff:** Public information available through 2026-06-10  
**Primary question:** How will advanced packaging evolve from 2024 to 2030, and what does that mean for Marvell's ability to win hyperscaler custom XPU programs?

## Start here

- [Executive presentation dashboard](dashboard/index.html)
- [Dashboard user guide](dashboard/README.md)
- [Generated index](index.md)
- [Main report](reports/advanced_packaging_main_report.md)
- [Executive summary](reports/executive_summary_for_marvell_leadership.md)
- [Marvell XPU implications](reports/marvell_xpu_implications.md)
- [Corporate development watchlist](reports/corp_dev_and_partnership_watchlist.md)
- [Technology profiles](technologies/README.md)
- [Vendor profiles](vendors/README.md)
- [Mermaid visual catalog](assets/diagrams/mermaid_catalog.md)

## Repository operation

The `.yaml` databases use JSON syntax, which is valid YAML 1.2. This permits dependency-free parsing with Python's standard library.

### Use the executive dashboard

Build the latest dashboard data and start a local server:

```bash
python3 scripts/serve_dashboard.py
```

Open `http://localhost:8000/dashboard/`. Choose an audience preset, apply technology/vendor/year filters, select the briefing modules to show, and use **Present** or **Print / PDF** for an executive presentation. Sessions can be saved in the browser or exported as JSON. The dashboard has no third-party runtime dependencies.

### Refresh the entire database

Use the full refresh prompt below, follow [the full refresh workflow](scripts/refresh_full_database_template.md), preserve old sources, run validation, then rebuild the index.

### Refresh one section

Use the section prompt below and [the section workflow](scripts/refresh_section_template.md). Update the markdown profile, affected YAML records, figures, benchmarks and refresh log together.

### Add a technology profile

1. Add the normalized record to `data/technology_taxonomy.yaml`.
2. Create `technologies/<technology_id>.md` using existing metadata and decision-close conventions.
3. Add source IDs, figure IDs and table IDs.
4. Add roadmap entries and benchmarks where supported.
5. Run validation and rebuild the index.

### Add a vendor profile

1. Add the vendor record to `data/vendor_roadmaps.yaml`.
2. Create `vendors/<vendor_id>.md`.
3. Separate shipping evidence from announced or expected roadmap claims.
4. Score Marvell relevance, threat, partnership and acquisition relevance with written logic.
5. Validate and rebuild.

### Add a source

Add every required field to `data/source_database.yaml`; use a stable `SRC-<PUBLISHER>-<NNN>` ID. Capture extracted facts and caveats. Link the ID from every affected paragraph or database record.

### Add a figure

Prefer an author-created Mermaid or SVG schematic. Add the asset and a complete `data/figure_registry.yaml` record. For an external figure, record URL, access date and explicit license/usage basis. Do not store an external image when reuse rights are unclear.

### Validate the database

```bash
python3 scripts/validate_database.py
```

### Rebuild the index

```bash
python3 scripts/build_dashboard.py
python3 scripts/build_index.py
```

## Confidence and roadmap status

| Label | Interpretation |
|---|---|
| High | Primary standard, filing, shipping product or repeated product evidence |
| Medium-high | Strong primary disclosure with some configuration or qualification uncertainty |
| Medium | Credible announcement or multi-source inference with material execution gates |
| Low-medium | Directionally plausible late-roadmap expectation |
| Low | Speculative scenario; monitor only |

| Roadmap status | Meaning |
|---|---|
| Confirmed | Standardized, shipping or directly evidenced in production |
| Announced | Vendor has publicly committed or introduced it; qualification may be incomplete |
| Expected | Repository inference supported by technical and ecosystem evidence |
| Speculative | Long-range concept or insufficiently corroborated claim |

## Future Refresh Prompts

### A. Full database refresh prompt

> Refresh the entire advanced packaging database and report. Review every technology, vendor, roadmap, benchmark, source, figure, and Marvell strategy section. Search for new public information published after the last_refreshed date in each section. Add new sources to /data/source_database.yaml, update affected technology and vendor profiles, update roadmap tables, update figures and diagrams where needed, update /data/refresh_log.yaml, rerun validation, rebuild /index.md, and provide a summary of all changes. Clearly distinguish new confirmed facts, changed roadmap assumptions, contradicted prior claims, removed outdated information, and unresolved diligence questions. Preserve the existing repository structure and do not delete prior source history.

### B. Section-specific refresh prompt

> Refresh only the [SECTION NAME] section of the advanced packaging database. Use the section’s last_refreshed date as the starting point. Search for new sources published after that date. Update the relevant markdown file, YAML database entries, source database, benchmark database, figure registry, and refresh log. Rebuild the index and summarize what changed, what remains uncertain, and what Marvell should monitor next.

### C. Marvell-specific refresh prompt

> Refresh all Marvell-specific sections of the database, including custom XPU packaging, custom HBM architecture, CPO architecture, silicon photonics, die-to-die interconnect, SerDes, UALink, Ethernet, and hyperscaler XPU implications. Prioritize Marvell investor events, earnings calls, press releases, technical presentations, and credible hyperscaler/custom ASIC ecosystem sources. Update Marvell strategy recommendations, competitive positioning versus Broadcom/NVIDIA/AMD/Intel, and corporate development watchlist implications.

### D. HBM roadmap refresh prompt

> Refresh the HBM packaging roadmap, including HBM3E, HBM4, HBM4E, future HBM generations, custom HBM base die concepts, HBM stack count, HBM thermal constraints, HBM supply chain, and implications for AI XPUs. Update SK hynix, Samsung Memory, Micron, JEDEC, TSMC, Marvell, NVIDIA, AMD, and Broadcom-related entries where relevant.

### E. CPO and optical I/O refresh prompt

> Refresh the CPO and optical I/O sections, including CPO for switch ASICs, CPO for custom XPUs, silicon photonics, external laser sources, optical I/O chiplets, LPO, pluggable optics, optical scale-up networks, and Marvell’s silicon photonics/DSP/CPO strategy. Update OIF, Ethernet, hyperscaler, Marvell, Broadcom, NVIDIA, Coherent, Lumentum, Ayar Labs, Celestial AI, Lightmatter, Ranovus, and Intel silicon photonics references where relevant.

### F. Corporate development watchlist refresh prompt

> Refresh the corporate development and partnership watchlist. Identify new startups, private companies, public companies, IP vendors, OSATs, substrate suppliers, EDA vendors, silicon photonics companies, thermal vendors, and chiplet ecosystem players relevant to Marvell’s custom XPU and advanced packaging strategy. Add or update build/partner/acquire recommendations, but do not invent valuation, revenue, customer, or fundraising data unless sourced.

### G. Figure and visual refresh prompt

> Refresh the visual layer of the database. Review every Mermaid diagram, table, scorecard, roadmap, and figure. Add new visuals where sections are text-heavy. Update outdated diagrams based on new roadmap information. Verify that every external figure has a figure_registry.yaml entry with source, URL, date accessed, license/usage note, caption, and related source IDs. Prefer author-created schematics when external image reuse rights are unclear.

## Editorial rules

- Preserve prior source history; supersede rather than silently delete.
- Keep facts, management claims, estimates and rumors visibly separate.
- Do not promote an announced item to confirmed without qualification or shipping evidence.
- Record benchmark conditions and comparability caveats.
- Add a refresh-log entry for every material update.
