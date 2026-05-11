---
description: Tối ưu bài cũ — Brand audit + rewrite + QA
---

# Lệnh: /optimize [path] [options]

## Options Hỗ Trợ
- `--step`: Tối ưu chi tiết từng bước (Khám bệnh -> Đề xuất sửa -> Chờ duyệt -> Viết lại).
- `--auto`: Tối ưu nhanh (Khám bệnh và tự động sửa thẳng vào bài mà không cần chờ duyệt).

## Nhiệm vụ
Cập nhật và tối ưu lại một bài viết cũ đang tồn tại để tăng thứ hạng, đảm bảo tính cập nhật của Brand và tiêu chuẩn SEO mới.

## Quy trình thực thi

1. **Intake & Tracking (Nạp Dữ Liệu & Gắn nhãn):** 
   - Đọc bài viết gốc từ `content/blog/3-finalized/Final-[slug].md`.
   - Cập nhật trạng thái của từ khóa/bài viết này trong `knowledge/4-content/sprint-backlog.md` thành `Optimizing` (Đang tối ưu).
   - Tạo một bản sao làm việc (working copy) lưu vào `content/blog/2-user-review/Optimize-[slug].md`. Toàn bộ quá trình sửa chữa sẽ diễn ra trên bản sao này để không ảnh hưởng bài gốc đang live.

2. **Audit (Thu thập Bối cảnh & Khám bệnh):**
   - Gọi **SEO Collector** để kiểm tra lại SERP hiện tại cho từ khóa chính của bài viết, tìm kiếm Gap nội dung.
   - Gọi **Brand Guardian** phân tích bài cũ dựa trên `knowledge/3-pipeline/anti-ai-rules.md` để tìm lỗi.

3. **Proposal (Đề xuất & Chờ Duyệt - Nếu dùng `--step`):**
   - Kích hoạt kỹ năng `.antigravity/skills/seo-optimization/SKILL.md`.
   - In ra màn hình **Báo cáo Tình trạng Bài viết & Đề xuất sửa chữa** (phân loại rõ: Giữ nguyên, Cập nhật, Thêm mới).
   - Dừng lại và chờ người dùng gõ lệnh `/approve`.
   *(Nếu dùng `--auto`, bỏ qua bước chờ duyệt, AI tự chốt đề xuất và nhảy sang bước 4).*

4. **Execution (Tiến hành Rewrite):**
   - Mở file `Optimize-[slug].md` và tiến hành viết lại các phần lỗi thời, bổ sung thông tin theo Proposal.

5. **QA & Output:**
   - Gọi **Quality Guardian** để soát lỗi.
   - Lưu kết quả cuối cùng vào `Optimize-[slug].md`. 
   - Bài viết gốc trong `3-finalized` vẫn nằm im. Chỉ khi nào người dùng đọc bản Optimize và gõ lệnh `/approve`, hệ thống mới lấy bản Optimize ghi đè lên bài gốc.
