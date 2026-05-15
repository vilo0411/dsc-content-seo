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

## 🔄 Mandatory Context Protocol
> Mọi agent/skill phải load context sau **trước tiên** — không có exception:
> 1. `knowledge/1-brand/profile.md`
> 2. `knowledge/3-pipeline/anti-ai-rules.md`
> 3. `knowledge/3-pipeline/glossary.md`
> 4. `.antigravity/memory/instincts.md`
> 5. _(Agent-specific files theo từng agent's Context Loading block)_

## ✍️ Content Edit Rule (Áp dụng cho mọi yêu cầu sửa nội dung — kể cả chat trực tiếp)
> **Bất kỳ khi nào được yêu cầu sửa / viết lại / chỉnh đoạn trong file thuộc `knowledge/4-content/`**, dù là slash command hay chat tự do, đều phải:
> 1. Đọc `knowledge/3-pipeline/anti-ai-rules.md` trước khi viết bất kỳ dòng nào
> 2. Đọc `.antigravity/memory/instincts.md` để tránh lặp lỗi cũ
> 3. Chạy Self-Audit Checklist (Phần 6 của anti-ai-rules.md) trên bản sửa trước khi trình bày
>
> **Không có exception.** Yêu cầu "sửa nhanh" hay "sửa 1 câu" vẫn phải qua bước này.

---

## 🤖 Sub-Agent Architecture

| Sub-Agent | Instructions | Responsibility |
| :--- | :--- | :--- |
| **SEO Collector** | `.antigravity/agents/seo-collector.md` | SERP research + Content Brief |
| **Brand Guardian** | `.antigravity/agents/brand-guardian.md` | Brand audit & Style enforcement |
| **Quality Guardian** | `.antigravity/agents/quality-guardian.md` | Independent QA/QC |
| **Research Agent** | `.antigravity/agents/research-agent.md` | Build Knowledge Base (Phase 0-3) |
| **Visual Architect** | `.antigravity/agents/visual-architect.md` | Image strategy & prompts |

---

## ⌨️ Slash Commands

| Command | Workflow File | Description |
| :--- | :--- | :--- |
| `/write [keyword]` | `.agents/workflows/write.md` | **Full Pipeline** — Outline → Draft → Finalize. Options: `--step`, `--auto`, `--no-serp`, `--sprint`. |
| `/outlining [keyword]` | `.agents/workflows/outlining.md` | **Phase 1 & 2 only** — Research SERP + Expert Outline. Dừng trước drafting. |
| `/drafting [slug]` | `.agents/workflows/drafting.md` | **Phase 3 only** — Chuyển Outline đã approve thành Draft + QA. |
| `/approve` | `.agents/workflows/approve.md` | Phê duyệt stage hiện tại (context-aware: Outline / Draft / Optimize). |
| `/revise [slug]` | `.agents/workflows/revise.md` | Sửa đoạn / section cụ thể — có context load + self-audit bắt buộc. |
| `/optimize [path]` | `.agents/workflows/optimize.md` | Re-optimize bài cũ với 7 Sweeps Framework. |
| `/learn [slug?]` | `.agents/workflows/learn.md` | Tổng hợp feedback → cập nhật anti-ai-rules + instincts. |
| `/image [slug]` | `.agents/workflows/image.md` | Tạo chiến lược hình ảnh cho bài viết (Visual Architect). |
| `/link` | `.agents/workflows/link.md` | Backfill internal links từ bài cũ sang bài mới. |
| `/cluster` | `.agents/workflows/cluster.md` | Keyword Clustering từ `knowledge/3-pipeline/keywords.csv`. |
| `/keyword-plan [N] [persona]` | `.agents/workflows/keyword-plan.md` | Chọn N bài nên viết tiếp từ cluster map theo persona. |
| `/setup` | `.agents/workflows/setup.md` | Build Knowledge Base lần đầu (chạy 1 lần). |

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
