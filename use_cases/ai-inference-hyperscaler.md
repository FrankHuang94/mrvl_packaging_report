# AI Inference Hyperscaler


> **Section metadata**
> - **Section title:** AI Inference Hyperscaler
> - **Owner placeholder:** Advanced Packaging Intelligence Owner
> - **Last refreshed date:** 2026-06-10
> - **Refresh status:** Current baseline
> - **Source count:** 4
> - **Confidence level:** Medium-high; confirmed facts separated from announced and inferred roadmap items
> - **Key changes since last refresh:** Initial repository baseline
> - **Open questions:** Customer qualification timing, package-level yields, commercial terms, and capacity allocation
> - **Links to related sections:** [reports/marvell_xpu_implications.md](../reports/marvell_xpu_implications.md), [data/technology_taxonomy.yaml](../data/technology_taxonomy.yaml)
> - **Figures included:** FIG-MMD-022
> - **Tables included:** TBL-USE-AI-INFERENCE-HYPERSCALER
> - **Next suggested refresh date:** 2026-09-10


Optimizes cost per token, power efficiency, capacity utilization and workload-specific precision. Packaging selection should rank HBM capacity and bandwidth, power efficiency, rack density, yielded cost, time-to-market, software coupling, supply resilience and thermal serviceability. Marvell should present at least two architecture points: a performance-maximized package and a cost/supply-optimized package. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-NVIDIA-001]](../data/source_database.yaml)

| Requirement | Priority | Packaging implication |
|---|---:|---|
| HBM bandwidth and capacity | 4/5 | Stack count, generation and thermal margin |
| Power efficiency | 5/5 | D2D, HBM, SerDes and voltage-conversion co-design |
| Yield and supply | 5/5 | Known-good-die, capacity reservation and alternate flows |
| Time-to-market | 5/5 | Reusable IP and qualified package reference |
| Serviceability | 4/5 | Cooling, optics and replaceable assembly strategy |

> **Marvell implication:** Translate the customer's workload and fleet economics into a package architecture before proposing a specific foundry flow.
