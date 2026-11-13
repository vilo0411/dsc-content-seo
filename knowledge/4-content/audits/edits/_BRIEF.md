# Brief: viết bản sửa sẵn-để-dán cho bài cũ trên dsc.com.vn/kien-thuc (04/11/2026)

Hôm nay là **04/11/2026**. Người dùng (biên tập viên SEO của Chứng khoán DSC) sẽ duyệt rồi **copy trực tiếp vào CMS**.
Vì vậy đầu ra phải là **câu chữ cuối cùng**, không phải đề xuất hay hướng sửa.

## Nguồn sự thật
- Thân bài đang live: `knowledge/raw/live/html/<slug>.html` (mỗi block HTML 1 dòng). Chỉ sửa dựa trên file này.
- Title live: cột `title` trong `knowledge/raw/live/pages.csv`.
- Không đọc file `Final-*.md` để lấy câu gốc — chúng có thể lệch với live.

## Đầu ra: 1 file JSON của batch bạn, tại `knowledge/4-content/audits/edits/<batch>.json`
```json
{"group": "rate|stock|data|legal", "priority": "P0", "issue": "Mô tả ngắn vì sao bài cũ (áp dụng cho các bài trong file)",
 "edits": [
  {"slug": "...", "field": "title", "find": "<title live, khớp y hệt pages.csv>", "replace": "<title mới>", "sources": []},
  {"slug": "...", "field": "meta", "find": "", "replace": "<meta description mới, 140–160 ký tự>"},
  {"slug": "...", "find": "<HTML thô khớp ĐÚNG 1 lần trong file live>", "replace": "<HTML mới>",
   "sources": ["https://..."], "note": "tuỳ chọn: cảnh báo cho người duyệt", "issue": "tuỳ chọn: vấn đề riêng của bài"}
 ]}
```
- `find` là chuỗi con HTML thô, copy nguyên văn từ file live (kể cả `<strong>`, `style="..."`, `&amp;`). Phải khớp đúng 1 lần.
- Đơn vị sửa nên là: nội dung 1 ô bảng, 1 đoạn `<p>`, 1 `<li>`, 1 heading, hoặc **nguyên cả `<table>...</table>`** khi bảng số liệu đổi nhiều ô (người dùng sẽ dán đè cả bảng).
- Giữ nguyên mọi `<a href>` / link nội bộ / CTA / banner đang có trong đoạn bị sửa. Không xoá link.
- Đổi heading H2/H3 thì thêm `note` nhắc kiểm tra mục lục (id cũ).
- Nhiều chỗ trong một bài là nhiều edit riêng. Một chuỗi xuất hiện nhiều lần → mở rộng `find` cho tới khi duy nhất.
- Kiểm tra: `PYTHONIOENCODING=utf-8 python scripts/stale_refresh.py check` → chỉ cần không còn dòng lỗi nào mang tên file của bạn (file của batch khác báo lỗi thì bỏ qua). Sửa cho đến khi sạch.

## Quy tắc số liệu (quan trọng nhất)
- Mọi con số mới phải có nguồn tìm được **ngay bây giờ** (WebSearch/WebFetch): website chính thức ngân hàng/doanh nghiệp, BCTC, HOSE/HNX/UBCKNN/NHNN/Bộ Tài chính/GSO/thuvienphapluat, hoặc báo tài chính (CafeF, VnExpress, Vietstock, VnEconomy, Tuổi Trẻ, Dân trí…) **có ngày đăng**. Ghi URL vào `sources` của edit.
- Ưu tiên số liệu tháng 10–11/2026. Không tìm được số mới thì **giữ số cũ, không bịa**, thêm `note` nói rõ chưa xác minh được gì.
- Giá cổ phiếu/chỉ số: `PYTHONIOENCODING=utf-8 python scripts/market_facts.py --ticker HPG` (hoặc `--brief --tickers A,B`). Tin mới: `python scripts/news_feed.py --topic "<kw>" --days 30`.
- Ghi kỳ dữ liệu cạnh số: "BCTC quý 3/2026", "biểu lãi suất ngày 03/11/2026". Chỉ ghi "tháng 11/2026" khi số liệu thật sự là của tháng 11.
- Số thập phân tiếng Việt dùng dấu phẩy (4,8%), hàng nghìn dùng dấu chấm (1.250 tỷ đồng). Khi đã thay cả bảng thì chuẩn hoá toàn bảng.
- Với bài khuyến nghị cổ phiếu: không đưa giá mục tiêu/khuyến nghị mua bán do DSC tự đặt. Nếu dẫn giá mục tiêu thì ghi rõ của CTCK nào, ngày nào.

## Văn phong
- Đọc `knowledge/3-pipeline/anti-ai-rules.md` PHẦN 1 (từ cấm), 2 (S3 số liệu có nguồn), 8.3, 8.7 trước khi viết. Brand: `knowledge/1-brand/profile.md`.
- Xưng "bạn", câu ngắn, cụ thể, không sáo rỗng ("vô cùng", "đáng kể", "không thể phủ nhận", "trong bối cảnh"...). Giữ giọng văn và độ dài gần như đoạn gốc; chỉ viết lại phần sai/cũ, không viết lại cả bài.
- Không thêm emoji, không dùng "---".

## Giới hạn
- Chỉ ghi file JSON của batch bạn. Không sửa file nào khác, không chạy `sync_live.py`, không `pip install` (máy công ty có Kaspersky).
- Trên Windows, đặt `PYTHONIOENCODING=utf-8` khi chạy python.

## Báo cáo cuối (ngắn)
Mỗi slug: số edit, đã thay số liệu gì (kỳ dữ liệu), cái gì không xác minh được. Kết quả lệnh `check` cho file của bạn.
