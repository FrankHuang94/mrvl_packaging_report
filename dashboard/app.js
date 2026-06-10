(function () {
  "use strict";

  const DATA = window.DASHBOARD_DATA || {
    technologies: [], vendors: [], roadmap_items: [], benchmarks: [],
    companies: [], sources: [], figures: [], generated_at: "unknown"
  };

  const MODULES = {
    kpis: ["Executive scorecard", "Headline portfolio and evidence metrics"],
    takeaways: ["Strategic takeaways", "Decision-oriented implications and risks"],
    technology: ["Technology priority matrix", "Relevance, threat and partnership positioning"],
    vendors: ["Vendor landscape", "Competitive threat and partnership options"],
    roadmap: ["2024-2030 roadmap", "Evidence status and timing by year"],
    watchlist: ["Corporate-development watchlist", "Build, partner, invest and monitor options"],
    benchmarks: ["Technical benchmarks", "Source-linked quantitative reference points"],
    diligence: ["Leadership diligence", "Questions and quarterly monitoring triggers"]
  };

  const PRESETS = {
    leadership: ["kpis", "takeaways", "technology", "vendors", "roadmap", "diligence"],
    engineering: ["kpis", "technology", "roadmap", "benchmarks", "diligence"],
    strategy: ["kpis", "takeaways", "technology", "vendors", "roadmap", "watchlist"],
    corpdev: ["kpis", "vendors", "watchlist", "diligence"]
  };

  const COLORS = ["#0077b6", "#0f8b8d", "#f2b134", "#d1495b", "#6f5aa8", "#27865f", "#e07a3f", "#23b5d3", "#5c6f82"];
  const DEFAULT_STATE = {
    view: "briefing",
    preset: "leadership",
    search: "",
    category: "all",
    vendorCategory: "all",
    relevance: 3,
    yearFrom: 2024,
    yearTo: 2030,
    modules: PRESETS.leadership.slice(),
    showCaveats: true,
    compactTables: false,
    darkCharts: false,
    sessionName: "Leadership Briefing",
    sort: { key: "", direction: "desc" }
  };

  let state = clone(DEFAULT_STATE);
  let currentRows = [];
  let currentColumns = [];
  let toastTimer = null;

  const el = (id) => document.getElementById(id);
  const content = el("dashboardContent");

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function titleCase(value) {
    return String(value || "").replace(/[-_]/g, " ").replace(/\b\w/g, (m) => m.toUpperCase());
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function numberScore(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function searchable(record) {
    return JSON.stringify(record).toLowerCase();
  }

  function matchesSearch(record) {
    return !state.search || searchable(record).includes(state.search.toLowerCase());
  }

  function categoryColor(category, categories) {
    const index = Math.max(0, categories.indexOf(category));
    return COLORS[index % COLORS.length];
  }

  function confidenceRank(value) {
    const normalized = String(value).toLowerCase();
    if (normalized === "high") return 5;
    if (normalized === "medium-high") return 4;
    if (normalized === "medium") return 3;
    if (normalized === "low-medium") return 2;
    return 1;
  }

  function statusClass(value) {
    const text = String(value).toLowerCase();
    if (text.includes("ship") || text.includes("qualified") || text.includes("confirmed")) return "confirmed";
    if (text.includes("announc") || text.includes("ramp")) return "announced";
    if (text.includes("expect")) return "expected";
    return "speculative";
  }

  function filteredTechnologies() {
    return DATA.technologies.filter((item) =>
      matchesSearch(item) &&
      (state.category === "all" || item.category === state.category) &&
      numberScore(item.Marvell_relevance_score) >= state.relevance
    );
  }

  function filteredVendors() {
    return DATA.vendors.filter((item) =>
      matchesSearch(item) &&
      (state.vendorCategory === "all" || item.category === state.vendorCategory) &&
      numberScore(item.Marvell_relevance) >= state.relevance
    );
  }

  function filteredRoadmap() {
    return DATA.roadmap_items.filter((item) =>
      Number(item.year) >= state.yearFrom &&
      Number(item.year) <= state.yearTo &&
      matchesSearch(item)
    );
  }

  function filteredCompanies() {
    return DATA.companies.filter(matchesSearch);
  }

  function link(path, label) {
    return `<a href="../${escapeHtml(path)}" target="_blank" rel="noopener">${escapeHtml(label)}</a>`;
  }

  function score(value, risk) {
    const numeric = numberScore(value);
    const cls = risk ? "risk" : numeric >= 4 ? "high" : "";
    return `<span class="score ${cls}">${numeric}/5</span>`;
  }

  function showToast(message) {
    const toast = el("toast");
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2200);
  }

  function moduleCard(id, title, subtitle, body, badge) {
    return `
      <section class="module-card" data-module="${escapeHtml(id)}">
        <div class="module-header">
          <div><h2>${escapeHtml(title)}</h2><p class="subhead">${escapeHtml(subtitle)}</p></div>
          ${badge ? `<span class="badge">${escapeHtml(badge)}</span>` : ""}
        </div>
        ${body}
      </section>`;
  }

  function evidenceNote(text) {
    if (!state.showCaveats) return "";
    return `<p class="source-note"><strong>Evidence note:</strong> ${escapeHtml(text)}</p>`;
  }

  function kpiHtml() {
    const techs = filteredTechnologies();
    const vendors = filteredVendors();
    const roadmap = filteredRoadmap();
    const highPriority = techs.filter((item) => numberScore(item.Marvell_relevance_score) >= 4).length;
    const highThreat = vendors.filter((item) => numberScore(item.competitive_threat) >= 4).length;
    const nearTerm = roadmap.filter((item) => Number(item.year) <= 2027).length;
    return `
      <div class="kpi-grid">
        <div class="kpi-card"><div class="label">Priority technologies</div><div class="value">${highPriority}</div><div class="detail">Relevance score 4-5</div></div>
        <div class="kpi-card"><div class="label">Visible vendors</div><div class="value">${vendors.length}</div><div class="detail">${highThreat} high-threat competitors</div></div>
        <div class="kpi-card"><div class="label">Roadmap events</div><div class="value">${roadmap.length}</div><div class="detail">${nearTerm} through 2027</div></div>
        <div class="kpi-card"><div class="label">Evidence sources</div><div class="value">${DATA.sources.length}</div><div class="detail">Source-backed repository records</div></div>
        <div class="kpi-card"><div class="label">Corp-dev assets</div><div class="value">${filteredCompanies().length}</div><div class="detail">Capability-led watchlist</div></div>
      </div>`;
  }

  function executiveTakeaways() {
    const techs = filteredTechnologies().slice().sort((a, b) =>
      numberScore(b.Marvell_relevance_score) - numberScore(a.Marvell_relevance_score) ||
      numberScore(b.competitive_threat_score) - numberScore(a.competitive_threat_score)
    );
    const vendors = filteredVendors().slice().sort((a, b) =>
      numberScore(b.competitive_threat) - numberScore(a.competitive_threat)
    );
    const topTech = techs[0];
    const topPartner = techs.slice().sort((a, b) => numberScore(b.partnership_potential_score) - numberScore(a.partnership_potential_score))[0];
    const topThreat = vendors[0];
    return `
      <div class="chart-grid">
        <div class="insight-list">
          <div class="insight action"><strong>Decision thesis</strong><span>Packaging differentiates when Marvell converts architecture, capacity, test and thermal data into a more credible customer PPA, schedule and supply commitment.</span></div>
          <div class="insight"><strong>Highest visible technology priority</strong><span>${topTech ? escapeHtml(topTech.name) + ": " + escapeHtml(topTech.description) : "No technology matches the active filters."}</span></div>
          <div class="insight"><strong>Strongest partnership signal</strong><span>${topPartner ? escapeHtml(topPartner.name) + " scores " + topPartner.partnership_potential_score + "/5 for partnership potential." : "No partnership candidate matches."}</span></div>
          <div class="insight risk"><strong>Competitive watch</strong><span>${topThreat ? escapeHtml(topThreat.name) + " is the highest-threat visible vendor at " + topThreat.competitive_threat + "/5." : "No vendor matches the active filters."}</span></div>
        </div>
        <div class="insight-list">
          <div class="insight"><strong>Build</strong><span>Reusable package reference architectures, custom HBM controls, D2D interfaces, package telemetry and customer trade-space tools.</span></div>
          <div class="insight"><strong>Partner</strong><span>Foundry packaging, HBM supply, OSAT/test, optical attach, lasers, thermal structures and EDA signoff.</span></div>
          <div class="insight action"><strong>Acquire or invest</strong><span>Scarce optical, test analytics, thermal or design-automation capabilities only when control changes XPU win probability.</span></div>
          <div class="insight risk"><strong>Monitor</strong><span>Glass substrates, panel-level high-end packaging, post-HBM memory and broad XPU optical I/O until qualification evidence improves.</span></div>
        </div>
      </div>
      ${evidenceNote("Recommendations are repository synthesis. Vendor announcements remain distinct from customer-qualified production evidence.")}`;
  }

  function scatterChart(items, config) {
    if (!items.length) return `<div class="empty-state">No records match the active filters.</div>`;
    const width = 760, height = 390;
    const margin = { left: 58, right: 25, top: 30, bottom: 55 };
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const categories = Array.from(new Set(items.map((item) => item[config.category]))).sort();
    const x = (scoreValue) => margin.left + ((numberScore(scoreValue) - 1) / 4) * plotW;
    const y = (scoreValue) => margin.top + plotH - ((numberScore(scoreValue) - 1) / 4) * plotH;
    const bubbles = items.map((item) => {
      const label = item.name;
      const cx = x(item[config.x]);
      const cy = y(item[config.y]);
      const radius = 7 + numberScore(item[config.size]) * 2.3;
      const fill = categoryColor(item[config.category], categories);
      return `<g><circle class="bubble" cx="${cx}" cy="${cy}" r="${radius}" fill="${fill}"><title>${escapeHtml(label)} | ${escapeHtml(config.xLabel)} ${item[config.x]}/5 | ${escapeHtml(config.yLabel)} ${item[config.y]}/5</title></circle><text class="chart-label" x="${cx + radius + 3}" y="${cy + 4}">${escapeHtml(label.length > 22 ? label.slice(0, 20) + "..." : label)}</text></g>`;
    }).join("");
    const grid = [1, 2, 3, 4, 5].map((tick) => {
      const gx = x(tick), gy = y(tick);
      return `<line class="grid-line" x1="${gx}" y1="${margin.top}" x2="${gx}" y2="${margin.top + plotH}"/><line class="grid-line" x1="${margin.left}" y1="${gy}" x2="${margin.left + plotW}" y2="${gy}"/><text class="chart-label" x="${gx}" y="${height - 31}" text-anchor="middle">${tick}</text><text class="chart-label" x="${margin.left - 13}" y="${gy + 4}" text-anchor="end">${tick}</text>`;
    }).join("");
    const legend = categories.map((cat) => `<span class="legend-item"><span class="legend-swatch" style="background:${categoryColor(cat, categories)}"></span>${escapeHtml(cat)}</span>`).join("");
    return `
      <div class="chart-frame">
        <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(config.title)}">
          <text class="chart-title" x="${width / 2}" y="18" text-anchor="middle">${escapeHtml(config.title)}</text>
          ${grid}
          <line class="axis-line" x1="${margin.left}" y1="${margin.top + plotH}" x2="${margin.left + plotW}" y2="${margin.top + plotH}"/>
          <line class="axis-line" x1="${margin.left}" y1="${margin.top}" x2="${margin.left}" y2="${margin.top + plotH}"/>
          <text class="chart-label" x="${margin.left + plotW / 2}" y="${height - 7}" text-anchor="middle">${escapeHtml(config.xLabel)} (1-5)</text>
          <text class="chart-label" transform="translate(15 ${margin.top + plotH / 2}) rotate(-90)" text-anchor="middle">${escapeHtml(config.yLabel)} (1-5)</text>
          ${bubbles}
        </svg>
      </div>
      <div class="legend">${legend}</div>`;
  }

  function technologyModule() {
    const rows = filteredTechnologies().slice().sort((a, b) =>
      numberScore(b.Marvell_relevance_score) - numberScore(a.Marvell_relevance_score) ||
      numberScore(b.competitive_threat_score) - numberScore(a.competitive_threat_score)
    );
    const chart = scatterChart(rows, {
      title: "Technology Priority Map",
      x: "partnership_potential_score", xLabel: "Partnership potential",
      y: "Marvell_relevance_score", yLabel: "Marvell relevance",
      size: "competitive_threat_score", category: "category"
    });
    const tableRows = rows.map((item) => ({
      technology: item.name,
      category: item.category,
      maturity: item.maturity_level,
      relevance: item.Marvell_relevance_score,
      threat: item.competitive_threat_score,
      partnership: item.partnership_potential_score,
      bottleneck: (item.bottlenecks || []).join("; "),
      path: item.profile_path
    }));
    return `<div class="chart-grid"><div>${chart}</div><div>${priorityBars(rows.slice(0, 8), "Marvell_relevance_score", "Top technology priorities")}</div></div>
      ${renderTable(tableRows, [
        ["technology", "Technology"], ["category", "Category"], ["maturity", "Maturity"],
        ["relevance", "Relevance"], ["threat", "Threat"], ["partnership", "Partner"],
        ["bottleneck", "Principal bottlenecks"]
      ], "technology")}
      ${evidenceNote("Scores are directional strategy assessments. Bubble size represents competitive threat; position represents relevance and partnership potential.")}`;
  }

  function vendorModule() {
    const rows = filteredVendors().slice().sort((a, b) =>
      numberScore(b.Marvell_relevance) - numberScore(a.Marvell_relevance) ||
      numberScore(b.competitive_threat) - numberScore(a.competitive_threat)
    );
    const chart = scatterChart(rows, {
      title: "Vendor Competitive and Partnership Landscape",
      x: "partnership_potential", xLabel: "Partnership potential",
      y: "Marvell_relevance", yLabel: "Marvell relevance",
      size: "competitive_threat", category: "category"
    });
    const tableRows = rows.map((item) => ({
      vendor: item.name,
      category: item.category,
      portfolio: (item.packaging_technologies || []).join(", "),
      relevance: item.Marvell_relevance,
      threat: item.competitive_threat,
      partnership: item.partnership_potential,
      confidence: item.confidence_level,
      path: item.profile_path
    }));
    return `<div class="chart-grid"><div>${chart}</div><div>${priorityBars(rows.slice().sort((a,b) => b.competitive_threat-a.competitive_threat).slice(0,8), "competitive_threat", "Highest competitive threat")}</div></div>
      ${renderTable(tableRows, [
        ["vendor", "Vendor"], ["category", "Category"], ["portfolio", "Portfolio"],
        ["relevance", "Relevance"], ["threat", "Threat"], ["partnership", "Partner"], ["confidence", "Confidence"]
      ], "vendor")}
      ${evidenceNote("Vendor scores assess strategic position, not company quality or valuation. Public customer and production disclosures vary materially.")}`;
  }

  function priorityBars(items, field, title) {
    if (!items.length) return `<div class="empty-state">No ranked records.</div>`;
    const bars = items.map((item) => {
      const value = numberScore(item[field]);
      return `<div style="margin:10px 0"><div style="display:flex;justify-content:space-between;gap:10px;font-size:.72rem;font-weight:750"><span>${escapeHtml(item.name)}</span><span>${value}/5</span></div><div style="height:8px;margin-top:4px;background:#e7edf2;border-radius:99px;overflow:hidden"><div style="width:${value*20}%;height:100%;background:${value>=4?'#0f8b8d':'#0077b6'}"></div></div></div>`;
    }).join("");
    return `<div class="chart-frame"><h3>${escapeHtml(title)}</h3>${bars}</div>`;
  }

  function roadmapChart(items) {
    if (!items.length) return `<div class="empty-state">No roadmap events match the active filters.</div>`;
    const years = Array.from(new Set(items.map((item) => Number(item.year)))).sort();
    const classes = ["confirmed", "announced", "expected", "speculative"];
    const color = { confirmed: "#27865f", announced: "#0077b6", expected: "#f2b134", speculative: "#d1495b" };
    const counts = {};
    years.forEach((year) => {
      counts[year] = { confirmed: 0, announced: 0, expected: 0, speculative: 0 };
      items.filter((item) => Number(item.year) === year).forEach((item) => counts[year][statusClass(item.status)]++);
    });
    const max = Math.max(...years.map((year) => classes.reduce((sum, cls) => sum + counts[year][cls], 0)), 1);
    const width = 760, height = 350, left = 55, bottom = 45, top = 25, plotH = 265, plotW = 675;
    const groupW = plotW / years.length;
    const bars = years.map((year, index) => {
      let currentY = top + plotH;
      const stack = classes.map((cls) => {
        const h = counts[year][cls] / max * plotH;
        currentY -= h;
        return `<rect x="${left + index * groupW + groupW * .18}" y="${currentY}" width="${groupW * .64}" height="${h}" fill="${color[cls]}"><title>${year} ${cls}: ${counts[year][cls]}</title></rect>`;
      }).join("");
      return `${stack}<text class="chart-label" x="${left + index * groupW + groupW / 2}" y="${height - 17}" text-anchor="middle">${year}</text>`;
    }).join("");
    const grid = [0, .25, .5, .75, 1].map((part) => {
      const y = top + plotH - part * plotH;
      return `<line class="grid-line" x1="${left}" y1="${y}" x2="${left + plotW}" y2="${y}"/><text class="chart-label" x="${left - 9}" y="${y + 4}" text-anchor="end">${Math.round(part * max)}</text>`;
    }).join("");
    const legend = classes.map((cls) => `<span class="legend-item"><span class="legend-swatch" style="background:${color[cls]}"></span>${titleCase(cls)}</span>`).join("");
    return `<div class="chart-frame"><svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Roadmap evidence status by year"><text class="chart-title" x="${width/2}" y="16" text-anchor="middle">Roadmap Evidence Status by Year</text>${grid}${bars}</svg></div><div class="legend">${legend}</div>`;
  }

  function roadmapModule() {
    const rows = filteredRoadmap().slice().sort((a, b) => Number(a.year) - Number(b.year) || a.technology.localeCompare(b.technology));
    const tableRows = rows.map((item) => ({
      year: item.year,
      technology: item.technology,
      vendor: item.vendor,
      capability: item.claimed_capability,
      status: item.status,
      confidence: item.confidence_level,
      relevance: item.Marvell_relevance,
      risk: item.key_risk
    }));
    return `<div class="chart-grid"><div>${roadmapChart(rows)}</div><div class="insight-list">
      <div class="insight"><strong>Near term</strong><span>Use shipping, qualification and contracted-capacity evidence for customer commitments.</span></div>
      <div class="insight action"><strong>Mid term</strong><span>Track announced package scale, HBM4 base-die models, UCIe interoperability and CPO field evidence.</span></div>
      <div class="insight risk"><strong>Late decade</strong><span>Keep glass, broad optical I/O and post-HBM scenarios outside committed plans until qualification improves.</span></div>
      </div></div>
      ${renderTable(tableRows, [
        ["year", "Year"], ["technology", "Technology"], ["vendor", "Vendor"],
        ["capability", "Capability"], ["status", "Status"], ["confidence", "Confidence"],
        ["relevance", "Marvell relevance"], ["risk", "Key risk"]
      ], "roadmap")}
      ${evidenceNote("Roadmap status is normalized from heterogeneous sources. Expected and speculative records are scenarios, not supplier commitments.")}`;
  }

  function watchlistModule() {
    const rows = filteredCompanies().slice().sort((a, b) =>
      String(a.category).localeCompare(String(b.category)) || String(a.name).localeCompare(String(b.name))
    );
    const categoryCounts = {};
    rows.forEach((item) => { categoryCounts[item.category] = (categoryCounts[item.category] || 0) + 1; });
    const categoryItems = Object.entries(categoryCounts).sort((a,b) => b[1]-a[1]).map(([name, count]) => ({ name, value: count }));
    const tableRows = rows.map((item) => ({
      company: item.name,
      category: item.category,
      technology: item.technology,
      recommendation: item.build_partner_acquire,
      maturity: item.estimated_maturity,
      fit: item.fit_with_Marvell,
      tension: item.competitive_tension,
      valuation: item.valuation
    }));
    return `<div class="chart-grid"><div>${horizontalCountChart(categoryItems, "Watchlist concentration by capability")}</div><div class="insight-list">
      <div class="insight"><strong>Primary screen</strong><span>Does privileged access or ownership materially improve custom XPU win rate, qualification time or supply assurance?</span></div>
      <div class="insight action"><strong>Preferred sequence</strong><span>Partner first when manufacturing scale dominates; invest or acquire when interface IP, data or a scarce team requires control.</span></div>
      <div class="insight risk"><strong>Do not infer</strong><span>Availability, valuation, revenue, customer concentration or transaction willingness remain unavailable unless sourced.</span></div>
      </div></div>
      ${renderTable(tableRows, [
        ["company", "Company"], ["category", "Category"], ["technology", "Technology"],
        ["recommendation", "Posture"], ["maturity", "Maturity"], ["fit", "Marvell fit"],
        ["tension", "Competitive tension"], ["valuation", "Valuation"]
      ], "watchlist")}
      ${evidenceNote("The watchlist is capability-led and does not imply transaction availability or a recommendation to transact without full diligence.")}`;
  }

  function horizontalCountChart(items, title) {
    if (!items.length) return `<div class="empty-state">No records match.</div>`;
    const max = Math.max(...items.map((item) => item.value), 1);
    return `<div class="chart-frame"><h3>${escapeHtml(title)}</h3>${items.map((item, index) =>
      `<div style="margin:11px 0"><div style="display:flex;justify-content:space-between;gap:12px;font-size:.72rem;font-weight:750"><span>${escapeHtml(item.name)}</span><span>${item.value}</span></div><div style="height:10px;margin-top:5px;background:#e8edf2;border-radius:99px;overflow:hidden"><div style="width:${item.value/max*100}%;height:100%;background:${COLORS[index%COLORS.length]}"></div></div></div>`
    ).join("")}</div>`;
  }

  function benchmarkModule() {
    const rows = DATA.benchmarks.filter(matchesSearch).map((item) => ({
      technology: item.technology,
      metric: item.metric,
      value: `${item.value} ${item.unit}`,
      condition: item.condition,
      confidence: item.confidence_level,
      source: item.source_id,
      caveat: item.caveat
    }));
    return `${renderTable(rows, [
      ["technology", "Technology"], ["metric", "Metric"], ["value", "Value"],
      ["condition", "Condition"], ["confidence", "Confidence"], ["source", "Source ID"],
      ["caveat", "Comparability caveat"]
    ], "benchmarks")}
    ${evidenceNote("Quantitative values are shown only with their measurement or specification condition. Cross-technology comparisons require engineering normalization.")}`;
  }

  function diligenceModule() {
    const questions = [
      ["Architecture", "Which package configuration is fully characterized at the customer's target HBM count, power map and coolant condition?"],
      ["Supply", "What capacity is contracted for the exact interposer, substrate, assembly and test configuration?"],
      ["Yield", "Which defects can be detected before expensive logic and HBM are irreversibly combined?"],
      ["HBM", "Who controls custom base-die IP, verification, failure analysis and memory-vendor qualification?"],
      ["CPO", "What field replacement, laser redundancy, fiber attach and optical test model is proven?"],
      ["Alternatives", "Which claimed second source survives design-rule, performance, test and reliability comparison?"],
      ["Competition", "Where do Broadcom or NVIDIA have a scale, capacity or proprietary-fabric advantage?"],
      ["Corp Dev", "Which target changes XPU win probability rather than merely adding AI market exposure?"],
      ["Timing", "What roadmap trigger would force a package architecture decision before the next quarterly review?"],
      ["Governance", "Which statement is confirmed, announced, expected or speculative, and who owns promotion of its status?"]
    ];
    const rows = questions.map((item, index) => ({ priority: index + 1, domain: item[0], question: item[1], owner: "Assign", trigger: "Quarterly or event-driven" }));
    return `${renderTable(rows, [
      ["priority", "#"], ["domain", "Domain"], ["question", "Leadership question"],
      ["owner", "Owner"], ["trigger", "Review trigger"]
    ], "diligence")}
    <div class="insight-list" style="margin-top:14px">
      <div class="insight action"><strong>Quarterly monitoring package</strong><span>HBM samples and qualification, foundry package rules, substrate lead times, capacity allocation, yield learning, CPO field evidence, customer fabric choices and competitor socket wins.</span></div>
    </div>`;
  }

  function renderTable(rows, columns, tableName) {
    currentRows = rows;
    currentColumns = columns;
    if (!rows.length) return `<div class="empty-state">No table rows match the active filters.</div>`;
    const sorted = sortRows(rows);
    const head = columns.map(([key, label]) => `<th data-sort="${escapeHtml(key)}" title="Sort by ${escapeHtml(label)}">${escapeHtml(label)}</th>`).join("");
    const body = sorted.map((row) => `<tr>${columns.map(([key]) => {
      let value = row[key];
      if (key === "technology" && row.path) value = link(row.path, value);
      else if (key === "vendor" && row.path) value = link(row.path, value);
      else if (["relevance", "partnership"].includes(key) && Number.isFinite(Number(value))) value = score(value, false);
      else if (key === "threat" && Number.isFinite(Number(value))) value = score(value, true);
      else if (key === "status") value = `<span class="status ${statusClass(value)}">${escapeHtml(value)}</span>`;
      else value = escapeHtml(Array.isArray(value) ? value.join(", ") : value);
      return `<td>${value}</td>`;
    }).join("")}</tr>`).join("");
    return `<div class="table-wrap ${state.compactTables ? "compact" : ""}" data-table="${escapeHtml(tableName)}"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
  }

  function sortRows(rows) {
    if (!state.sort.key) return rows;
    const direction = state.sort.direction === "asc" ? 1 : -1;
    return rows.slice().sort((a, b) => {
      const av = a[state.sort.key], bv = b[state.sort.key];
      if (Number.isFinite(Number(av)) && Number.isFinite(Number(bv))) return (Number(av) - Number(bv)) * direction;
      return String(av || "").localeCompare(String(bv || "")) * direction;
    });
  }

  function briefingHeader() {
    const visible = state.modules.map((id) => MODULES[id] && MODULES[id][0]).filter(Boolean);
    return `<section class="briefing-header">
      <div class="eyebrow">${escapeHtml(titleCase(state.preset))} session | ${escapeHtml(DATA.generated_at)}</div>
      <h2>${escapeHtml(state.sessionName)}</h2>
      <p>Selected presentation: ${escapeHtml(visible.join(" | "))}. Filters show relevance ${state.relevance}/5 or higher, roadmap years ${state.yearFrom}-${state.yearTo}${state.search ? `, search "${escapeHtml(state.search)}"` : ""}.</p>
    </section>`;
  }

  function renderBriefing() {
    const renderers = {
      kpis: () => kpiHtml(),
      takeaways: () => moduleCard("takeaways", MODULES.takeaways[0], MODULES.takeaways[1], executiveTakeaways(), "Decision view"),
      technology: () => moduleCard("technology", MODULES.technology[0], MODULES.technology[1], technologyModule(), `${filteredTechnologies().length} records`),
      vendors: () => moduleCard("vendors", MODULES.vendors[0], MODULES.vendors[1], vendorModule(), `${filteredVendors().length} records`),
      roadmap: () => moduleCard("roadmap", MODULES.roadmap[0], MODULES.roadmap[1], roadmapModule(), `${state.yearFrom}-${state.yearTo}`),
      watchlist: () => moduleCard("watchlist", MODULES.watchlist[0], MODULES.watchlist[1], watchlistModule(), `${filteredCompanies().length} assets`),
      benchmarks: () => moduleCard("benchmarks", MODULES.benchmarks[0], MODULES.benchmarks[1], benchmarkModule(), `${DATA.benchmarks.length} benchmarks`),
      diligence: () => moduleCard("diligence", MODULES.diligence[0], MODULES.diligence[1], diligenceModule(), "Action required")
    };
    return briefingHeader() + state.modules.map((id) => renderers[id] ? renderers[id]() : "").join("");
  }

  function renderView() {
    document.body.classList.toggle("dark-charts", state.darkCharts);
    let html = "";
    if (state.view === "briefing") html = renderBriefing();
    if (state.view === "technology") html = briefingHeader() + kpiHtml() + moduleCard("technology", "Technology portfolio", "Filter, rank and compare package technologies", technologyModule(), `${filteredTechnologies().length} visible`);
    if (state.view === "vendors") html = briefingHeader() + kpiHtml() + moduleCard("vendors", "Vendor landscape", "Compare relevance, threat and partnership potential", vendorModule(), `${filteredVendors().length} visible`);
    if (state.view === "roadmap") html = briefingHeader() + kpiHtml() + moduleCard("roadmap", "Roadmap intelligence", "Separate shipping, announced, expected and speculative events", roadmapModule(), `${filteredRoadmap().length} events`);
    if (state.view === "watchlist") html = briefingHeader() + kpiHtml() + moduleCard("watchlist", "Corporate development", "Capability-led build, partner, invest and monitor screen", watchlistModule(), `${filteredCompanies().length} assets`);
    content.innerHTML = html || `<div class="empty-state">Choose a dashboard view.</div>`;
    attachTableSorting();
    syncControls();
  }

  function attachTableSorting() {
    content.querySelectorAll("th[data-sort]").forEach((header) => {
      header.addEventListener("click", () => {
        const key = header.dataset.sort;
        if (state.sort.key === key) state.sort.direction = state.sort.direction === "asc" ? "desc" : "asc";
        else state.sort = { key, direction: "asc" };
        renderView();
      });
    });
  }

  function initializeControls() {
    const categories = Array.from(new Set(DATA.technologies.map((item) => item.category))).sort();
    const vendorCategories = Array.from(new Set(DATA.vendors.map((item) => item.category))).sort();
    el("categoryFilter").innerHTML += categories.map((item) => `<option value="${escapeHtml(item)}">${escapeHtml(item)}</option>`).join("");
    el("vendorCategoryFilter").innerHTML += vendorCategories.map((item) => `<option value="${escapeHtml(item)}">${escapeHtml(item)}</option>`).join("");
    const years = Array.from(new Set(DATA.roadmap_items.map((item) => Number(item.year)))).sort();
    el("yearFrom").innerHTML = years.map((year) => `<option value="${year}">${year}</option>`).join("");
    el("yearTo").innerHTML = years.map((year) => `<option value="${year}">${year}</option>`).join("");
    el("moduleSelector").innerHTML = Object.entries(MODULES).map(([id, values]) =>
      `<label class="module-item"><input type="checkbox" value="${id}"><span><strong>${escapeHtml(values[0])}</strong><small>${escapeHtml(values[1])}</small></span></label>`
    ).join("");

    el("searchFilter").addEventListener("input", (event) => { state.search = event.target.value; renderView(); });
    el("categoryFilter").addEventListener("change", (event) => { state.category = event.target.value; renderView(); });
    el("vendorCategoryFilter").addEventListener("change", (event) => { state.vendorCategory = event.target.value; renderView(); });
    el("relevanceFilter").addEventListener("input", (event) => { state.relevance = Number(event.target.value); renderView(); });
    el("yearFrom").addEventListener("change", (event) => { state.yearFrom = Number(event.target.value); if (state.yearFrom > state.yearTo) state.yearTo = state.yearFrom; renderView(); });
    el("yearTo").addEventListener("change", (event) => { state.yearTo = Number(event.target.value); if (state.yearTo < state.yearFrom) state.yearFrom = state.yearTo; renderView(); });
    el("showCaveats").addEventListener("change", (event) => { state.showCaveats = event.target.checked; renderView(); });
    el("compactTables").addEventListener("change", (event) => { state.compactTables = event.target.checked; renderView(); });
    el("darkCharts").addEventListener("change", (event) => { state.darkCharts = event.target.checked; renderView(); });
    el("sessionName").addEventListener("input", (event) => { state.sessionName = event.target.value || "Executive Briefing"; renderView(); });

    el("moduleSelector").addEventListener("change", () => {
      state.modules = Array.from(el("moduleSelector").querySelectorAll("input:checked")).map((input) => input.value);
      state.preset = "custom";
      renderView();
    });
    document.querySelectorAll(".preset").forEach((button) => button.addEventListener("click", () => applyPreset(button.dataset.preset)));
    document.querySelectorAll(".view-tab").forEach((button) => button.addEventListener("click", () => { state.view = button.dataset.view; state.sort = {key:"",direction:"desc"}; renderView(); }));

    el("resetDashboard").addEventListener("click", () => { state = clone(DEFAULT_STATE); renderView(); showToast("Dashboard reset"); });
    el("selectAllModules").addEventListener("click", () => { state.modules = Object.keys(MODULES); state.preset = "custom"; renderView(); });
    el("saveSession").addEventListener("click", saveSession);
    el("loadSession").addEventListener("click", loadSession);
    el("exportSession").addEventListener("click", exportSession);
    el("exportCsv").addEventListener("click", exportCsv);
    el("copySummary").addEventListener("click", copySummary);
    el("printBriefing").addEventListener("click", () => window.print());
    el("presentationMode").addEventListener("click", togglePresentation);
  }

  function syncControls() {
    el("searchFilter").value = state.search;
    el("categoryFilter").value = state.category;
    el("vendorCategoryFilter").value = state.vendorCategory;
    el("relevanceFilter").value = state.relevance;
    el("relevanceValue").textContent = state.relevance;
    el("yearFrom").value = state.yearFrom;
    el("yearTo").value = state.yearTo;
    el("showCaveats").checked = state.showCaveats;
    el("compactTables").checked = state.compactTables;
    el("darkCharts").checked = state.darkCharts;
    if (document.activeElement !== el("sessionName")) el("sessionName").value = state.sessionName;
    document.querySelectorAll(".preset").forEach((button) => button.classList.toggle("active", button.dataset.preset === state.preset));
    document.querySelectorAll(".view-tab").forEach((button) => button.classList.toggle("active", button.dataset.view === state.view));
    el("moduleSelector").querySelectorAll("input").forEach((input) => { input.checked = state.modules.includes(input.value); });
  }

  function applyPreset(name) {
    state.preset = name;
    state.modules = (PRESETS[name] || PRESETS.leadership).slice();
    state.view = "briefing";
    if (name === "engineering") state.relevance = 2;
    else state.relevance = 3;
    renderView();
    showToast(`${titleCase(name)} preset applied`);
  }

  function sessions() {
    try { return JSON.parse(localStorage.getItem("mrvl-dashboard-sessions") || "{}"); }
    catch (_) { return {}; }
  }

  function saveSession() {
    const store = sessions();
    store[state.sessionName] = { ...clone(state), savedAt: new Date().toISOString() };
    localStorage.setItem("mrvl-dashboard-sessions", JSON.stringify(store));
    showToast(`Saved "${state.sessionName}"`);
  }

  function loadSession() {
    const store = sessions();
    const names = Object.keys(store);
    if (!names.length) { showToast("No saved sessions"); return; }
    const requested = window.prompt(`Saved sessions:\n${names.join("\n")}\n\nEnter a session name to load:`, names[0]);
    if (!requested || !store[requested]) return;
    state = { ...clone(DEFAULT_STATE), ...store[requested] };
    renderView();
    showToast(`Loaded "${requested}"`);
  }

  function download(name, body, type) {
    const blob = new Blob([body], { type });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = name;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  function exportSession() {
    const payload = { dashboard: "Marvell Advanced Packaging Executive Dashboard", exportedAt: new Date().toISOString(), state };
    download(`${slug(state.sessionName)}.json`, JSON.stringify(payload, null, 2), "application/json");
    showToast("Session JSON exported");
  }

  function slug(value) {
    return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "dashboard-session";
  }

  function exportCsv() {
    if (!currentRows.length || !currentColumns.length) { showToast("No visible table to export"); return; }
    const csv = [
      currentColumns.map(([, label]) => csvCell(label)).join(","),
      ...sortRows(currentRows).map((row) => currentColumns.map(([key]) => csvCell(Array.isArray(row[key]) ? row[key].join("; ") : row[key])).join(","))
    ].join("\n");
    download(`${slug(state.sessionName)}-table.csv`, csv, "text/csv;charset=utf-8");
    showToast("Visible table exported");
  }

  function csvCell(value) {
    return `"${String(value == null ? "" : value).replace(/"/g, '""')}"`;
  }

  function executiveSummaryText() {
    const techs = filteredTechnologies().slice().sort((a,b) => b.Marvell_relevance_score-a.Marvell_relevance_score).slice(0,5);
    const vendors = filteredVendors().slice().sort((a,b) => b.competitive_threat-a.competitive_threat).slice(0,5);
    return [
      state.sessionName,
      `Data generated: ${DATA.generated_at}`,
      `Scope: relevance ${state.relevance}/5+, roadmap ${state.yearFrom}-${state.yearTo}.`,
      "",
      "Priority technologies:",
      ...techs.map((item, index) => `${index+1}. ${item.name} - relevance ${item.Marvell_relevance_score}/5; ${item.description}.`),
      "",
      "Competitive watch:",
      ...vendors.map((item, index) => `${index+1}. ${item.name} - threat ${item.competitive_threat}/5; partnership ${item.partnership_potential}/5.`),
      "",
      "Leadership thesis: Own package architecture, reusable interfaces, qualification data and customer trade-space; partner for manufacturing scale; acquire only scarce capabilities that change XPU win probability."
    ].join("\n");
  }

  function copySummary() {
    const text = executiveSummaryText();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => showToast("Executive summary copied")).catch(() => fallbackCopy(text));
    } else fallbackCopy(text);
  }

  function fallbackCopy(text) {
    const area = document.createElement("textarea");
    area.value = text;
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
    showToast("Executive summary copied");
  }

  function togglePresentation() {
    const active = document.body.classList.toggle("presentation");
    el("presentationMode").textContent = active ? "Exit presentation" : "Present";
    if (active && document.documentElement.requestFullscreen) document.documentElement.requestFullscreen().catch(() => {});
    if (!active && document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(() => {});
  }

  document.addEventListener("fullscreenchange", () => {
    if (!document.fullscreenElement && document.body.classList.contains("presentation")) {
      document.body.classList.remove("presentation");
      el("presentationMode").textContent = "Present";
    }
  });

  function validateData() {
    const required = ["technologies", "vendors", "roadmap_items", "benchmarks", "companies", "sources"];
    const missing = required.filter((key) => !Array.isArray(DATA[key]));
    if (missing.length) throw new Error(`Dashboard data missing: ${missing.join(", ")}`);
    el("dataStatus").textContent = `Repository snapshot ${DATA.generated_at} | ${DATA.technologies.length} technologies | ${DATA.vendors.length} vendors | ${DATA.roadmap_items.length} roadmap items`;
  }

  try {
    validateData();
    initializeControls();
    renderView();
  } catch (error) {
    content.innerHTML = `<div class="empty-state"><strong>Dashboard initialization failed.</strong><br>${escapeHtml(error.message)}</div>`;
    el("dataStatus").textContent = "Dashboard data error";
    console.error(error);
  }
})();
