---
name: market-research
description: "Nghiên cứu thị trường chứng khoán / nhà đầu tư cá nhân cho DSC: quy mô & xu hướng (số tài khoản, thanh khoản, quy định mới), mối quan tâm và nỗi lo của nhà đầu tư theo persona, bản đồ đối thủ. Dùng khi hỏi market research, xu hướng thị trường, insight khách hàng, cập nhật market landscape, chuẩn bị kế hoạch quý."
---

# Market Research

`/market-research [landscape | audience | <chủ đề>]` — theo quý hoặc trước khi lập kế hoạch lớn.
Khung theo `customer-research` + `content-strategy` của coreyhaines31/marketingskills: insight xếp theo tần suất × mức độ, mỗi insight có độ tin cậy (cao / vừa / thấp) và nguồn.

## Bước 0 — Context
`.agents/context.md` · `knowledge/2-market/market-landscape.md` (bản hiện tại) · `knowledge/1-brand/personas.md` qua `python scripts/persona.py --matrix`.

## Bước 1 — Nguồn theo loại câu hỏi
| Câu hỏi | Nguồn (ưu tiên script / nguồn chính thức) |
|---|---|
| Số liệu thị trường (VN-Index, thanh khoản, mã) | `python scripts/market_facts.py --brief` |
| Số tài khoản, quy định, văn bản | nguồn trong `knowledge/1-brand/source-whitelist.md` (VSDC, UBCKNN, HOSE…) — ghi kỳ số liệu |
| Tin mới / sự kiện | `python scripts/news_feed.py --topic "<chủ đề>" --days 30` |
| Nhà đầu tư quan tâm gì | GSC query của DSC (MCP `query_search_analytics`, nhóm theo chủ đề) · PAA/related trong `knowledge/3-seo/strategy/serp-opportunities.md` · `knowledge/raw/intel/dump.md` |
| Đối thủ đang đẩy chủ đề gì | `knowledge/2-market/competitors/watch/` (4 tuần gần nhất) · `competitor_watch.py discover` |
Chỉ WebSearch khi các nguồn trên không trả lời được.

## Bước 2 — Output
- `landscape` → cập nhật `knowledge/2-market/market-landscape.md` (giữ cấu trúc; mỗi số có kỳ + link; đổi `Last_Updated`).
- `audience` / chủ đề → `knowledge/2-market/research/<chu-de>-YYYY-MM.md`:
```
# <Chủ đề> — YYYY-MM
## Tóm tắt (3–5 dòng)
## Insight chính (xếp theo tần suất × mức độ) — mỗi insight: bằng chứng · độ tin cậy · persona liên quan
## Số liệu thị trường (bảng, kỳ, nguồn)
## Hàm ý: content (→ /keyword-plan), sản phẩm/CTA (→ /copy-landing), kênh (→ /ads-copy, /email-sequence)
## Câu hỏi còn mở / cần lãnh đạo xác nhận (→ knowledge/1-brand/confirm-with-leadership.md)
```
Dữ kiện / suy luận tách riêng. Không có nguồn → không đưa số.

## Related Skills
`/competitor-watch` · `/competitor-profile` · `/keyword-plan` · `/analytics-report`
