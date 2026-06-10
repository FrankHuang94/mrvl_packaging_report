# TSMC SoIC


> **Section metadata**
> - **Section title:** TSMC SoIC
> - **Owner placeholder:** Advanced Packaging Intelligence Owner
> - **Last refreshed date:** 2026-06-10
> - **Refresh status:** Current baseline
> - **Source count:** 2
> - **Confidence level:** Medium-high; confirmed facts separated from announced and inferred roadmap items
> - **Key changes since last refresh:** Initial repository baseline
> - **Open questions:** Customer qualification timing, package-level yields, commercial terms, and capacity allocation
> - **Links to related sections:** [data/technology_taxonomy.yaml](../data/technology_taxonomy.yaml), [reports/advanced_packaging_main_report.md](../reports/advanced_packaging_main_report.md), [reports/marvell_xpu_implications.md](../reports/marvell_xpu_implications.md)
> - **Figures included:** FIG-MMD-009
> - **Tables included:** TBL-TECH-009
> - **Next suggested refresh date:** 2026-09-10


**Technology ID:** `soic`  
**Category:** 3D stacking  
**Evidence status:** ramping  

TSMC SoIC is defined in this database as fine-pitch hybrid-bonded die or wafer stacking. The profile is intended for architecture selection and supplier diligence, not as a substitute for foundry design rules or customer qualification data. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Architecture

The architecture should be evaluated as a system partitioning decision, not as a package label. The decisive boundary is where bandwidth-intensive functions sit relative to compute, memory, I/O and power delivery. A package that minimizes one link may worsen another, so floorplanning must jointly optimize HBM escape routing, die-to-die reach, optical or electrical I/O placement, decoupling and coolant access. Applied to TSMC SoIC, the immediate diligence item is **cache stacking**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Manufacturing flow

The manufacturing sequence determines accumulated yield and cycle time. Wafer sort, thinning, TSV reveal, redistribution, bump or hybrid-bond preparation, die placement, underfill or molding, substrate attach, lid attach and final test each create distinct defect opportunities. The commercially relevant metric is good systems per start and delivery predictability, not the yield of an isolated process module. Applied to TSMC SoIC, the immediate diligence item is **logic-on-logic**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Materials and process dependencies

Key dependencies include low-loss dielectrics, copper line and via control, ABF or alternative substrate capacity, temporary bonding materials, underfill, molding compound, thermal interface material and metrology. Material choices couple electrical loss, coefficient-of-thermal-expansion mismatch, moisture sensitivity and warpage; substituting a material therefore requires package requalification rather than a procurement-only change. Applied to TSMC SoIC, the immediate diligence item is **3D I/O**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Metrics and benchmark discipline

Bandwidth density, energy per bit, latency and pitch are useful only when test conditions are explicit. A short-reach die-to-die demonstration cannot be compared directly with a rack-reach SerDes link, and a bonding-pitch claim does not reveal routable bandwidth after power, keep-out and redundancy are included. The database therefore records ranges and caveats instead of false point precision. Applied to TSMC SoIC, the immediate diligence item is **known-good-die**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Economics and yield

Cost is dominated by more than assembly price. Expensive known-good logic and HBM make scrap exposure material; larger interposers and substrates reduce units per panel or wafer; additional test insertions raise cost but can prevent higher downstream loss. The correct model values expected good-package cost, schedule risk and customer revenue exposure from missed ramps. Applied to TSMC SoIC, the immediate diligence item is **thermal density**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Thermal and power

Thermal design is becoming an architecture constraint. HBM, logic, optical engines and voltage conversion compete for package edge, vertical heat paths and coolant temperature budget. Hot spots, lateral gradients and thermo-mechanical cycling can reduce attainable frequency or lifetime even when average package power remains within a cold-plate rating. Applied to TSMC SoIC, the immediate diligence item is **bond yield**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Supply chain and adoption

