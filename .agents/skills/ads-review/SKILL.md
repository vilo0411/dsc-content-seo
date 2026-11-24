---
name: ads-review
description: Đọc hiệu quả quảng cáo Meta (account / campaign / job), chẩn đoán theo phễu, đề xuất việc cần làm. Read-only — không sửa campaign.
---

# /ads-review [job|campaign_id|account] [--days 7|14|30]

## Bước 0 — Context
`.antigravity/domains/ads/README.md`, `references/meta-ads-playbook.md` §4, `learnings.md`. Không cần load anti-ai / persona (không viết nội dung).

## Bước 1 — Kéo số (read-only)
1. `ads_get_ad_accounts` nếu chưa biết account; job có `ads/meta-ids.md` → dùng các ID trong đó.
2. `ads_get_ad_entities` (level campaign → ad set → ad, kỳ `--days`, mặc định 14) và chạy hết `next_actions` read-only theo hướng dẫn MCP.
3. `ads_insights_performance_trend`; nếu có bất thường `ads_insights_anomaly_signal`; ngưỡng so sánh `ads_insights_performance_vs_peers` / `ads_insights_industry_benchmark`.
4. Lưu cache: `knowledge/raw/ads/<YYYY-MM-DD>-<id>.json`.

## Bước 2 — Chẩn đoán (playbook §4)
Phân phối → chi tiêu → KPI chính vs brief → tầng phễu hỏng → creative fatigue. Ad set chưa đủ 1.000 impression / 3 ngày → "chưa đủ dữ liệu", không kết luận.

## Bước 3 — Báo cáo
`<job>/ads/review-<YYYY-MM-DD>.md` (không có job → `knowledge/raw/ads/review-<YYYY-MM-DD>.md`):
- 5 dòng tóm tắt: chi tiêu, KPI chính, so mục tiêu, top/bottom ad.
- Đề xuất đánh số, mỗi đề xuất: hành động · lý do (số) · mức ảnh hưởng ước tính · cần user xác nhận không.
- Muốn trực quan: dùng Dashboard artifact (quickstart intent "other").
Trình bày ≤ 25 dòng. Mọi thay đổi trên Meta (tắt ad, đổi budget) chỉ làm khi user yêu cầu rõ. Có pattern lặp → gợi ý `/ads-learn`.
