---
name: creative
description: Dựng ảnh quảng cáo Meta / post social / carousel từ file copy đã lint — design.json → PNG đúng brand (chữ tiếng Việt thật, logo, màu), QA máy + QA mắt, duyệt theo version. Tự chạy trong /meta-ads-copy và /social-post.
---

# /creative <file copy | design.json> [--only id,id] [--bump]

## Bước 0 — Context
`knowledge/1-brand/DESIGN.md` (chuẩn hình fanpage — đọc trước) + `.agents/core/creative/README.md` (luồng, schema, layout, QA) + `knowledge/1-brand/brand.json`. Không cần load anti-ai / persona — chữ đã được duyệt ở file copy.

## Bước 1 — design.json
- Chưa có: `python scripts/creative.py init <copy.md>` → `<kênh>/creatives/design.json`.
- Chỉnh design.json (không sửa HTML/PNG):
  - Chọn layout (`python scripts/creative.py layouts`). Mặc định: quảng cáo / ảnh bìa / post chính → `kv-right`/`kv-left`/`kv-center` (theme `emerald` cho sản phẩm & thị trường, `ivory` cho văn hoá & thông báo) + mục `kv`; con số là ý chính → `bignum` theme `emerald`; slide giữa carousel → `rows`; slide cuối → `cta-end` theme `emerald`. `hero` (minh hoạ isometric blog) chỉ khi cần ảnh nhanh; `thesis` (chỉ chữ) khi user muốn tối giản.
  - Khối chữ KV: `badge` (tên sự kiện/sản phẩm, ≤ 3 từ) → `script` (dòng cảm xúc 2–5 từ, chữ viết tay) → `headline` (in hoa ánh kim; `type` serif cho trang trọng, sans cho sự kiện/số) → `sub`. Tối đa 2 font display.
  - `kv`: `subject` mô tả chủ thể + ẩn dụ (đồng hành → đôi hạc; hướng dẫn → đèn lồng; bắt đầu → bậc đá đầu tiên), `motifs` theo DESIGN.md §5, `mood`. **Lấy nền theo thứ tự rẻ → đắt:** (1) `python scripts/creative.py pick <design.json>` — chọn từ thư viện `knowledge/1-brand/assets/library/` (0 quota, vài giây; xem `library/README.md`), có thể thêm motif tách nền qua `"layers"`; (2) ảnh nào không có nền hợp mới `generate`. KV mới được duyệt → `python scripts/asset_lib.py add …` vào thư viện.
Với (2): `python scripts/creative.py generate <design.json> --dry-run` (kiểm prompt) → hỏi user trước khi tạo thật (tốn quota Codex) → `generate <design.json> [--only id]` → ảnh vào `assets/`. Tạo thử 1 ảnh, cho user xem, rồi mới tạo cả bộ. Ảnh xấu → sửa `kv` trong design.json rồi `generate --only id --force`. Máy không có Codex → `creative.py prompt` (prompts.md để dán tay).
  - Minh hoạ: lấy từ kho `knowledge/3-seo/content/images/` trước (README §5), copy vào `creatives/assets/`, chỉnh `focus`. Quảng cáo: không chọn ảnh có đồng xu / $ / mũi tên đi lên.
  - Thêm `eyebrow` (nhãn 2–4 từ) và `sub` (1 câu từ copy đã duyệt) để ảnh đủ tầng thông tin.
  - Đánh `**cụm nhấn**` 1 chỗ / tiêu đề. Không đổi chữ của headline — chữ bị khoá theo file copy (`TEXT-locked`). Muốn đổi chữ → sửa file copy, chạy `mkt_lint`, xoá design.json, init lại.
  - Carousel: điền mọi `TODO` (headline + items của slide giữa, câu chốt slide cuối). Chữ mới trên slide phải lấy từ nội dung post đã duyệt, không thêm claim mới.
  - Có claim phí/lãi suất trên ảnh → `note` pháp lý phải có.

## Bước 1b — Đa kênh
User cần nhiều kênh/khổ → `python scripts/creative.py adapt <design.json> --channel <kênh>` (hoặc `--sizes`). Mặc định quảng cáo Meta: `--channel meta-ads` (feed 4:5, vuông, story 9:16, ngang 1.91:1).

## Bước 2 — Render + QA (tối đa 2 vòng)
```bash
python scripts/creative.py render <design.json> [--only id]
```
- Exit 1 = còn lỗi máy → sửa design.json (rút gọn, đổi layout/khổ) rồi render lại.
- Sau khi máy đạt: chạy `creative-qa` (`.agents/core/agents/creative-qa.md`, sub-agent read-only) đọc PNG — bố cục, khoảng trống, dòng ngắt, ý ảnh khớp post.

## Bước 3 — Gate
Trình bày ≤ 20 dòng: bảng id · khổ · layout · trạng thái QA; đường dẫn `v<N>/preview.html` (xem cả bộ + cỡ điện thoại); việc cần user (ảnh minh hoạ, chữ cần đổi). Dừng chờ duyệt.

## Bước 4 — Duyệt
```bash
python scripts/creative.py approve <design.json> --ids all|id,id --xac-nhan "<nguyên văn lời duyệt của user>"
```
→ `<job>/approved/<JOB>-<id>-v<N>.png`. Từ chối nếu còn lỗi QA (trừ khi user chấp nhận → `--chap-nhan-loi`). Sửa sau duyệt: `render --bump`.
Đưa lên Meta: tên ad theo `<JOB> | <id> | v<N>` (README §6).