Adoption requires simultaneous readiness across foundry packaging, memory, substrate, OSAT or test, EDA signoff, system cooling and customer qualification. A nominally mature process may still be unavailable at the required body size, HBM count or regional supply path. Supplier concentration should therefore be tracked by qualified configuration, not vendor logo count. Applied to TSMC SoIC, the immediate diligence item is **cache stacking**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Competitive implications

Control of design rules, characterization data and capacity reservations can create a competitive moat. NVIDIA and Broadcom can optimize around large internal volumes, while merchant custom-silicon providers must convert ecosystem breadth and reusable IP into comparable schedule certainty. Open standards reduce switching friction only after interoperable silicon, test and software are proven. Applied to TSMC SoIC, the immediate diligence item is **logic-on-logic**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Marvell implication

Marvell should package this capability as part of an end-to-end XPU platform: architecture exploration, reusable die-to-die and HBM IP, package and board co-design, manufacturing ownership, test strategy and lifecycle telemetry. The differentiation is not ownership of every factory step; it is the ability to give a hyperscaler a credible performance, cost, yield and supply plan before design freeze. Applied to TSMC SoIC, the immediate diligence item is **3D I/O**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Corporate development implication

Partnership or investment should target capability gaps that are difficult to reproduce through ordinary sourcing: optical attach, thermal materials and structures, chiplet test, multi-physics automation, advanced substrate process know-how and interoperable die-to-die IP. Acquisitions deserve consideration only where control materially improves XPU win probability or protects a strategic interface. Applied to TSMC SoIC, the immediate diligence item is **known-good-die**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Roadmap through 2030

The likely trajectory is larger and more heterogeneous packages, finer vertical connections, more customized memory base dies, greater use of local bridges or RDL to manage cost, and optics moving closer to high-radix switch and selected compute packages. The pace will be gated by yield learning, serviceability and power removal rather than by interconnect demonstrations alone. Applied to TSMC SoIC, the immediate diligence item is **thermal density**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

## Diligence priorities

Leadership should request configuration-specific evidence: qualified dimensions, HBM stack count, power map, thermal resistance, warpage, known-good-die coverage, repair flow, monthly capacity, cycle time, second-source path and cost sensitivity. Claims without these fields should remain announced or expected in the roadmap rather than promoted to confirmed. Applied to TSMC SoIC, the immediate diligence item is **bond yield**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. [[SRC-TSMC-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)


**Technology scorecard - TBL-TECH-009**

| Dimension | Score / status | Decision logic |
|---|---:|---|
| Marvell custom XPU relevance | 3/5 | Measures direct effect on performance, power, time-to-market, yield or customer differentiation. |
| Competitive threat | 3/5 | Measures the risk that competitors control scarce capability or create a proprietary platform advantage. |
| Partnership potential | 3/5 | Measures the value of ecosystem access, co-development and multi-source leverage. |
| Current maturity | ramping | Separates production evidence from announced targets and research concepts. |
| Leadership action | Quarterly review | Escalate when qualification, capacity, cost or customer architecture changes. |



## Decision close

- **Why it matters:** Fine-pitch hybrid-bonded die or wafer stacking.
- **Current maturity:** ramping.
- **Key bottlenecks:** known-good-die, thermal density, bond yield.
- **Leading vendors:** TSMC.
- **Roadmap:** 2026 qualification and capacity evidence; 2027-2028 density and cost learning; 2029-2030 broader heterogeneous integration.
- **Marvell implication:** Convert this technology into a reusable, characterized XPU package option with explicit customer tradeoffs.
- **Corporate development implication:** Partner where manufacturing scale dominates; invest or acquire where interface IP, tooling or process knowledge changes program control.
- **Open questions:** What is qualified at target package size?; What is the yield and monthly capacity?; What is the credible second-source path?
- **Figures and tables included:** FIG-MMD-009, TBL-TECH-009.
- **Next refresh recommendation:** 2026-09-10.
