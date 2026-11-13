# Điều hành SEO

Mở [bảng điều hành](index.html) để xem internal link, stale, content audit, QA/SERP, GSC và công việc sau publish. Kho tài liệu trên cùng trang tìm cả tài liệu hiện hành và lưu trữ. [status.json](status.json) lưu kết quả tổng hợp.

## Cập nhật tiến độ

Từ thư mục gốc dự án:

```powershell
python scripts/build_content_index.py
```

Lệnh cập nhật cả danh mục CMS và bảng điều hành. Không gọi mạng, không sửa trạng thái nguồn. Xuất CMS bằng `md_to_cms_html.py` cũng chạy bước này.

Sau khi sửa CMS, dùng quy trình sync hiện có rồi chạy lại lệnh trên. Snapshot có thể chỉ sync một phần; ngày `last_run` không phải ngày cập nhật của mọi bài. Bảng không xác nhận website hiện tại nếu chưa sync mới.

## Nguồn tiến độ

| Nhóm | Nguồn | Ý nghĩa |
| --- | --- | --- |
| Trạng thái bài | `../4-content/topic-clusters.md`, `topic_status.py` | Trạng thái pipeline; Finalized chưa chứng minh đã publish |
| Internal link | `../3-pipeline/internal-links/plans/*.json` | Verifier hiện có kiểm tra snapshot; các đợt có thể trùng hoặc thay thế nhau |
| Stale | `../4-content/audits/edits/*.json` | Đối chiếu đoạn trước/sau trong snapshot; title/meta cần kiểm tra riêng |
| Content audit | `../3-pipeline/content-audit-2026-11-05-tracker.html` | Tiến độ lưu trong trình duyệt; xuất/nhập bằng chức năng của tracker |
| Sau publish | `../3-pipeline/publish-ledger.csv` | Các mốc đã ghi nhận; `seed` là dữ liệu lịch sử, không phải ngày publish |
| QA/SERP | `../4-content/audits/**/validation*.json` | Kết quả kiểm tra đã lưu; chưa chứng minh bản hiện tại đã qua QA |
| Đo lường | `monitoring.csv` trong từng đợt audit | Chỉ tính dòng có `actual_date`; không tự đặt lịch |

`sprint-backlog.md` có trạng thái cũ lệch nguồn chính; dùng `topic_status.py <slug>` để tra trạng thái bài. Bảng liệt kê trường hợp lệch khi từ khóa khớp chính xác.

## Quy tắc lưu công việc

- Bắt đầu ở `knowledge/operations/index.html` để xem việc, tiến độ và mở file nguồn.
- Internal link: mỗi đợt một cặp `plans/YYYY-MM-DD-<ten>.json` và `.html`.
- Stale, QA, SERP: đợt mới dùng `4-content/audits/<nhom>-YYYY-MM-DD/`; bản tiếp theo trong `v2/`, `v3/`.
- CMS: `4-content/4-cms/<slug>.html`, chứa thân bài để dán.
- Giữ vị trí tracker cũ để giữ dấu tick và liên kết đã dùng. Có báo cáo chưa có nghĩa là hoàn thành công việc.
- Làm việc sau publish bằng `/weekly`; cập nhật ledger qua công cụ hiện có thay vì tick thêm ở bảng điều hành.

Bảng điều hành được sinh từ nguồn, không sửa tay `status.json` hay `index.html`. Các script không tự đổi quyết định xóa, gộp, redirect hay publish.
