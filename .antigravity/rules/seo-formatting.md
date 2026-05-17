---
description: Quy định bắt buộc về cấu trúc và định dạng cho mọi bài viết SEO.
---

# Định Dạng SEO (SEO Formatting Rules)

Bất kỳ bài viết nào được tạo ra bởi bất kỳ Agent hay Skill nào trong hệ thống này ĐỀU PHẢI tuân thủ các quy tắc định dạng SEO sau đây:

1. **Heading Structure (Cấu trúc thẻ phạt):**
   - Chỉ sử dụng MỘT (1) thẻ `#` (H1) cho Title của bài viết.
   - Các ý chính phải dùng `##` (H2).
   - Các ý phụ hỗ trợ cho H2 phải dùng `###` (H3). Không được nhảy cóc (ví dụ từ H1 xuống H3).

2. **Đoạn văn (Paragraphs):**
   - Ngắn gọn, súc tích. Tối đa 2-3 câu trên mỗi đoạn.
   - Mỗi câu không nên vượt quá 25 từ để đảm bảo dễ đọc trên thiết bị di động.

3. **In đậm và Nhấn mạnh (Styling):**
   - Luôn **in đậm** (bold) từ khóa chính ở lần xuất hiện đầu tiên.
   - In đậm các khái niệm quan trọng để người đọc dễ dàng lướt (skim) nội dung.

4. **Danh sách (Lists):**
   - Bắt buộc sử dụng Bullet points (`-`) hoặc Numbered lists (`1.`) cho các phần liệt kê lợi ích, tính năng, hoặc các bước thực hiện.
   - Trước mỗi danh sách phải có một câu dẫn dắt có dấu hai chấm `:`.

5. **Featured Snippet Optimization:**

   Field `Featured_Snippet` trong outline YAML xác định dạng cần tối ưu. Áp dụng pattern tương ứng:

   - **Paragraph snippet:** Viết câu trả lời trực tiếp **40–60 từ** ngay sau H2 (trước khi giải thích chi tiết). Câu đầu tiên phải chứa target keyword. Không dùng bullet, không dùng bảng trong đoạn này.

   - **List snippet:** Dùng numbered list **6–8 items**, mỗi item bắt đầu bằng động từ hành động. H2 dẫn vào list phải chứa keyword dạng "Cách...", "Các bước...", "X điều cần...".

   - **Table snippet:** Bảng so sánh với header row rõ ràng, cột đầu là thực thể được so sánh. H2 chứa từ "so sánh", "khác nhau", "bảng". Tối thiểu 3 cột, 4 hàng dữ liệu.

   - **None:** Không cần tối ưu featured snippet — viết tự nhiên theo flow bài.
