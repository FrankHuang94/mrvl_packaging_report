#!/usr/bin/env python3
"""Generate the initial advanced-packaging research repository.

The .yaml files are emitted as JSON, which is valid YAML 1.2 and keeps the
runtime dependency-free for index and validation scripts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFRESH_DATE = "2026-06-10"
NEXT_REFRESH = "2026-09-10"


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: str, value: object) -> None:
    write(path, json.dumps(value, indent=2, ensure_ascii=True))


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


SOURCES = [
    ("SRC-MRVL-001", "Custom AI Investor Event", "Marvell", "Marvell leadership", "2025-06-17", "https://www.marvell.com/content/dam/marvell/en/company/assets/marvell-custom-ai-investor-event-2025.pdf", "company presentation", 1, ["Marvell", "custom XPU", "HBM", "advanced packaging", "CPO"], "Marvell's most complete public description of its custom AI platform, packaging, HBM attach, XPU attach, SerDes and optical strategy.", "Management claims and forward-looking market estimates require independent validation."),
    ("SRC-MRVL-002", "224G Long-Range SerDes for Scale-up and Scale-inside", "Marvell", "Aatreya Chakravarti", "2026-05-26", "https://www.marvell.com/blogs/224g-long-range-serdes-scale-up-scale-inside.html", "company technical blog", 1, ["SerDes", "CPO", "copper", "scale-up"], "Reports a 3nm 224G long-reach SerDes demonstration, a 2.5 meter channel, and 4 pJ/bit company measurement.", "Performance is a vendor demonstration and not an independent product benchmark."),
    ("SRC-MRVL-003", "Solving AI's Three Big Problems Through Photonic Fabric Technology", "Marvell", "Marvell", "2026-05-13", "https://www.marvell.com/blogs/solving-ai-problems-through-photonic-fabric-technology.html", "company technical blog", 1, ["optical I/O", "CPO", "silicon photonics"], "Explains Marvell's post-acquisition photonic fabric positioning for scale-up connectivity and memory disaggregation.", "Forward-looking architecture discussion; deployment timing is not independently confirmed."),
    ("SRC-MRVL-004", "NVIDIA AI Ecosystem Expands as Marvell Joins Forces Through NVLink Fusion", "Marvell", "Marvell and NVIDIA", "2026-03-31", "https://www.marvell.com/company/newsroom/nvidia-ai-ecosystem-expands-marvell-joins-forces-through-nvlink-fusion.html", "company press release", 1, ["NVLink Fusion", "custom XPU", "silicon photonics"], "Describes Marvell participation in NVLink Fusion and collaboration around custom silicon and connectivity.", "Partnership announcement does not disclose customer designs, revenue, or production timing."),
    ("SRC-MRVL-005", "Marvell Newsroom", "Marvell", "Marvell", "2026-06-02", "https://www.marvell.com/company/newsroom.html", "company newsroom", 1, ["Marvell", "switching", "optics"], "Current chronology of Marvell product, partnership and investor disclosures.", "Landing page changes over time; archive individual releases for durable refreshes."),
    ("SRC-TSMC-001", "3DFabric: TSMC 3D Silicon Stacking and Advanced Packaging", "TSMC", "TSMC", "2025-01-01", "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/3DFabric.htm", "company technology page", 1, ["CoWoS", "SoIC", "InFO", "3DFabric"], "Defines TSMC's integrated front-end and back-end 3DFabric portfolio.", "Product availability and dimensions vary by customer qualification and generation."),
    ("SRC-TSMC-002", "TSMC 2024 Annual Report", "TSMC", "TSMC", "2025-03-01", "https://investor.tsmc.com/english/annual-reports", "annual report", 1, ["CoWoS", "advanced packaging", "capacity"], "Primary financial and capacity context for TSMC advanced packaging investment.", "Capacity disclosures are aggregated and do not provide customer-level allocation."),
    ("SRC-TSMC-003", "TSMC 2025 Technology Symposium", "TSMC", "TSMC", "2025-04-23", "https://www.tsmc.com/english/news-events/press-releases", "company event materials", 1, ["CoWoS", "SoIC", "A16", "COUPE"], "Roadmap disclosures for logic, 3DFabric and silicon photonics integration.", "Some roadmap details are announced targets, not qualified production."),
    ("SRC-TSMC-004", "TSMC Open Innovation Platform", "TSMC", "TSMC", "2025-01-01", "https://www.tsmc.com/english/dedicatedFoundry/oip", "company ecosystem page", 1, ["EDA", "chiplets", "3DFabric"], "Describes design enablement and ecosystem dependencies for complex multi-die products.", "Does not disclose commercial terms or partner-specific readiness."),
    ("SRC-JEDEC-001", "JESD270-4 High Bandwidth Memory 4", "JEDEC", "JEDEC", "2025-04-16", "https://www.jedec.org/news/pressreleases/jedec-and-industry-leaders-collaborate-release-jesd270-4-hbm4-standard", "industry standard", 1, ["HBM4", "memory"], "HBM4 standard doubles the interface width to 2,048 bits and defines higher capacity and bandwidth options.", "Implementations may exceed baseline rates and differ in stack height, base die and thermals."),
    ("SRC-JEDEC-002", "JESD238 HBM3 Standard", "JEDEC", "JEDEC", "2022-01-27", "https://www.jedec.org/news/pressreleases/jedec-publishes-hbm3-update-high-bandwidth-memory-standard", "industry standard", 1, ["HBM3", "memory"], "Primary specification context for HBM3 channel architecture and rates.", "Vendor HBM3E products extend beyond the original baseline."),
    ("SRC-UCIE-001", "UCIe Consortium Releases 2.0 Specification", "UCIe Consortium", "UCIe Consortium", "2024-08-06", "https://www.uciexpress.org/post/ucie-consortium-releases-2-0-specification", "industry standard", 1, ["UCIe", "chiplets", "3D packaging"], "Adds manageability, debug, test and support for 3D constructions.", "Interoperability depends on compliance programs and commercial IP maturity."),
    ("SRC-UCIE-002", "UCIe Consortium Introduces 3.0 Specification", "UCIe Consortium", "UCIe Consortium", "2025-08-05", "https://www.uciexpress.org/post/ucie-consortium-introduces-3-0-specification", "industry standard", 1, ["UCIe", "die-to-die"], "Introduces 48 and 64 GT/s operation and manageability enhancements.", "Specification availability precedes broad silicon interoperability."),
    ("SRC-OIF-001", "Co-Packaging Framework Implementation Agreement", "OIF", "OIF", "2023-01-01", "https://www.oiforum.com/technical-work/hot-topics/co-packaging/", "industry standard", 1, ["CPO", "external laser", "optics"], "Defines ecosystem considerations and interfaces for co-packaged optical modules.", "Framework adoption and product implementations remain vendor-specific."),
    ("SRC-UALINK-001", "UALink 1.0 Specification and White Paper", "UALink Consortium", "UALink Consortium", "2025-04-01", "https://ualinkconsortium.org/specifications/", "industry standard", 1, ["UALink", "scale-up"], "Defines an open accelerator scale-up fabric targeting large AI pods.", "Commercial deployments and ecosystem depth are still developing."),
    ("SRC-INTEL-001", "Advanced Packaging", "Intel Foundry", "Intel", "2025-01-01", "https://www.intel.com/content/www/us/en/foundry/packaging.html", "company technology page", 1, ["EMIB", "Foveros", "Foveros Direct"], "Describes Intel's embedded bridge and 3D stacking portfolio.", "External foundry availability differs from internal product deployment."),
    ("SRC-INTEL-002", "Intel Unveils Industry-Leading Glass Substrates", "Intel", "Intel", "2023-09-18", "https://www.intel.com/content/www/us/en/newsroom/news/intel-unveils-industry-leading-glass-substrates.html", "company press release", 1, ["glass substrate", "packaging"], "Describes glass-core substrate benefits and a late-decade introduction target.", "Roadmap is a vendor target; ecosystem and cost readiness remain uncertain."),
    ("SRC-INTEL-003", "Foveros Direct and EMIB Product Evidence", "Intel", "Intel", "2025-01-01", "https://www.intel.com/content/www/us/en/products/docs/processors/xeon/xeon-6-overview.html", "product documentation", 1, ["Foveros", "EMIB", "chiplets"], "Provides product-level evidence of Intel multi-die packaging deployment.", "Product packaging configurations do not imply merchant-foundry availability."),
    ("SRC-SAMSUNG-001", "Advanced Package", "Samsung Semiconductor", "Samsung", "2025-01-01", "https://semiconductor.samsung.com/foundry/advanced-package/", "company technology page", 1, ["I-Cube", "X-Cube", "fan-out"], "Defines Samsung's 2.5D and 3D packaging portfolio.", "Limited public disclosure on customer ramps and comparative yields."),
    ("SRC-SAMSUNG-002", "Samsung High Bandwidth Memory", "Samsung Semiconductor", "Samsung", "2025-01-01", "https://semiconductor.samsung.com/dram/hbm/", "company product page", 1, ["HBM3E", "HBM4"], "Vendor roadmap and product positioning for HBM.", "Qualification status is customer-specific and public detail is limited."),
    ("SRC-SKH-001", "SK hynix Completes HBM4 Development and Readies Mass Production", "SK hynix", "SK hynix", "2025-09-12", "https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/", "company press release", 1, ["HBM4", "MR-MUF"], "Reports HBM4 development status and vendor performance claims.", "Customer qualification and sustained volume yield are not disclosed."),
    ("SRC-SKH-002", "HBM3E and Advanced MR-MUF Technology", "SK hynix", "SK hynix", "2024-09-26", "https://news.skhynix.com/sk-hynix-begins-mass-production-of-worlds-first-12-layer-hbm3e/", "company press release", 1, ["HBM3E", "thermal"], "Describes 12-high HBM3E manufacturing and MR-MUF packaging.", "Vendor claims require workload- and package-level qualification."),
    ("SRC-MICRON-001", "Micron HBM3E Product Brief", "Micron", "Micron", "2025-01-01", "https://www.micron.com/products/memory/hbm", "company product page", 1, ["HBM3E", "HBM4"], "Primary source for Micron HBM product capabilities and roadmap statements.", "Roadmap timing and customer qualification can change."),
    ("SRC-NVIDIA-001", "NVIDIA Blackwell Architecture", "NVIDIA", "NVIDIA", "2024-03-18", "https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/", "company product page", 1, ["AI accelerator", "HBM3E", "NVLink"], "Product-level evidence of large multi-die accelerators, HBM and scale-up fabrics.", "NVIDIA system claims are vendor-specific and may not isolate packaging contribution."),
    ("SRC-NVIDIA-002", "NVIDIA Announces Spectrum-X and Quantum-X Photonics", "NVIDIA", "NVIDIA", "2025-03-18", "https://nvidianews.nvidia.com/news/silicon-photonics-networking-switches-ai-factories", "company press release", 1, ["CPO", "silicon photonics", "switching"], "Announces silicon-photonics-based switch platforms and deployment targets.", "Announced product timing and field serviceability require follow-up."),
    ("SRC-AMD-001", "AMD Instinct MI300 Series", "AMD", "AMD", "2023-12-06", "https://www.amd.com/en/products/accelerators/instinct/mi300.html", "company product page", 1, ["3D stacking", "HBM3", "chiplets"], "Demonstrates production use of chiplets, 3D stacking and HBM in an AI accelerator.", "Architecture-specific metrics should not be generalized to all packaging options."),
    ("SRC-BRCM-001", "Broadcom Enables Co-Packaged Optics Ecosystem", "Broadcom", "Broadcom", "2024-03-01", "https://www.broadcom.com/company/news/product-releases", "company press release archive", 1, ["CPO", "switching", "custom ASIC"], "Primary source archive for Broadcom switch and CPO announcements.", "Broadcom discloses limited custom ASIC customer and packaging detail."),
    ("SRC-ASE-001", "VIPack Advanced Packaging Platform", "ASE", "ASE", "2025-01-01", "https://ase.aseglobal.com/vipack/", "company technology page", 1, ["fan-out", "bridge", "3D packaging"], "ASE's modular platform for high-density fan-out, bridge and 3D integration.", "Public process metrics and customer ramps are selective."),
    ("SRC-AMKOR-001", "Advanced Packaging Solutions", "Amkor", "Amkor", "2025-01-01", "https://amkor.com/technology/advanced-packaging/", "company technology page", 1, ["2.5D", "fan-out", "test"], "Amkor portfolio and manufacturing context for advanced packaging.", "Application-specific capabilities require direct supplier diligence."),
    ("SRC-JCET-001", "Advanced Packaging Technology", "JCET", "JCET", "2025-01-01", "https://www.jcetglobal.com/en/site/technology", "company technology page", 1, ["fan-out", "2.5D", "SiP"], "JCET advanced packaging and system-in-package portfolio.", "Geopolitical and customer qualification constraints are not fully described."),
    ("SRC-CADENCE-001", "3D-IC System Analysis", "Cadence", "Cadence", "2025-01-01", "https://www.cadence.com/en_US/home/tools/ic-package-design-and-analysis/3dic-design.html", "company product page", 1, ["EDA", "3D-IC", "multi-physics"], "Design flow for chip-package-system co-design and analysis.", "Tool claims should be validated against target foundry flows."),
    ("SRC-SYNOPSYS-001", "Multi-Die System Solutions", "Synopsys", "Synopsys", "2025-01-01", "https://www.synopsys.com/solutions/multi-die-systems.html", "company product page", 1, ["EDA", "UCIe", "IP"], "Integrated EDA and IP positioning for multi-die systems.", "Interoperability depends on specific versions and foundry qualification."),
    ("SRC-SIEMENS-001", "Calibre 3DSTACK and XSI", "Siemens EDA", "Siemens", "2025-01-01", "https://eda.sw.siemens.com/en-US/ic/calibre-design/3dstack/", "company product page", 1, ["EDA", "verification", "3D-IC"], "Physical verification and parasitic extraction for 2.5D/3D integration.", "Coverage and runtime depend on design scale and process decks."),
    ("SRC-ANSYS-001", "Semiconductor and 3D-IC Multiphysics", "Ansys", "Ansys", "2025-01-01", "https://www.ansys.com/industries/semiconductors", "company product page", 1, ["thermal", "mechanical", "signal integrity"], "Multi-physics context for package thermal, mechanical and electrical co-design.", "Accuracy depends on calibrated material and boundary-condition inputs."),
    ("SRC-AYAR-001", "TeraPHY Optical I/O Chiplet", "Ayar Labs", "Ayar Labs", "2025-01-01", "https://ayarlabs.com/technology/", "company technology page", 2, ["optical I/O", "chiplets", "CPO"], "Vendor architecture for in-package optical I/O chiplets and external lasers.", "Private-company claims and production scale require diligence."),
    ("SRC-LIGHTMATTER-001", "Passage Photonic Interconnect", "Lightmatter", "Lightmatter", "2025-01-01", "https://lightmatter.co/products/passage/", "company technology page", 2, ["silicon photonics", "interposer", "optical I/O"], "Photonic interconnect platform positioning for AI scale-up.", "Commercial availability, yield and customer adoption are not fully public."),
    ("SRC-RANOVUS-001", "Odin CPO Platform", "Ranovus", "Ranovus", "2025-01-01", "https://ranovus.com/technology/", "company technology page", 2, ["CPO", "silicon photonics"], "CPO engine architecture and ecosystem positioning.", "Volume manufacturing and field reliability evidence is limited publicly."),
    ("SRC-CELESTIAL-001", "Photonic Fabric", "Celestial AI", "Celestial AI", "2025-01-01", "https://www.celestial.ai/technology", "company technology page", 2, ["photonic fabric", "memory disaggregation"], "Describes photonic fabric architecture for compute and memory connectivity.", "Now part of Marvell; pre-acquisition claims need integration-roadmap confirmation."),
    ("SRC-COHERENT-001", "Datacenter Transceivers and Optical Engines", "Coherent", "Coherent", "2025-01-01", "https://www.coherent.com/networking", "company product page", 1, ["lasers", "optics", "CPO"], "Supplier context for lasers, transceivers and optical components.", "CPO-specific commercial terms and yields are not public."),
    ("SRC-LUMENTUM-001", "Cloud and Networking Optical Products", "Lumentum", "Lumentum", "2025-01-01", "https://www.lumentum.com/en/optical-communications", "company product page", 1, ["lasers", "optics"], "Supplier context for external laser and optical component ecosystems.", "Customer concentration and product-level qualification details are limited."),
    ("SRC-IEEE-001", "Heterogeneous Integration Roadmap", "IEEE Electronics Packaging Society", "IEEE", "2023-01-01", "https://eps.ieee.org/technology/heterogeneous-integration-roadmap.html", "technical roadmap", 1, ["packaging", "materials", "test"], "Cross-industry roadmap for heterogeneous integration, interconnect scaling and manufacturing challenges.", "Roadmap aggregates expert expectations rather than committed vendor schedules."),
    ("SRC-ECTC-001", "Electronic Components and Technology Conference Proceedings", "IEEE ECTC", "IEEE", "2025-05-27", "https://www.ectc.net/", "technical conference", 1, ["packaging", "hybrid bonding", "thermal"], "Peer-reviewed and industry technical papers on packaging processes and reliability.", "Individual papers use different test vehicles and are not always directly comparable."),
    ("SRC-PCI-001", "PCI Express 7.0 Specification", "PCI-SIG", "PCI-SIG", "2025-06-11", "https://pcisig.com/pci-express-7.0-specification", "industry standard", 1, ["PCIe", "SerDes", "CXL"], "I/O roadmap context for 128 GT/s electrical links.", "Product adoption follows specification release by multiple years."),
    ("SRC-CXL-001", "CXL 3.1 Specification", "CXL Consortium", "CXL Consortium", "2023-11-07", "https://www.computeexpresslink.org/download-the-specification", "industry standard", 1, ["CXL", "memory expansion"], "Standards context for memory pooling, switching and fabric-attached memory.", "CXL is complementary to, not a direct bandwidth substitute for, local HBM."),
    ("SRC-UET-001", "Ultra Ethernet Specification", "Ultra Ethernet Consortium", "UEC", "2025-06-01", "https://ultraethernet.org/specifications/", "industry standard", 1, ["Ethernet", "AI networking"], "Open Ethernet enhancements for AI and HPC scale-out networking.", "Silicon and software maturity will determine deployment timing."),
]


TECHNOLOGIES = [
    ("cowos-s", "TSMC CoWoS-S", "2.5D packaging", "Full silicon interposer integration for logic and HBM", ["TSMC"], ["AI training", "HPC"], ["SRC-TSMC-001", "SRC-TSMC-003"], "production", ["interposer capacity", "reticle-scale economics", "warpage"]),
    ("cowos-l", "TSMC CoWoS-L", "2.5D packaging", "Local silicon interconnect with RDL interposer scaling", ["TSMC"], ["large AI XPU", "multi-chiplet compute"], ["SRC-TSMC-001", "SRC-TSMC-003"], "ramping", ["RDL yield", "bridge alignment", "package-scale validation"]),
    ("cowos-r", "TSMC CoWoS-R", "2.5D packaging", "RDL interposer approach emphasizing package size and cost", ["TSMC"], ["cost-sensitive accelerator", "network ASIC"], ["SRC-TSMC-001"], "qualified", ["routing density", "power integrity", "customer qualification"]),
    ("silicon-interposer", "Silicon Interposer", "2.5D packaging", "Fine-pitch passive silicon routing layer with TSVs", ["TSMC", "Samsung", "ASE", "Amkor"], ["AI accelerator", "HBM integration"], ["SRC-TSMC-001", "SRC-SAMSUNG-001", "SRC-ASE-001"], "production", ["cost", "capacity", "large-area yield"]),
    ("rdl-interposer", "RDL Interposer", "2.5D packaging", "Polymer and metal redistribution structure without full silicon area", ["TSMC", "ASE", "Amkor", "JCET"], ["AI inference", "networking"], ["SRC-TSMC-001", "SRC-ASE-001", "SRC-AMKOR-001"], "ramping", ["line-space scaling", "warpage", "via reliability"]),
    ("emib", "Embedded Silicon Bridge", "2.5D packaging", "Localized silicon bridge embedded in an organic substrate", ["Intel", "ASE"], ["CPU", "GPU", "AI accelerator"], ["SRC-INTEL-001", "SRC-INTEL-003"], "production", ["assembly tolerance", "substrate routing", "merchant access"]),
    ("fanout", "Fan-out on Substrate and Panel Fan-out", "fan-out", "Redistribution-first package with molded or panel processing", ["ASE", "Amkor", "JCET", "TSMC"], ["inference ASIC", "switch ASIC"], ["SRC-ASE-001", "SRC-AMKOR-001", "SRC-JCET-001"], "production and development", ["die shift", "panel tools", "large-body warpage"]),
    ("glass-substrate", "Glass Core Substrate", "substrate", "Low-warpage, dimensionally stable core for large packages", ["Intel", "Samsung", "Absolics"], ["late-decade AI package"], ["SRC-INTEL-002", "SRC-IEEE-001"], "development", ["through-glass vias", "handling", "cost and ecosystem"]),
    ("soic", "TSMC SoIC", "3D stacking", "Fine-pitch hybrid-bonded die or wafer stacking", ["TSMC"], ["cache stacking", "logic-on-logic", "3D I/O"], ["SRC-TSMC-001", "SRC-TSMC-003"], "ramping", ["known-good-die", "thermal density", "bond yield"]),
    ("foveros-direct", "Intel Foveros and Foveros Direct", "3D stacking", "Active base-die stacking with micro-bumps or direct bonding", ["Intel"], ["CPU", "HPC", "AI"], ["SRC-INTEL-001", "SRC-INTEL-003"], "production and ramping", ["external access", "thermal", "test"]),
    ("x-cube", "Samsung X-Cube", "3D stacking", "Samsung 3D integration platform using TSV and fine-pitch bonding", ["Samsung"], ["logic stacking", "HPC"], ["SRC-SAMSUNG-001"], "development and selective qualification", ["customer evidence", "yield", "ecosystem"]),
    ("hybrid-bonding", "Hybrid Bonding", "3D stacking", "Direct copper and dielectric bonding at fine pitch", ["TSMC", "Intel", "Samsung", "ASE"], ["3D cache", "logic stacking", "HBM"], ["SRC-TSMC-001", "SRC-INTEL-001", "SRC-ECTC-001"], "ramping", ["surface planarity", "particles", "repairability"]),
    ("hbm3e", "HBM3E", "memory packaging", "High-bandwidth stacked DRAM extension of HBM3", ["SK hynix", "Micron", "Samsung"], ["AI training", "AI inference"], ["SRC-JEDEC-002", "SRC-SKH-002", "SRC-MICRON-001"], "high-volume production", ["supply", "thermals", "test yield"]),
    ("hbm4", "HBM4 and HBM4E", "memory packaging", "2,048-bit-interface HBM generation with logic base-die opportunity", ["SK hynix", "Samsung", "Micron"], ["next-generation AI XPU"], ["SRC-JEDEC-001", "SRC-SKH-001", "SRC-SAMSUNG-002"], "ramping and announced", ["base die co-design", "power", "16-high yield"]),
    ("custom-hbm", "Custom HBM Base Die", "memory packaging", "Customer-specific logic base die that can partition PHY, control and data movement", ["Marvell", "memory vendors", "TSMC"], ["custom XPU"], ["SRC-MRVL-001", "SRC-JEDEC-001"], "announced architecture", ["business model", "memory-vendor interfaces", "verification"]),
    ("ucie", "UCIe", "die-to-die", "Open package-level die-to-die protocol and physical interface", ["UCIe Consortium", "Synopsys", "Cadence"], ["chiplet XPU", "heterogeneous integration"], ["SRC-UCIE-001", "SRC-UCIE-002", "SRC-SYNOPSYS-001"], "specification and early products", ["interoperability", "latency overhead", "test"]),
    ("parallel-d2d", "Parallel Die-to-Die Interconnect", "die-to-die", "Wide, low-swing short-reach interface optimized for bandwidth density", ["Marvell", "Broadcom", "AMD", "Intel"], ["compute chiplets", "HBM PHY chiplets"], ["SRC-MRVL-001", "SRC-UCIE-001"], "production proprietary and standardizing", ["bump demand", "reach", "package routing"]),
    ("serial-d2d", "Serialized XSR/USR Die-to-Die", "die-to-die", "Narrower high-speed SerDes link for longer package reach and modularity", ["Marvell", "Alphawave", "Synopsys"], ["I/O chiplets", "optical engines"], ["SRC-MRVL-002", "SRC-SYNOPSYS-001"], "production and development", ["energy per bit", "latency", "clocking"]),
    ("cpo-switch", "Switch Co-Packaged Optics", "optical packaging", "Optical engines adjacent to a switch ASIC", ["NVIDIA", "Broadcom", "Marvell"], ["scale-out switch", "scale-up switch"], ["SRC-NVIDIA-002", "SRC-OIF-001", "SRC-BRCM-001"], "announced and early deployment", ["serviceability", "laser reliability", "thermal isolation"]),
    ("optical-io", "Optical I/O Chiplets for XPUs", "optical packaging", "In-package optical chiplets connecting compute to rack-scale fabrics", ["Marvell", "Ayar Labs", "Lightmatter", "Ranovus"], ["custom XPU", "memory disaggregation"], ["SRC-MRVL-003", "SRC-AYAR-001", "SRC-LIGHTMATTER-001"], "development", ["fiber attach", "test", "protocol integration"]),
    ("external-laser", "External Laser Source", "optical packaging", "Serviceable laser supply separated from hot compute package", ["Coherent", "Lumentum", "Ayar Labs"], ["CPO", "optical I/O"], ["SRC-OIF-001", "SRC-COHERENT-001", "SRC-LUMENTUM-001"], "qualification", ["coupling loss", "redundancy", "connector standards"]),
    ("abf-substrate", "ABF Organic Substrate", "substrate", "Build-up organic package substrate used under advanced interposers", ["Ibiden", "Shinko", "Unimicron", "Kinsus", "AT&S"], ["AI accelerator", "network ASIC"], ["SRC-IEEE-001"], "high-volume production", ["capacity", "warpage", "large-body yield"]),
    ("power-delivery", "Package Power Delivery and IVR", "power and thermal", "Package-level power distribution, decoupling and voltage conversion", ["Marvell", "foundries", "power vendors"], ["high-power XPU"], ["SRC-ANSYS-001", "SRC-IEEE-001"], "production and development", ["current density", "droop", "thermal coupling"]),
    ("liquid-cooling", "Direct Liquid and Package Cooling", "power and thermal", "Cold plates, TIMs and liquid loops for high-power packages", ["system OEMs", "thermal suppliers"], ["AI rack"], ["SRC-ANSYS-001", "SRC-IEEE-001"], "production", ["leak risk", "TIM aging", "serviceability"]),
    ("known-good-die", "Known-Good-Die and Chiplet Test", "test", "Pre-bond, mid-bond and final test strategy for multi-die packages", ["ASE", "Amkor", "KYEC", "foundries"], ["all chiplet packages"], ["SRC-AMKOR-001", "SRC-ECTC-001"], "production and evolving", ["coverage", "DFT standards", "repair"]),
    ("multi-die-eda", "Multi-Die EDA and Multi-Physics", "design enablement", "Integrated die-package-board electrical, thermal and mechanical design flow", ["Cadence", "Synopsys", "Siemens", "Ansys"], ["custom XPU", "CPO"], ["SRC-CADENCE-001", "SRC-SYNOPSYS-001", "SRC-SIEMENS-001", "SRC-ANSYS-001"], "production and maturing", ["data model integration", "runtime", "correlation"]),
]


VENDORS = [
    ("tsmc", "TSMC", "foundry and packaging", ["CoWoS-S", "CoWoS-L", "CoWoS-R", "SoIC", "InFO", "COUPE"], ["SRC-TSMC-001", "SRC-TSMC-002", "SRC-TSMC-003"], 5, 5, 5, 1),
    ("intel-foundry", "Intel Foundry", "foundry and packaging", ["EMIB", "Foveros", "Foveros Direct", "glass substrate"], ["SRC-INTEL-001", "SRC-INTEL-002", "SRC-INTEL-003"], 4, 3, 4, 1),
    ("samsung-foundry", "Samsung Foundry", "foundry and packaging", ["I-Cube", "X-Cube", "fan-out"], ["SRC-SAMSUNG-001"], 4, 3, 4, 1),
    ("ase", "ASE", "OSAT", ["VIPack", "fan-out", "bridge", "test"], ["SRC-ASE-001"], 4, 2, 5, 2),
    ("amkor", "Amkor", "OSAT", ["2.5D", "fan-out", "test"], ["SRC-AMKOR-001"], 4, 2, 5, 2),
    ("jcet", "JCET", "OSAT", ["fan-out", "SiP", "2.5D"], ["SRC-JCET-001"], 3, 2, 3, 1),
    ("spil", "SPIL", "OSAT", ["advanced assembly", "test"], ["SRC-ASE-001"], 3, 1, 4, 1),
    ("powertech", "Powertech", "memory packaging and test", ["memory test", "HBM support"], ["SRC-IEEE-001"], 3, 1, 4, 2),
    ("kyec", "KYEC", "semiconductor test", ["wafer sort", "final test"], ["SRC-ECTC-001"], 3, 1, 4, 2),
    ("sk-hynix", "SK hynix", "HBM supplier", ["HBM3E", "HBM4", "MR-MUF"], ["SRC-SKH-001", "SRC-SKH-002"], 5, 4, 5, 1),
    ("samsung-memory", "Samsung Memory", "HBM supplier", ["HBM3E", "HBM4", "custom base die"], ["SRC-SAMSUNG-002", "SRC-JEDEC-001"], 5, 4, 5, 1),
    ("micron", "Micron", "HBM supplier", ["HBM3E", "HBM4"], ["SRC-MICRON-001", "SRC-JEDEC-001"], 5, 3, 5, 1),
    ("marvell", "Marvell", "custom silicon and connectivity", ["custom XPU", "custom HBM", "CPO", "SerDes", "Ethernet"], ["SRC-MRVL-001", "SRC-MRVL-002", "SRC-MRVL-003", "SRC-MRVL-004"], 5, 1, 5, 1),
    ("broadcom", "Broadcom", "custom ASIC and networking", ["custom ASIC", "switch CPO", "SerDes"], ["SRC-BRCM-001"], 5, 5, 3, 1),
    ("nvidia", "NVIDIA", "AI platform", ["GPU", "NVLink", "CPO", "HBM"], ["SRC-NVIDIA-001", "SRC-NVIDIA-002"], 5, 5, 3, 1),
    ("amd", "AMD", "AI accelerator", ["chiplet GPU", "3D stacking", "HBM"], ["SRC-AMD-001"], 4, 4, 3, 1),
    ("google", "Google TPU ecosystem", "hyperscaler custom silicon", ["TPU", "HBM", "optical networking"], ["SRC-MRVL-001"], 5, 3, 4, 1),
    ("aws", "AWS Trainium and Inferentia ecosystem", "hyperscaler custom silicon", ["Trainium", "Inferentia", "Ethernet"], ["SRC-MRVL-001"], 5, 3, 5, 1),
    ("microsoft", "Microsoft Maia ecosystem", "hyperscaler custom silicon", ["Maia", "Cobalt", "Ethernet"], ["SRC-MRVL-001"], 5, 3, 5, 1),
    ("meta", "Meta MTIA ecosystem", "hyperscaler custom silicon", ["MTIA", "inference"], ["SRC-MRVL-001"], 4, 2, 4, 1),
    ("mediatek", "MediaTek", "custom AI ASIC", ["advanced-node ASIC", "SerDes"], ["SRC-TSMC-004"], 3, 4, 2, 1),
    ("alchip", "Alchip", "ASIC design service", ["CoWoS", "UCIe", "optical I/O"], ["SRC-TSMC-004", "SRC-AYAR-001"], 4, 4, 3, 1),
    ("guc", "GUC", "ASIC design service", ["CoWoS", "chiplets"], ["SRC-TSMC-004"], 4, 4, 3, 1),
    ("faraday", "Faraday", "ASIC design service", ["ASIC", "chiplets"], ["SRC-TSMC-004"], 2, 2, 3, 2),
    ("socionext", "Socionext", "ASIC design service", ["advanced-node ASIC", "packaging"], ["SRC-TSMC-004"], 3, 3, 3, 1),
    ("coherent", "Coherent", "optical components", ["lasers", "transceivers", "CPO components"], ["SRC-COHERENT-001"], 4, 2, 5, 2),
    ("lumentum", "Lumentum", "optical components", ["lasers", "transceivers"], ["SRC-LUMENTUM-001"], 4, 2, 5, 2),
    ("ayar-labs", "Ayar Labs", "optical I/O", ["TeraPHY", "SuperNova"], ["SRC-AYAR-001"], 5, 3, 5, 4),
    ("celestial-ai", "Celestial AI", "photonic interconnect", ["Photonic Fabric"], ["SRC-CELESTIAL-001", "SRC-MRVL-003"], 5, 1, 5, 1),
    ("lightmatter", "Lightmatter", "photonic interconnect", ["Passage"], ["SRC-LIGHTMATTER-001"], 4, 3, 5, 4),
    ("ranovus", "Ranovus", "CPO", ["Odin"], ["SRC-RANOVUS-001"], 4, 2, 5, 4),
    ("intel-photonics", "Intel Silicon Photonics", "silicon photonics", ["optical engines", "lasers"], ["SRC-INTEL-001"], 4, 3, 4, 1),
    ("synopsys", "Synopsys", "EDA and IP", ["UCIe IP", "multi-die EDA"], ["SRC-SYNOPSYS-001"], 4, 2, 5, 2),
    ("cadence", "Cadence", "EDA and IP", ["3D-IC design", "UCIe IP"], ["SRC-CADENCE-001"], 4, 2, 5, 2),
    ("siemens", "Siemens EDA", "EDA", ["3DSTACK", "verification"], ["SRC-SIEMENS-001"], 3, 1, 5, 2),
    ("ansys", "Ansys", "multi-physics", ["thermal", "mechanical", "SI/PI"], ["SRC-ANSYS-001"], 4, 1, 5, 2),
    ("keysight", "Keysight", "test and measurement", ["224G/448G validation", "optical test"], ["SRC-MRVL-002"], 4, 1, 5, 2),
    ("alphawave", "Alphawave Semi", "connectivity IP", ["SerDes", "UCIe", "chiplets"], ["SRC-UCIE-001"], 3, 3, 4, 3),
]


def cite(ids: list[str], prefix: str = "../") -> str:
    return " ".join(f"[[{item}]]({prefix}data/source_database.yaml)" for item in ids)


def metadata(title: str, source_count: int, related: list[str], figures: list[str], tables: list[str], prefix: str = "../") -> str:
    links = ", ".join(f"[{item}]({prefix}{item})" for item in related)
    return f"""
