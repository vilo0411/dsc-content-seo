# SEO Writer Agent Boilerplate

This system is a modular SEO content production engine. 

---

## ⚖️ Project Rules
All operations must strictly follow the rules defined in:
- [.antigravity/rules/workflow-integrity.md](file:///.antigravity/rules/workflow-integrity.md)
- [.antigravity/rules/file-naming-standards.md](file:///.antigravity/rules/file-naming-standards.md)
- [.antigravity/rules/content-anti-ai.md](file:///.antigravity/rules/content-anti-ai.md)
- [.antigravity/rules/seo-formatting.md](file:///.antigravity/rules/seo-formatting.md)
- [.antigravity/rules/learning-loop.md](file:///.antigravity/rules/learning-loop.md)

---

## 🤖 Sub-Agent Architecture

| Sub-Agent | Instructions | Responsibility |
| :--- | :--- | :--- |
| **SEO Collector** | `.antigravity/agents/seo-collector.md` | SERP research + Content Brief |
| **Brand Guardian** | `.antigravity/agents/brand-guardian.md` | Brand audit & Style enforcement |
| **Quality Guardian** | `.antigravity/agents/quality-guardian.md` | Independent QA/QC |
| **Research Agent** | `.antigravity/agents/research-agent.md` | Build Knowledge Base (Phase 0-3) |

---

## ⌨️ Slash Commands

| Command | Description |
| :--- | :--- |
| `/outlining` | **Phase 1 & 2** — Research SERP and generate Expert Outline. |
| `/drafting` | **Phase 3** — Convert approved outline to Human-centric Draft. |
| `/approve` | Approve current stage (context-aware). |
| `/learn` | Trigger **`content-feedback-loop`** to synthesize historical feedback. |
| `/cluster` | **Keyword Clustering** — Uses `knowledge/3-pipeline/keywords.csv`. |
| `/optimize` | Re-optimize existing content in `knowledge/4-content/`. |
| `/link` | Backfill internal links from old articles to new ones. |

---

## 📂 Standardized Workspace Structure
```text
.antigravity/       # [THE ENGINE] Logic, Agents, Scripts, Memory
├── agents/         # Personas (Who)
├── rules/          # Master Rules & Compliance
├── skills/         # Standardized Skills (How & What)
│   ├── seo-outlining/          # Phase 1-2: Research & Briefing
│   ├── seo-drafting/           # Phase 3: Writing & QA
│   ├── internal-linking/       # Linking & Audit scripts
│   ├── qa-qc/                  # Quality assurance
│   └── content-feedback-loop/  # System learning
└── memory/         # Project history (DECISIONS.md)

knowledge/          # [THE BRAIN & FACTORY] All data and content
├── 1-brand/        # Identity, Personas, ICP
├── 2-market/       # Market Landscape
├── 3-pipeline/     # Strategy: Keywords, Backlog, Anchor Index
├── 4-content/      # Production: 1-outlines -> 3-finalized
└── raw/            # Raw unprocessed uploads
```
