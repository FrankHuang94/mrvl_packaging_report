# Executive Dashboard

The dashboard is a dependency-free presentation builder for the advanced-packaging database.

## Open it

Run:

```bash
python3 scripts/serve_dashboard.py
```

Then open `http://localhost:8000/dashboard/`.

The generated data bundle also allows `dashboard/index.html` to be opened directly from the filesystem.

## Functions

- Filter technologies, vendors, roadmap years and Marvell relevance.
- Choose executive, engineering, strategy or corporate-development presets.
- Select which modules appear in the briefing.
- Generate SVG portfolio, competitive-positioning and roadmap charts.
- Generate presentation-ready sortable tables.
- Save and reload dashboard sessions in browser storage.
- Export a session as JSON.
- Export the visible table as CSV.
- Enter distraction-free presentation mode.
- Print the selected briefing to PDF.

## Refresh

After changing any repository database, rebuild the dashboard bundle:

```bash
python3 scripts/build_dashboard.py
python3 scripts/validate_database.py
python3 scripts/build_index.py
```

No external JavaScript libraries, fonts or network services are required.