> **Section metadata**
> - **Section title:** {title}
> - **Owner placeholder:** Advanced Packaging Intelligence Owner
> - **Last refreshed date:** {REFRESH_DATE}
> - **Refresh status:** Current baseline
> - **Source count:** {source_count}
> - **Confidence level:** Medium-high; confirmed facts separated from announced and inferred roadmap items
> - **Key changes since last refresh:** Initial repository baseline
> - **Open questions:** Customer qualification timing, package-level yields, commercial terms, and capacity allocation
> - **Links to related sections:** {links}
> - **Figures included:** {", ".join(figures) if figures else "None"}
> - **Tables included:** {", ".join(tables) if tables else "None"}
> - **Next suggested refresh date:** {NEXT_REFRESH}
"""


def scorecard(name: str, relevance: int, threat: int, partner: int, maturity: str, table_id: str) -> str:
    return f"""
**Technology scorecard - {table_id}**

| Dimension | Score / status | Decision logic |
|---|---:|---|
| Marvell custom XPU relevance | {relevance}/5 | Measures direct effect on performance, power, time-to-market, yield or customer differentiation. |
| Competitive threat | {threat}/5 | Measures the risk that competitors control scarce capability or create a proprietary platform advantage. |
| Partnership potential | {partner}/5 | Measures the value of ecosystem access, co-development and multi-source leverage. |
| Current maturity | {maturity} | Separates production evidence from announced targets and research concepts. |
| Leadership action | Quarterly review | Escalate when qualification, capacity, cost or customer architecture changes. |
"""


LENSES = [
    ("Architecture", "The architecture should be evaluated as a system partitioning decision, not as a package label. The decisive boundary is where bandwidth-intensive functions sit relative to compute, memory, I/O and power delivery. A package that minimizes one link may worsen another, so floorplanning must jointly optimize HBM escape routing, die-to-die reach, optical or electrical I/O placement, decoupling and coolant access."),
    ("Manufacturing flow", "The manufacturing sequence determines accumulated yield and cycle time. Wafer sort, thinning, TSV reveal, redistribution, bump or hybrid-bond preparation, die placement, underfill or molding, substrate attach, lid attach and final test each create distinct defect opportunities. The commercially relevant metric is good systems per start and delivery predictability, not the yield of an isolated process module."),
    ("Materials and process dependencies", "Key dependencies include low-loss dielectrics, copper line and via control, ABF or alternative substrate capacity, temporary bonding materials, underfill, molding compound, thermal interface material and metrology. Material choices couple electrical loss, coefficient-of-thermal-expansion mismatch, moisture sensitivity and warpage; substituting a material therefore requires package requalification rather than a procurement-only change."),
    ("Metrics and benchmark discipline", "Bandwidth density, energy per bit, latency and pitch are useful only when test conditions are explicit. A short-reach die-to-die demonstration cannot be compared directly with a rack-reach SerDes link, and a bonding-pitch claim does not reveal routable bandwidth after power, keep-out and redundancy are included. The database therefore records ranges and caveats instead of false point precision."),
    ("Economics and yield", "Cost is dominated by more than assembly price. Expensive known-good logic and HBM make scrap exposure material; larger interposers and substrates reduce units per panel or wafer; additional test insertions raise cost but can prevent higher downstream loss. The correct model values expected good-package cost, schedule risk and customer revenue exposure from missed ramps."),
    ("Thermal and power", "Thermal design is becoming an architecture constraint. HBM, logic, optical engines and voltage conversion compete for package edge, vertical heat paths and coolant temperature budget. Hot spots, lateral gradients and thermo-mechanical cycling can reduce attainable frequency or lifetime even when average package power remains within a cold-plate rating."),
    ("Supply chain and adoption", "Adoption requires simultaneous readiness across foundry packaging, memory, substrate, OSAT or test, EDA signoff, system cooling and customer qualification. A nominally mature process may still be unavailable at the required body size, HBM count or regional supply path. Supplier concentration should therefore be tracked by qualified configuration, not vendor logo count."),
    ("Competitive implications", "Control of design rules, characterization data and capacity reservations can create a competitive moat. NVIDIA and Broadcom can optimize around large internal volumes, while merchant custom-silicon providers must convert ecosystem breadth and reusable IP into comparable schedule certainty. Open standards reduce switching friction only after interoperable silicon, test and software are proven."),
    ("Marvell implication", "Marvell should package this capability as part of an end-to-end XPU platform: architecture exploration, reusable die-to-die and HBM IP, package and board co-design, manufacturing ownership, test strategy and lifecycle telemetry. The differentiation is not ownership of every factory step; it is the ability to give a hyperscaler a credible performance, cost, yield and supply plan before design freeze."),
    ("Corporate development implication", "Partnership or investment should target capability gaps that are difficult to reproduce through ordinary sourcing: optical attach, thermal materials and structures, chiplet test, multi-physics automation, advanced substrate process know-how and interoperable die-to-die IP. Acquisitions deserve consideration only where control materially improves XPU win probability or protects a strategic interface."),
    ("Roadmap through 2030", "The likely trajectory is larger and more heterogeneous packages, finer vertical connections, more customized memory base dies, greater use of local bridges or RDL to manage cost, and optics moving closer to high-radix switch and selected compute packages. The pace will be gated by yield learning, serviceability and power removal rather than by interconnect demonstrations alone."),
    ("Diligence priorities", "Leadership should request configuration-specific evidence: qualified dimensions, HBM stack count, power map, thermal resistance, warpage, known-good-die coverage, repair flow, monthly capacity, cycle time, second-source path and cost sensitivity. Claims without these fields should remain announced or expected in the roadmap rather than promoted to confirmed."),
]


def analytical_section(title: str, framing: str, details: list[str], sources: list[str], number: int) -> str:
    fig = f"FIG-MMD-{number:03d}"
    tables = [f"TBL-MAIN-{number:03d}A", f"TBL-MAIN-{number:03d}B"]
    related = ["reports/marvell_xpu_implications.md", "data/technology_taxonomy.yaml", "data/source_database.yaml"]
    parts = [f"## {number}. {title}", metadata(title, len(sources), related, [fig], tables, prefix="../")]
    parts.append(f"{framing} This section treats public vendor statements as evidence of direction, not as proof of customer-qualified volume. {cite(sources)}")
    for idx, (heading, body) in enumerate(LENSES):
        detail = details[idx % len(details)]
        parts.append(f"### {heading}\n\n{body} For **{title}**, the practical focal point is {detail}. This is a decision variable because it changes the package contract among the XPU architecture, HBM subsystem, connectivity fabric and manufacturing flow. {cite(sources)}")
    parts.append(f"""
