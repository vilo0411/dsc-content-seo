---
name: analytics-report
description: Báo cáo marketing tháng hoặc tuần cho DSC (SEO + GA4 + Google Ads + AI traffic), so kỳ trước, giải thích nguyên nhân và đề xuất việc làm tiếp. Dùng khi cần báo cáo KPI, báo cáo tháng, monthly report, weekly report, lead, CPL, CPA, traffic theo kênh.
---

# Analytics Report

`/analytics-report [YYYY-MM | YYYY-Www] [--compare ly]` — mặc định: tháng trước, so với tháng liền trước.

## Bước 0: Context
1. `.agents/context.md`
2. `knowledge/5-analytics/kpi-definitions.md` (công thức + nguồn MCP của từng chỉ số)
3. Báo cáo kỳ trước trong `knowledge/5-analytics/reports/` nếu có — để nối tiếp việc đã đề xuất.

## Bước 1: Lấy số (SEO Dashboard MCP, `property_url = sc-domain:dsc.com.vn`)
Dùng `start_date`/`end_date` đúng kỳ, `compare_mode=prev_period` (hoặc `same_period_ly` khi `--compare ly`). Gọi song song:
- `get_data_freshness` — kỳ chưa đủ dữ liệu thì ghi rõ trong báo cáo, không ngoại suy.
- SEO: `get_overview`, `get_brand_split`, `get_rank_changes`, `get_new_lost_rankings`, `get_pages` (top + giảm mạnh).
- GA4: `get_ga4_acquisition`, `get_ga4_engagement`, `get_conversion_breakdown`, `get_ga4_funnels`.
- Ads: `get_ads_overview`, `get_ads_breakdown`.
- Chi phí: `get_cost_cpl`. AI: `get_ai_traffic`.
- Ngữ cảnh: `get_google_updates`, `list_annotations` (bài mới, sửa link, thay đổi site).

Không có MCP → `python scripts/dashboard_cache.py status` / `report`, và ghi rõ báo cáo dùng số cache ngày nào.

## Bước 2: Phân tích
- Chỉ số nào đổi ≥ 10% MoM → tìm nguyên nhân: Google update? annotation? trang/query nào đóng góp? brand hay non-brand? Cần đào sâu traffic SEO giảm thì dùng skill plugin `seodash-diagnose` nếu agent có.
- Đối chiếu SEO với Ads: query vừa trả tiền vừa rank top 3 organic (`get_opportunities` mục paid/organic overlap) → đề xuất cho `/ads-audit`.
- Lead: tách theo kênh và landing page. CVR giảm mà traffic tăng → vấn đề chuyển đổi (`/cro`, `/copy-landing`), không phải SEO.

## Bước 3: Viết báo cáo → `knowledge/5-analytics/reports/<kỳ>.md`
```
# Báo cáo marketing <kỳ>  (so <kỳ so sánh>, dữ liệu tới <ngày>)
## Tóm tắt (≤ 5 dòng: Lead, CPL SEO, CPA Ads, 1 điểm tốt, 1 điểm xấu)
## Bảng KPI theo kênh (SEO · Ads · AI · Tổng) — giá trị, MoM %
## SEO: clicks / impressions / position; brand vs non-brand; trang tăng giảm mạnh
## Google Ads: chi phí, conversions, CPA, campaign nổi bật
## Chuyển đổi: Lead theo kênh / landing page, funnel
## Vì sao thay đổi (mỗi ý có số làm bằng chứng)
## Việc nên làm (≤ 5, có owner skill: /optimize, /ads-audit, /cro…, ước lượng tác động)
## Theo dõi việc kỳ trước (đã làm? kết quả?)
```
Số trong bảng lấy từ `meta.totals` của MCP, không tự cộng dòng. Trình bày trong chat: tóm tắt + bảng KPI + đường dẫn file.

## Ghi activity log (bước cuối)
Sau khi lưu output (và sau mỗi lần user duyệt → `--action approve`): `python scripts/activity_log.py add --domain analytics --skill analytics-report --action report --target <YYYY-MM | tuần> --path <file báo cáo>`. Hiện ở tab **Hoạt động** của `knowledge/0-dashboard/index.html`.

## Related Skills
`/ads-audit` (chi tiết Ads) · `/optimize`, `/weekly` (việc SEO) · `/cro`, `/copy-landing` (CVR) · `seo-dashboard` (cách dùng MCP + cache)
