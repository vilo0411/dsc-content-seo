---
name: outlining
description: "Phase 1-2: kiểm cannibalization, SERP research (serp_research.py), dựng Expert Outline + outline_lint, dừng chờ duyệt. Dùng khi /outlining <keyword> hoặc 'lên dàn ý'. Muốn chạy luôn tới draft thì /write."
---

# Nghiên cứu SERP & Tạo Expert Outline

Dùng khi chỉ muốn làm Research + Outline, chưa viết bài. Tương đương Giai đoạn 1 của `/write`.
**Quy tắc chi tiết nằm ở `.agents/skills/outlining/references/playbook.md`** — file này chỉ là thứ tự các bước.

## Quy trình

### Bước 0: Context Load (1 lần / session)
`knowledge/1-brand/profile.md` · `knowledge/1-brand/anti-ai-rules.md` · `knowledge/1-brand/glossary.md` · `.agents/memory/instincts.md` (+ `instincts-by-scope/<topic>.md` nếu bài thuộc topic đó).
- Trạng thái bài: `python scripts/topic_status.py <slug>`. Không đọc `pages.csv`.
- Persona: `python scripts/persona.py P<n>` sau Bước 2 (không mở `personas.md`).

### Bước 0.5: Cannibalization Gate (trước khi gọi SERP có phí)
- Có MCP `SEO Dashboard`: `query_search_analytics` (`property_url: "sc-domain:dsc.com.vn"`, `dimensions: ["page"]`, `query_value: "[keyword]"`, `days: 90`, `limit: 10`).
- Không có MCP: `python scripts/find_links.py "[keyword]" --top 5`.
- Đã có URL DSC cùng intent đang ở top 10, hoặc keyword là `pillar_keyword` / dòng `Merged → …` (outline_lint `KW-pillar`) → **DỪNG**, đề xuất `/optimize [slug]`. Khác intent → ghi ranh giới vào mục Gap Synthesis + link chéo 2 chiều.

### Bước 1: SEO Collector — SERP, khung bài, dữ liệu, link
Agent `.agents/skills/outlining/references/seo-collector.md` chạy Step 1–3 của `outlining/references/playbook.md`:
1. `serp_research.py` → kiểm `⚠️ SERP_CHECK` (SERP sai → refetch / nhờ user dán SERP ẩn danh) → **chốt khung bài theo block `SERP Format & Intent`** → chốt độ dài, vị trí H2 hướng dẫn, kiểu sapo theo block `Structure consensus` (đọc từ full text đối thủ, không chỉ heading).
2. SERP degraded → báo user trước khi đi tiếp.
3. **EAV (thuộc tính phải nêu giá trị):** `serp_research.py "[keyword]" --eav` (đọc full text đối thủ trong cache, 0 phí; chưa có nội dung thì chạy `--extract 5` trước) + `python scripts/registry.py cluster <mã cụm>` (thực thể, thuộc tính cụm, `bridge_to`). Gộp tên đồng nghĩa → khối `EAV:` của outline: mọi thuộc tính **root**, ≥ 1 dòng **rare/unique**; value lấy từ `brand-facts.json` / `market_facts.py` / URL whitelist — số của đối thủ chỉ là bằng chứng, không phải nguồn. Cụm `outer` → outline có 1 đoạn/H2 cầu nối về `bridge_to` (qa_lint `LINK-bridge`).
4. Dữ liệu: `market_facts.py --brief`, `news_feed.py`. Ưu tiên số năm hiện tại.
5. Internal links: `find_links.py`, 3–6 link `/kien-thuc/`.

> **30-second Rule:** data/insight hay nhưng không dùng cho bài này → ghi 1 dòng vào `knowledge/raw/intel/dump.md` (ngày + nguồn + mô tả).

### Bước 2: Brand Guardian — Brand Context
Agent `.agents/skills/qa-qc/references/brand-guardian.md` → Writer Profile + 3 đặc điểm tone, USP, lỗi cũ, xung đột instinct ↔ phản hồi user. Ghi vào **mục 4 Brand Context** của outline (không để chỉ trong chat).

### Bước 3: Dựng outline + Gate
- Theo `.agents/skills/outlining/references/brief-template.md`, lưu tại `knowledge/3-seo/content/1-outlines/[slug].md`.
- `python scripts/outline_lint.py knowledge/3-seo/content/1-outlines/[slug].md` → FAIL thì sửa, tối đa 2 vòng.
- `python scripts/topic_status.py [slug] --set Outlining`.

### 🚧 APPROVAL GATE
> Trình bày: khung bài đã chọn + bảng SERP Format, Thesis, cây H2/H3 (vị trí H2 hướng dẫn so với median đối thủ), **sapo nguyên văn**, số từ so với median, kết quả lint.
> **DỪNG. Chờ `/approve`.** Khi approve: `python scripts/topic_status.py [slug] --set Outline-Approved`.