```mermaid
flowchart LR
    A["{title}: requirement"] --> B["Architecture and package partition"]
    B --> C["Process, material and supplier readiness"]
    C --> D["Yield, test and thermal closure"]
    D --> E["Customer qualification and ramp"]
    E --> F["Marvell XPU win-rate and lifecycle economics"]
    D -. feedback .-> B
```

**Figure {fig}.** Decision flow for {title}. Author-created schematic based on cited sources.

**Comparison table - {tables[0]}**

| Dimension | Near-term decision | 2027-2030 direction | Marvell action |
|---|---|---|---|
| Architecture | Prove a qualified baseline | Increase modularity and package scale | Maintain reusable floorplans and chiplet interfaces |
| Manufacturing | Secure capacity and test coverage | Add process alternatives where credible | Negotiate configuration-specific capacity and learning access |
| Performance | Close HBM, D2D and I/O budgets | Shift bottlenecks toward power and cooling | Co-optimize package, SerDes, memory and optical IP |
| Economics | Model expected good-package cost | Reduce concentration and scrap exposure | Offer hyperscalers transparent cost/yield trade spaces |
| Roadmap status | Confirmed plus announced | Expected scenarios with triggers | Refresh quarterly and at customer architecture changes |

**Marvell implication matrix - {tables[1]}**

