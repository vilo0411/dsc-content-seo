---
name: campaign-brief
description: Khởi tạo chiến dịch marketing đa kênh — tạo job folder CMP-YYMMDD-slug, điền brief (mục tiêu, persona, thông điệp, kênh) và tách việc con cho /write, /social-post, /ads-brief, /landing.
---

# /campaign-brief <tên chiến dịch> [--channels seo,social,ads,landing]

## Bước 0 — Context
`.antigravity/core/README.md` §1 + `.antigravity/domains/campaign/README.md` + `.antigravity/rules/cta-conversion.md`.

## Bước 1 — Tạo job
```bash
python scripts/campaign.py new <slug> --title "<tên>" --channels <kênh>
```
In ra đường dẫn job; brief.md sinh từ `.antigravity/domains/campaign/references/brief-template.md`.

## Bước 2 — Điền brief
- Hỏi user 1 lần (gộp) những gì không suy ra được: mục tiêu kinh doanh + số, thời gian, ngân sách, offer.
- Persona & trigger: `python scripts/persona.py --matrix`. Insight thật: SEO Dashboard MCP (`query_search_analytics` theo query liên quan) hoặc `python scripts/dashboard_cache.py report <slug>`; PAA từ `serp_research.py` cache nếu có.
- Bằng chứng: chỉ số từ `profile.md`, `market_facts.py --brief`. Claim mới → mục "Claim cần pháp chế duyệt".
- Bảng việc con: mỗi kênh 1–3 việc, ghi lệnh sẽ chạy. SEO: kiểm keyword đã có URL DSC rank chưa (`python scripts/find_links.py "<kw>"`) trước khi đề xuất bài mới.

## Bước 3 — Gate
Trình bày brief ≤ 25 dòng + đường dẫn. Dừng chờ duyệt. Duyệt → `python scripts/campaign.py set <slug> --status "Đang làm"` rồi chạy việc con theo thứ tự: landing (đích của ads) → ads → social → SEO.
