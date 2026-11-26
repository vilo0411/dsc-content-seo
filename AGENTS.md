# DSC Digital Marketing Agent (SEO là lõi)

Bộ skill marketing cho **Chứng khoán DSC**: SEO (lõi) + Analytics, Google Ads, Meta Ads, Social/Fanpage, Campaign đa kênh, Email/Landing, Creative.
Chỉ dẫn chung cho **mọi coding agent** (Claude Code, Antigravity, Codex, Cursor, Gemini CLI…). `CLAUDE.md` / `GEMINI.md` chỉ import file này. Output cho user bằng tiếng Việt; code comment bằng tiếng Anh.

- Skill = thư mục phẳng `.agents/skills/<tên>/` (`SKILL.md` + `references/` + `scripts/`). Lệnh `/x` = mở `.agents/skills/<x>/SKILL.md` và làm theo.
- Bối cảnh marketing chung: `.agents/context.md`. Claude Code thấy skill qua junction `.claude/skills` (`python scripts/link_agent_dirs.py` sau khi clone).

---

## 🧭 1. Chọn skill theo việc
User không gõ lệnh → chọn skill theo bảng, mở đúng 1 `SKILL.md` rồi làm. Không mở skill khác "cho chắc".

| User muốn | Skill | Không nhầm với |
|---|---|---|
| Viết bài SEO mới từ keyword | `/write` (cả pipeline) · chỉ outline: `/outlining` · outline đã duyệt → draft: `/drafting` | — |
| Duyệt outline / draft / proposal | `/approve` | — |
| Sửa 1 đoạn / câu / section theo ý user | `/revise` | `/optimize` = làm lại cả bài cũ theo dữ liệu |
| Bài cũ tụt hạng, cần refresh cả bài | `/optimize` | `/revise` |
| CTA / banner / Product Bridge **trong bài SEO** | `/cro` | `/copy-landing` = viết cả trang đích |
| Internal link cho 1 bài / backfill bài cũ → bài mới | `/link` | `/weekly` = backfill theo lô hằng tuần |
| Việc sau publish, đo bài sau 14 ngày live | `/weekly` | — |
| Chọn bài nên viết tiếp | `/keyword-plan` (cluster map mới từ CSV: `/cluster`) | — |
| Cơ hội từ GSC → `gsc-opportunities.md` | `/gsc-sync` | `/analytics-report` = báo cáo KPI đa kênh |
| Hỏi số GSC/GA4/Ads lẻ (1 bài, 1 query) | gọi MCP thẳng theo `seo-dashboard` | không cần skill lớn |
| Báo cáo tháng/tuần, KPI, Lead, CPL, CPA | `/analytics-report` | — |
| Google Ads: hiệu quả, search term, negative | `/ads-audit` · viết quảng cáo: `/ads-copy` | Meta Ads → `/ads-brief` … |
| Meta Ads: brief, copy, đọc số, rút bài học | `/ads-brief` → `/meta-ads-copy` · `/ads-review` · `/ads-learn` | `/ads-copy` = Google RSA |
| Post Fanpage / Zalo OA / LinkedIn, lịch nội dung tháng | `/social-post` · `/social-plan` | `/syndicate` = kênh cộng đồng từ bài SEO |
| Chiến dịch đa kênh (job `CMP-*`), báo cáo chiến dịch, trạng thái mọi việc | `/campaign-brief` · `/campaign-report` · `/mkt-status` | `/analytics-report` = KPI tháng |
| Landing 1 trang cho chiến dịch (copy + HTML theo `brand.json`) | `/landing` | `/copy-landing` = chỉ copy trang có sẵn |
| Ảnh quảng cáo / post / carousel đúng brand | `/creative` (tự chạy trong `/meta-ads-copy`, `/social-post`) | `/image` = ảnh trong bài SEO |
| Phân phối bài lên social / sheet Publishing | `/syndicate` | — |
| Chuỗi email | `/email-sequence` | — |
| Copy landing page | `/copy-landing` | `/cro` |
| Ảnh bài viết | `/image` | — |
| Học từ feedback, cập nhật rule | `/learn` | — |
| QA độc lập trước publish | `/qa-qc` (sau khi `qa_gate.py` PASS) | — |
| Nghiên cứu SERP 1 keyword | `web-serp` (`serp_research.py`) | không dùng browser / WebSearch |
| Đối thủ tuần này đăng gì, nhịp đăng, ai đang rank top keyword X | `/competitor-watch` | — |
| Phân tích sâu 1 đối thủ | `/competitor-profile <domain>` | `/competitor-watch` = theo dõi hằng tuần |
| Xu hướng thị trường, insight nhà đầu tư | `/market-research` | — |