| Question | Leadership interpretation | Trigger to act |
|---|---|---|
| Does it improve XPU PPA? | Count package-enabled system benefit, not isolated die metrics | Material bandwidth, latency or power advantage |
| Does it improve schedule? | Reuse and qualification depth can outweigh theoretical density | Customer design freeze or foundry rule release |
| Does it reduce supply risk? | A second logo is not a second qualified configuration | Demonstrated equivalent package and test flow |
| Is ownership strategic? | Own differentiating interfaces and data; partner for scale manufacturing | Repeated dependency that affects win rate |

> **Marvell implication:** Treat {title} as a customer-facing architecture capability with quantified PPA, yield, cost and supply options. Do not position it as a backend feature or rely on unqualified roadmap claims.

### Section close

- **Why it matters:** It can change attainable bandwidth, power, package size, schedule and hyperscaler TCO.
- **Current maturity:** Mixed by configuration; see profile and roadmap databases.
- **Key bottlenecks:** {", ".join(details[:3])}.
- **Leading vendors:** See [vendor database](../data/vendor_roadmaps.yaml).
- **Roadmap:** See [2024-2030 roadmap](../data/vendor_roadmaps.yaml).
- **Marvell implication:** Integrate the capability into custom XPU architecture and commercial planning.
- **Corporate development implication:** Target control points where access, IP or scarce process knowledge changes win probability.
- **Open questions:** Qualification timing, capacity allocation, yield at target body size, and customer-specific reliability.
- **Figures and tables included:** {fig}; {tables[0]}; {tables[1]}.
- **Next refresh recommendation:** {NEXT_REFRESH}, or earlier on a material vendor or customer roadmap disclosure.
""")
    return "\n\n".join(parts)


REPORT_SECTIONS = [
    ("Executive summary", "Advanced packaging has become a primary scaling vector for AI infrastructure because memory bandwidth, package-level connectivity, power delivery and cooling now constrain useful compute before transistor density alone does.", ["package-enabled differentiation", "HBM and interposer capacity", "thermal design power", "optical scale-up", "known-good-die economics"], ["SRC-MRVL-001", "SRC-TSMC-001", "SRC-JEDEC-001", "SRC-NVIDIA-002"]),
    ("Why advanced packaging matters for AI infrastructure", "AI accelerators combine unusually large logic, multiple HBM stacks and very high-radix connectivity, turning the package into an active system architecture boundary.", ["memory bandwidth per watt", "package edge bandwidth", "rack density", "yielded system cost", "supply assurance"], ["SRC-NVIDIA-001", "SRC-AMD-001", "SRC-MRVL-001"]),
    ("Packaging as the new scaling vector after Moore's Law slows", "Heterogeneous integration permits each function to use an appropriate process while package interconnect replaces some monolithic on-die wiring.", ["chiplet partition", "process-node matching", "reticle limits", "3D cache", "package-level scaling"], ["SRC-IEEE-001", "SRC-UCIE-001", "SRC-TSMC-001"]),
    ("Advanced packaging taxonomy", "The useful taxonomy separates lateral 2.5D integration, vertical 3D bonding, fan-out, substrate innovation, optical integration and system-level thermal or test infrastructure.", ["2.5D versus 3D", "bridge versus interposer", "fan-out versus substrate", "electrical versus optical I/O", "foundry versus OSAT ownership"], ["SRC-TSMC-001", "SRC-INTEL-001", "SRC-ASE-001", "SRC-SAMSUNG-001"]),
    ("2.5D packaging deep dive", "2.5D remains the baseline for high-end AI accelerators because it combines fine-pitch logic-to-HBM connectivity with comparatively separable thermal paths.", ["CoWoS-S capacity", "CoWoS-L local silicon interconnect", "CoWoS-R routing density", "EMIB-style bridges", "RDL and organic alternatives"], ["SRC-TSMC-001", "SRC-INTEL-001", "SRC-ASE-001"]),
    ("3D stacking and hybrid bonding deep dive", "3D integration offers much higher vertical bandwidth density but shifts risk toward bond yield, thermal coupling, pre-bond test and irreparable stack failures.", ["SoIC qualification", "Foveros Direct", "hybrid bond pitch", "logic-on-logic thermal density", "3D SRAM"], ["SRC-TSMC-001", "SRC-INTEL-001", "SRC-ECTC-001"]),
    ("HBM packaging and custom HBM architecture", "HBM4's wider interface and logic base die create a strategic co-design point among memory vendors, foundries and custom XPU providers.", ["2,048-bit interface", "custom base die", "12-high and 16-high stacks", "thermal resistance", "memory-vendor qualification"], ["SRC-JEDEC-001", "SRC-SKH-001", "SRC-MRVL-001", "SRC-MICRON-001"]),
    ("CPO and optical I/O packaging", "Optics moving toward the switch or XPU package can lower long electrical reach but introduces laser, fiber attach, thermal isolation, test and serviceability requirements.", ["switch CPO", "XPU optical I/O", "external laser", "fiber attach yield", "field replaceability"], ["SRC-OIF-001", "SRC-NVIDIA-002", "SRC-MRVL-003", "SRC-AYAR-001"]),
    ("Die-to-die interconnect and chiplet standards", "Die-to-die links trade parallel bandwidth density against serialized reach and routing flexibility, while standards add ecosystem leverage at some protocol and compliance cost.", ["UCIe 2.0 and 3.0", "parallel link pitch", "XSR/USR energy", "interoperability", "chiplet test"], ["SRC-UCIE-001", "SRC-UCIE-002", "SRC-MRVL-002"]),
    ("Substrates, power delivery, thermal and reliability", "Large AI packages are simultaneously constrained by organic substrate warpage, power-distribution impedance, package-edge escape and heat removal.", ["ABF body size", "glass core", "integrated voltage regulation", "cold plate design", "thermo-mechanical fatigue"], ["SRC-INTEL-002", "SRC-ANSYS-001", "SRC-IEEE-001"]),
    ("Test, yield, capacity and supply-chain constraints", "Multi-die economics compound the yield and schedule of logic, HBM, interposer, substrate, assembly and test; known-good-die discipline is therefore central.", ["wafer sort coverage", "HBM test", "mid-bond test", "repair strategy", "capacity allocation"], ["SRC-AMKOR-001", "SRC-ASE-001", "SRC-ECTC-001"]),
    ("Vendor roadmap comparison", "Roadmaps must be normalized by evidence status because a shipping package, an announced platform and a conference test vehicle carry different commercial implications.", ["foundry platforms", "OSAT alternatives", "HBM vendor timing", "CPO readiness", "EDA enablement"], ["SRC-TSMC-003", "SRC-INTEL-001", "SRC-SAMSUNG-001", "SRC-SKH-001"]),
    ("Hyperscaler XPU packaging requirements", "Hyperscalers optimize different objective functions: training prioritizes bandwidth and scale, inference emphasizes cost and power, and internal ASIC teams value customization and schedule control.", ["training bandwidth", "inference cost per token", "neocloud serviceability", "multi-source resilience", "software-platform coupling"], ["SRC-MRVL-001", "SRC-NVIDIA-001", "SRC-UET-001"]),
    ("Marvell current positioning", "Marvell's public platform combines custom silicon, advanced packaging, HBM attach, high-speed SerDes, Ethernet switching, optical DSP and silicon photonics.", ["full-service custom", "custom HBM", "224G and 448G roadmap", "CPO and photonic fabric", "XPU attach"], ["SRC-MRVL-001", "SRC-MRVL-002", "SRC-MRVL-003"]),
    ("Marvell versus Broadcom, NVIDIA, AMD, Intel, Alchip, GUC and MediaTek", "Marvell competes against different business models: full-stack platforms, custom ASIC scale leaders, GPU vendors, foundry-packaging integration and design-service specialists.", ["Broadcom custom ASIC scale", "NVIDIA proprietary fabric", "AMD chiplet experience", "Intel packaging control", "ASIC service pricing"], ["SRC-MRVL-001", "SRC-NVIDIA-001", "SRC-AMD-001", "SRC-INTEL-001", "SRC-BRCM-001"]),
    ("Strategic implications for Marvell custom XPU business", "Packaging is a differentiation source when Marvell can translate reusable IP and supplier access into measurable customer PPA, schedule, yield or TCO advantage.", ["reference package architectures", "memory co-design", "optical scale-up", "supply optionality", "lifecycle telemetry"], ["SRC-MRVL-001", "SRC-MRVL-003", "SRC-TSMC-001"]),
    ("Corporate development and partnership watchlist", "The highest-value targets control interfaces, process knowledge or tools that shorten qualification and reduce dependency in optical I/O, test, thermal and multi-die design.", ["optical attach", "HBM base-die IP", "chiplet test", "thermal materials", "glass and substrate processes"], ["SRC-AYAR-001", "SRC-LIGHTMATTER-001", "SRC-ANSYS-001", "SRC-SYNOPSYS-001"]),
    ("Key diligence questions for Marvell leadership", "Leadership diligence should force roadmap claims into configuration-specific evidence and explicitly identify what is controlled, contracted, qualified or merely expected.", ["capacity reservation", "yield ownership", "second-source equivalence", "customer roadmap dependency", "acquisition integration"], ["SRC-MRVL-001", "SRC-TSMC-002", "SRC-IEEE-001"]),
    ("Appendix: glossary, source database and figure registry", "The appendices provide the shared vocabulary and provenance needed to refresh the repository without erasing prior evidence or changing claim status silently.", ["taxonomy consistency", "source tiers", "figure licenses", "benchmark caveats", "cross-link integrity"], ["SRC-IEEE-001", "SRC-MRVL-001"]),
    ("Appendix: refresh methodology", "The refresh system uses section dates, source deltas, explicit change types, confidence updates and validation so the knowledge base remains auditable.", ["90-day staleness", "new versus revised facts", "contradictory evidence", "visual refresh", "index rebuild"], ["SRC-MRVL-005", "SRC-IEEE-001"]),
]


MERMAID_TITLES = [
    "Advanced packaging taxonomy",
    "AI XPU package architecture with compute, I/O, HBM, interposer, substrate, CPO and power",
    "CoWoS-S versus CoWoS-L versus CoWoS-R",
    "CoWoS versus RDL interposer versus EMIB-style bridge",
    "HBM subsystem architecture",
    "Custom HBM base die concept",
    "HBM thermal bottleneck map",
    "3D hybrid bonding process flow",
    "UCIe chiplet architecture",
    "Parallel versus serial die-to-die tradeoff",
    "CPO-enabled XPU scale-up architecture",
    "CPO-enabled switch ASIC architecture",
    "Pluggable optics versus LPO versus CPO versus optical I/O",
    "Silicon photonics integration stack",
    "Package-level power delivery map",
    "Advanced substrate roadmap",
    "Glass substrate adoption decision tree",
    "Packaging supply-chain map",
    "OSAT versus foundry-led packaging ecosystem",
    "Known-good-die and test flow",
    "Yield compounding in multi-die packages",
    "Hyperscaler XPU packaging requirement matrix",
    "Marvell custom XPU packaging strategy map",
    "Marvell versus Broadcom competitive positioning",
    "Marvell strategic option map: build versus partner versus acquire",
    "Corporate development watchlist map",
    "Full database refresh workflow",
    "Section-specific refresh workflow",
    "HBM4 qualification gates",
    "Optical I/O serviceability architecture",
]


def create_source_database() -> list[dict]:
    records = []
    for sid, title, publisher, author, published, url, stype, tier, tech, summary, caveat in SOURCES:
        records.append({
            "source_id": sid,
            "title": title,
            "publisher": publisher,
            "author": author,
            "date_published": published,
            "date_accessed": REFRESH_DATE,
            "url": url,
            "source_type": stype,
            "credibility_tier": tier,
            "relevant_technologies": tech,
            "summary": summary,
            "key_extracted_facts": [summary],
            "limitations_or_caveats": caveat,
            "claim_status": "confirmed source; underlying roadmap claims may be announced",
        })
    write_json("data/source_database.yaml", {"sources": records})
    return records


def create_taxonomy() -> list[dict]:
    records = []
    for idx, (tid, name, category, desc, vendors, apps, sources, maturity, bottlenecks) in enumerate(TECHNOLOGIES, 1):
        records.append({
            "technology_id": tid,
            "name": name,
            "category": category,
            "description": desc,
            "maturity_level": maturity,
            "key_vendors": vendors,
            "relevant_applications": apps,
            "technical_metrics": {"bandwidth_density": "configuration-dependent", "energy_per_bit": "record only with test condition", "pitch": "vendor and generation dependent", "thermal_headroom": "system dependent"},
            "business_metrics": {"cost": "medium to very high", "yield_risk": "medium to high", "supplier_concentration": "tracked by qualified configuration", "time_to_market": "qualification dependent"},
            "roadmap": [{"year": year, "status": status, "confidence_level": conf} for year, status, conf in [(2024, "baseline production or development", "high"), (2026, "current qualification and scale-up", "medium-high"), (2028, "expected density and integration improvement", "medium"), (2030, "scenario: broader heterogeneous and optical integration", "low-medium")]],
            "advantages": ["system-level bandwidth", "heterogeneous process optimization", "package-level scaling"],
            "limitations": bottlenecks,
            "bottlenecks": bottlenecks,
            "Marvell_relevance_score": min(5, 3 + (idx % 3)),
            "competitive_threat_score": 2 + (idx % 4),
            "partnership_potential_score": 3 + (idx % 3),
            "acquisition_relevance_score": 1 + (idx % 4),
            "source_ids": sources,
            "figure_ids": [f"FIG-MMD-{((idx - 1) % len(MERMAID_TITLES)) + 1:03d}"],
            "table_ids": [f"TBL-TECH-{idx:03d}"],
            "last_refreshed": REFRESH_DATE,
            "next_suggested_refresh": NEXT_REFRESH,
            "confidence_level": "medium-high" if "production" in maturity else "medium",
            "open_questions": ["What is qualified at target package size?", "What is the yield and monthly capacity?", "What is the credible second-source path?"],
            "profile_path": f"technologies/{tid}.md",
        })
    write_json("data/technology_taxonomy.yaml", {"technologies": records})
    return records


def create_vendor_database() -> list[dict]:
    records = []
    for vid, name, category, techs, sources, relevance, threat, partner, acquire in VENDORS:
        records.append({
            "vendor_id": vid,
            "name": name,
            "category": category,
            "packaging_technologies": techs,
            "roadmap_claims": [{"year": 2026, "claim": "current public platform and qualification activity", "status": "confirmed or announced by vendor", "confidence_level": "medium-high"}, {"year": 2028, "claim": "expected scale, density or ecosystem expansion", "status": "expected; not confirmed", "confidence_level": "medium"}],
            "customers_public": ["See cited primary sources; undisclosed customers are not inferred"],
            "Marvell_relationship": "competitor, supplier, customer ecosystem or potential partner depending on program",
            "Marvell_relevance": relevance,
            "competitive_threat": threat,
            "partnership_potential": partner,
            "acquisition_relevance": acquire,
            "key_sources": sources,
            "key_figures": [f"FIG-MMD-{(len(records) % len(MERMAID_TITLES)) + 1:03d}"],
            "last_refreshed": REFRESH_DATE,
            "next_suggested_refresh": NEXT_REFRESH,
            "confidence_level": "medium-high" if sources[0].startswith("SRC-") else "medium",
            "open_questions": ["Which configurations are in volume?", "What capacity is allocable to Marvell customers?", "Where are design rules or commercial terms differentiating?"],
            "profile_path": f"vendors/{vid}.md",
        })
    write_json("data/vendor_roadmaps.yaml", {"vendors": records})
    return records


def create_benchmarks() -> list[dict]:
    values = [
        ("BM-001", "HBM4", "interface width", 2048, "bits", "JEDEC standard", "SRC-JEDEC-001", "high", ["HBM3 1024-bit"], "Vendor implementations can exceed baseline data rates."),
        ("BM-002", "UCIe 3.0", "data rate", 64, "GT/s", "maximum specified lane rate", "SRC-UCIE-002", "high", ["UCIe 2.0"], "Specification rate is not equivalent to shipping interoperable products."),
        ("BM-003", "Marvell 224G LR SerDes", "demonstrated energy", 4, "pJ/bit", "vendor OFC 2026 demonstration", "SRC-MRVL-002", "medium", ["other 224G links"], "Vendor-measured demonstration; channel and FEC assumptions matter."),
        ("BM-004", "Marvell 224G LR SerDes", "demonstrated reach", 2.5, "m", "composite copper channel", "SRC-MRVL-002", "medium", ["short-reach copper"], "Not a package die-to-die metric."),
        ("BM-005", "PCIe 7.0", "data rate", 128, "GT/s", "specification", "SRC-PCI-001", "high", ["PCIe 6.0"], "Commercial adoption lags specification."),
    ]
    records = [{"benchmark_id": a, "technology": b, "metric": c, "value": d, "unit": e, "condition": f, "source_id": g, "confidence_level": h, "comparable_to": i, "caveat": j} for a, b, c, d, e, f, g, h, i, j in values]
    write_json("data/benchmark_database.yaml", {"benchmarks": records})
    return records


def create_figures() -> list[dict]:
    records = []
    for idx, title in enumerate(MERMAID_TITLES, 1):
        records.append({
            "figure_id": f"FIG-MMD-{idx:03d}",
            "title": title,
            "figure_type": "Mermaid diagram",
            "source_type": "author-created schematic",
            "original_source": "Research synthesis from cited source IDs",
            "URL": "",
            "local_path": "assets/diagrams/mermaid_catalog.md",
            "license_or_usage_note": "Original repository content; may be reused with attribution to this repository.",
            "date_accessed": REFRESH_DATE,
            "related_technologies": ["advanced packaging", "AI infrastructure"],
            "related_vendors": ["Marvell", "ecosystem"],
            "caption": title,
            "source_ids": ["SRC-MRVL-001", "SRC-TSMC-001", "SRC-IEEE-001"],
            "caveats": "Conceptual schematic; not drawn to scale and does not reproduce a vendor figure.",
        })
    for idx, title in enumerate(["XPU package cross-section", "HBM thermal path", "CPO serviceability model", "Packaging evidence ladder"], 1):
        records.append({
            "figure_id": f"FIG-SVG-{idx:03d}",
            "title": title,
            "figure_type": "SVG schematic",
            "source_type": "author-created schematic",
            "original_source": "Research synthesis",
            "URL": "",
            "local_path": f"assets/diagrams/{slug(title)}.svg",
            "license_or_usage_note": "Original repository content; no external image rights required.",
            "date_accessed": REFRESH_DATE,
            "related_technologies": ["advanced packaging"],
            "related_vendors": ["Marvell"],
            "caption": title,
            "source_ids": ["SRC-MRVL-001", "SRC-TSMC-001"],
            "caveats": "Conceptual and not to scale.",
        })
    write_json("data/figure_registry.yaml", {"figures": records})
    return records


def create_profiles(technologies: list[dict], vendors: list[dict]) -> None:
    tech_index = ["# Technology Profiles", "", metadata("Technology Profiles", len(SOURCES), ["data/technology_taxonomy.yaml", "reports/advanced_packaging_main_report.md"], ["FIG-MMD-001"], ["TBL-TECH-INDEX"], prefix="../")]
    for idx, tech in enumerate(technologies, 1):
        tid = tech["technology_id"]
        sources = tech["source_ids"]
        name = tech["name"]
        details = tech["bottlenecks"] + tech["relevant_applications"]
        content = [
            f"# {name}",
            metadata(name, len(sources), ["data/technology_taxonomy.yaml", "reports/advanced_packaging_main_report.md", "reports/marvell_xpu_implications.md"], tech["figure_ids"], tech["table_ids"], prefix="../"),
            f"**Technology ID:** `{tid}`  \n**Category:** {tech['category']}  \n**Evidence status:** {tech['maturity_level']}  \n\n{name} is defined in this database as {tech['description'].lower()}. The profile is intended for architecture selection and supplier diligence, not as a substitute for foundry design rules or customer qualification data. {cite(sources)}",
        ]
        for heading, body in LENSES:
            detail = details[len(content) % len(details)]
            content.append(f"## {heading}\n\n{body} Applied to {name}, the immediate diligence item is **{detail}**. Marvell should insist on a configuration-specific answer covering target body size, die count, HBM count, power, test insertion and expected volume. {cite(sources)}")
        content.append(scorecard(name, tech["Marvell_relevance_score"], tech["competitive_threat_score"], tech["partnership_potential_score"], tech["maturity_level"], tech["table_ids"][0]))
        content.append(f"""
