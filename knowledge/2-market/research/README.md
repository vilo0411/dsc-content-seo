# knowledge/2-market/research/ — Nghiên cứu Thị trường & Voice of Customer (VoC)

Thư mục này lưu các báo cáo nghiên cứu khách hàng và chủ đề thị trường do skill `/market-research` sinh ra.

## Quy tắc chống bịa dữ liệu (Zero-Hallucination Policy)

1. **Không bao giờ tự bịa quote, survey hay testimonial của khách hàng.**
2. Mọi nhận định về mối quan tâm, câu hỏi hoặc rào cản tâm lý (Objections) của nhà đầu tư trong thư mục này bắt buộc phải trích xuất từ **5 nguồn dữ liệu thật có thể kiểm chứng**:
   - **Nguồn 1 — SERP PAA & Related Searches:** `knowledge/3-seo/strategy/serp-opportunities.md` (128 câu PAA + 755 related searches trích tự động từ DataForSEO SERP cache).
   - **Nguồn 2 — Google Search Console (GSC):** `knowledge/3-seo/strategy/gsc-opportunities.md` hoặc truy vấn trực tiếp qua SEO Dashboard MCP (`query_search_analytics`, property `sc-domain:dsc.com.vn`).
   - **Nguồn 3 — Google Ads / Meta Ads:** Search terms thật (`get_ads_search_terms`) và hiệu quả angle quảng cáo thực tế trong `.agents/domains/ads/learnings.md`.
   - **Nguồn 4 — Revision Log & Content Audit:** `knowledge/3-seo/logs/revision-log.md` (những điểm độc giả/user yêu cầu làm rõ trong bài viết).
   - **Nguồn 5 — Intel Dump:** `knowledge/raw/intel/dump.md` (ghi chú nhanh của team trong quá trình research).

## Danh mục file hiện có

| File | Mục đích | Ai đọc |
|---|---|---|
| [`voc-objections.md`](voc-objections.md) | **Sổ tay Ngôn ngữ Khách hàng (VoC) & Xử lý Rào cản (Objections)** theo 4 Persona P1–P4, tổng hợp từ 114 SERP cache + GSC `dsc.com.vn`. | `/copy-landing`, `/landing`, `/ads-brief`, `/meta-ads-copy`, `/ads-copy`, `/outlining`, `/cro` |
| `<chu-de>-YYYY-MM.md` | Báo cáo nghiên cứu chuyên đề theo tháng/quý do `/market-research <chủ đề>` tạo ra. | `/keyword-plan`, `/campaign-brief` |
