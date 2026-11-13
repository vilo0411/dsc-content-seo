# DSC — Mẫu thiết kế cho syndication

Trạng thái: đề xuất để xem và chọn hướng; chưa phải ảnh đã duyệt để đăng.

## Nguyên tắc

- Giữ màu, logo chuẩn DSC. Logo góc trên trái, cách mép ít nhất 4%. Không dùng màu đỏ.
- Một ảnh truyền đạt một luận điểm. Chọn bố cục theo chức năng nội dung, không dùng cùng một mẫu checklist cho mọi bài.
- Chữ có ba cấp rõ: tiêu đề, thông tin chính, chú thích. Bản 1080 px: tiêu đề khoảng 64–88 px, nội dung 32–40 px, nguồn 22–26 px; thử xem ở kích thước điện thoại.
- Font mẫu: Be Vietnam Pro Regular/Bold, nhúng trực tiếp để không phụ thuộc font trên máy người xem. Chuẩn hóa tiếng Việt NFC; không ép độ đậm giả, không dùng tracking âm; tiêu đề line-height tối thiểu khoảng 1.25. Chờ tải font hoàn tất trước khi xuất ảnh. Font và giấy phép OFL lưu trong design-fonts/.
- Giữ khoảng trống giữa các nhóm thông tin; không bắt ảnh social chứa chữ phải đạt tỷ lệ trống dành cho ảnh bìa blog.
- AI chỉ tạo phần minh họa khi có lợi; chữ Việt, số liệu, logo được dàn chính xác bằng công cụ thiết kế. Không dùng ảnh AI giả lập biểu đồ tài chính hay số liệu không có nguồn.
- Không tạo nhiều ảnh trước khi chọn hướng thiết kế. Một bài ưu tiên một mẫu chính và một biến thể cần thiết.
- Các kích thước dưới đây là kích thước thiết kế đề xuất, không khẳng định giới hạn kỹ thuật của nền tảng.

## S01 — Luận điểm lớn

Nền navy, tiêu đề lớn lệch trái, nhấn xanh một cụm từ, một minh họa nhỏ bên phải hoặc dưới. Không có danh sách nhiều ô. Dùng cho một hiểu lầm, câu hỏi phân tích hoặc một nhận định giáo dục.

Đề xuất 1080×1350 hoặc 1080×1080. Tiêu đề 8–14 từ, tối đa 3 dòng; giải thích 20–35 từ. Chủ đề thử: “Lợi nhuận cao chưa đủ chứng minh con hào”. Phù hợp LinkedIn, BAND, X hoặc Mastodon khi có ảnh.

## S02 — Sơ đồ giải thích

Nền mint nhạt, một sơ đồ trung tâm: đối tượng → cơ chế → kết quả cần kiểm chứng. Nhánh có nhãn ngắn, đường dẫn rõ; không vẽ mạng trang trí. Đường và nhãn phải có ý nghĩa, không ngụ ý quan hệ nhân quả đã được xác nhận khi chỉ là giả thuyết.

Đề xuất 1000×1500 cho bản dọc hoặc 1200×900 cho bản giải thích ngang. Chủ đề thử: “Chi phí chuyển đổi: dữ liệu, đào tạo, gián đoạn”. Phù hợp Pinterest, Pixbender (nếu hỗ trợ ảnh), ảnh trong bài dài.

## S03 — Đối chiếu bằng chứng

Nền trắng/ngà, chữ navy, hai cột có tiêu đề đối xứng và các hàng cùng tiêu chí. Chỉ một dải nhấn xanh. So sánh tối đa 3–4 tiêu chí, không dùng hai màu như tín hiệu mua/bán.

Đề xuất 1080×1350 hoặc 1080×1080. Chủ đề thử: “Dấu hiệu ban đầu / Bằng chứng cần tìm”: tên tuổi thương hiệu / sức mạnh định giá; khách ở lại / chi phí chuyển đổi; doanh thu tăng / chất lượng tăng trưởng. Đây là câu hỏi nghiên cứu, không phải khuyến nghị cổ phiếu.

## S04 — Chuỗi câu hỏi

Carousel hoặc bộ ảnh có cùng lưới: bìa với một câu hỏi; ba slide, mỗi slide một ý; slide kết với link/CTA. Dùng số trang và thanh tiến trình nhỏ để giữ nhịp, tránh lặp một khung năm ô trên mọi slide.

Đề xuất bộ 5 ảnh 1080×1350. Chủ đề thử: “Khách hàng ở lại vì điều gì?” → cơ chế → bằng chứng → điều có thể thay đổi → đọc bài nguồn. Chỉ xuất bộ ảnh nếu nền tảng/tài khoản thực tế cho phép định dạng tương ứng; nếu không, dùng ảnh S01 hoặc S03 đơn lẻ.

## Quy trình chọn và giao ảnh

1. Ghi luận điểm cần thể hiện và chọn S01–S04, kênh, kích thước, nội dung chữ, nguồn.
2. Làm một bản xem trước; kiểm tra chữ Việt, khoảng trống, logo và độ rõ khi thu nhỏ.
3. Duyệt style/bố cục trước khi sản xuất nhiều biến thể.
4. Không cần tạo mới: điền URL ảnh gốc DSC đã xác minh vào asset_path và asset_url. Cần tạo ảnh mới nhưng đang chờ tạo/duyệt/upload: để cả hai trường trống, ghi lý do trong notes. Không dùng ảnh cũ thay cho một thiết kế mới đang chờ.

Bảng xem mẫu local: design-preview.html. Tab Visual Styles trên Sheet chứa thông số và cách dùng, không chứa đường dẫn local giả làm tài nguyên online.
