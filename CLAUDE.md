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
> | Check nhịp câu / mật độ bằng chứng / trùng khung (AI slop) | đọc lại bài rồi đoán "nghe như AI" | `python scripts/slop_check.py <file> [-v]` · `--baseline` để lấy lại phân bố corpus |
> | Lấy số liệu thị trường để viết | tự nhớ giá, chỉ số | `python scripts/market_facts.py --brief [--tickers VCB,HPG]` |
> | Kiểm chứng số liệu trong bài | đọc lại bằng mắt | `python scripts/market_facts.py --verify <file>` |
> | Tin tức / sự kiện mới quanh keyword | WebSearch tốn quota | `python scripts/news_feed.py --topic "<kw>" --days 14` |
> | Đọc persona | cả `personas.md` (14 KB) | chỉ section persona đã chọn |
> | Xem lỗi cũ của bài | cả `revision-log.md` | `grep -n "<slug>" knowledge/3-pipeline/revision-log.md` |
| Số GSC của 1 bài (clicks, CTR, query, so kỳ trước) | đoán / mở dashboard bằng tay | SEO Dashboard MCP `query_search_analytics` → `python scripts/dashboard_cache.py save page-queries <slug>`; không có MCP: `python scripts/dashboard_cache.py report <slug>` |
| Trước khi viết bài mới: keyword đã có URL DSC rank chưa | tạo outline luôn | SEO Dashboard MCP `query_search_analytics` dimensions `page` + `query_value` (Bước 0.5 `/outlining`) |

## ✍️ Content Edit Rule (Áp dụng cho mọi yêu cầu sửa nội dung — kể cả chat trực tiếp)
> **Bất kỳ khi nào được yêu cầu sửa / viết lại / chỉnh đoạn trong file thuộc `knowledge/4-content/`**, dù là slash command hay chat tự do, đều phải:
> 1. Đọc `knowledge/3-pipeline/anti-ai-rules.md` trước khi viết bất kỳ dòng nào (nếu chưa có trong session)
> 2. Đọc `.antigravity/memory/instincts.md` để tránh lặp lỗi cũ (nếu chưa có trong session)
> 3. Chạy cả 3 tầng check trên bản sửa — `python scripts/qa_lint.py <file>` (tầng A: từ vựng/format) → `python scripts/slop_check.py <file>` (tầng B: nhịp câu, mật độ bằng chứng; score < 80 = FAIL) → `python scripts/market_facts.py --verify <file>` (tầng dữ liệu: số liệu sai/cũ, advisory) — rồi Self-Audit phần ngữ nghĩa (mở/kết bài, nguồn số liệu, persona) trước khi trình bày. Cách sửa từng rule `SLOP-*`: `knowledge/3-pipeline/anti-ai-rules.md` §8.7
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
| `/cro [slug]` | `.agents/skills/cro/SKILL.md` | Tối ưu chuyển đổi — audit CTA, dựng Product Bridge, chèn banner. Options: `--audit-all`, `--variants N`, `--apply`, `--utm`. Tự chạy trong `/write` & `/optimize`. |
| `/link` | `.agents/skills/link/SKILL.md` | Backfill internal links từ bài cũ sang bài mới. |
| `/cluster` | `.agents/skills/cluster/SKILL.md` | Keyword Clustering từ `knowledge/3-pipeline/keywords.csv`. |
| `/keyword-plan [N] [persona]` | `.agents/skills/keyword-plan/SKILL.md` | Chọn N bài nên viết tiếp từ cluster map theo persona. |
| `/setup` | `.agents/skills/setup/SKILL.md` | Build Knowledge Base lần đầu (chạy 1 lần). |
| `/gsc-sync` | `.agents/skills/gsc-sync/SKILL.md` | Đồng bộ Google Search Console → `gsc-opportunities.md`. Nguồn: SEO Dashboard MCP (ưu tiên) hoặc GSC API. |

