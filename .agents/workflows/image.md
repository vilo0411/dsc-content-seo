---
description: Tạo chiến lược hình ảnh cho bài viết đã có draft hoặc finalized
---

# Lệnh: /image [slug]

Kích hoạt Visual Architect để đề xuất hệ thống hình ảnh phù hợp với bài viết.
Thường chạy sau khi Draft được approve hoặc bài đã finalized.

## Quy trình thực thi

### 🔄 Bước 0: Context Load
1. `knowledge/1-brand/visual-brand-guidelines.md` — Brand color, style guidelines
2. `knowledge/4-content/1-outlines/[slug].md` — Outline để hiểu intent bài
3. Nếu draft tồn tại: `knowledge/4-content/2-drafts/Draft-[slug].md`
4. Nếu đã finalized: `knowledge/4-content/3-finalized/Final-[slug].md`

### Bước 1: Visual Architect Analysis
- Kích hoạt agent `.antigravity/agents/visual-architect.md`.
- Đọc `visual-brand-guidelines.md` cho brand colors, forbidden styles.
- Phân tích intent và tone của bài viết.

### Bước 2: Output — Visual Strategy Report
Agent xuất ra `Visual Strategy Recommendation` theo format chuẩn trong agent file:
- Số lượng hình ảnh đề xuất (Featured + Inline).
- Kích thước từng loại (Featured: 1200x630, Inline: 800x450).
- Prompt cụ thể cho từng hình (style, subject, mood, negative prompts).
- Mapping vị trí chèn hình vào bài (dưới H2 nào, trước section nào).

> Sau khi nhận Visual Strategy Report, người dùng có thể dùng prompts để generate ảnh bằng công cụ ngoài (Midjourney, DALL-E, v.v.).