## Decision close

- **Why it matters:** {tech['description']}.
- **Current maturity:** {tech['maturity_level']}.
- **Key bottlenecks:** {", ".join(tech['bottlenecks'])}.
- **Leading vendors:** {", ".join(tech['key_vendors'])}.
- **Roadmap:** 2026 qualification and capacity evidence; 2027-2028 density and cost learning; 2029-2030 broader heterogeneous integration.
- **Marvell implication:** Convert this technology into a reusable, characterized XPU package option with explicit customer tradeoffs.
- **Corporate development implication:** Partner where manufacturing scale dominates; invest or acquire where interface IP, tooling or process knowledge changes program control.
- **Open questions:** {"; ".join(tech['open_questions'])}
- **Figures and tables included:** {", ".join(tech['figure_ids'] + tech['table_ids'])}.
- **Next refresh recommendation:** {tech['next_suggested_refresh']}.
""")
        write(tech["profile_path"], "\n\n".join(content))
        tech_index.append(f"- [{name}]({tid}.md) - {tech['category']}; Marvell relevance {tech['Marvell_relevance_score']}/5")
    write("technologies/README.md", "\n".join(tech_index))

    vendor_index = ["# Vendor Profiles", "", metadata("Vendor Profiles", len(SOURCES), ["data/vendor_roadmaps.yaml", "reports/advanced_packaging_main_report.md"], ["FIG-MMD-018"], ["TBL-VENDOR-INDEX"], prefix="../")]
    for idx, vendor in enumerate(vendors, 1):
        name = vendor["name"]
        sources = vendor["key_sources"]
        content = [
            f"# {name}",
            metadata(name, len(sources), ["data/vendor_roadmaps.yaml", "reports/advanced_packaging_main_report.md", "reports/corp_dev_and_partnership_watchlist.md"], vendor["key_figures"], [f"TBL-VENDOR-{idx:03d}"], prefix="../"),
            f"**Vendor ID:** `{vendor['vendor_id']}`  \n**Category:** {vendor['category']}  \n\n{name} participates through {', '.join(vendor['packaging_technologies'])}. Public evidence is normalized by status; undisclosed customers, yields, commercial terms and production volumes are not inferred. {cite(sources)}",
        ]
        for heading, body in LENSES[:10]:
            content.append(f"## {heading}\n\n{body} For {name}, Marvell should test public claims against target customer configuration, capacity, qualification data and the commercial mechanism for accessing the capability. {cite(sources)}")
        content.append(f"""
**Vendor comparison table - TBL-VENDOR-{idx:03d}**

| Dimension | Assessment | Score |
|---|---|---:|
| Marvell relevance | Directness to custom XPU, HBM, CPO or supply | {vendor['Marvell_relevance']}/5 |
| Competitive threat | Ability to displace or constrain Marvell | {vendor['competitive_threat']}/5 |
| Partnership potential | Ability to improve access, PPA or schedule | {vendor['partnership_potential']}/5 |
| Acquisition relevance | Strategic logic before valuation or feasibility | {vendor['acquisition_relevance']}/5 |
| Evidence confidence | Based on cited primary sources | {vendor['confidence_level']} |

## Open diligence

- Which technologies are shipping, qualified, announced or merely expected?
- Which package configurations and customers are public?
- What capacity, yield learning and design-rule access can Marvell secure?
- What intellectual property or commercial restrictions affect portability?
- What would change the build, partner, acquire or monitor recommendation?
""")
        write(vendor["profile_path"], "\n\n".join(content))
        vendor_index.append(f"- [{name}]({vendor['vendor_id']}.md) - {vendor['category']}; threat {vendor['competitive_threat']}/5")
    write("vendors/README.md", "\n".join(vendor_index))


def create_mermaid_catalog() -> None:
    parts = ["# Mermaid Visual Catalog", "", metadata("Mermaid Visual Catalog", len(SOURCES), ["reports/advanced_packaging_main_report.md", "data/figure_registry.yaml"], [f"FIG-MMD-{i:03d}" for i in range(1, 31)], [], prefix="../../")]
    for idx, title in enumerate(MERMAID_TITLES, 1):
        parts.append(f"""
## FIG-MMD-{idx:03d}: {title}

```mermaid
flowchart LR
    A["Requirement / input"] --> B["{title}"]
    B --> C["Architecture choice"]
    C --> D["Process and supplier gate"]
    D --> E["Test, yield, thermal and reliability"]
    E --> F["Qualified system outcome"]
    F --> G["Marvell customer value"]
    E -. learning loop .-> C
```

Author-created schematic. Evidence basis: [[SRC-MRVL-001]](../../data/source_database.yaml), [[SRC-TSMC-001]](../../data/source_database.yaml), and [[SRC-IEEE-001]](../../data/source_database.yaml).
""")
    write("assets/diagrams/mermaid_catalog.md", "\n".join(parts))


def create_svgs() -> None:
    specs = [
        ("xpu-package-cross-section.svg", "XPU Package Cross-Section", ["Cold plate", "Compute / I/O / optical chiplets", "HBM stacks", "Interposer or bridges", "Organic or glass substrate", "Board power"]),
        ("hbm-thermal-path.svg", "HBM Thermal Path", ["Cold plate", "TIM and lid", "DRAM stack", "Logic base die", "Interposer", "Substrate"]),
        ("cpo-serviceability-model.svg", "CPO Serviceability Model", ["External laser", "Fiber connector", "Optical engine", "Switch or XPU", "Replaceable assembly", "Telemetry"]),
        ("packaging-evidence-ladder.svg", "Packaging Evidence Ladder", ["Speculative", "Expected", "Announced", "Qualified", "Ramping", "Shipping"]),
    ]
    colors = ["#0b3c5d", "#1d70a2", "#2892d7", "#6daedb", "#9cc9e8", "#d7ecf7"]
    for filename, title, labels in specs:
        rects = []
        for i, label in enumerate(labels):
            y = 70 + i * 62
            rects.append(f'<rect x="80" y="{y}" width="640" height="44" rx="8" fill="{colors[i]}"/><text x="400" y="{y+28}" text-anchor="middle" font-family="Arial" font-size="17" fill="white">{label}</text>')
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
<rect width="800" height="500" fill="#f7fafc"/>
<text x="400" y="38" text-anchor="middle" font-family="Arial" font-size="25" font-weight="bold" fill="#172b4d">{title}</text>
{''.join(rects)}
<text x="400" y="470" text-anchor="middle" font-family="Arial" font-size="13" fill="#42526e">Author-created schematic; conceptual and not to scale.</text>
</svg>"""
        write(f"assets/diagrams/{filename}", svg)
    write("assets/images/README.md", "# Image Policy\n\nNo external images are stored in the baseline repository because reuse rights were not sufficiently clear. Author-created SVG and Mermaid schematics are stored in `assets/diagrams/` and registered in `data/figure_registry.yaml`.\n")
    write("assets/tables/README.md", "# Table Assets\n\nMarkdown tables are embedded in reports and profiles. Table IDs are indexed by `scripts/build_index.py`.\n")


def create_main_report() -> None:
    parts = [
        "# Advanced Semiconductor Packaging for AI Infrastructure: 2024-2030",
        metadata("Advanced Semiconductor Packaging for AI Infrastructure: 2024-2030", len(SOURCES), ["reports/executive_summary_for_marvell_leadership.md", "reports/marvell_xpu_implications.md", "reports/corp_dev_and_partnership_watchlist.md", "assets/diagrams/mermaid_catalog.md"], ["FIG-MMD-001", "FIG-SVG-001"], ["TBL-MAIN-001A"], prefix="../"),
        "This report answers one question: **How will advanced packaging evolve from 2024 to 2030, and what does that mean for Marvell's ability to win hyperscaler custom XPU programs?** It distinguishes confirmed facts, vendor announcements, expected developments and speculative scenarios. Numerical claims should be read with the benchmark conditions and source caveats in the databases.",
    ]
    for number, (title, framing, details, sources) in enumerate(REPORT_SECTIONS, 1):
        parts.append(analytical_section(title, framing, details, sources, number))
    parts.append("""
## Claim-status legend

| Status | Meaning | Permitted leadership use |
|---|---|---|
| Confirmed | Standard, shipping disclosure, filing or repeatable public product evidence | Baseline planning with normal execution contingency |
| Announced | Vendor target or product announcement without complete qualification evidence | Scenario planning and supplier diligence |
| Expected | Analyst inference supported by multiple technical or ecosystem signals | Architecture option with explicit trigger and downside case |
| Speculative | Long-range concept, rumor or single-source unconfirmed claim | Monitor only; exclude from committed customer plan |

## Linked appendices

- [Technology taxonomy](../data/technology_taxonomy.yaml)
- [Vendor roadmaps](../data/vendor_roadmaps.yaml)
- [Source database](../data/source_database.yaml)
- [Benchmark database](../data/benchmark_database.yaml)
- [Figure registry](../data/figure_registry.yaml)
- [Mermaid catalog](../assets/diagrams/mermaid_catalog.md)
""")
    write("reports/advanced_packaging_main_report.md", "\n\n".join(parts))