## 🛠️ Helper Scripts (chạy thay vì đọc file lớn)

| Script | Dùng để |
| :--- | :--- |
| `scripts/qa_lint.py <file> [--outline] [--original] [--cta] [--fix] [--json] [--log]` | Lint deterministic ~28 check (CL1/2/3/5/6, link, GEO, word count, PAA coverage + FAQ format khi có `--outline`) + Score 0–100. Exit 1 = FAIL. `--cta` bật thêm 6 check CTA-* (chưa mặc định — corpus chưa backfill banner). |
| `scripts/slop_check.py <file> [-v] [--json]` · `--baseline [--csv f] [--top N]` · `--thresholds` | **Tầng B** — 13 rule `SLOP-*` thống kê (burstiness, rhythm_gap, evidence/100w, unanchored, vague, template_sim…). Bắt slop mà tầng A không thấy: bài sạch 100% từ cấm vẫn có thể phẳng nhịp, không bằng chứng. Ngưỡng **relative theo corpus DSC** (baseline 2026-10-16, 182 bài → `knowledge/3-pipeline/slop-audit-2026-10-16.md`). Gate: score < 80 = FAIL. Offline, 0 API call. |
| `scripts/market_facts.py --brief [--tickers …]` · `--ticker VCB` · `--index VNINDEX --years 2022,2026` · `--verify <file>` | **Script duy nhất có network trong pipeline viết.** OHLCV thật (VNDirect dchart) + danh sách mã niêm yết (SSI iboard), cache 24h ở `scripts/market-cache.json`. `--verify` bắt `FACT-index-wrong` (số chỉ số sai) / `FACT-ticker` (mã không niêm yết) / `FACT-stale` (mọi mốc cũ hơn 18 tháng). **Exit 3 = nguồn chết → KHÔNG chặn pipeline**, dùng dữ kiện cấu trúc thay thế. |
| `scripts/news_feed.py --topic "<kw>" [--days N]` · `--latest` · `--feeds` | RSS 6 nguồn (CafeF ×2, VnExpress, Vietstock, Tuổi Trẻ, Dân Trí), cache 6h. Dùng để tìm góc bài + mốc sự kiện **có ngày**; KHÔNG dùng để viết lại tin — nội dung DSC là evergreen. |
| `scripts/find_links.py "<kw>" [--exclude slug]` / `--backfill <slug>` | Tra anchor-index + sitemap-cache; tìm bài cũ nên link tới bài mới kèm dòng gợi ý. |
| `scripts/topic_status.py <slug> [--set S]` / `--find` / `--list` | Đọc/ghi 1 ô trạng thái trong topic-clusters.md. |
| `scripts/dashboard_cache.py save <kind> [slug]` · `report <slug>` · `status` | Cache dùng chung cho **SEO Dashboard MCP** (GSC/GA4/Ads/cannibalization). Agent có MCP gọi tool → `save`; agent không có MCP (Antigravity chưa cấu hình, Cursor…) đọc `report`. `save pages` / `save page-query` ghi luôn `pages.csv` / `queries.csv` theo schema `sync_gsc.py` → `process_gsc.py`, `find_links.py --backfill` chạy không cần credentials. Playbook: `.antigravity/skills/seo-dashboard/SKILL.md` · cấu hình: `.antigravity/config/seo-dashboard-mcp.md`. 0 network. |
| `scripts/cta_audit.py <file\|slug\|URL>` / `--all [--ga4 csv]` / `--refresh` | Audit tầng chuyển đổi: banner, vị trí theo % thân bài, đoạn dẫn, link mở TK, CRO score. Nhận cả URL — ưu tiên file local, không có thì fetch trang live bằng urllib (~0.6s, cache `knowledge/raw/pages/`). **Không dùng web-serp/Firecrawl cho URL dsc.com.vn.** Chỉ đọc, không ghi. |
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