---

## ⚖️ 2. Quy tắc chung (bắt buộc)
1. **Pipeline bài SEO:** Research → Outline → `/approve` → Draft → QA → `/approve` → Finalize. Không bỏ bước, không draft khi outline chưa `Outline-Approved` (`python scripts/topic_status.py <slug>`). Sau mỗi gate: `topic_status.py <slug> --set …`.
2. **Không bịa số.** Lãi suất, giá, chỉ số, mã CK lấy từ SERP cache, knowledge base hoặc `market_facts.py`; fact DSC từ `knowledge/1-brand/brand-facts.json`. Nguồn không truy cập được (exit 3) → dùng fact cấu trúc không hết hạn (biên độ HOSE 7% / HNX 10% / UPCoM 15%, T+2, lô 100 cp — `anti-ai-rules.md` §8.7e); vẫn thiếu → dừng, hỏi user.
3. **QA 3 tầng cho mọi file `knowledge/3-seo/content/`** trước khi trình bày/finalize — 1 lệnh: `python scripts/qa_gate.py <file>` (A `qa_lint` hình thức + `coverage`/`trust` → B `slop_check` score < 80 = FAIL → dữ liệu `market_facts --verify`, advisory). Quality Guardian (`/qa-qc`) chỉ chạy khi A+B PASS. Draft còn FAIL không được trình để duyệt.
4. **Tối đa 2 vòng** sửa → QA. Vẫn FAIL → dừng, trình kèm `⚠️ Remaining issues`. Không tự chạy vòng 3.
5. **User yêu cầu sửa trong chat** → ghi ngay `python scripts/revision_log.py add <slug> --fix … --pattern … --rule … --scope …` trước khi sửa. Không mở `revision-log.md`.
6. **Trình bày ở gate:** tóm tắt ≤ 25 dòng + đường dẫn file. Không dán cả file vào chat. Trước khi trình: `python scripts/build_content_index.py` → bài hiện ở mục **Chờ duyệt** của `knowledge/0-dashboard/index.html` (user đọc + copy `/approve` ở đó).
7. **Phạm vi:** đang làm 1 bài thì chỉ sửa bài đó; không lan sang bài khác trừ khi user yêu cầu.
8. **File:** tên slug thường, không dấu (`lai-suat-acb.md`). Không để file tạm ở root — dùng `scratch/` (gitignored). Outline / Proposal / Draft / Optimize có YAML đầu file với `Created: YYYY-MM-DD` (ngày tạo) + `Updated: YYYY-MM-DD` (`topic_status.py --set` tự ghi); dashboard đọc 2 trường này. File còn sót sau Finalize: `topic_status.py --stale [--apply]`.
9. **Mọi việc đều có dấu vết.** Script tự ghi activity log khi đổi trạng thái / QA / duyệt / xuất CMS. Skill tạo output bằng tay → bước cuối `python scripts/activity_log.py add --domain … --skill … --action … --target … --path …` (hook ghi dự phòng khi tạo file). Dashboard tự dựng lại cuối lượt; tab **Kênh** + **Hoạt động** đọc log này.
10. **Không publish / gửi / chạy thật** (CMS, email, Ads, social). Chỉ soạn bản nháp + đề xuất.
11. **Bài đứng tên Chứng khoán DSC;** link ngoài chỉ tới nguồn trong `knowledge/1-brand/source-whitelist.md`.
12. **Mọi thiết kế** (ảnh blog, creative, banner CTA, landing, ảnh syndication) chỉ dùng màu / gradient / font trong `knowledge/1-brand/DESIGN.md` v1.0 (máy đọc: `brand.json`): Gunmetal · Pine Teal · Lime · Emerald · Frosted Mint · White, font Plus Jakarta Sans. Không tự đặt hex/font; chữ trắng không đặt trên Lime/Emerald. Theme Tết/lễ (§7) chỉ khi brief ghi rõ.

