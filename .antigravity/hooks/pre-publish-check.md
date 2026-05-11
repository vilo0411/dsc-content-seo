---
description: Tự động hóa quá trình rà soát trước khi xuất bản bản nháp cuối cùng.
trigger: Trước khi hệ thống báo "Hoàn thành" một file bài viết nháp.
---

# Hook: Pre-Publish Check

## Điều kiện kích hoạt (Trigger)
Hook này phải được Agent thực thi một cách *tự động* (không cần người dùng gọi) ngay sau khi kỹ năng `seo-writing` hoàn thành việc tạo nội dung, nhưng *trước khi* hiển thị kết quả cuối cùng cho người dùng.

## Hành động (Actions)
1. **Quét đạo văn nội bộ (Self-check):** Đọc lướt lại toàn bộ bài viết để đảm bảo không lặp lại nguyên xi các đoạn văn đã từng viết.
2. **Kiểm tra Mật độ Từ khóa (Keyword Density):**
   - Xác minh từ khóa chính có xuất hiện trong tiêu đề (H1).
   - Xác minh từ khóa chính có xuất hiện trong thẻ H2 đầu tiên.
   - Xác minh từ khóa phụ có được rải đều tự nhiên không.
3. **Gọi Agent: Quality Guardian:** Chuyển nội dung cho `quality-guardian` đọc và chấm điểm dựa trên các `rules` đang có.

## Xử lý Ngoại lệ
Nếu Quality Guardian đánh giá bài viết dưới mức tiêu chuẩn (VD: quá lậm văn phong AI, hoặc nhồi nhét từ khóa), Hook này yêu cầu `seo-writing` tự động viết lại phần bị lỗi trước khi giao cho người dùng.
