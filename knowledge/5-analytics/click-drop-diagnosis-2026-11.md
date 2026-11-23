# Click giảm: xu hướng hay SEO yếu đi? (dsc.com.vn, 23/11/2026)

Chart report: [click-drop-diagnosis-2026-11.html](click-drop-diagnosis-2026-11.html) (4 nhóm A–D, mở bằng trình duyệt; nhóm A có 4 chart chung trục thời gian, rê chuột lên 1 chart thì cả 4 chart hiện cùng tuần).
Nguồn: GSC + GA4 qua SEO Dashboard MCP, dữ liệu 29/07/2025 → 20/11/2026. Script tính toán nằm ở `scratch/click-drop/` (data.py, analyze.py, build.py).

## Kết luận

Click giảm **chủ yếu do xu hướng (khoảng 59–88%)**. Phần **SEO yếu thật chiếm khoảng 17–41%**, tập trung ở một số cụm và sửa được.

| Nguyên nhân | Tỷ trọng click mất (YoY T8–10) | Bằng chứng |
|---|---|---|
| CTR/SERP: zero-click, AI Overview (lực chính) | ~70% (gộp theo nhóm) | CTR toàn site gãy từ 2,2% xuống 1,3% trong khoảng 27/10–15/12/2025, sau đó đi ngang 11 tháng. Ở vị trí 1–2, CTR giảm từ 12,9% xuống 6,1%. 95 query non-brand giữ nguyên top 3: CTR giảm từ 15,4% xuống 6,8%, chỉ 15/95 query có CTR tăng. 18/21 SERP lấy từ 09/11/2026 có AI Overview |
| Nhu cầu tìm kiếm giảm (lực phụ) | ~18% | T10/2026 so với T10/2025: impressions toàn bộ query -16% (click -59%), brand -39%, nhóm 'là gì' -37%, nhóm mua CP / mở tài khoản -37%. Bing -23%, Cốc Cốc -46%. Đỉnh T12/2025–T3/2026 là sóng thị trường |
| Tụt hạng | 17% (gộp theo nhóm) đến 41% (tính theo từng query trong 150 query mất nhiều nhất) | Vị trí TB tốt nhất ~5,6 vào T3/2026, sau Core T3 và Core T5/2026 lùi về 7–7,8. Nhóm 'cách mua cổ phiếu / chơi chứng khoán / mở tài khoản' tụt từ top 1–2 xuống 4–12 |
| Chuyển sang hỏi AI | ~0 | Sessions từ ChatGPT/Gemini… đứng yên (2.497 → 2.487) trong khi click Google mất 54.477 |

Lưu ý khi đọc số:
- 53% click mất (29.008) nằm ở **query ẩn danh**. GSC không cho biết query nên không phân bổ được nguyên nhân. Bảng trên chỉ tính cho 25.469 click mất ở các query có ghi nhận.
- Giữa T9/2025 Google bỏ tham số `num=100`, làm impressions và vị trí TB trước và sau mốc này lệch nhau. Vì vậy các chỉ số dùng **T10/2025 làm gốc**. Vị trí "tốt lên" từ ~9 xuống ~7 trong T9/2025 là do cách đo, không phải SEO tốt lên.
- Mẫu query giữ top 3 được chọn từ 686 query (gộp top 500 theo impressions 2026, top 500 theo click 2026 và 150 query mất nhiều nhất), không chỉ lấy query đã mất click. Tiêu chí: không chứa 'dsc', vị trí ≤ 3 ở cả 2 kỳ, vị trí lệch ≤ 0,5, impressions ≥ 50 ở cả 2 kỳ.
- Không có số Google Trends. Phần nhu cầu được suy ra từ impressions brand, các công cụ tìm kiếm khác và query giữ hạng.

## 5 phát hiện chính

1. **Hai nấc giảm:** T11/2025 (CTR gãy, impressions vẫn tăng) và sau đỉnh T3/2026 (impressions và vị trí cùng giảm). Từ T6/2026 click vẫn trượt chậm, khoảng 4% mỗi tháng.
2. **Zero-click là lực chính và đánh mạnh nhất vào bài định nghĩa ('là gì')** và nhóm 'cổ phiếu'. Ví dụ: "thị trường tiền tệ và thị trường vốn" giữ vị trí 1,2, impressions không đổi (180 → 177) nhưng CTR giảm từ 51% xuống 11%.
3. **Nhu cầu brand giảm ~40%** (so với T10/2025). "bảng giá dsc", "dsc demo" gần như mất impressions. Cần kiểm tra xem bảng giá hoặc demo có chuyển sang domain hay app khác không. Cùng kỳ, Google Ads tăng từ 4,2k lên 22,9k sessions, nên có thể đang nhận một phần click brand.
4. **Phần SEO yếu thật** là cụm "cách mua cổ phiếu / mua chứng khoán / chơi chứng khoán / mở tài khoản" (vị trí 1,2–3 → 4–12) và 3 trang: `cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau` (click -93%), `top-10-cuon-sach-hay-ve-dau-tu-tai-chinh…`, `gdp-la-gi`.
5. **Nội dung mới có hiệu quả:** nhóm 'lãi suất' tăng từ 86 lên 1.340 click, mục `/kinh-te-vi-mo/` mới có 1.034 click.

## Việc nên làm

**Phần do xu hướng (không lấy lại được click, chỉ thích nghi được):**
- Đổi KPI SEO: theo dõi impressions, vị trí, số query top 3 và lead, thay vì chỉ nhìn click. So sánh với Bing và Cốc Cốc để tách phần nhu cầu.
- Tối ưu để được AI Overview trích dẫn (sapo trả lời thẳng, H2 dạng câu hỏi, đã có check `GEO-*`). Ưu tiên các bài 'là gì' đang top 3.
- Dồn nội dung mới vào intent ít bị zero-click: so sánh, hướng dẫn thao tác, dữ liệu cập nhật (lãi suất, top cổ phiếu theo tháng).

**Phần do SEO (sửa được):**
- `/optimize` theo thứ tự: `cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau` → các bài cách mua cổ phiếu theo mã (VNM, FPT, HPG) → `top-10-cuon-sach…` → `gdp-la-gi`.
- Kiểm tra cannibalization trong cụm "cách mua cổ phiếu": ngày 25/03/2026 có đợt viết thêm bài cùng chủ đề, ngay trước Core T3/2026.
- Kiểm tra brand: nơi đặt bảng giá và DSC demo, xem Google Ads có đang chạy trên từ khoá brand không.

## Kỳ tiếp theo
Core T11/2026 bắt đầu từ 10/11 và đang rollout. Nên đo lại vào khoảng 08/12/2026, khi rollout xong và có thêm 2 tuần dữ liệu.
