# Landing 1 trang — khung chuẩn

Thứ tự section (bỏ section không có chất liệu thật, không độn):
1. **Hero** — headline = lời hứa của ad dẫn tới (khớp chữ), 1 câu phụ, CTA chính, hình S01 hoặc ảnh app thật.
2. **3 lợi ích** — mỗi lợi ích 1 con số/điều kiện kiểm chứng được (`profile.md`).
3. **Cách hoạt động** — 3 bước (vd. eKYC → nạp tiền → đặt lệnh), ảnh chụp màn hình thật nếu có.
4. **Bằng chứng** — số liệu có nguồn + mốc thời gian; không testimonial bịa.
5. **FAQ** — 4–6 câu từ PAA / GSC query của keyword liên quan.
6. **CTA cuối + miễn trừ** — CTA lặp lại, dòng pháp lý (điều kiện ưu đãi, "không phải khuyến nghị đầu tư" nếu có nhận định).

## Kỹ thuật
- HTML 1 file, CSS inline từ `knowledge/1-brand/brand.json` (màu, font Plus Jakarta Sans, thang chữ `fonts.web_scale_pt` — DESIGN.md v1.0), mobile-first, không màu đỏ.
- 1 CTA chính lặp lại (hero, giữa, cuối) → `open_account_url` hoặc form; không 3 CTA khác nhau.
- Copy đi qua `mkt_lint.py --channel landing` trước khi dựng HTML.
- Thẻ meta title/description; nếu cần index thì brief SEO riêng qua `/outlining`.