**Rule chi tiết — chỉ mở khi tới bước cần:**
| File | Mở khi |
|---|---|
| `.agents/rules/seo-formatting.md` | Drafting / optimize: heading, đoạn, list, featured snippet |
| `.agents/rules/cta-conversion.md` | Đặt CTA / banner (`/cro`, `/copy-landing`, bước CTA của `/write`, `/optimize`) |

---

## 🎯 3. Thế nào là output tốt
Bài tốt = bài **rank được và được AI trích**. Sạch từ cấm / đúng format chỉ là điều kiện cần. Mỗi bài phải đạt 5 điều, đều có check máy:

| Tiêu chí | Outline (`outline_lint`) | Draft (`qa_lint`) |
|---|---|---|
| Đúng intent, đúng khung SERP | `FMT-*`, `SERP-paa-fake` | `PAA-missing`, `FAQ-*` |
| Phủ entity / chủ đề con đối thủ đều có | `ENT-outline` | `ENT-missing`, `ENT-acronym` |
| Có giá trị mới so với top 5 | `IG-shape`, `IG-not-new` | `IG-missing`, `DUP-h2`, `DUP-faq` |
| Tin được (E-E-A-T, YMYL) | `DATA-source` | `SRC-*`, `YMYL-disclaimer`, `EEAT-firsthand`, `CL5-fact` |
| AI đọc và trích được | Sapo trả lời thẳng | `GEO-h2-answer`, `GEO-*`, `FAQ-long-answer` |

Điểm `coverage` / `trust` thấp mà điểm hình thức cao = bài chưa có lý do để rank → báo user, không trình bày như bài đạt. Copy ngắn (ads, email, landing): đúng persona, số khớp brand-facts `verified`, không hứa lợi nhuận.

---

## 🔄 4. Context — load 1 lần / session
**Viết / sửa nội dung SEO** (`/write`, `/outlining`, `/drafting`, `/revise`, `/optimize`, `/cro`, sửa file trong `knowledge/3-seo/content/`):
1. `knowledge/1-brand/profile.md`
2. `knowledge/1-brand/anti-ai-rules.md` — cách sửa từng rule `SLOP-*`: §8.7
3. `knowledge/1-brand/glossary.md`
4. `.agents/memory/instincts.md` + `instincts-by-scope/<topic>.md` **chỉ khi** bài thuộc topic đó (danh sách ở đầu instincts.md). Không mở `instincts-archive.md` — cần 1 rule cũ: `python scripts/optimize_instincts.py --show <ID|tag|slug>`.
5. File riêng theo block Context của skill.

**Skill ngoài SEO** (`analytics-report`, `ads-*`, `email-sequence`, `copy-landing`, `syndicate`): `.agents/context.md` + skill tự liệt kê phần còn lại.
**Social / Meta Ads / Campaign / Landing / Creative:** thêm `.agents/core/README.md` (vòng đời job, gate, QA `scripts/mkt_lint.py`) + `.agents/core/rules/compliance-finance.md` + README của domain (`.agents/domains/<social|ads|campaign>/`). Brand kit máy đọc: `knowledge/1-brand/brand.json`, chuẩn hình `knowledge/1-brand/DESIGN.md`. Ghi lên Meta chỉ khi user yêu cầu rõ, luôn `PAUSED`, không đổi ngân sách.

Đã có trong session thì **không đọc lại** (kể cả ở QA, rewrite, approve). Không chắc đã đọc chưa → đọc lại 1 lần, đừng đoán rule.

---

## 🛠️ 5. Tra cứu bằng script, không đọc file lớn
Mọi script có `--help`; chi tiết cờ: `scripts/README.md` (chỉ mở khi cần). Claude Code có hook chặn đọc nguyên các file lớn dưới đây.

