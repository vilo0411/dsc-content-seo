# Tra cứu nội dung

Xem toàn bộ công việc và tiến độ tại [bảng điều hành SEO](../operations/index.html): internal link, stale, content audit, QA, GSC và các mốc sau publish.

Mở [trang tra cứu HTML CMS và audit](index.html) bằng trình duyệt. Tìm theo slug, tên file hoặc đợt audit; chọn CMS hoặc Audit để lọc. Tìm kiếm hỗ trợ tiếng Việt không dấu.

| Thư mục | Nội dung |
| --- | --- |
| `3-finalized/` | Bản Markdown đã duyệt, tên `Final-<slug>.md` |
| `4-cms/` | HTML thân bài để dán vào CMS, tên `<slug>.html` |
| `audits/` | Báo cáo và dữ liệu kiểm tra, nhóm theo đợt audit |
| `archive/<slug>/` | Các bản lưu theo bài |

Trong một đợt audit, `index.html` là trang tổng hợp; `*.preview.html` là bản xem trước; `*.body.html` là thân bài; `baseline-*` là bản trước khi sửa; `v2/` là phiên bản tiếp theo. HTML audit dùng để đối chiếu; lấy bản đưa lên CMS từ `4-cms/`.

Đợt audit mới nên dùng `audits/<nhom>-YYYY-MM-DD/`, lưu báo cáo và dữ liệu cùng đợt vào đó. Các phiên bản tiếp theo dùng `v2/`, `v3/` trong thư mục đợt.

Sau khi thêm hoặc đổi vị trí tài liệu audit, chạy từ thư mục gốc dự án:

```powershell
python scripts/build_content_index.py
```

Xuất HTML bằng `scripts/md_to_cms_html.py` sẽ tự cập nhật trang tra cứu.
