---
name: campaign-report
description: Báo cáo kết quả 1 chiến dịch đa kênh — gộp GSC (SEO), Meta Ads, social/syndication vào report.md so với KPI trong brief; đề xuất bước tiếp.
---

# /campaign-report <job> [--date YYYY-MM-DD]

## Bước 0 — Context
`<job>/brief.md` (KPI, kênh, ngày Live). Không load anti-ai/persona.

## Bước 1 — Số theo kênh (đọc cache trước, gọi API khi thiếu)
| Kênh | Nguồn |
|---|---|
| SEO | SEO Dashboard MCP `query_search_analytics` theo page của các slug trong `seo/` → `python scripts/dashboard_cache.py save page-queries <slug>`; không có MCP: `python scripts/dashboard_cache.py report <slug>` |
| Ads | `knowledge/raw/ads/*.json` mới nhất của các ID trong `ads/meta-ids.md`; cũ hơn 3 ngày → `/ads-review` (read-only) |
| Social | số user dán / export Meta Business Suite; syndication: `knowledge/raw/operations/syndication/ledger.csv` (checks +7/+14/+28) |

Kênh thiếu số → ghi "chưa có số", không ước đoán.

## Bước 2 — report.md
`<job>/report.md`: bảng KPI (mục tiêu · thực tế · % đạt · nguồn), mỗi kênh 3 dòng nhận xét, 3 đề xuất có lý do bằng số. Muốn trực quan → Dashboard artifact (quickstart intent "other").
`python scripts/campaign.py set <job> --status "Đo kết quả"` (hoặc "Đóng" khi user xác nhận kết thúc).

## Bước 3
Trình bày ≤ 20 dòng. Có bài học ads → gợi ý `/ads-learn`; bài SEO tụt → `/optimize`.