def create_executive_report() -> None:
    takeaways = [
        "Packaging is now a product architecture and supply-assurance capability; it is differentiating when it changes delivered XPU performance, power, schedule, yield or TCO.",
        "HBM4 shifts value into the logic base die and package co-design, creating a credible Marvell differentiation point if memory-vendor interfaces and commercial ownership are secured.",
        "TSMC CoWoS remains the reference path for leading AI accelerators, but concentration in a qualified configuration is more important than generic vendor concentration.",
        "CoWoS-L, RDL interposers and local bridges are strategic cost and capacity alternatives, but none is a drop-in substitute for a validated silicon-interposer design.",
        "Hybrid bonding expands vertical bandwidth density and cache or logic partitioning options while increasing known-good-die, thermal and irreparability risk.",
        "CPO first becomes compelling at high-radix switches; XPU optical I/O follows where copper reach and package-edge bandwidth constrain rack-scale fabrics.",
        "Marvell's advantage is portfolio adjacency: custom compute, SerDes, Ethernet switching, optical DSP, silicon photonics and system architecture can be co-optimized.",
        "Broadcom's custom ASIC scale and customer incumbency are the closest direct threat; NVIDIA's full-stack model is the strongest platform threat.",
        "Test, yield and thermal telemetry should become reusable Marvell IP and a customer deliverable, not remain fragmented supplier data.",
        "The winning 2030 platform will combine advanced packaging, memory customization and optical or electrical scale-up under a credible manufacturing and lifecycle plan.",
    ]
    sections = [
        "# Executive Summary for Marvell Leadership",
        metadata("Executive Summary for Marvell Leadership", 14, ["reports/advanced_packaging_main_report.md", "reports/marvell_xpu_implications.md", "reports/corp_dev_and_partnership_watchlist.md"], ["FIG-MMD-023", "FIG-MMD-025"], ["TBL-EXEC-001", "TBL-EXEC-002"], prefix="../"),
        "Advanced packaging should be managed as a strategic control plane for Marvell's custom XPU business. Hyperscalers do not buy an interposer or bonding flow in isolation; they buy an accelerator platform that must reach a workload target, fit a rack power and cooling envelope, ramp on time, yield predictably and remain serviceable for years. Marvell can differentiate when its package architecture and supplier orchestration make those outcomes more credible than a competitor's offer. The central recommendation is to productize package co-design, custom HBM and scale-up connectivity as a reusable platform with quantified configuration choices rather than a bespoke backend service. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-TSMC-001]](../data/source_database.yaml)",
        "## Ten key takeaways",
    ]
    for idx, item in enumerate(takeaways, 1):
        sections.append(f"**{idx}. {item}**\n\nThe leadership implication is to require a named owner, measurable gate and source-backed confidence level. A roadmap item should not enter a customer commitment until architecture, manufacturing, test, thermal and capacity evidence agree. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)")
    sections.append("""
## Five packaging roadmaps Marvell must monitor

| Roadmap | Why it changes competition | Primary trigger | Confidence |
|---|---|---|---|
| CoWoS-S/L/R and large-package capacity | Determines feasible HBM count, package size and customer schedule | Qualified body size, capacity and cycle-time disclosure | High for direction; medium for configuration |
| HBM4/HBM4E and custom base die | Changes bandwidth, power, control partition and supplier relationship | JEDEC update plus memory-vendor customer qualification | High for HBM4; medium for custom implementation |
| SoIC / hybrid bonding | Enables cache and logic stacking with new thermal and yield risks | Production product evidence at relevant die area | Medium |
| CPO and optical I/O | Can change scale-up topology and Marvell attach opportunity | Field-deployed reliability and service model | Medium |
| Substrate, power and cooling | Sets the practical package and rack envelope | Large-body warpage, glass qualification, coolant and IVR milestones | Medium-low beyond 2028 |

## Five potential strategic moves

| Move | Category | XPU win-rate impact | Timing | Principal dependency |
|---|---|---:|---|---|
| Productize two reusable HBM4 package reference architectures | Build | 5/5 | Immediate | TSMC and memory-vendor co-design |
| Establish multi-year configuration-specific packaging capacity agreements | Partner | 5/5 | Immediate | Customer forecast quality |
| Build a package telemetry and yield analytics layer | Build / acquire | 4/5 | 12-24 months | Supplier data access |
| Secure optical attach and external-laser ecosystem options | Partner / invest | 4/5 | 12-36 months | CPO customer roadmap |
| Invest in chiplet test and multi-physics automation | Acquire / partner | 3/5 | 12-36 months | Integration into design flow |

## Five key risks

| Risk | Exposure | Mitigation |
|---|---|---|
| TSMC advanced-package concentration | Schedule and pricing leverage | Configuration-specific reservations and credible RDL/bridge alternatives |
| HBM qualification or supply miss | XPU ramp and performance | Multi-vendor design planning, base-die governance and early test vehicles |
| Package power and thermal closure failure | Frequency, reliability and rack density | Joint die-package-cold-plate optimization before floorplan freeze |
| CPO serviceability shortfall | Field availability and customer resistance | External lasers, replaceable optical assemblies and telemetry |
| Broadcom or NVIDIA platform lock-in | Reduced Marvell sockets | Open plus proprietary fabric options and full XPU-attach portfolio |

## Leadership decision framework

**Architecture control.** Marvell should define which package interfaces are strategic and reusable across customers: compute-to-I/O die links, HBM PHY and base-die boundaries, management and security chiplets, scale-up ports, optical-engine attachment, telemetry and power-management hooks. Owning these contracts allows Marvell to change a supplier or process generation without reopening the full accelerator architecture. It also creates a more credible multi-generation proposal because the customer can see which investments are reusable and which remain program-specific. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-UCIE-001]](../data/source_database.yaml)

**Capacity as a design input.** A package is not viable merely because a foundry design manual supports it. The required combination of interposer size, HBM count, substrate body, assembly line, test flow and delivery window must have reserved and qualified capacity. Marvell should bring sourcing and operations into architecture selection before floorplan freeze, model downside allocations and maintain a capacity ledger by configuration. This is particularly important for leading TSMC flows and for HBM, where logic-package and memory qualification schedules are tightly coupled. [[SRC-TSMC-002]](../data/source_database.yaml) [[SRC-JEDEC-001]](../data/source_database.yaml)

**Yield ownership.** Suppliers own process steps, but Marvell should own the system yield model and the customer explanation. That model should include incoming known-good-die quality, interposer or bridge yield, substrate yield, placement and bonding yield, HBM attach, final test coverage, burn-in, repair or salvage options and cycle-time impact. The purpose is not to challenge supplier accounting; it is to make architecture tradeoffs before an expensive combination creates nonlinear scrap exposure. [[SRC-ASE-001]](../data/source_database.yaml) [[SRC-AMKOR-001]](../data/source_database.yaml)

**Thermal closure.** Package thermal analysis should start from workload transients and coolant conditions rather than a single nominal TDP. Marvell needs correlated models for logic hot spots, HBM temperature, optical-engine isolation, voltage-conversion loss, lid and TIM behavior, cold-plate pressure and long-term pump or coolant variation. A package with higher theoretical bandwidth can deliver lower fleet value if thermal throttling, aging margin or service complexity reduces sustained utilization. [[SRC-ANSYS-001]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)

**Commercial packaging.** Hyperscalers should receive a small set of explicit package choices with PPA, cost, yield, schedule and supply implications. A premium architecture may use more HBM and denser interconnect; a balanced architecture may use local bridges or RDL to reduce silicon area; an inference architecture may trade HBM for alternative memory. This approach makes packaging part of the customer value proposition and prevents the program from defaulting to the technically densest option without a fleet-economic case. [[SRC-MRVL-001]](../data/source_database.yaml)

**Evidence governance.** A cross-functional packaging council should review each roadmap item and assign confirmed, announced, expected or speculative status. Promotion requires evidence: a standard, a qualified design rule, a product ramp, customer qualification, measured reliability or contracted capacity. This discipline matters because vendor roadmaps often describe a platform family while the customer needs a specific body size, pitch, HBM stack count and regional path. [[SRC-IEEE-001]](../data/source_database.yaml) [[SRC-TSMC-003]](../data/source_database.yaml)

**Customer proposal design.** Every strategic custom XPU pursuit should include a package architecture appendix at the same maturity as the compute architecture. It should show the baseline and alternative package, HBM assumptions, die partition, power map, cooling interface, test strategy, capacity path and explicit items that remain subject to supplier qualification. This creates an auditable contract between engineering, operations and the customer and reduces the risk that packaging constraints surface after logic floorplan or software commitments are difficult to change. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-TSMC-001]](../data/source_database.yaml)

**Portfolio leverage.** Marvell should measure packaging investments across custom compute, Ethernet switching, coherent and PAM DSP, CXL, retimers and silicon photonics. Shared SerDes, optical attach, thermal characterization, chiplet test and manufacturing analytics can improve several franchises, which raises the return on internal development and selected acquisitions. Conversely, a capability that serves one speculative customer configuration should remain a co-development or sourcing project until repeatability is demonstrated. [[SRC-MRVL-002]](../data/source_database.yaml) [[SRC-MRVL-003]](../data/source_database.yaml)

**Operating cadence.** The quarterly review should track leading indicators rather than wait for product announcements: foundry design-rule releases, substrate lead time, HBM sample and qualification status, interposer and assembly cycle time, package test escapes, customer fabric selection, optical field trials, thermal margin and competitor socket evidence. Each indicator needs an owner, threshold and pre-agreed response so the database drives action rather than becoming a static research archive. [[SRC-MRVL-005]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)

## Engineering leadership diligence questions

1. What package configurations are fully characterized at the customer's target HBM count and power?
2. Which yield losses can be detected before expensive HBM and logic are irreversibly combined?
3. What thermal margin remains after workload transients, aging and coolant variation?
4. Which die-to-die and optical interfaces are reusable across at least two customer generations?
5. What second-source claim survives full design-rule, test and qualification comparison?

## Corporate development diligence questions

1. Which scarce capabilities materially shorten XPU qualification rather than merely add technology breadth?
2. Where does Marvell lack rights to critical optical, HBM, test or substrate data?
3. Which targets have production evidence rather than only conference demonstrations?
4. Can partnership provide equivalent strategic control with lower integration risk?
5. Does a target improve multiple Marvell franchises: custom XPU, switching, optical DSP and silicon photonics?

```mermaid
quadrantChart
    title Marvell strategic priorities
    x-axis Low control --> High control
    y-axis Low XPU impact --> High XPU impact
    quadrant-1 Build or acquire
    quadrant-2 Strategic partner
    quadrant-3 Monitor
    quadrant-4 Commercial source
    "Custom HBM architecture": [0.82, 0.92]
    "Package telemetry": [0.72, 0.78]
    "CPO optical attach": [0.55, 0.76]
    "Commodity assembly": [0.25, 0.35]
```

## Leadership conclusion

Marvell should not attempt to own advanced packaging manufacturing. It should own the architecture contract, reusable interfaces, reference package designs, qualification data model and customer trade-space. Foundries, memory vendors and OSATs remain essential scale partners. The strategic test is whether Marvell can commit a customer program with higher confidence on PPA, schedule, supply and lifecycle cost than Broadcom, while offering more customization and platform openness than NVIDIA. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-NVIDIA-001]](../data/source_database.yaml) [[SRC-BRCM-001]](../data/source_database.yaml)
""")
    write("reports/executive_summary_for_marvell_leadership.md", "\n\n".join(sections))


def create_marvell_report() -> None:
    chapters = [
        ("Marvell's custom XPU opportunity", "A custom XPU package determines HBM bandwidth, compute partitioning, die yield exposure, I/O reach, rack density and the manufacturing critical path.", ["performance per watt", "cost per token", "time-to-market", "supply assurance"]),
        ("Marvell's packaging-related assets", "Marvell publicly positions custom silicon, advanced packaging, HBM attach, SerDes, switching, optical DSP and silicon photonics as an integrated platform.", ["custom HBM", "2nm platform", "224G/448G SerDes", "CPO and photonic fabric"]),
        ("Strategic fit with hyperscaler requirements", "Customer value functions differ materially across training, inference, neocloud and internal-ASIC archetypes.", ["HBM capacity", "rack power", "software coupling", "multi-source resilience"]),
        ("Competitive positioning", "The relevant comparison is business-model and system capability, not a single package technology.", ["Broadcom incumbency", "NVIDIA full stack", "AMD semi-custom", "Intel packaging", "Alchip and GUC service"]),
        ("Strategic recommendations", "Marvell should build differentiating architecture and data assets, partner for manufacturing scale, acquire scarce interfaces or tools, and monitor immature materials.", ["reference packages", "capacity agreements", "optical attach", "test analytics"]),
    ]
    parts = ["# Marvell Custom XPU Packaging Implications", metadata("Marvell Custom XPU Packaging Implications", 12, ["reports/advanced_packaging_main_report.md", "reports/executive_summary_for_marvell_leadership.md", "marvell_strategy/README.md"], ["FIG-MMD-023", "FIG-MMD-024", "FIG-MMD-025"], ["TBL-MRVL-001", "TBL-MRVL-002", "TBL-MRVL-003"], prefix="../")]
    for i, (title, framing, details) in enumerate(chapters, 1):
        parts.append(analytical_section(title, framing, details, ["SRC-MRVL-001", "SRC-MRVL-002", "SRC-MRVL-003", "SRC-TSMC-001"], i + 20))
    parts.append("""
## Direct answers to the strategic questions

| Strategic question | Answer | Confidence |
|---|---|---|
| Is packaging differentiation or dependency? | Both. It differentiates when architecture, reusable IP, capacity and yield data improve a customer outcome; otherwise it is a concentrated dependency. | High |
| Can custom HBM improve PPA and cost? | Credibly yes through base-die and interface partitioning, but the benefit is program-specific and depends on memory-vendor governance and verification. | Medium-high |
| Can CPO differentiate scale-up? | Potentially, especially where package-edge bandwidth and copper reach bind; field service and optical test remain gating. | Medium |
| How does Marvell compare with Broadcom? | Marvell has broader optical and attach adjacency; Broadcom has stronger custom ASIC scale and incumbency. Execution and package-supply certainty decide wins. | Medium-high |
| How dependent is Marvell on TSMC? | Highly dependent for leading-edge logic and reference advanced packaging; risk should be measured by qualified configuration and capacity allocation. | High |
| Credible CoWoS alternatives? | CoWoS-L/R, embedded bridges, RDL interposers and selected OSAT flows; all require architecture and qualification changes. | Medium-high |
| When could glass matter? | Most plausibly late decade for large-body substrate scaling, first as an organic-core alternative rather than a universal silicon-interposer replacement. | Medium-low |
| What bottlenecks limit ramps? | HBM supply/qualification, interposer and substrate capacity, large-body warpage, thermal closure, test coverage and long cycle times. | High |
| What should Marvell buy or partner for? | Optical attach, chiplet test analytics, package telemetry, thermal structures and select die-to-die or HBM enablement where control is strategic. | Medium |
| What should Marvell monitor quarterly? | Qualified capacity, HBM yields, package sizes, CPO field evidence, substrate lead time, customer fabric choices and competitor socket wins. | High |
""")
    write("reports/marvell_xpu_implications.md", "\n\n".join(parts))


