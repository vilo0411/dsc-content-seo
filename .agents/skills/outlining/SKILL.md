---
name: outlining
description: Nghiên cứu SERP và tạo Expert Outline (Phase 1 & 2 của write pipeline).
---

# Nghiên cứu SERP & Tạo Expert Outline

Dùng khi chỉ muốn làm Research + Outline, chưa viết bài. Tương đương Giai đoạn 1 của `/write`.
**Quy tắc chi tiết nằm ở `.antigravity/skills/seo-outlining/SKILL.md`** — file này chỉ là thứ tự các bước.

## Quy trình

### Bước 0: Context Load (1 lần / session)
`knowledge/1-brand/profile.md` · `knowledge/3-pipeline/anti-ai-rules.md` · `knowledge/3-pipeline/glossary.md` · `.antigravity/memory/instincts.md` (+ `instincts-by-scope/<topic>.md` nếu bài thuộc topic đó).
- Trạng thái bài: `python scripts/topic_status.py <slug>`. Không đọc `topic-clusters.md`.
- Persona: `python scripts/persona.py P<n>` sau Bước 2 (không mở `personas.md`).

### Bước 0.5: Cannibalization Gate (trước khi gọi SERP có phí)
- Có MCP `SEO Dashboard`: `query_search_analytics` (`property_url: "sc-domain:dsc.com.vn"`, `dimensions: ["page"]`, `query_value: "[keyword]"`, `days: 90`, `limit: 10`).
- Không có MCP: `python scripts/find_links.py "[keyword]" --top 5`.
- Đã có URL DSC cùng intent đang ở top 10 → **DỪNG**, đề xuất `/optimize [slug]`. Khác intent → ghi ranh giới vào mục Gap Synthesis + link chéo 2 chiều.

### Bước 1: SEO Collector — SERP, khung bài, dữ liệu, link
Agent `.antigravity/agents/seo-collector.md` chạy Step 1–3 của `seo-outlining/SKILL.md`:
1. `serp_research.py` → **chốt khung bài theo block `SERP Format & Intent`** (toplist / how-to / định nghĩa / so sánh…).
2. SERP degraded → báo user trước khi đi tiếp.
3. Dữ liệu: `market_facts.py --brief`, `news_feed.py`. Ưu tiên số năm hiện tại.
4. Internal links: `find_links.py`, 3–6 link `/kien-thuc/`.

> **30-second Rule:** data/insight hay nhưng không dùng cho bài này → ghi 1 dòng vào `knowledge/raw/intel/dump.md` (ngày + nguồn + mô tả).

### Bước 2: Brand Guardian — Brand Context
Agent `.antigravity/agents/brand-guardian.md` → Writer Profile + 3 đặc điểm tone, USP, lỗi cũ, xung đột instinct ↔ phản hồi user. Ghi vào **mục 4 Brand Context** của outline (không để chỉ trong chat).

### Bước 3: Dựng outline + Gate
- Theo `.antigravity/skills/seo-outlining/references/brief-template.md`, lưu tại `knowledge/4-content/1-outlines/[slug].md`.
- `python scripts/outline_lint.py knowledge/4-content/1-outlines/[slug].md` → FAIL thì sửa, tối đa 2 vòng.
- `python scripts/topic_status.py [slug] --set Outlining`.

### 🚧 APPROVAL GATE
> Trình bày: khung bài đã chọn + bảng SERP Format, Thesis, cây H2/H3, kết quả lint.
> **DỪNG. Chờ `/approve`.** Khi approve: `python scripts/topic_status.py [slug] --set Outline-Approved`.
