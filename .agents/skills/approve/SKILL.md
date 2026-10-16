---
name: approve
description: Phê duyệt giai đoạn hiện tại (Outline → Draft/Final/Optimize) trong Content Pipeline.
---

# Phê duyệt giai đoạn hiện tại

## Nhiệm vụ
Cho phép người dùng phê duyệt một bản nháp, outline, hoặc bản tối ưu để đẩy nó sang giai đoạn tiếp theo trong Content Pipeline.

## 🔄 Context Load (Trước khi thực thi)
1. `python scripts/topic_status.py [slug]` — xác nhận slug/trạng thái (không đọc `topic-clusters.md`)
2. `.antigravity/memory/instincts-archive.md` — chỉ để **append** bài học mới (không cần đọc toàn bộ; `instincts.md` sinh lại bằng `python scripts/optimize_instincts.py`)
3. `knowledge/3-pipeline/revision-log.md` — chỉ **append** theo format chuẩn (không đọc toàn bộ)

## Quy trình thực thi

### Bước 1: Xác định context
Xác định file đang ở stage nào dựa trên tên file hoặc stage đang được thảo luận trong conversation:

### Bước 2: Thực thi theo stage

**Nếu stage là Outline (`knowledge/4-content/1-outlines/[slug].md`):**
- `python scripts/topic_status.py [slug] --set Outline-Approved`
- Thông báo: "Outline đã được approve. Gõ `/drafting [slug]` để bắt đầu viết bài."

**Nếu stage là Draft (`knowledge/4-content/2-drafts/Draft-[slug].md`):**
- **BẮT BUỘC — Hỏi trước khi finalize:**
  > *"Ngoài các chỉnh sửa đã trao đổi trong chat, bạn có tự sửa thêm gì trong file không? Mô tả ngắn để tôi ghi log. (Gõ 'không' để bỏ qua.)"*
- Tổng hợp **toàn bộ** những gì đã sửa trong session này (từ chat + file trực tiếp nếu user khai báo) → ghi vào `knowledge/3-pipeline/revision-log.md` theo format chuẩn.
- **GATE trước khi move file** (DSC không có `finalize.py`, nên gate chạy tay ở đây):
  ```bash
  python scripts/qa_lint.py [đường dẫn file đang approve] --no-sitemap
  python scripts/slop_check.py [đường dẫn file đang approve]
  python scripts/market_facts.py --verify [đường dẫn file đang approve]
  ```
  Còn `CRITICAL` (tầng A) hoặc slop score < 80 (tầng B) → **KHÔNG move file**; báo lại cho user kèm danh sách lỗi và chờ quyết định. `FACT-*` là advisory: in ra cho user, không chặn (exit 3 = nguồn dữ liệu chết, bỏ qua). Chỉ bỏ qua gate khi user nói rõ "cứ finalize".
- **BẮT BUỘC**: Di chuyển file sang `knowledge/4-content/3-finalized/Final-[slug].md`.
- **BẮT BUỘC**: Xóa file outline gốc `knowledge/4-content/1-outlines/[slug].md` (nếu tồn tại) để dọn dẹp hệ thống.
- `python scripts/topic_status.py [slug] --set Finalized`
- `python scripts/qa_lint.py knowledge/4-content/3-finalized/Final-[slug].md --log` — ghi score vào `revision-log.md` (theo dõi xu hướng chất lượng).
- `python scripts/slop_check.py knowledge/4-content/3-finalized/Final-[slug].md` — ghi slop score kèm vào dòng log đó (xu hướng tầng B).
- Auto-trigger: Kích hoạt skill `.antigravity/skills/content-feedback-loop/SKILL.md` để tổng hợp bài học → append vào `instincts-archive.md` → chạy `python scripts/optimize_instincts.py`.
- Cập nhật `knowledge/3-pipeline/anchor-index.md` — chèn 1 dòng mới vào cluster phù hợp (không đọc cả file).

**Nếu stage là Optimize (`knowledge/4-content/2-drafts/Optimize-[slug].md`):**
- **BẮT BUỘC — Hỏi trước khi finalize:**
  > *"Ngoài các chỉnh sửa đã trao đổi trong chat, bạn có tự sửa thêm gì trong file không? Mô tả ngắn để tôi ghi log. (Gõ 'không' để bỏ qua.)"*
- Tổng hợp **toàn bộ** những gì đã sửa trong session này (từ chat + file trực tiếp nếu user khai báo) → ghi vào `knowledge/3-pipeline/revision-log.md` theo format chuẩn.
- **GATE trước khi move file** (DSC không có `finalize.py`, nên gate chạy tay ở đây):
  ```bash
  python scripts/qa_lint.py [đường dẫn file đang approve] --no-sitemap
  python scripts/slop_check.py [đường dẫn file đang approve]
  python scripts/market_facts.py --verify [đường dẫn file đang approve]
  ```
  Còn `CRITICAL` (tầng A) hoặc slop score < 80 (tầng B) → **KHÔNG move file**; báo lại cho user kèm danh sách lỗi và chờ quyết định. `FACT-*` là advisory: in ra cho user, không chặn (exit 3 = nguồn dữ liệu chết, bỏ qua). Chỉ bỏ qua gate khi user nói rõ "cứ finalize".
- Ghi đè bản nâng cấp lên file gốc: `knowledge/4-content/3-finalized/Final-[slug].md`.
- Xóa file `Optimize-[slug].md` và file `Proposal-[slug].md` (nếu có) trong `2-drafts/`.
- `python scripts/topic_status.py [slug] --set Finalized`
- `python scripts/qa_lint.py knowledge/4-content/3-finalized/Final-[slug].md --log` — ghi score vào `revision-log.md`.
- `python scripts/slop_check.py knowledge/4-content/3-finalized/Final-[slug].md` — ghi slop score kèm vào dòng log đó.
- Auto-trigger: Kích hoạt skill `.antigravity/skills/content-feedback-loop/SKILL.md` để tổng hợp bài học → append vào `instincts-archive.md` → chạy `python scripts/optimize_instincts.py`.

### Bước 3: Xác nhận
Sau khi hoàn thành, báo cáo cho người dùng:
- Đường dẫn file final.
- Trạng thái mới trong topic-clusters.md (output của `topic_status.py`) + QA Score (tầng A) + Slop Score (tầng B).
- Tóm tắt bài học mới từ Content Feedback Loop.