| Việc | KHÔNG làm | Làm |
|---|---|---|
| Trạng thái bài / tổng quan cluster | đọc registry `pages.csv` (400 KB) | `python scripts/topic_status.py <slug> [--set "…"]` · `--summary` · `--find "<từ>"` |
| Chiến lược cụm: core/outer, thực thể, `bridge_to`, thuộc tính còn thiếu | đọc `taxonomy.json` (116 KB) | `python scripts/registry.py cluster [<mã>]` · `suggest-core` (sửa: `taxonomy.json` → `topics`; định vị: `profile.md` §0) |
| Thêm bài mới vào index | mở file rồi Edit | `topic_status.py <slug> --add --keyword … --cluster …` · `find_links.py --add-anchor <slug> --anchor … --cluster …` |
| Tìm internal link | đọc registry `pages.csv` | `python scripts/find_links.py "<keyword>" --exclude <slug>` |
| Bài cũ nên link tới bài mới | đọc các file Final | `python scripts/find_links.py --backfill <slug>` |
| Persona | đọc `personas.md` (14 KB) | `python scripts/persona.py P2 [--part bridge\|tone]` · `--matrix` |
| QA draft (A+B+dữ liệu) | chạy 3 script, đọc 3 báo cáo | `python scripts/qa_gate.py <draft>` · vòng 2: `--changed` |
| Lint riêng / tự sửa lỗi cơ học | grep bằng mắt | `python scripts/qa_lint.py <file> [--outline …] [--fix]` · outline: `outline_lint.py` |
| AI slop (nhịp câu, bằng chứng) | đọc lại rồi đoán | `python scripts/slop_check.py <file> [-v]` |
| Số liệu thị trường để viết / kiểm | tự nhớ giá, chỉ số | `python scripts/market_facts.py --brief [--tickers VCB,HPG]` · `--verify <file>` |
| Fact DSC lệch ở bài nào | grep tay | `python scripts/fact_consistency.py [--due] [--changed <id>]` |
| Tin tức quanh keyword | WebSearch | `python scripts/news_feed.py --topic "<kw>" --days 14` |
| SERP + đối thủ + thuật ngữ cần phủ | browser / WebSearch | `python .agents/skills/web-serp/scripts/serp_research.py "<kw>" --extract 5` (cache, block `Topic Coverage`) |
| Thuộc tính (EAV) đối thủ có, root / rare | đọc bài đối thủ | `serp_research.py "<kw>" --eav` (full text trong cache, 0 phí) → khối `EAV:` của outline |
| Lỗi cũ của bài | đọc `revision-log.md` (95 KB) | `grep -rn "<slug>" knowledge/3-seo/logs/revision-log*` |
| Ghi revision-log | mở rồi Edit | `python scripts/revision_log.py add …` · `/learn`: `brief` → cuối `mark-learn` |
| User đã sửa gì so với bản AI | đọc 2 bản | `python scripts/article_snapshot.py <slug> --diff` |
| Nội dung / link đang live | mở file Final / CSV cũ | `python scripts/sync_live.py --only <slug>` · `--show <slug>` |
| Số GSC/GA4/Ads | đoán / mở dashboard | SEO Dashboard MCP (`sc-domain:dsc.com.vn`) → lưu `dashboard_cache.py save …`; không có MCP: `dashboard_cache.py report <slug>` |
| Keyword đã có URL DSC rank chưa (trước khi viết) | tạo outline luôn | MCP `query_search_analytics` (`dimensions: ["page"]`, `query_value: "<kw>"`, `days: 90`) — Bước 0.5 `/outlining` |
| 1 bài: cluster, role, hub, anchor, slug live | mở `pages.csv` | `python scripts/registry.py show <slug>` |
| Registry lệch (slug live chưa khớp, trùng key, thiếu cluster) | tự dò | `python scripts/registry.py refresh` → `check` |
| Đối thủ tuần này / nhịp đăng | WebSearch, mở site đối thủ | `python scripts/competitor_watch.py run` → `report` |
| Ai rank top keyword của DSC · keyword đối thủ thắng DSC | đoán | `competitor_watch.py discover [--keyword …]` · `gap <domain>` (cache SERP, 0 phí) |
| Ai đã làm gì, kênh nào, khi nào | hỏi lại / dò file | `python scripts/activity_log.py tail [--domain …] [--days 7]` · `stats [--month]` · tab Hoạt động |
| Việc tuần này | tự nhớ | `python scripts/weekly_review.py` · bảng `knowledge/0-dashboard/index.html` |

