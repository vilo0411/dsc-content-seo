# Continuous Learning: Instincts (Bản năng)

> **Bắt buộc:** Mọi agent, skill, và workflow đều phải đọc file này trước khi thực thi.
> **Cập nhật:** Được auto-append sau mỗi `/approve` hoặc thủ công qua `/learn`.

File này lưu trữ những "bản năng" mà hệ thống AI học được qua quá trình sửa bài cùng người dùng.
Mỗi khi người dùng đưa ra phản hồi chỉnh sửa, hãy trích xuất nguyên lý và lưu vào đây.

---

## Format chuẩn cho mỗi bản năng

```
### [Tên ngắn gọn]
- **Trạng thái:** ACTIVE / DEPRECATED
- **Nguồn:** [Tên bài viết hoặc "Global feedback"]
- **Phản hồi từ User:** "[Quote phản hồi gốc]"
- **Bản năng:** [Quy tắc hành động cụ thể]
- **Phạm vi:** [Global / Chỉ topic: X]
```

---

## Bản năng Active

### Tránh mở bài vĩ mô
- **Trạng thái:** ACTIVE
- **Nguồn:** Feedback chung
- **Phản hồi từ User:** "Đừng bao giờ mở bài bằng cụm 'Trong kỷ nguyên số ngày nay...'"
- **Bản năng:** Mở bài đi thẳng vào vấn đề cụ thể của người dùng. Không dạo đầu bằng bối cảnh vĩ mô (kỷ nguyên số, thế giới công nghệ, thị trường biến động...).
- **Phạm vi:** Global

### Loại bỏ ngoặc kép nhấn mạnh (Emphatic Quotes)
- **Trạng thái:** ACTIVE
- **Nguồn:** adx-la-gi
- **Phản hồi từ User:** "sao tôi thấy đang sử dụng các ngoặc kép. Loại bỏ kiểu trình bày nài, AI quá"
- **Bản năng:** Tuyệt đối không sử dụng dấu ngoặc kép cho các cụm từ ẩn dụ, ví von hoặc thuật ngữ thông thường (ví dụ: đu đỉnh, vùng kiếm tiền). Viết thẳng và trực diện để tránh cảm giác máy móc.
- **Phạm vi:** Global

### Ưu tiên Môi giới 1:1 trong Product Bridge
- **Trạng thái:** ACTIVE
- **Nguồn:** adx-la-gi
- **Phản hồi từ User:** "dẫn về dịch vụ môi giới chứng khoán hoặc mở tài khoản chứng khoán DSC thay vì tư vấn số nhé"
- **Bản năng:** Khi viết bài về phân tích kỹ thuật chuyên sâu cho Active Traders, hãy ưu tiên dẫn dắt về dịch vụ Môi giới 1:1 và Mở tài khoản eKYC thay vì các công cụ Tư vấn số tự động, để tạo sự tin cậy và cá nhân hóa.
- **Phạm vi:** Global

### Thỏa mãn Search Intent kỹ thuật trong bài phân tích
- **Trạng thái:** ACTIVE
- **Nguồn:** bao-cao-luu-chuyen-tien-te
- **Phản hồi từ User:** (Tham khảo AI Overview)
- **Bản năng:** Đối với các bài viết về báo cáo tài chính hoặc công cụ kỹ thuật, ngoài việc phân tích chiến lược cho nhà đầu tư, cần bổ sung các kiến thức nền tảng như 'Phương pháp lập' hoặc 'Cấu tạo chi tiết'. Điều này giúp thỏa mãn các truy vấn tìm kiếm mang tính học thuật mà không làm loãng ảnh hưởng chiến lược của DSC.
- **Phạm vi:** Global

---

*(Agent tự động append bản năng mới vào section "Bản năng Active" sau mỗi vòng viết.)*