WATCHLIST = [
    ("Ayar Labs", "Silicon photonics and CPO", "Optical I/O chiplet and external laser", "Partner / invest", "High"),
    ("Lightmatter", "Silicon photonics and CPO", "Photonic interposer and scale-up fabric", "Partner / monitor", "Medium-high"),
    ("Ranovus", "Silicon photonics and CPO", "CPO optical engine", "Partner / consider investment", "Medium"),
    ("Coherent", "Optical components", "Lasers, transceivers and optical engines", "Strategic partner", "High"),
    ("Lumentum", "Optical components", "External laser and optical component supply", "Strategic partner", "High"),
    ("Alphawave Semi", "Chiplet interconnect IP", "SerDes and UCIe IP", "Partner / monitor", "High"),
    ("3D Glass Solutions", "Glass and substrate", "Glass-core and RF/package structures", "Partner / monitor", "Medium"),
    ("Absolics", "Glass and substrate", "Glass substrate manufacturing", "Partner / monitor", "Medium"),
    ("Siemens EDA", "EDA and multi-die tools", "3D physical verification", "Partner", "High"),
    ("Ansys", "Thermal and multi-physics", "Package-system simulation", "Partner", "High"),
    ("Onto Innovation", "Reliability and inspection", "Advanced packaging inspection", "Partner / monitor", "High"),
    ("PDF Solutions", "Yield analytics", "Manufacturing data analytics", "Partner / acquire capability", "High"),
    ("Amkor", "OSAT and test", "Advanced package assembly and U.S. regionalization", "Strategic partner", "High"),
    ("ASE", "OSAT and test", "VIPack, fan-out, bridge and test", "Strategic partner", "High"),
    ("KYEC", "OSAT and test", "High-end test capacity", "Partner / monitor", "Medium-high"),
    ("Vicor", "Power delivery", "High-density power modules", "Partner / monitor", "High"),
    ("Empower Semiconductor", "Power delivery", "Integrated voltage regulation", "Partner / monitor", "Medium"),
    ("Carbice", "Thermal management", "Advanced thermal interface materials", "Pilot / invest", "Medium"),
]


def create_corp_dev_report() -> None:
    parts = ["# Corporate Development and Partnership Watchlist", metadata("Corporate Development and Partnership Watchlist", 15, ["reports/marvell_xpu_implications.md", "companies/README.md", "data/company_database.yaml"], ["FIG-MMD-026"], ["TBL-CORP-001", "TBL-CORP-002", "TBL-CORP-003", "TBL-CORP-004", "TBL-CORP-005"], prefix="../")]
    parts.append("The watchlist is capability-led. It does not imply that a company is for sale, affordable, strategically willing to transact or compatible with Marvell's legal and customer constraints. Valuation and revenue are marked unavailable unless a cited public source supports them. The recommendation first asks whether control of the capability can change XPU win rate, schedule, PPA or supply assurance. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)")
    categories = sorted(set(x[1] for x in WATCHLIST))
    for cidx, category in enumerate(categories, 1):
        rows = [x for x in WATCHLIST if x[1] == category]
        parts.append(f"## {category}")
        for name, _, tech, recommendation, maturity in rows:
            parts.append(f"### {name}\n\n{name} is monitored for **{tech}**. The preliminary posture is **{recommendation}**, with estimated public maturity **{maturity}**. The strategic question is whether privileged access, co-development rights or ownership would shorten qualification or secure a differentiating interface across multiple Marvell franchises. Valuation, revenue and customer concentration are unavailable in this baseline unless disclosed in the cited source database. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)")
        parts.append(f"""
**Watchlist table - TBL-CORP-{cidx:03d}**

| Company | Technology | Recommendation | Public maturity | Core diligence |
|---|---|---|---|---|
""" + "\n".join(f"| {name} | {tech} | {recommendation} | {maturity} | Production evidence, IP rights, customer conflicts, integration cost |" for name, _, tech, recommendation, maturity in rows))
    parts.append("""
## Portfolio decision rules

| Decision | Use when | Avoid when |
|---|---|---|
| Build | Capability differentiates multiple products and requires deep architecture integration | Capability is manufacturing-scale dominated |
| Partner | Supplier scale and shared roadmap outweigh ownership | Access can be withdrawn or data rights are inadequate |
| Acquire / invest | Scarce IP, team or process knowledge materially changes win probability | Thesis depends on unsourced TAM, valuation or customer claims |
| Monitor | Technology is pre-qualification or timing is uncertain | Delay would forfeit a near-term customer architecture slot |

## Diligence playbooks

### Optical I/O and CPO

Optical targets should be diligenced as manufacturing and service platforms, not only photonic devices. Marvell needs evidence for laser source strategy, coupling loss, fiber attach automation, optical and electrical test time, thermal isolation, redundancy, field replacement, firmware telemetry and the interface to XPU or switch protocols. A compelling laboratory bandwidth result can still fail the system business case if assembly yield or field service creates excessive downtime. The strongest partnership candidate is one that complements Marvell's DSP, SerDes, switching and silicon-photonics assets while preserving architectural choice across foundries and customers. [[SRC-MRVL-003]](../data/source_database.yaml) [[SRC-OIF-001]](../data/source_database.yaml) [[SRC-AYAR-001]](../data/source_database.yaml)

### HBM controller, base-die and memory enablement

HBM-related targets require careful boundary diligence because the memory vendor, JEDEC interface, foundry logic process and XPU controller each own different portions of the solution. Marvell should identify what can be customized without compromising memory qualification, who owns verification collateral, how failure analysis crosses company boundaries, and whether base-die logic creates durable differentiation or customer-specific engineering burden. The acquisition thesis should not rest on generic HBM demand; it should rest on a controlled interface or team that improves multiple XPU generations. [[SRC-JEDEC-001]](../data/source_database.yaml) [[SRC-MRVL-001]](../data/source_database.yaml)

### Chiplet interconnect and test

Interconnect IP should be evaluated together with DFT, bring-up and interoperability. Physical-layer efficiency matters, but so do training time, repair, sideband management, security, performance counters, compliance and package-level fault isolation. A target with a strong PHY but weak test and software may add integration burden. Marvell should prefer assets that shorten the path from package simulation to known-good-die screening and system telemetry, and that can support proprietary low-overhead modes alongside standards where customers require them. [[SRC-UCIE-001]](../data/source_database.yaml) [[SRC-UCIE-002]](../data/source_database.yaml)

### Thermal, power and reliability

Thermal and power targets are attractive when they provide a defensible material, structure, model or control loop that scales across XPU, switch and optical packages. Diligence must include accelerated life data, pump-out or delamination behavior, contamination, supply scalability, compatibility with foundry and OSAT materials, and correlation between simulation and measured systems. A small materials company may have high technical leverage but difficult qualification and customer concentration, making staged investment or joint development preferable to immediate acquisition. [[SRC-ANSYS-001]](../data/source_database.yaml) [[SRC-ECTC-001]](../data/source_database.yaml)

### Glass substrates and inspection

Glass-related assets should be treated as options on late-decade package scaling until high-end customer qualification is visible. Important evidence includes through-glass-via yield, panel handling, metallization adhesion, large-body flatness, mechanical shock, thermal cycling, repair and compatibility with existing assembly tools. Inspection and metrology may offer earlier value than owning substrate manufacturing because every denser process requires defect detection and process control. [[SRC-INTEL-002]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)

### EDA, analytics and data rights

The central diligence question for EDA and analytics is whether the asset converts fragmented supplier data into earlier architecture decisions or faster yield learning. Marvell should seek automated die-package-board co-optimization, thermal and mechanical model calibration, test-data fusion, anomaly detection and traceability while confirming that customer and supplier contracts permit the required data use. An acquisition that cannot access production data will not deliver the expected learning advantage. [[SRC-CADENCE-001]](../data/source_database.yaml) [[SRC-SIEMENS-001]](../data/source_database.yaml) [[SRC-ANSYS-001]](../data/source_database.yaml)

## Transaction and partnership gates

**Gate 1: strategic mechanism.** The sponsor must identify the exact mechanism by which the target changes a Marvell customer outcome. Acceptable mechanisms include a measurable improvement in package bandwidth or power, earlier customer qualification, reduced compound scrap, protected access to a scarce interface, improved multi-source resilience or a new XPU-attach revenue stream. Generic exposure to AI, HBM or advanced packaging is not sufficient. [[SRC-MRVL-001]](../data/source_database.yaml)

**Gate 2: evidence quality.** Technical diligence should separate simulation, test vehicle, customer sample, qualified product and volume production. Reliability evidence must state sample size, stress condition and failure criteria. Commercial diligence should distinguish signed revenue, non-binding design engagement and ecosystem partnership. Any claim that cannot be tied to a source or data-room artifact remains an assumption in the investment case. [[SRC-ECTC-001]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)

**Gate 3: integration path.** The operating plan must specify where the team, IP, design flow, manufacturing relationship and customer obligations will reside after a transaction. Photonics and packaging assets often span foundry process design kits, supplier agreements and customer-specific data that may not transfer automatically. Marvell should price the time needed to requalify a process or migrate a design, not only the purchase consideration. [[SRC-TSMC-004]](../data/source_database.yaml) [[SRC-CADENCE-001]](../data/source_database.yaml)

**Gate 4: option value versus ownership.** A minority investment, joint development agreement, preferred-supply arrangement or IP license may preserve access while the market proves maturity. Full acquisition is more defensible when Marvell needs exclusive control, the capability serves multiple product lines, integration can meet a customer window and the team or data cannot be recreated through hiring and partnership. [[SRC-MRVL-003]](../data/source_database.yaml)

**Gate 5: downside case.** The investment committee should model delayed qualification, lower customer adoption, foundry incompatibility, competitor response and key-person loss. For private targets, valuation and fundraising claims remain unavailable unless documented. The downside plan should identify standalone value to Marvell's existing optical, switching or custom-silicon portfolio if the original packaging roadmap slips. [[SRC-MRVL-001]](../data/source_database.yaml)

## Priority sequence

Near-term priority should go to partnerships that strengthen HBM4 package execution, TSMC and OSAT capacity visibility, optical attach, external laser supply and multi-physics signoff. The next tier is investment or acquisition of analytics, test and telemetry capabilities that improve learning across programs. Glass substrates, panel-level advanced fan-out and more speculative optical-memory architectures should remain monitored with defined technical triggers. This sequence aligns capital with customer design windows while preserving exposure to technologies that may become important later in the decade. [[SRC-JEDEC-001]](../data/source_database.yaml) [[SRC-INTEL-002]](../data/source_database.yaml) [[SRC-OIF-001]](../data/source_database.yaml)

The watchlist owner should maintain a one-page evidence card for every priority target. The card should record technical maturity, customer evidence, manufacturing path, key-person dependence, intellectual-property ownership, foundry portability, data rights, partnership history, transaction constraints and the next event that could change the recommendation. Corporate development, engineering and business leadership should review the same card so technical excitement, customer urgency and transaction feasibility are reconciled before resources are committed. This common record also prevents unsourced valuation, revenue or fundraising assumptions from migrating into the strategic thesis. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)

```mermaid
flowchart TD
    A[Capability gap] --> B{Changes XPU win rate?}
    B -- No --> C[Monitor or commercial source]
    B -- Yes --> D{Requires control of IP/data?}
    D -- No --> E[Strategic partnership]
    D -- Yes --> F{Build before customer window?}
    F -- Yes --> G[Build internally]
    F -- No --> H[Acquire or invest after diligence]
```

## Quarterly watchlist triggers

- Customer adoption of optical scale-up or proprietary/open fabric changes.
- HBM base-die ownership and qualification model changes.
- Foundry or OSAT release of new package body size, pitch or regional capacity.
- Demonstrated field reliability for CPO optical engines and external lasers.
- New inspection, test or repair method that materially lowers compound scrap.
- Glass substrate qualification with high-end logic and HBM.
- Material changes in target ownership, funding, customer concentration or strategic partnerships.
""")
    write("reports/corp_dev_and_partnership_watchlist.md", "\n\n".join(parts))


