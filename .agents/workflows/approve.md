---
description: Phê duyệt giai đoạn hiện tại (Outline → Draft/Final/Optimize)
---

# Lệnh: /approve

## Nhiệm vụ
Cho phép người dùng phê duyệt một bản nháp, outline, hoặc bản tối ưu để đẩy nó sang giai đoạn tiếp theo trong Content Pipeline.

## Quy trình thực thi
1. Xác định file đang được mở hoặc file vừa được generate gần nhất.
2. Nếu file là `1-outlines/Outline-[slug].md`: 
   - Đổi trạng thái trong `knowledge/4-content/sprint-backlog.md` thành `Outline-Approved` và chuyển sang bước viết Draft.
3. Nếu file là `2-user-review/Draft-[slug].md`:
   - Ghi nhận các chỉnh sửa thủ công của user vào `.antigravity/memory/instincts.md` để học hỏi.
   - Đổi tên file và di chuyển sang `content/blog/3-finalized/Final-[slug].md`.
   - Cập nhật Progress Log và đổi trạng thái thành `Finalized`.
4. Nếu file là `2-user-review/Optimize-[slug].md`:
   - Ghi đè (overwrite) bản nâng cấp này lên file gốc nằm trong `content/blog/3-finalized/Final-[slug].md`.
   - Xóa file nháp `Optimize-[slug].md` trong thư mục `2-user-review`.
   - Đổi trạng thái từ `Optimizing` thành `Finalized` trong Sprint Backlog.
