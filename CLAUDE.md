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
- [.antigravity/rules/cta-conversion.md](file:///.antigravity/rules/cta-conversion.md)

---

## 🎯 Thế nào là output tốt
Bài tốt = bài **rank được và được AI trích**. Sạch từ cấm / đúng format chỉ là điều kiện cần. Mỗi bài phải đạt 5 điều, đều có check máy:

| Tiêu chí | Outline (`outline_lint`) | Draft (`qa_lint`) |
|---|---|---|
| Đúng intent, đúng khung SERP | `FMT-*`, `SERP-paa-fake` | `PAA-missing`, `FAQ-*` |
| Phủ entity / chủ đề con đối thủ đều có | `ENT-outline` | `ENT-missing`, `ENT-acronym` |
| Có giá trị mới so với top 5 | `IG-shape`, `IG-not-new` | `IG-missing`, `DUP-h2`, `DUP-faq` |
| Tin được (E-E-A-T, YMYL) | `DATA-source` | `SRC-*`, `YMYL-disclaimer`, `EEAT-firsthand`, `CL5-fact` |
| AI đọc và trích được | Sapo trả lời thẳng | `GEO-h2-answer`, `GEO-*`, `FAQ-long-answer` |

Điểm `coverage` / `trust` thấp mà điểm hình thức cao = bài chưa có lý do để rank → báo user, không trình bày như bài đạt. Bài đứng tên **Chứng khoán DSC**; link ngoài chỉ tới nguồn trong `source-whitelist.md`.

---

## 🔄 Mandatory Context Protocol
> Mọi agent/skill phải load context sau **trước tiên** — không có exception:
> 1. `knowledge/1-brand/profile.md`
> 2. `knowledge/3-pipeline/anti-ai-rules.md`
> 3. `knowledge/3-pipeline/glossary.md`
> 4. `.antigravity/memory/instincts.md` (~8 KB, sinh tự động, rule đầy đủ không cắt) + `instincts-by-scope/<topic>.md` **chỉ khi** bài thuộc topic đó (danh sách ở đầu instincts.md). *Không mở `instincts-archive.md` (~130 KB) — cần 1 rule / ghi chú cũ của 1 bài thì `python scripts/optimize_instincts.py --show <ID|tag|slug>`.* *Lịch sử gốc ở `instincts-archive.md` — không load khi viết.*
> 5. _(Agent-specific files theo từng agent's Context Loading block)_
>
> **Load 1 lần / session.** Các bước sau (QA, rewrite, approve) không đọc lại các file trên. Đọc tối thiểu, tra cứu bằng script:
>
> | Việc | KHÔNG làm | Làm |
> |---|---|---|
> | Đổi/kiểm tra trạng thái bài | đọc `topic-clusters.md` (27 KB) | `python scripts/topic_status.py <slug> [--set "..."]` · tổng quan cho `/keyword-plan`: `--summary` |
> | Tìm internal link | đọc `anchor-index.md` (189 KB) | `python scripts/find_links.py "<keyword>" --exclude <slug>` |
> | Tìm bài cũ nên link tới bài mới | đọc 5 file Final | `python scripts/find_links.py --backfill <slug>` |
> | Check SEO/Anti-AI/format cơ học | grep bằng mắt theo checklist | `python scripts/qa_lint.py <file> [--outline ...] [--original ...] [--fix]` (`--outline` còn check từng câu `PAA_Questions` có mặt trong draft + format FAQ) |
> | Check nhịp câu / mật độ bằng chứng / trùng khung (AI slop) | đọc lại bài rồi đoán "nghe như AI" | `python scripts/slop_check.py <file> [-v]` · `--baseline` để lấy lại phân bố corpus |
> | Lấy số liệu thị trường để viết | tự nhớ giá, chỉ số | `python scripts/market_facts.py --brief [--tickers VCB,HPG]` |
> | Kiểm chứng số liệu trong bài | đọc lại bằng mắt | `python scripts/market_facts.py --verify <file>` |
> | Tin tức / sự kiện mới quanh keyword | WebSearch tốn quota | `python scripts/news_feed.py --topic "<kw>" --days 14` |
> | Đọc persona | cả `personas.md` (14 KB) | `python scripts/persona.py P2 [--part bridge]` · `--matrix` |
> | Xem lỗi cũ của bài | cả `revision-log.md` | `grep -rn "<slug>" knowledge/3-pipeline/revision-log*` |
> | Ghi revision-log (/approve, /write) | mở `revision-log.md` (95 KB) rồi Edit | `python scripts/revision_log.py add <slug> --fix … --pattern … --rule … --scope …` |
> | `/learn` không slug | đọc cả revision-log | `python scripts/revision_log.py brief` (mục từ lần /learn trước) → cuối: `mark-learn` |
> | User đã sửa gì so với bản AI trình | đọc 2 bản bài | `python scripts/article_snapshot.py <slug> --diff` |
> | QA draft (tầng A+B+dữ liệu) | chạy 3 script, đọc 3 báo cáo | `python scripts/qa_gate.py <draft>` · vòng 2 QG: `--changed` |
> | Bài cần phủ thuật ngữ / chủ đề con nào để ngang đối thủ | đọc từng bài đối thủ | block `Topic Coverage` của `serp_research.py "<kw>" --extract 5` (đọc cache, 0 phí) |
> | Link ra nguồn nào được phép | tự chọn nguồn | `knowledge/3-pipeline/source-whitelist.md` (cơ quan quản lý, sở, văn bản luật) |
> | Thêm bài mới vào anchor-index / topic-clusters | mở file rồi Edit | `find_links.py --add-anchor <slug> --anchor … --cluster …` · `topic_status.py <slug> --add --keyword … --cluster …` |
> | Trình bày outline / draft / proposal ở gate | dán cả file vào chat | tóm tắt ≤ 25 dòng + đường dẫn file |
> | Nội dung / link hiện đang live của 1 bài đã publish | mở CSV Screaming Frog cũ / file Final | `python scripts/sync_live.py --only <slug>` → `knowledge/raw/live/html/<slug>.html` · `--show <slug>` |
| Số GSC của 1 bài (clicks, CTR, query, so kỳ trước) | đoán / mở dashboard bằng tay | SEO Dashboard MCP `query_search_analytics` → `python scripts/dashboard_cache.py save page-queries <slug>`; không có MCP: `python scripts/dashboard_cache.py report <slug>` |
| Trước khi viết bài mới: keyword đã có URL DSC rank chưa | tạo outline luôn | SEO Dashboard MCP `query_search_analytics` dimensions `page` + `query_value` (Bước 0.5 `/outlining`) |

## ✍️ Content Edit Rule (Áp dụng cho mọi yêu cầu sửa nội dung — kể cả chat trực tiếp)
> **Bất kỳ khi nào được yêu cầu sửa / viết lại / chỉnh đoạn trong file thuộc `knowledge/4-content/`**, dù là slash command hay chat tự do, đều phải:
> 1. Đọc `knowledge/3-pipeline/anti-ai-rules.md` trước khi viết bất kỳ dòng nào (nếu chưa có trong session)
> 2. Đọc `.antigravity/memory/instincts.md` để tránh lặp lỗi cũ (nếu chưa có trong session)
> 3. Chạy cả 3 tầng check trên bản sửa bằng 1 lệnh — `python scripts/qa_gate.py <file>` = tầng A `qa_lint` (hình thức + thực chất: `coverage`, `trust`) → tầng B `slop_check` (nhịp câu, mật độ bằng chứng; score < 80 = FAIL) → tầng dữ liệu `market_facts --verify` (advisory) — rồi Self-Audit phần ngữ nghĩa (mở/kết bài, nguồn số liệu, persona) trước khi trình bày. Cách sửa từng rule `SLOP-*`: `knowledge/3-pipeline/anti-ai-rules.md` §8.7
>
> **Không có exception.** Yêu cầu "sửa nhanh" hay "sửa 1 câu" vẫn phải qua bước này.
>
> **Vòng lặp QA có giới hạn:** FAIL → sửa → QA lại **tối đa 2 vòng**. Vẫn FAIL → dừng, trình bày kèm `⚠️ Remaining issues` cho người dùng quyết định. Không tự lặp vòng 3.
>
> *Lưu ý:* Khi học bản năng mới (`/learn`): qua cổng nhận rule (lặp ở bài khác? máy bắt được? đã có rule cùng Tag → sửa tại chỗ theo ID), rồi `python scripts/optimize_instincts.py --check`. Nếu lỗi đó máy bắt được bằng regex → thêm vào `qa_lint.py` / `anti-ai-rules-blacklist.md` thay vì thêm instinct.

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
| `/cro [slug]` | `.agents/skills/cro/SKILL.md` | Tối ưu chuyển đổi — audit CTA, dựng Product Bridge, chèn banner. Options: `--audit-all`, `--variants N`, `--apply`, `--utm`. Tự chạy trong `/write` & `/optimize`. |
| `/link` | `.agents/skills/link/SKILL.md` | Backfill internal links từ bài cũ sang bài mới. |
| `/cluster` | `.agents/skills/cluster/SKILL.md` | Keyword Clustering từ `knowledge/3-pipeline/keywords.csv`. |
| `/keyword-plan [N] [persona]` | `.agents/skills/keyword-plan/SKILL.md` | Chọn N bài nên viết tiếp từ cluster map theo persona. |
| `/setup` | `.agents/skills/setup/SKILL.md` | Build Knowledge Base lần đầu (chạy 1 lần). |
| `/gsc-sync` | `.agents/skills/gsc-sync/SKILL.md` | Đồng bộ Google Search Console → `gsc-opportunities.md`. Nguồn: SEO Dashboard MCP (ưu tiên) hoặc GSC API. |
| `/weekly` | `.agents/skills/weekly/SKILL.md` | Việc sau publish gom 1 lần/tuần: sync live, backfill link theo lô, đo GSC bài 4–8 tuần (→ `/optimize`), dọn log. Nguồn: `publish-ledger.csv`. |

## 🛠️ Helper Scripts
Bảng đầy đủ (cờ, output, khi nào chạy): [`scripts/README.md`](scripts/README.md) — **chỉ mở khi cần chi tiết 1 script**; việc thường ngày dùng bảng "Việc → Làm" ở trên. Mọi script có `--help`.

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
├── 3-pipeline/     # Strategy: Keywords, Backlog, rules
│   └── internal-links/  # anchor-index.md, link-clusters.json, dashboard.md, link-graph.html, archive/
├── 4-content/      # Production: 1-outlines -> 3-finalized -> 4-cms (HTML dán CMS)
└── raw/            # Raw unprocessed uploads · live/ = snapshot site live (sync_live.py)
```
