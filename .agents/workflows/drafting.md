---
description: Chuyển Outline đã duyệt thành bài viết nháp chuẩn Human-centric (Phase 3)
---

# Lệnh: /drafting [slug]

Dùng sau khi Outline đã được `/approve`. Chỉ thực hiện Phase 3 (Drafting + QA).
`[slug]` là tên file outline, ví dụ: `lai-suat-tiet-kiem-acb`.

## Quy trình thực thi

### 🔄 Bước 0: Context Load (BẮT BUỘC)
1. `knowledge/4-content/1-outlines/[slug].md` — Outline đã approve (BẮT BUỘC)
2. `knowledge/1-brand/profile.md`
3. `knowledge/1-brand/service-operations.md`
4. `knowledge/3-pipeline/anti-ai-rules.md`
5. `knowledge/3-pipeline/glossary.md`
6. `knowledge/3-pipeline/anchor-index.md` — Danh sách bài để link nội bộ
7. `.antigravity/memory/instincts.md`

> **Nếu Outline không tồn tại hoặc chưa có trạng thái `Outline-Approved` trong `topic-clusters.md`: DỪNG LẠI và yêu cầu người dùng chạy `/outlining [keyword]` trước.**

### Bước 1: Drafting
- Kích hoạt skill `.antigravity/skills/seo-drafting/SKILL.md` → Step 1: Execute.
- Viết bài tuân thủ Outline, áp dụng 3S Rule xuyên suốt.
- Lưu bản nháp tại: `knowledge/4-content/2-drafts/Draft-[slug].md`.

### Bước 2: Internal Linking
- Kích hoạt skill `.antigravity/skills/internal-linking/SKILL.md` → Mode: Contextual Insertion.
- Chèn tối thiểu 2 internal links từ `anchor-index.md` vào draft.

### Bước 3: Quality Guardian (QA — BẮT BUỘC)
- Kích hoạt agent `.antigravity/agents/quality-guardian.md`.
- QA load đầy đủ context của agent trước khi audit.
- Kết quả PASS → tiếp tục. Kết quả FAIL → sửa và QA lại.

### 🚧 APPROVAL GATE:
> Trình bày Draft + QA PASS report.
> **DỪNG LẠI. Chờ người dùng đọc và gõ `/approve`.**
> Khi approve: trigger `.antigravity/skills/seo-drafting/SKILL.md` → Step 2: Finalize & Learn.
