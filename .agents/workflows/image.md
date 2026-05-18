---
description: Tạo chiến lược hình ảnh và Gemini prompts cho bài viết đã có draft hoặc finalized
---

# Lệnh: /image [slug]

Kích hoạt Visual Architect + SEO Image Skill để tạo hệ thống hình ảnh cho bài viết.
Output: Gemini prompts sẵn sàng paste — lưu file + show inline.

Thường chạy sau khi Draft được approve hoặc bài đã finalized.

## Quy trình thực thi

### 🔄 Bước 0: Context Load
1. `.antigravity/skills/seo-image/skill.md` — Image skill (brand DNA, templates, QA)
2. `knowledge/4-content/3-finalized/Final-[slug].md` — ưu tiên file final
3. Nếu chưa final: `knowledge/4-content/2-drafts/Draft-[slug].md`
4. `knowledge/4-content/1-outlines/[slug].md` — để hiểu cấu trúc section

### Bước 1: Phân tích bài viết
- Xác định: topic chính, tone bài, các H2 section chính.
- Xác định: bài có bảng so sánh / how-to / timeline không? → quyết định có cần infographic.
- Chọn **Style Option** phù hợp từ skill (Editorial Photo / Abstract Finance / Flat Illustration).

### Bước 2: Lập Image Manifest
Quyết định số lượng và vị trí ảnh, announce cho user:

```
📸 Image Manifest — [slug]
Style: [style đã chọn]
─────────────────────────────
featured-01: [concept ngắn] → đầu bài
inline-01:   [concept ngắn] → dưới H2 "[tên section]"
inline-02:   [concept ngắn] → dưới H2 "[tên section]"
[infographic-01: nếu cần]
```

### Bước 3: Compose Gemini Prompts
- Dùng templates trong `.antigravity/skills/seo-image/skill.md`.
- Điền Brand DNA block + Image Spec + Content + Negative cho từng ảnh.
- Prompt bằng **tiếng Anh** — Imagen cho kết quả tốt nhất với English prompts.
- 1 prompt = 1 ảnh (không mega prompt).

### Bước 4: Save + Show
1. **SAVE** toàn bộ vào `knowledge/4-content/2-drafts/[slug]-image-prompts.md`
2. **SHOW** từng prompt trong code block — user copy paste thẳng vào Gemini

### Bước 5: QA Checklist
Sau khi user nhận ảnh về từ Gemini, chạy QA Checklist từ skill file.
Fail bất kỳ điểm → hướng dẫn user câu regen cụ thể.
