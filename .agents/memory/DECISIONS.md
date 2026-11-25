# Strategic Decisions & Lessons Learned (DECISIONS.md)

This file tracks key decisions made during the project lifecycle to ensure long-term consistency.

---

## 🏛️ Architectural Decisions
- **2026-11-25:** Gộp nhánh Marketing Workspace (main 2026-11-24) vào cấu trúc `.agents/`: `core/` + `domains/{social,ads,campaign}/` chuyển từ `.antigravity/` sang `.agents/`; job đa kênh ở `knowledge/6-campaigns/` (5 đã dùng cho `5-analytics`). Skill Meta Ads copy đổi tên `/meta-ads-copy`; `/ads-copy` giữ cho Google RSA. Học của social/ads ghi `domains/<d>/learnings.md`, không vào `instincts-by-scope/`. Ghi lên Meta chỉ khi user yêu cầu rõ, luôn PAUSED.
- **2026-05-17:** Adopted the **Multi-Agent (Sub-agent) Framework** for modularity.
- **2026-05-17:** All production files must follow the `0-sources` -> `1-outlines` -> `2-drafts` -> `3-finalized` pipeline.
- **2026-05-17:** Slash commands are the primary interface for triggering workflows.
- **2026-05-17:** Writer profiles added (`knowledge/1-brand/writers/`) — phân loại theo loại bài: educational / analytical / comparison.
- **2026-05-17:** Intel capture system added (`knowledge/raw/intel/`) — 30-second rule áp dụng khi SERP research.

## ✍️ Content & Style Decisions
- **2026-05-17:** Anti-AI rules established in `knowledge/1-brand/anti-ai-rules.md`. Chuẩn câu: tối đa 25 từ/câu, 2-3 câu/đoạn.
- **2026-05-17:** Target Persona selection is mandatory for every outline.
- **2026-05-17:** Mandatory linking strategy based on `anchor-index.md`.
- **2026-05-17:** Brand guidelines + anti-ai-rules luôn có độ ưu tiên cao hơn writer profiles khi xung đột.

## 💡 Lessons Learned (Retrospective)
- **2026-05-17:** Product Bridge cho bài kỹ thuật (P3) → ưu tiên Môi giới 1:1, không phải công cụ tư vấn số.
- **2026-05-17:** Bài về báo cáo tài chính cần thêm phần nền tảng ("cách tạo ra", "cấu trúc chi tiết") để satisfy academic search intent.
- **2026-05-17:** Không dùng ngoặc kép nhấn mạnh cho từ thông thường — trông AI rõ ràng.

## 🗂️ 2026-11-19 — Tái cấu trúc thành Digital Marketing OS
- Skill gộp 1 tầng: `.agents/skills/<tên>/` (SKILL.md + references/ + scripts/), bỏ `.antigravity/`. Chỉ dẫn chung `AGENTS.md` (CLAUDE.md / GEMINI.md import). Theo quy ước coreyhaines31/marketingskills.
- Thêm mảng: analytics-report, ads-audit, ads-copy, email-sequence, copy-landing; social dùng `/syndicate`.
- `knowledge/` chia theo mục đích: `0-dashboard` (sinh tự động), rule viết về `1-brand` (dùng cho mọi kênh), `3-pipeline` → `3-seo/{opportunities,site-structure,internal-links,logs}`, audit theo đợt về `4-content/audits/`, syndication → `5-channels/social`.
- Hook Claude Code: `guard_read.py` (chặn đọc nguyên file index lớn), `qa_reminder.py` (nhắc qa_gate 1 lần/file). Test `tests/test_skills.py` kiểm frontmatter + đường dẫn.

## 🔧 Nút thắt pipeline đã xử lý (đến 2026-11-10)

