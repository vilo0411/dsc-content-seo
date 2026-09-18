---
name: drafting
description: Chuyển Outline đã duyệt thành bài viết nháp chuẩn Human-centric (Phase 3).
---

# Drafting

Dùng sau khi Outline đã được `/approve`. Chỉ thực hiện Phase 3 (Drafting + QA).
`[slug]` là tên file outline, ví dụ: `lai-suat-tiet-kiem-acb`.

## Quy trình thực thi

### 🔄 Bước 0: Context Load (BẮT BUỘC)
1. `knowledge/4-content/1-outlines/[slug].md` — Outline đã approve (BẮT BUỘC)
2. `knowledge/1-brand/profile.md`
3. `knowledge/1-brand/service-operations.md`
4. `knowledge/3-pipeline/anti-ai-rules.md`
5. `knowledge/3-pipeline/glossary.md`
6. ~~`anchor-index.md`~~ — **Không đọc.** Dùng `python scripts/find_links.py "[keyword]" --exclude [slug]` ở Bước 2.
7. `.antigravity/memory/instincts.md` (+ `instincts-by-scope/<topic>.md` nếu topic khớp)
8. `knowledge/1-brand/writers/[Writer_Profile].md` — Đọc field `Writer_Profile` trong outline YAML, load file tương ứng (`educational` / `analytical` / `comparison`). Nếu không có field này → dùng `educational` làm default.

> **Kiểm tra trạng thái:** `python scripts/topic_status.py [slug]` — nếu Outline không tồn tại hoặc trạng thái chưa phải `Outline-Approved`: DỪNG LẠI và yêu cầu người dùng chạy `/outlining [keyword]` trước.

### Bước 1: Drafting
- Kích hoạt skill `.antigravity/skills/seo-drafting/SKILL.md` → Step 1: Execute.
- Viết bài tuân thủ Outline, áp dụng 3S Rule xuyên suốt.
- Lưu bản nháp tại: `knowledge/4-content/2-drafts/Draft-[slug].md`.

### Bước 2: Internal Linking
- Kích hoạt skill `.antigravity/skills/internal-linking/SKILL.md` → Mode: Contextual Insertion.
- Lấy ứng viên: `python scripts/find_links.py "[keyword]" --top 8 --exclude [slug]` — chỉ dùng URL có Sitemap ✓.
- Chèn tối thiểu 3-5 internal links vào draft.
- **BẮT BUỘC:** Luôn chèn ít nhất 01 link chuyển đổi dẫn về trang **Mở tài khoản chứng khoán DSC** (`https://www.dsc.com.vn/mo-tai-khoan`) tại phần Product Bridge hoặc CTA cuối bài.

### Bước 3: Lint + Quality Guardian (QA — BẮT BUỘC)
- Lint trước:
  ```bash
  python scripts/qa_lint.py knowledge/4-content/2-drafts/Draft-[slug].md --outline knowledge/4-content/1-outlines/[slug].md --fix
  ```
  Exit 1 → sửa đúng các dòng CRITICAL/MAJOR, chạy lại. Chưa gọi Quality Guardian khi lint chưa PASS.
- Lint PASS → kích hoạt agent `.antigravity/agents/quality-guardian.md` (chỉ checklist ngữ nghĩa; context đã có từ Bước 0, QA không load lại).
- Kết quả PASS → tiếp tục. FAIL → sửa và QA lại **tối đa 2 vòng**; sau vòng 2 vẫn FAIL → dừng, trình bày kèm `⚠️ Remaining issues`.

### 🚧 APPROVAL GATE:
> Trình bày Draft + QA PASS report.
> **DỪNG LẠI. Chờ người dùng đọc và gõ `/approve`.**
> Khi approve: trigger `.antigravity/skills/seo-drafting/SKILL.md` → Step 2: Finalize & Learn.
