---
name: ads-audit
description: Audit tài khoản Google Ads của DSC từ dữ liệu thật — campaign/ad group kém, search term lãng phí, negative keyword nên thêm, chỗ trả tiền cho query đã rank top organic. Dùng khi hỏi về Google Ads, PPC, SEM, chi phí quảng cáo, CPA cao, search terms, negative keywords.
---

# Ads Audit

`/ads-audit [số ngày | YYYY-MM]` — mặc định 30 ngày gần nhất, so với kỳ liền trước. Chỉ đọc và đề xuất; **không sửa tài khoản Ads**.

## Bước 0: Context
`.agents/context.md` · `knowledge/5-analytics/kpi-definitions.md` · audit gần nhất trong `knowledge/4-channels/ads/` (nếu có, để biết đề xuất nào đã áp dụng).

## Bước 1: Lấy số (MCP, `sc-domain:dsc.com.vn`, `compare_mode=prev_period`)
- `get_ads_overview` — chi phí, clicks, conversions, CPA, CTR toàn tài khoản.
- `get_ads_breakdown` — theo campaign → ad group (và device nếu tool hỗ trợ).
- `get_ads_search_terms` — search term thật.
- `get_opportunities` + `query_search_analytics` (dimension `query`) — đối chiếu organic.
- `get_conversion_breakdown` — lead GA4 từ Paid Search, để so với conversion Ads đã báo (lệch nhiều → kiểm tra tracking).

## Bước 2: Phân tích (mỗi phát hiện kèm số)
1. **Hiệu quả theo campaign / ad group:** xếp theo CPA so với CPA trung bình tài khoản. Có chi phí, 0 conversion, ≥ 2× CPA mục tiêu → ứng viên tạm dừng hoặc thu hẹp.
2. **Search term lãng phí:** term tốn tiền mà 0 conversion; term lệch intent (tuyển dụng, "lừa đảo", tên CTCK khác khi không chạy campaign đối thủ, học thuật "là gì" cho campaign chuyển đổi). Gom thành danh sách **negative keyword** kèm match type và cấp áp dụng (campaign / account).
3. **Term tốt chưa thành keyword:** có conversion nhưng chỉ khớp qua broad/phrase → đề xuất thêm exact.
4. **Trùng paid và organic:** query brand hoặc query DSC đã rank top 3 organic mà vẫn tốn nhiều tiền → đề xuất thử giảm bid / tách brand campaign, ghi rõ rủi ro mất vị trí trên SERP.
5. **Ngược lại — khoảng trống organic:** term Ads convert tốt mà DSC chưa có bài rank → chuyển cho `/keyword-plan` / `/write`.
6. **Tracking:** conversion Ads lệch > 20% so với Lead GA4 từ Paid → cảnh báo trước khi kết luận về hiệu quả.

## Bước 3: Output → `knowledge/4-channels/ads/YYYY-MM-DD-audit.md`
```
Status: Draft
## Tóm tắt (chi phí, conversions, CPA, MoM; ước tính chi phí lãng phí/tháng)
## Việc nên làm, xếp theo tiền tiết kiệm hoặc lead tăng (ICE)
## Negative keywords đề xuất (bảng: term · chi phí · clicks · conv · match type · cấp)
## Keyword nên thêm (bảng)
## Paid ↔ Organic (bảng: query · vị trí organic · chi phí Ads · đề xuất)
## Campaign / ad group cần xem lại
## Ghi chú tracking
```
Trình bày trong chat: tóm tắt + top 5 việc + đường dẫn file.

## Related Skills
`/ads-copy` (viết lại quảng cáo cho ad group kém) · `/analytics-report` · `/keyword-plan`, `/write` (khoảng trống organic) · `/copy-landing` (landing của campaign)