| # | Trước | Sau |
|---|---|---|
| B1 | `anti-ai-rules.md` 30 KB load nguyên file, mâu thuẫn với instincts | v3.0 12,6 KB, chỉ phần phán đoán; phần máy bắt trỏ tới lint; bản cũ ở `archive/` |
| B2 | 44 cache SERP hỏng | `serp_research.py` tự coi cache hỏng là hết hạn, lấy lại khi dùng keyword đó |
| B3 | 3 script + 3 báo cáo dài mỗi vòng; QG đọc lại cả bài | `qa_gate.py` 1 lệnh, chỉ in lỗi chặn; QG vòng 2 chỉ đọc `--changed` |
| B4 | Finalize xoá outline, mất bản v1 | `article_snapshot.py` lưu outline/gate2/final; `/learn` dùng `--diff` |
| B5 | revision-log 285 KB, bảng điểm trong file | Giữ 30 ngày + file theo quý; điểm QA (kèm slop) ở `qa-score-log.csv` |
| B6 | Backfill sửa CMS từng bài | `/weekly` gom 1 spec cho cả tuần (CMS vẫn sửa tay — không có API) |
| B7 | Đo GSC chỉ là lời nhắc | `publish-ledger.csv` + `/weekly` liệt kê bài 28–56 ngày và quy tắc quyết định |
| + | Brand Guardian load cả revision-log (95 KB) | Dùng instincts + `--show` |
| B8 | `/approve`, `/write` mở revision-log 95 KB để Edit; mục log dài 2–3 KB | `revision_log.py add` ghi thẳng, chặn trường > 400 ký tự |
| B9 | `/learn` không slug đọc cả revision-log | `revision_log.py brief` 1 dòng/mục từ lần /learn trước (~14 KB), `mark-learn` đặt mốc |
| B10 | "Chỉ đọc section persona" nhưng vẫn phải mở `personas.md` 14,5 KB | `persona.py P2 [--part bridge]` (~0,3–3 KB) |
| B11 | `/keyword-plan` đọc cả `topic-clusters.md` 27 KB + trỏ sai thư mục persona | `topic_status.py --summary` (~4 KB) + `persona.py` |
| B12 | `/optimize` load 2 skill (30 KB) lặp nhau, có chỗ lỗi thời (jina crawl, grep tay, ảnh placeholder vs sinh ảnh) | Gộp vào `optimize/SKILL.md` (11 KB); `seo-optimization/` chỉ còn template; GSC chỉ qua `dashboard_cache`; ảnh qua `/image` |
| B13 | Cổng QA chỉ đo hình thức; mọi bài 94–100 điểm | `qa_lint` thêm nhóm `coverage` + `trust`; `/approve` chặn MAJOR của 2 nhóm này |
| B14 | Entity đối thủ chỉ là cụm viết hoa, không gộp, không so với draft | `Topic Coverage` gộp đối thủ hợp lệ → `ENT-outline` / `ENT-missing` (≥ 70%) |
| B15 | `Information_Gain` chỉ kiểm "có điền"; outline có PAA tự bịa | Danh sách có `h2` + `proof` → `IG-missing`; `SERP-paa-fake`; `DUP-h2` / `DUP-faq` giữa các bài |
| B16 | 7/210 bài có link ngoài, tác giả ghi tên công cụ | `source-whitelist.md` + `SRC-missing`, `YMYL-disclaimer`, `EEAT-firsthand`; Author = Chứng khoán DSC |
| B17 | Không kiểm câu đầu mỗi H2; slop phạt câu định nghĩa | `GEO-h2-answer`; `SLOP-h2-open` miễn heading "X là gì" |
| B18 | Digest SERP ~30 KB chép vào outline; gate dán lại cả bài | Digest gọn 6–10 KB; outline không chép cây heading; gate chỉ in tóm tắt ≤ 25 dòng |
| B19 | `CLAUDE.md` 20,7 KB; finalize / QA / quy tắc link chép ở 5–9 file | `CLAUDE.md` 12 KB (bảng script → `scripts/README.md`); mỗi quy trình 1 nguồn |
| B20 | Thêm bài vào `anchor-index` / `topic-clusters` phải mở file lớn | `find_links.py --add-anchor`, `topic_status.py --add` |
| B21 | Kết quả GSC không quay lại pipeline; pillar đang rank bị tái cấu trúc | Sổ lưu GSC cạnh điểm QA (`--outcomes`); `/optimize` giới hạn khi vị trí ≤ 5 |

## 🧩 2026-11-19 (đợt 2) — MECE, registry, theo dõi đối thủ
- `knowledge/` MECE: nền (`1-brand`, `2-market`) → kênh (`3-seo` lõi = strategy/content/links/logs, `4-channels`) → đo lường (`5-analytics`) · `raw/` · `0-dashboard/`.
- Internal link + trạng thái bài: 1 nguồn `3-seo/strategy/pages.csv` (`scripts/registry.py`), kiến trúc ở `taxonomy.json` (đổi tên từ link-clusters.json). Bỏ anchor-index.md, anchor-keys.csv, topic-clusters.md (archive `links/archive/legacy-2026-11-19/`). Lý do: 3 cách chia cluster lệch nhau; slug file ≠ slug live không có chỗ map.
- Theo dõi đối thủ: `competitor_watch.py` (sitemap/listing diff, stdlib). Sitemap lastmod không dùng (VPBankS gắn 1 ngày cho mọi URL) → "mới" = URL chưa thấy, ngày = published trên trang. Đối thủ chọn từ SERP cache (VCBS, DNSE, ACBS, Vietcap, VFS) + VPBankS.
- Dashboard theo workflow: bài theo bước, registry, đối thủ, báo cáo tháng, bản nháp kênh.