---

## ⚡ 6. Dùng tool tiết kiệm
- Gọi song song các lệnh độc lập trong 1 lượt (vd 3 lệnh MCP, hoặc `topic_status` + `find_links` + `persona`).
- Ưu tiên: script / MCP → đọc 1 đoạn file (offset/limit, `grep -n`) → đọc cả file. File > 20 KB: không đọc nguyên.
- Đã Edit thì không Read lại để kiểm; dùng script check (qa_gate, lint) thay vì đọc lại bài.
- Sửa nhiều chỗ trong 1 file: gộp vào ít lần Edit; sửa máy được (`qa_lint --fix`) thì để script sửa.
- Không WebSearch / browser cho việc đã có script hoặc MCP. Kết quả MCP: dùng `meta.totals`, không tự cộng dòng.
- Lệnh lỗi: đọc thông báo lỗi, sửa nguyên nhân; không chạy lại y nguyên.

---

## 🤖 7. Vai trò (roles)
Hướng dẫn dạng văn bản trong `references/` của skill dùng chúng. Agent có subagent → giao cho subagent (brief đủ đường dẫn + tiêu chí); không có → tự làm theo file. Chỉ agent chính viết nội dung cuối.
SEO Collector `outlining/references/seo-collector.md` · Brand Guardian + Quality Guardian `qa-qc/references/` · Research Agent `setup/references/research-agent.md` · Visual Architect `image/references/visual-architect.md` (đều dưới `.agents/skills/`).

---

## 📂 8. Cấu trúc
```text
.agents/  context.md · skills/<tên>/ · rules/ · memory/ (instincts) · templates/ · config/ (gitignored)
          core/ (protocol, compliance-finance, creative layouts) · domains/ (social, ads, campaign)
knowledge/   (mục đích từng thư mục: knowledge/README.md)
  0-dashboard/ bảng điều hành, sinh tự động — không sửa tay
  1-brand/     DSC + cách viết cho mọi kênh: profile, personas, brand-facts.json, anti-ai-rules, glossary, source-whitelist
  2-market/    market-landscape · research/ · competitors/ (competitors.json, watch/<tuần>.md, profiles/)
  3-seo/       TOÀN BỘ kênh SEO
    strategy/    pages.csv (registry: 1 dòng/URL) · taxonomy.json (pillar/hub/spoke) · opportunities · topical-map
    content/     1-outlines → 2-drafts → 3-finalized → 4-cms · archive/ · images/ · audits/<đợt>/
    links/       plans/ (đợt sửa link) · dashboard.md, link-graph.html (audit) · archive/
    logs/        revision-log, qa-*-log, publish-ledger (script ghi, không sửa tay)
  4-channels/  ads/ · email/ · landing/ · social/ (syndication)
  5-analytics/ KPI, báo cáo
  6-campaigns/ job đa kênh CMP-YYMMDD-slug/ (scripts/campaign.py)
  raw/         dữ liệu thô, live/ snapshot site, serp/ cache
scripts/  script Python dùng chung · hooks/ (Claude Code) · tests/ unittest (`python -m unittest discover -s tests`)
```

---

## 🗓️ 9. Nhịp làm việc (gợi ý bước tiếp theo cho user)
| Nhịp | Thứ tự |
|---|---|
| Đầu tháng | `/analytics-report` → `/ads-audit` → `/gsc-sync` → `/keyword-plan` (ra danh sách bài tháng) |
| Mỗi bài | `/write` (Gate 1 outline, Gate 2 draft) → `/approve` → user dán CMS → `/link` backfill → `/syndicate` |
| Hằng tuần | `/weekly` (sync live, registry refresh, backfill theo lô, đo bài live ≥ 14 ngày) → bài tụt: `/optimize` · `/competitor-watch` |
| Hằng quý | `/market-research` · `/competitor-profile` đối thủ vượt DSC · `/link` chế độ audit cấu trúc |
| Khi có campaign | `/campaign-brief` → `/landing` hoặc `/copy-landing` → `/ads-brief` → `/meta-ads-copy` / `/ads-copy` → `/social-post` → `/email-sequence` → `/campaign-report` |
| Sau đợt duyệt / lỗi lặp | `/learn` |
