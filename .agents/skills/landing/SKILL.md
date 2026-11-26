---
name: landing
description: Viết copy và dựng landing page HTML 1 trang theo brand.json cho 1 chiến dịch / sản phẩm DSC; QA copy bằng mkt_lint, CTA theo cta-conversion. Không publish lên CMS.
---

# /landing <job|sản phẩm> [--persona P<n>]

## Bước 0 — Context
`.agents/core/README.md` §1 (gồm `brand.json`) + `.agents/domains/campaign/references/landing-structure.md` + `.agents/rules/cta-conversion.md` + persona `python scripts/persona.py P<n> --part bridge` + `knowledge/2-market/research/voc-objections.md` (câu hỏi thật & rào cản chuyển đổi).
Thiết kế: load skill `frontend-design` nếu có trong session.

## Bước 1 — Copy
- Headline hero khớp chữ với lời hứa của ad (`<job>/approved/ads-copy-*.md`) nếu landing là đích quảng cáo.
- Section theo `landing-structure.md`; FAQ lấy câu hỏi thật (PAA / GSC).
- File: `<job>/landing/copy-v1.md`.
```bash
python scripts/mkt_lint.py <job>/landing/copy-v1.md --channel landing
```
+ Compliance Reviewer. Dừng ở gate copy trước khi dựng HTML.

## Bước 2 — HTML
- `<job>/landing/landing-v1.html`: 1 file, CSS inline từ `brand.json` / `DESIGN.md` v1.0 (palette Gunmetal/Pine Teal/Lime/Emerald/Frosted Mint, font Plus Jakarta Sans nhúng `@font-face` + thang chữ web H1 56/700 … Subtitle 14/400; nút Lime chữ Gunmetal), mobile-first, 1 CTA chính lặp 3 lần → `open_account_url` hoặc form user chỉ định.
- Kiểm: mở bằng trình duyệt (skill `run` / Claude in Chrome nếu user cho phép), chụp mobile 390px + desktop.
- Muốn xem/chia sẻ nội bộ: publish Artifact (private).

## Bước 3 — Gate
Trình bày ảnh chụp + đường dẫn file + lint. Duyệt → copy vào `<job>/approved/`. Đưa lên CMS là việc user (hoặc dev web) làm.
