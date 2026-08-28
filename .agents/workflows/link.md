---
description: Gắn internal links cho bài đang làm
---

# Lệnh: /link

## Nhiệm vụ
Đọc qua nội dung bài viết nháp và tự động chèn các internal links (liên kết nội bộ) phù hợp, dựa trên mạng lưới content đã có.

## Quy trình thực thi
1. Đọc nội dung file đang mở (bản draft/final).
2. Tra cứu dữ liệu từ Sitemap live (`https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml`) và `knowledge/3-pipeline/anchor-index.md` để lấy danh sách URL live thực tế trên website DSC.
3. Tìm kiếm các cụm từ (anchor text) phù hợp, tự nhiên trong bài và gắn URL live tới các bài viết liên quan (Spoke to Hub, Spoke to Spoke).
4. **BẮT BUỘC:** Luôn kiểm tra và chèn ít nhất 01 link chuyển đổi mở tài khoản chứng khoán DSC (`https://www.dsc.com.vn/mo-tai-khoan`) tại phần Product Bridge hoặc CTA Kết luận.
5. Đảm bảo mật độ link vừa phải (1 link / 100 - 150 từ), không chèn quá nhiều, không dùng anchor chung chung (như "tại đây", "xem thêm").
6. Đảm bảo định dạng chuẩn CMS: Không dùng code block lưu đồ ASCII (`+---+`) hoặc LaTeX formulas.
7. Áp dụng thay đổi trực tiếp vào file.
