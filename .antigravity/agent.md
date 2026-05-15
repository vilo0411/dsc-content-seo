# 🧠 Project Knowledge Hub (agent.md)

Welcome to the SEO Writer Agent ecosystem. This file provides an overview of the architecture and how Sub-Agents collaborate to produce high-quality SEO content.

---

## 🎯 Project Goal
Build a scalable, data-driven SEO content production system that eliminates "AI-vibe" through rigorous research and multi-stage verification.

## 👥 Sub-Agent Ecosystem
- **SEO Collector** (`.antigravity/agents/seo-collector.md`): SERP research & Content Briefing.
- **Brand Guardian** (`.antigravity/agents/brand-guardian.md`): Identity & Style compliance.
- **Quality Guardian** (`.antigravity/agents/quality-guardian.md`): Independent QA & Fact-checking.
- **Research Agent** (`.antigravity/agents/research-agent.md`): Knowledge Base building.

## 🗺️ Relationship Map
```mermaid
graph TD
    User((User)) -- "Triggers Command" --> MainAgent[Main Agent]
    MainAgent -- "Consults" --> Skills{Skills /SOP/}
    
    subgraph Engine [.antigravity]
        Skills -- "Directs" --> seo-outlining[Skill: seo-outlining]
        Skills -- "Directs" --> seo-drafting[Skill: seo-drafting]
        Skills -- "Directs" --> internal-linking[Skill: internal-linking]
    end
    
    subgraph Agents [Sub-Agents]
        seo-outlining -- "Calls for SERP" --> seo-collector[Agent: seo-collector]
        seo-outlining -- "Calls for Brand Audit" --> brand-guardian[Agent: brand-guardian]
        seo-drafting -- "Calls for QA" --> quality-guardian[Agent: quality-guardian]
    end
    
    subgraph Data [knowledge/]
        Agents -- "Reads/Writes" --> 1-brand[1-brand]
        Agents -- "Reads/Writes" --> 3-pipeline[3-pipeline]
        Agents -- "Produces" --> 4-content[4-content]
    end
```

## 🔄 Content Pipeline
The production process is split across two skills:
1. **Discovery:** `/setup` to build KB.
2. **Strategy:** `/cluster` to map topics. `/keyword-plan` to pick next articles.
3. **Outlining:** `/outlining` — `.antigravity/skills/seo-outlining/SKILL.md`
4. **Drafting:** `/drafting` or `/write` — `.antigravity/skills/seo-drafting/SKILL.md`

## 🗂️ Data Hierarchy
- **`.antigravity/`**: The system (skills, agents, internal templates).
- **`knowledge/`**: The strategic brain (Brand, Market, Pipeline, Content).

## 🛠️ Key Utilities
- **Internal Linking:** Use `/link` to backfill internal links from existing articles.
- **Skill Center:** Check `.antigravity/skills/` for specialized capabilities.
