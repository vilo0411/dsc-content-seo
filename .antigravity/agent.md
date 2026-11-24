# 🧠 Project Knowledge Hub (agent.md)

DSC Marketing Workspace: 1 lớp **core** dùng chung (brand, compliance, vòng đời job, QA) + các **domain** gắn vào. SEO là domain đầy đủ nhất; Social, Ads, Campaign/Landing thêm từ 2026-11-24.

---

## 🎯 Project Goal
Sản xuất nội dung marketing đứng tên Chứng khoán DSC — rank được, được AI trích, chuyển đổi được — không "AI-vibe", không vi phạm compliance tài chính, mọi output qua QA máy + gate duyệt của người.

## 🧱 Layers
```mermaid
graph TD
    User((User)) --> Router[CLAUDE.md · Domain router]
    Router --> Core
    subgraph Core [.antigravity/core]
        Protocol[README: context · job lifecycle · gate]
        Compliance[rules/compliance-finance]
        CR[agents/compliance-reviewer · read-only]
    end
    Core --> SEO[SEO · .antigravity/skills + agents]
    Core --> Social[domains/social]
    Core --> Ads[domains/ads · Facebook Ads MCP]
    Core --> Campaign[domains/campaign · landing]
    SEO --> C4[knowledge/4-content]
    Social --> C5[knowledge/5-campaigns/CMP-*]
    Ads --> C5
    Campaign --> C5
    Brand[knowledge/1-brand · brand.json · personas] --> Core
    Lint[scripts/qa_gate.py · scripts/mkt_lint.py] --> Core
```

---

## 👥 Sub-Agent Ecosystem (SEO)
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

## 📈 Performance Data (SEO Dashboard MCP)
- GSC / GA4 / Ads / cannibalization lấy qua MCP **SEO Dashboard** — playbook `.antigravity/skills/seo-dashboard/SKILL.md`, cấu hình Antigravity `.antigravity/config/seo-dashboard-mcp.md`.
- Agent có MCP gọi tool rồi lưu cache bằng `python scripts/dashboard_cache.py save ...`; agent không có MCP đọc `python scripts/dashboard_cache.py report <slug>`. Không bịa số GSC.
