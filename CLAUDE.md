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
> 4. `.antigravity/memory/instincts.md` (bản rút gọn, sinh tự động) + `instincts-by-scope/<topic>.md` **chỉ khi** bài thuộc topic đó (danh sách ở đầu instincts.md). *Lịch sử gốc ở `instincts-archive.md` — không load khi viết.*
> 5. _(Agent-specific files theo từng agent's Context Loading block)_
>
> **Load 1 lần / session.** Các bước sau (QA, rewrite, approve) không đọc lại các file trên. Đọc tối thiểu, tra cứu bằng script:
>
> | Việc | KHÔNG làm | Làm |
> |---|---|---|
> | Đổi/kiểm tra trạng thái bài | đọc `topic-clusters.md` (17 KB) | `python scripts/topic_status.py <slug> [--set "..."]` |
> | Tìm internal link | đọc `anchor-index.md` (180 KB) | `python scripts/find_links.py "<keyword>" --exclude <slug>` |
> | Tìm bài cũ nên link tới bài mới | đọc 5 file Final | `python scripts/find_links.py --backfill <slug>` |
> | Check SEO/Anti-AI/format cơ học | grep bằng mắt theo checklist | `python scripts/qa_lint.py <file> [--outline ...] [--original ...] [--fix]` (`--outline` còn check từng câu `PAA_Questions` có mặt trong draft + format FAQ) |
> | Đọc persona | cả `personas.md` (14 KB) | chỉ section persona đã chọn |
> | Xem lỗi cũ của bài | cả `revision-log.md` | `grep -n "<slug>" knowledge/3-pipeline/revision-log.md` |

## ✍️ Content Edit Rule (Áp dụng cho mọi yêu cầu sửa nội dung — kể cả chat trực tiếp)
> **Bất kỳ khi nào được yêu cầu sửa / viết lại / chỉnh đoạn trong file thuộc `knowledge/4-content/`**, dù là slash command hay chat tự do, đều phải:
> 1. Đọc `knowledge/3-pipeline/anti-ai-rules.md` trước khi viết bất kỳ dòng nào (nếu chưa có trong session)
> 2. Đọc `.antigravity/memory/instincts.md` để tránh lặp lỗi cũ (nếu chưa có trong session)
> 3. Chạy `python scripts/qa_lint.py <file>` trên bản sửa, rồi Self-Audit phần ngữ nghĩa (mở/kết bài, nguồn số liệu, persona) trước khi trình bày
>
> **Không có exception.** Yêu cầu "sửa nhanh" hay "sửa 1 câu" vẫn phải qua bước này.
>
> **Vòng lặp QA có giới hạn:** FAIL → sửa → QA lại **tối đa 2 vòng**. Vẫn FAIL → dừng, trình bày kèm `⚠️ Remaining issues` cho người dùng quyết định. Không tự lặp vòng 3.
>
> *Lưu ý:* Khi học bản năng mới (`/learn`), ghi metadata vào `instincts-archive.md` rồi chạy `python scripts/optimize_instincts.py`. Nếu lỗi đó máy bắt được bằng regex → thêm vào `qa_lint.py` / `anti-ai-rules-blacklist.md` thay vì thêm instinct.

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
| `/write [keyword]` | `.agents/skills/write/SKILL.md` | **Full Pipeline** — Outline → Draft → Finalize. Options: `--step`, `--auto`, `--no-serp`, `--sprint`. |
| `/outlining [keyword]` | `.agents/skills/outlining/SKILL.md` | **Phase 1 & 2 only** — Research SERP + Expert Outline. Dừng trước drafting. |
| `/drafting [slug]` | `.agents/skills/drafting/SKILL.md` | **Phase 3 only** — Chuyển Outline đã approve thành Draft + QA. |
| `/approve` | `.agents/skills/approve/SKILL.md` | Phê duyệt stage hiện tại (context-aware: Outline / Draft / Optimize). |
| `/revise [slug]` | `.agents/skills/revise/SKILL.md` | Sửa đoạn / section cụ thể — có context load + self-audit bắt buộc. |
| `/optimize [path]` | `.agents/skills/optimize/SKILL.md` | Re-optimize bài cũ với 7 Sweeps Framework. |
| `/learn [slug?]` | `.agents/skills/learn/SKILL.md` | Tổng hợp feedback → cập nhật anti-ai-rules + instincts. |
| `/image [slug]` | `.agents/skills/image/SKILL.md` | Tạo chiến lược hình ảnh cho bài viết (Visual Architect). |
| `/link` | `.agents/skills/link/SKILL.md` | Backfill internal links từ bài cũ sang bài mới. |
| `/cluster` | `.agents/skills/cluster/SKILL.md` | Keyword Clustering từ `knowledge/3-pipeline/keywords.csv`. |
| `/keyword-plan [N] [persona]` | `.agents/skills/keyword-plan/SKILL.md` | Chọn N bài nên viết tiếp từ cluster map theo persona. |
| `/setup` | `.agents/skills/setup/SKILL.md` | Build Knowledge Base lần đầu (chạy 1 lần). |
| `/gsc-sync` | `.agents/skills/gsc-sync/SKILL.md` | Đồng bộ Google Search Console → `gsc-opportunities.md`. |

## 🛠️ Helper Scripts (chạy thay vì đọc file lớn)

| Script | Dùng để |
| :--- | :--- |
| `scripts/qa_lint.py <file> [--outline] [--original] [--fix] [--json] [--log]` | Lint deterministic ~28 check (CL1/2/3/5/6, link, GEO, word count, PAA coverage + FAQ format khi có `--outline`) + Score 0–100. Exit 1 = FAIL. |
| `scripts/find_links.py "<kw>" [--exclude slug]` / `--backfill <slug>` | Tra anchor-index + sitemap-cache; tìm bài cũ nên link tới bài mới kèm dòng gợi ý. |
| `scripts/topic_status.py <slug> [--set S]` / `--find` / `--list` | Đọc/ghi 1 ô trạng thái trong topic-clusters.md. |
| `scripts/optimize_instincts.py` | Sinh lại `instincts.md` (dedupe, tách lint-covered, tách scope) từ archive. |
| `scripts/serp_opportunities.py [--min-count N]` | Gom PAA + Related Searches từ cache SERP → `knowledge/3-pipeline/serp-opportunities.md` (chưa có bài / có bài chưa giữ PAA / DSC đang giữ). 0 API call. Input cho `/keyword-plan`, `/optimize`. |
| `.antigravity/skills/web-serp/scripts/serp_research.py "<kw>" [--top 10] [--extract 5] [--paa-depth N]` | SERP Google VN (DataForSEO, **có phí**) + PAA (kèm đáp án Google đang hiện + đối thủ nào có heading khớp) + Related Searches + extract competitor (local Scrapling parser, Jina fallback cho trang JS). Cache 30 ngày ở `knowledge/raw/serp/` — không dùng `--no-cache` trừ khi user yêu cầu; `--paa-depth` tốn thêm, chỉ cho pillar. Keyword chưa có trong topic-clusters/sprint-backlog → script từ chối gọi API, cần `--force`. |
| `.antigravity/skills/internal-linking/scripts/sync_sitemap.py` | Cập nhật `sitemap-cache.json` từ sitemap live. |
| `.antigravity/skills/internal-linking/scripts/link_audit.py [--orphans]` | Dashboard in/out link + danh sách orphan trong `3-finalized/`. |

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
