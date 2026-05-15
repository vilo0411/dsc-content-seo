---
description: Phê duyệt giai đoạn hiện tại (Outline → Draft/Final/Optimize)
---

# Lệnh: /approve

## Nhiệm vụ
Cho phép người dùng phê duyệt một bản nháp, outline, hoặc bản tối ưu để đẩy nó sang giai đoạn tiếp theo trong Content Pipeline.

## 🔄 Context Load (Trước khi thực thi)
1. `knowledge/4-content/topic-clusters.md` — để xác định slug và cập nhật trạng thái
2. `.antigravity/memory/instincts.md` — để ghi nhận bài học mới (nếu có)
3. `knowledge/3-pipeline/revision-log.md` — để log revision

## Quy trình thực thi

### Bước 1: Xác định context
Xác định file đang ở stage nào dựa trên tên file hoặc stage đang được thảo luận trong conversation:

### Bước 2: Thực thi theo stage

**Nếu stage là Outline (`knowledge/4-content/1-outlines/[slug].md`):**
- Cập nhật `knowledge/4-content/topic-clusters.md` → trạng thái `Outline-Approved`.
- Thông báo: "Outline đã được approve. Gõ `/drafting [slug]` để bắt đầu viết bài."

**Nếu stage là Draft (`knowledge/4-content/2-drafts/Draft-[slug].md`):**
- **BẮT BUỘC — Hỏi trước khi finalize:**
  > *"Ngoài các chỉnh sửa đã trao đổi trong chat, bạn có tự sửa thêm gì trong file không? Mô tả ngắn để tôi ghi log. (Gõ 'không' để bỏ qua.)"*
- Tổng hợp **toàn bộ** những gì đã sửa trong session này (từ chat + file trực tiếp nếu user khai báo) → ghi vào `knowledge/3-pipeline/revision-log.md` theo format chuẩn.
- **BẮT BUỘC**: Di chuyển file sang `knowledge/4-content/3-finalized/Final-[slug].md`.
- Cập nhật `knowledge/4-content/topic-clusters.md` → trạng thái `Finalized`.
- Auto-trigger: Kích hoạt skill `.antigravity/skills/content-feedback-loop/SKILL.md` để tổng hợp bài học.
- Cập nhật `knowledge/3-pipeline/anchor-index.md` — thêm entry mới cho bài vừa finalized.

**Nếu stage là Optimize (`knowledge/4-content/2-drafts/Optimize-[slug].md`):**
- Ghi đè bản nâng cấp lên file gốc: `knowledge/4-content/3-finalized/Final-[slug].md`.
- Xóa file `Optimize-[slug].md` trong `2-drafts/`.
- Cập nhật `knowledge/4-content/topic-clusters.md` → trạng thái `Finalized`.

### Bước 3: Xác nhận
Sau khi hoàn thành, báo cáo cho người dùng:
- Đường dẫn file final.
- Trạng thái mới trong topic-clusters.md.
- (Nếu Draft approve): Tóm tắt bài học mới từ Content Feedback Loop.
