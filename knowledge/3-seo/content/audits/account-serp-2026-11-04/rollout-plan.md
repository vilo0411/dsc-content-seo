# Kế hoạch triển khai cụm mở tài khoản — 04/11/2026

Trạng thái: đã thực hiện bản sửa local cho hai bài; chưa cập nhật Final/CMS.

## Mục tiêu và bằng chứng
- Ảnh SERP người dùng: hướng dẫn VFS #7 cho cách mở, #8 cho mở tài khoản; nhóm so sánh VFS #2, DSC #3. Không biết thời điểm chụp chính xác; không coi đây là lịch sử ranking.
- Giữ bài so sánh cho nhu cầu chọn công ty. Cải thiện bài hướng dẫn cho nhóm mở/cách mở/online; không hứa Google sẽ đổi URL.
- GSC baseline 05/10–01/11/2026 trong gsc-baseline.csv, khác thời điểm ảnh và trước snapshot live03/11.
- Snapshot DataForSEO lọc bớt kết quả, không tái hiện ảnh; không dùng để phủ nhận ảnh.

## Việc đã thực hiện
1. Sync hai bài live, chụp baseline; lấy live làm gốc vì giống Final chỉ57% và13%.
2. So canonical, HTTP, nội dung trong HTML. Chưa có URL Inspection; không tuyên bố Google-selected canonical.
3. Tạo Proposal riêng trước khi sửa; giữ các bản Final/draft cũ.
4. Bài hướng dẫn: đưa bước làm lên trước pháp lý, thêm kiểm tra kênh/gói phí, giữ ảnh thao tác, sửa NFC/OTP/kích hoạt và lô lẻ, thêm3FAQ theo ảnh.
5. Bài lựa chọn: giữ title/H1/công ty, thay claim vốn/thị phần/so sánh thiếu nguồn, thêm bảng kênh đăng ký và điều kiện phí chính thức; giữ hướng dẫn ở mức đoạn dẫn.
6. Giữ6+4 ảnh và13+8 đích liên kết gốc. Thêm CTA đúng đích, không UTM.
7. Lint hai bài99. Slop primary74 chưa đạt; secondary91 đạt. Không có claim chỉ số theo ngày để fact checker kiểm, không đồng nghĩa mọi claim đã xác minh.

## Nguồn dữ kiện cần lưu ý
Biểu phí https://www.dsc.com.vn/bieu-phi hiệu lực20/08/2025 khác cách diễn đạt trong KB cũ: mức0,1% chỉ thuộc nhóm quản lý ghi riêng; tài khoản Môi giới có các bậc0,15–0,3%. Không hứa0,1% kèm Môi giới1:1 cho mọi người.
Form https://www.dsc.com.vn/mo-tai-khoan tách đăng ký, OTP, chọn số, rồi eKYC/hợp đồng. Hoàn tất form không chứng minh đủ điều kiện giao dịch.

## Những việc còn trước xuất bản
- Primary: style gate còn fail sau2vòng sửa. Có false-positive so với chính bài gốc vì filename có ngày, nhưng vẫn còn warning mật độ bằng chứng/nhịp đoạn. Không sửa linter/nhồi số để qua.
- Secondary: kiểm tra nguồn và năm của đồ thị thị phần, ảnh SSI có alt Top2. Giữ asset để tránh mất hình, kèm cảnh báo lịch sử; chưa coi đã xác minh.
- Secondary: nguồn VNDIRECT đầy đủ cho DGO/DSTOCK/mydgo ở additional-source-vndirect.txt; link ngắn trong bài chỉ xác nhận DSTOCK.
- Người phụ trách nghiệp vụ xác nhận quy trình thiết bị, thời gian tiếp nhận và gói dịch vụ trước khi CMS.
- Skill optimize Gate2 chờ người dùng /approve trước ghi Final; không ghi website trong session này.

## Checklist CMS sau khi duyệt
1. Backup body và metadata trong CMS; đối chiếu SHA baseline để tránh đè thay đổi mới.
2. Cập nhật bài hướng dẫn trước: title/meta từ metadata JSON, body từ HTML. Không đổi slug hoặc canonical.
3. Preview desktop/mobile360px; kiểm tra ảnh, bảng, CTA, link nội bộ và điều kiện phí.
4. Cập nhật bài so sánh sau khi xử lý ảnh cũ; giữ title/H1.
5. Kiểm tra live; sync_live chỉ2slug; so ảnh/link và title/meta. Kiểm tra HTTP/noindex/canonical.
6. Trong GSC, URL Inspection cả2URL và request indexing nếu nội dung đã đúng; chưa tự thực hiện.
7. Ghi T0 là ngày publish thật. Không dùng04/11 như ngày publish nếu chưa lênCMS.

## Đo kết quả
T+7 kiểm tra crawl/index; T+14 xem query×URL×device; T+28 vàT+42 đánh giá xu hướng cùng độ dài kỳ.
Mục tiêu bảo vệ nhóm so sánh đồng thời tăng impressions/click của URL hướng dẫn. Vị trí trung bình và CTR phụ thuộc query/device; không đặt cam kết top theo thời hạn.
Nếu URL so sánh vẫn đứng trên hướng dẫn, kiểm tra lại index, canonical, truy vấn thực và chất lượng trang trước khi cân nhắc cấu trúc; không gộp/redirect tự động.
Không mua backlink, không sửa thêm hàng loạt bài vệ tinh và không tạo lịch tự động trong giai đoạn này.

## Kiểm tra độc lập cuối

Bài so sánh chưa đạt QA ngữ nghĩa:1critical về ảnh/alt,2major về nguồn VNDIRECT và CTA1:1. Xem independent-review.md. Không sử dụng điểm lint99 làm bằng chứng sẵn sàng xuất bản.