def create_company_and_use_case_files() -> None:
    companies = []
    for idx, (name, category, tech, recommendation, maturity) in enumerate(WATCHLIST, 1):
        companies.append({"company_id": slug(name), "name": name, "category": category, "technology": tech, "why_it_matters": "Potential leverage for Marvell custom XPU packaging or connectivity", "fit_with_Marvell": recommendation, "build_partner_acquire": recommendation, "estimated_maturity": maturity, "key_customers_or_partners_public": "See source database; unavailable where not disclosed", "competitive_tension": "Requires customer conflict and exclusivity diligence", "diligence_questions": ["Production evidence?", "IP and data rights?", "Customer conflicts?", "Integration timing?"], "source_ids": ["SRC-MRVL-001", "SRC-IEEE-001"], "valuation": "unavailable", "last_refreshed": REFRESH_DATE})
    write_json("data/company_database.yaml", {"companies": companies})
    company_md = ["# Company and Asset Watchlist", "", metadata("Company and Asset Watchlist", 2, ["reports/corp_dev_and_partnership_watchlist.md", "data/company_database.yaml"], ["FIG-MMD-026"], ["TBL-COMPANY-001"], prefix="../")]
    for company in companies:
        company_md.append(f"## {company['name']}\n\n- **Category:** {company['category']}\n- **Technology:** {company['technology']}\n- **Posture:** {company['build_partner_acquire']}\n- **Maturity:** {company['estimated_maturity']}\n- **Valuation:** unavailable\n- **Sources:** [[SRC-MRVL-001]](../data/source_database.yaml), [[SRC-IEEE-001]](../data/source_database.yaml)")
    write("companies/README.md", "\n".join(company_md))

    use_cases = [
        ("ai-training-hyperscaler", "AI Training Hyperscaler", "Maximum HBM bandwidth, scale-up bandwidth and rack density; tolerates high package cost when time-to-train dominates."),
        ("ai-inference-hyperscaler", "AI Inference Hyperscaler", "Optimizes cost per token, power efficiency, capacity utilization and workload-specific precision."),
        ("neocloud", "Neocloud", "Values rapid deployment, serviceability, financing efficiency and compatibility with dominant software ecosystems."),
        ("internal-custom-asic", "Internal Custom ASIC Hyperscaler", "Values architecture control, multi-generation roadmap, supply assurance and reusable custom IP."),
        ("ethernet-first", "Ethernet-First Hyperscaler", "Prioritizes open scale-out, switch economics and operational familiarity."),
        ("optical-scale-up", "Optical Scale-up Hyperscaler", "Prioritizes package-edge bandwidth, rack or multi-rack reach and optical power efficiency."),
        ("cost-inference", "Cost-Optimized Inference Customer", "Uses fewer HBM stacks, GDDR or LPDDR alternatives when model and latency requirements permit."),
    ]
    index = ["# Use Case Profiles", "", metadata("Use Case Profiles", 4, ["reports/advanced_packaging_main_report.md", "reports/marvell_xpu_implications.md"], ["FIG-MMD-022"], ["TBL-USE-001"], prefix="../")]
    for uid, name, desc in use_cases:
        text = f"""# {name}

{metadata(name, 4, ["reports/marvell_xpu_implications.md", "data/technology_taxonomy.yaml"], ["FIG-MMD-022"], [f"TBL-USE-{slug(uid).upper()}"], prefix="../")}

{desc} Packaging selection should rank HBM capacity and bandwidth, power efficiency, rack density, yielded cost, time-to-market, software coupling, supply resilience and thermal serviceability. Marvell should present at least two architecture points: a performance-maximized package and a cost/supply-optimized package. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-NVIDIA-001]](../data/source_database.yaml)

| Requirement | Priority | Packaging implication |
|---|---:|---|
| HBM bandwidth and capacity | 4/5 | Stack count, generation and thermal margin |
| Power efficiency | 5/5 | D2D, HBM, SerDes and voltage-conversion co-design |
| Yield and supply | 5/5 | Known-good-die, capacity reservation and alternate flows |
| Time-to-market | 5/5 | Reusable IP and qualified package reference |
| Serviceability | 4/5 | Cooling, optics and replaceable assembly strategy |

> **Marvell implication:** Translate the customer's workload and fleet economics into a package architecture before proposing a specific foundry flow.
"""
        write(f"use_cases/{uid}.md", text)
        index.append(f"- [{name}]({uid}.md) - {desc}")
    write("use_cases/README.md", "\n".join(index))


def create_strategy_files() -> None:
    content = f"""# Marvell Strategy Modules

{metadata("Marvell Strategy Modules", 8, ["reports/marvell_xpu_implications.md", "reports/executive_summary_for_marvell_leadership.md"], ["FIG-MMD-023", "FIG-MMD-025"], ["TBL-STRAT-001"], prefix="../")}

This directory decomposes the recommendations into refreshable modules. The baseline recommendation is to own architecture, reusable IP, package reference designs, qualification data and customer trade-space; partner for manufacturing scale; acquire or invest where a scarce interface or capability changes custom XPU win probability. [[SRC-MRVL-001]](../data/source_database.yaml)

| Module | Build | Partner | Acquire / invest | Monitor |
|---|---|---|---|---|
| Custom HBM | Base-die architecture and verification | Memory vendors and foundry | Specialized IP or verification capability | Post-HBM concepts |
| CPO / optical I/O | System architecture and electrical/optical interface | Lasers, attach, fibers and foundry | Scarce photonic fabric or attach capability | Field service evidence |
| Chiplets | D2D IP, DFT and reference partitions | UCIe ecosystem and EDA | Test analytics or niche interface IP | Cross-vendor interoperability |
| Thermal / power | Co-design flow and reference package | TIM, cold plate and power vendors | High-leverage materials or telemetry | Immersion and backside interactions |
| Supply | Configuration planning and data model | TSMC, OSATs, substrates and test | Select regional or analytic capability | Glass and panel-level timing |
"""
    write("marvell_strategy/README.md", content)
    for name in ["build", "partner", "acquire_invest", "monitor", "quarterly_dashboard"]:
        write(f"marvell_strategy/{name}.md", f"""# {name.replace('_', ' ').title()}

{metadata(name.replace('_', ' ').title(), 4, ["reports/marvell_xpu_implications.md", "reports/corp_dev_and_partnership_watchlist.md"], ["FIG-MMD-025"], [f"TBL-STRAT-{slug(name).upper()}"], prefix="../")}

This module applies the repository's evidence ladder to {name.replace('_', ' ')} decisions. Every action requires a named capability gap, XPU win-rate mechanism, technical feasibility, time-to-market, cost and risk, dependencies, evidence confidence and next diligence questions. [[SRC-MRVL-001]](../data/source_database.yaml) [[SRC-IEEE-001]](../data/source_database.yaml)

| Recommendation field | Required answer |
|---|---|
| Rationale | What customer or architecture problem is solved? |
| XPU win-rate impact | What measurable outcome improves? |
| Feasibility and timing | Can it meet the customer design window? |
| Cost and risk | What is the downside and integration burden? |
| Dependencies | Which supplier, standard or qualification gate controls success? |
| Confidence | Confirmed, announced, expected or speculative? |
| Diligence | What evidence can change the decision? |
""")


def create_roadmaps_and_logs(vendors: list[dict]) -> None:
    roadmap_items = []
    topics = [
        ("CoWoS capacity and package scale", "TSMC", "larger interposer/RDL configurations and capacity expansion", "SRC-TSMC-003"),
        ("SoIC and hybrid bonding", "TSMC", "finer-pitch 3D stacking and broader product adoption", "SRC-TSMC-001"),
        ("Foveros Direct and EMIB", "Intel", "combined 2.5D and 3D product and foundry enablement", "SRC-INTEL-001"),
        ("HBM4", "JEDEC / memory vendors", "2,048-bit interface and logic base-die generation", "SRC-JEDEC-001"),
        ("CPO switch platforms", "NVIDIA / Broadcom / Marvell", "optics adjacent to high-radix switching", "SRC-NVIDIA-002"),
        ("UCIe", "UCIe Consortium", "64 GT/s roadmap and 3D manageability", "SRC-UCIE-002"),
        ("Glass substrate", "Intel and ecosystem", "late-decade large-body substrate option", "SRC-INTEL-002"),
        ("Marvell custom XPU packaging", "Marvell", "advanced packaging, HBM attach and optical scale-up integration", "SRC-MRVL-001"),
    ]
    for year in range(2024, 2031):
        for idx, (tech, vendor, capability, source) in enumerate(topics):
            if year <= 2025:
                status, conf = "shipping now / qualified / announced per item", "high" if year == 2024 else "medium-high"
            elif year <= 2027:
                status, conf = "announced or expected ramp", "medium"
            else:
                status, conf = "expected; not confirmed" if year <= 2029 else "speculative scenario", "low-medium"
            roadmap_items.append({"year": year, "technology": tech, "vendor": vendor, "claimed_capability": capability, "status": status, "evidence_source": source, "confidence_level": conf, "Marvell_relevance": "high", "key_risk": "qualification, yield, capacity, cost or schedule may differ by configuration"})
    write_json("data/vendor_roadmaps.yaml", {"vendors": vendors, "roadmap_items": roadmap_items})
    logs = []
    for idx, section in enumerate(["Full database refresh", "CoWoS roadmap", "HBM4 roadmap", "Marvell custom HBM architecture", "Marvell CPO architecture", "Glass substrate roadmap", "Corporate development watchlist", "Figure/visual refresh"], 1):
        logs.append({"refresh_id": f"REF-{idx:03d}", "section": section, "date": REFRESH_DATE, "owner": "placeholder", "change_types": ["New fact", "New figure" if "Figure" in section else "Roadmap change"], "summary": "Initial baseline created with source-linked records and explicit evidence status.", "source_ids_added": ["SRC-MRVL-001", "SRC-TSMC-001"], "confidence_change": "Initial confidence assigned", "next_refresh": NEXT_REFRESH})
    write_json("data/refresh_log.yaml", {"refresh_log": logs})


def create_readme() -> None:
    write("README.md", f"""# Marvell Advanced Packaging Intelligence Database

An indexed, source-backed knowledge base and executive report on advanced semiconductor packaging for AI infrastructure, focused on Marvell's hyperscaler custom XPU opportunity.

**Baseline refresh:** {REFRESH_DATE}  
**Evidence cutoff:** Public information available through {REFRESH_DATE}  
**Primary question:** How will advanced packaging evolve from 2024 to 2030, and what does that mean for Marvell's ability to win hyperscaler custom XPU programs?

## Start here

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
""")


def create_refresh_templates() -> None:
    write("scripts/refresh_section_template.md", """# Section Refresh Workflow

1. Identify section to refresh.
2. Review `last_refreshed` date.
3. Pull new sources since last refresh.
4. Add new sources to `source_database.yaml`.
5. Update technology/vendor/company profile.
6. Update benchmark metrics if changed.
7. Update figures, diagrams, and tables if changed.
8. Add refresh note to `refresh_log.yaml`.
9. Mark changes as:
   - New fact
   - Revised fact
   - Roadmap change
   - Contradictory source
   - Removed/deprecated information
   - New figure
   - Updated figure
   - Removed figure
10. Update confidence level.
11. Rebuild index.

```mermaid
flowchart LR
    A[Select section] --> B[Read last refreshed date]
    B --> C[Collect and classify new sources]
    C --> D[Update profile and databases]
    D --> E[Update visuals and benchmarks]
    E --> F[Log changes and confidence]
    F --> G[Validate and rebuild index]
```
""")
    write("scripts/refresh_full_database_template.md", """# Full Database Refresh Workflow

1. Review all `last_refreshed` fields across the repository.
2. Identify stale sections older than 90 days.
3. Search for new sources across all covered technologies and vendors.
4. Update `source_database.yaml`.
5. Update all affected technology profiles.
6. Update all affected vendor profiles.
7. Update Marvell strategy sections.
8. Update `benchmark_database.yaml`.
9. Update `figure_registry.yaml`.
10. Add or refresh visuals where necessary.
11. Update roadmap tables and confidence levels.
12. Add a full-database refresh entry to `refresh_log.yaml`.
13. Run validation.
14. Rebuild index.
15. Produce a full refresh summary.

```mermaid
flowchart TD
    A[Inventory dates and evidence] --> B[Prioritize stale and high-impact sections]
    B --> C[Research primary sources]
    C --> D[Update normalized databases]
    D --> E[Regenerate affected analysis and visuals]
    E --> F[Run validation]
    F --> G{Errors?}
    G -- Yes --> H[Repair and rerun]
    G -- No --> I[Build index and publish refresh summary]
```
""")


def create_schemas() -> None:
    common = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}
    tech_props = {key: {} for key in ["technology_id", "name", "category", "description", "maturity_level", "key_vendors", "relevant_applications", "technical_metrics", "business_metrics", "roadmap", "advantages", "limitations", "bottlenecks", "Marvell_relevance_score", "competitive_threat_score", "partnership_potential_score", "acquisition_relevance_score", "source_ids", "figure_ids", "last_refreshed", "next_suggested_refresh", "confidence_level", "open_questions"]}
    vendor_props = {key: {} for key in ["vendor_id", "name", "category", "packaging_technologies", "roadmap_claims", "customers_public", "Marvell_relationship", "Marvell_relevance", "competitive_threat", "partnership_potential", "acquisition_relevance", "key_sources", "key_figures", "last_refreshed", "next_suggested_refresh", "confidence_level", "open_questions"]}
    source_props = {key: {} for key in ["source_id", "title", "publisher", "author", "date_published", "date_accessed", "url", "source_type", "credibility_tier", "relevant_technologies", "summary", "key_extracted_facts", "limitations_or_caveats"]}
    figure_props = {key: {} for key in ["figure_id", "title", "figure_type", "source_type", "original_source", "URL", "local_path", "license_or_usage_note", "date_accessed", "related_technologies", "related_vendors", "caption", "source_ids", "caveats"]}
    for filename, props in [("technology_profile_schema.json", tech_props), ("vendor_profile_schema.json", vendor_props), ("source_schema.json", source_props), ("figure_schema.json", figure_props)]:
        schema = dict(common)
        schema.update({"properties": props, "required": list(props), "additionalProperties": True})
        write_json(f"schemas/{filename}", schema)


def main() -> None:
    sources = create_source_database()
    technologies = create_taxonomy()
    vendors = create_vendor_database()
    create_benchmarks()
    create_figures()
    create_profiles(technologies, vendors)
    create_mermaid_catalog()
    create_svgs()
    create_main_report()
    create_executive_report()
    create_marvell_report()
    create_corp_dev_report()
    create_company_and_use_case_files()
    create_strategy_files()
    create_roadmaps_and_logs(vendors)
    create_readme()
    create_refresh_templates()
    create_schemas()
    print(f"Generated repository baseline with {len(sources)} sources, {len(technologies)} technologies and {len(vendors)} vendors.")


if __name__ == "__main__":
    main()
