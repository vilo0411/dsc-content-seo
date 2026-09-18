---
name: link
description: Tự động chèn internal links phù hợp cho bài viết nháp dựa trên sitemap và anchor index.
---

# Gắn Internal Links

## Nhiệm vụ
Đọc qua nội dung bài viết nháp và tự động chèn các internal links (liên kết nội bộ) phù hợp, dựa trên mạng lưới content đã có.

## Quy trình thực thi
1. Đọc nội dung file đang mở (bản draft/final).
2. Lấy ứng viên link **bằng script, không đọc `anchor-index.md`** (đã đối soát `sitemap-cache.json`; nếu cache cũ chạy `python .antigravity/skills/internal-linking/scripts/sync_sitemap.py` trước):
   ```bash
   python scripts/find_links.py "[keyword chính của bài]" --top 8 --exclude [slug]
   python scripts/find_links.py "[chủ đề phụ xuất hiện trong bài]" --top 5 --exclude [slug]
   ```
   Chỉ dùng dòng có **Sitemap ✓**.
3. Tìm kiếm các cụm từ (anchor text) phù hợp, tự nhiên trong bài và gắn URL tới các bài viết liên quan (Spoke to Hub, Spoke to Spoke).
4. **Ưu tiên URL có traffic thực (nếu có GSC data):** Khi có nhiều candidate tương đương, ưu tiên URL có clicks cao trong `knowledge/3-pipeline/gsc-opportunities.md` (grep theo slug) — trang đang nhận traffic truyền authority mạnh hơn. Không có data → chọn theo semantic relevance.
5. **BẮT BUỘC:** Luôn kiểm tra và chèn ít nhất 01 link chuyển đổi mở tài khoản chứng khoán DSC (`https://www.dsc.com.vn/mo-tai-khoan`) tại phần Product Bridge hoặc CTA Kết luận.
6. Đảm bảo mật độ link vừa phải (1 link / 100 - 150 từ), không chèn quá nhiều, không dùng anchor chung chung (như "tại đây", "xem thêm").
7. Đảm bảo định dạng chuẩn CMS: Không dùng code block lưu đồ ASCII (`+---+`) hoặc LaTeX formulas.
8. Áp dụng thay đổi trực tiếp vào file.
9. Xác minh: `python scripts/qa_lint.py [file] --no-sitemap` nếu chỉ cần check nhanh, hoặc không flag để đối soát cả sitemap — mọi `LINK-*` phải sạch.
