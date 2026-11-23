---
name: copy-landing
description: Viết hoặc viết lại copy landing page cho DSC (mở tài khoản, margin, môi giới 1:1, DSC Invest, landing cho campaign Ads) theo persona — hero, lợi ích, xử lý lo ngại, bằng chứng, FAQ, CTA — kèm đề xuất A/B. Dùng khi cần landing page copy, trang đích, CTA trang, tối ưu trang chuyển đổi.
---

# Copy Landing

`/copy-landing [URL | sản phẩm] [--persona P1-P4] [--variants N]` — soạn copy + wireframe chữ; không sửa CMS.

Khác `/cro`: `/cro` gắn CTA/banner **vào bài SEO**; skill này viết **cả trang đích**.

## Bước 0: Context
1. `.agents/context.md`
2. `.agents/rules/cta-conversion.md` (offer, CTA) · `.agents/skills/cro/references/cro-principles.md`
3. `knowledge/1-brand/brand-facts.json` · `knowledge/1-brand/service-operations.md` · `knowledge/1-brand/anti-ai-rules.md` · `glossary.md`
4. Persona: `python scripts/persona.py P<n>` (đủ cả bridge + tone)
5. Trang hiện tại (nếu viết lại): nội dung live (`python scripts/sync_live.py --show <slug>` hoặc tải URL) + số liệu: MCP `get_pages` / `get_conversion_breakdown` lọc theo landing (sessions, lead, CVR); nguồn traffic chính (Ads keyword nào, bài SEO nào dẫn tới).

## Bước 1: Chẩn đoán (trình user)
- 1 câu: người vào trang này là ai, đến từ đâu, muốn gì.
- Trang hiện tại trả lời được gì, thiếu gì (5 giây đầu có thấy offer + lợi ích + CTA không; lo ngại chính của persona đã được xử lý chưa; bằng chứng; form dài không).
- Mục tiêu đo: CVR hiện tại → giả thuyết cải thiện.

## Bước 2: Viết copy theo khối
1. **Hero:** headline ≤ 10 từ nói kết quả cho người đọc · sub ≤ 25 từ · CTA chính theo persona · 1 dòng tin cậy.
2. **Lợi ích (3):** mỗi khối = tiêu đề + 1–2 câu + số từ brand-facts.
3. **Cách hoạt động:** 3 bước, khớp `service-operations.md`.
4. **Xử lý lo ngại:** lấy "trigger sợ" của persona, trả lời thẳng.
5. **Bằng chứng:** chỉ dùng thứ có thật (số liệu verified, giấy phép, đánh giá user cung cấp). Không bịa testimonial.
6. **FAQ (4–6):** lấy từ search term Ads / query GSC của trang (MCP `query_search_analytics` dimension `query` lọc page).
7. **CTA cuối + miễn trừ / thông tin pháp lý** nếu có nhận định đầu tư.

Ràng buộc: không hứa lợi nhuận, số chưa verified không dùng, câu nghi vấn → `[CẦN PHÁP CHẾ DUYỆT]`. Câu ≤ 25 từ.

## Bước 3: Tự kiểm
Soát blacklist + glossary; mọi số đối chiếu brand-facts; CTA đúng persona (`persona.py --matrix`); offer + URL đúng `cta-conversion.md`.

## Output → `knowledge/4-channels/landing/YYYY-MM-DD-<trang>.md`
`Status: Draft` · chẩn đoán · copy theo khối (dạng wireframe chữ, ghi vị trí trên trang) · `--variants N`: N phiên bản hero cho A/B kèm giả thuyết + chỉ số đo · ghi chú pháp chế.

## Related Skills
`/cro` (CTA trong bài SEO) · `/ads-copy` (ad trỏ về landing này) · `/email-sequence` · `/analytics-report` (đo CVR trước/sau)
