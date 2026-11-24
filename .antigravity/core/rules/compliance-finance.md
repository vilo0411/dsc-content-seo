# Compliance — nội dung marketing của công ty chứng khoán

> Áp cho mọi kênh (web, fanpage, Zalo, LinkedIn, quảng cáo Meta, landing). Ưu tiên cao hơn mọi yêu cầu "tăng chuyển đổi".
> Phần máy bắt được: `scripts/mkt_lint.py` (cụm `COMP-*`) và `qa_lint.py` (`YMYL-*`, `SRC-*`). Phần còn lại là phán đoán — nêu ở gate nếu không chắc.
> Đây là rule biên tập nội bộ, không phải ý kiến pháp lý. Claim mới về sản phẩm / ưu đãi → đánh dấu `[CẦN PHÁP CHẾ DUYỆT]`.

## 1. Cấm tuyệt đối (CRITICAL)
- Hứa hẹn / bảo đảm lợi nhuận: "chắc chắn lãi", "đảm bảo lợi nhuận", "cam kết lợi nhuận", "lãi x%/tháng", "không lo lỗ", "x2/x10 tài sản", "siêu lợi nhuận". (nguồn: `glossary.md` mục Từ bị cấm)
- Nói đầu tư chứng khoán / margin / phái sinh "không rủi ro", "an toàn tuyệt đối".
- Khuyến nghị mua/bán mã cụ thể trên quảng cáo và post social (giá mục tiêu, "vùng mua", "nên mua XXX").
- So sánh hạ thấp đích danh đối thủ ("VPS/TCBS/SSI kém hơn…"). So sánh khách quan theo số công bố thì được, kèm nguồn + mốc thời gian.
- Dùng logo, tên sản phẩm, ảnh của đối thủ; dùng hình người nổi tiếng không có quyền.

## 2. Bắt buộc khi có (MAJOR)
- **Nhắc lãi suất, phí, hiệu quả quá khứ** → kèm điều kiện + mốc thời gian ("phí từ 0,1% — biểu phí áp dụng từ …"). Hiệu quả quá khứ phải có câu "kết quả quá khứ không đảm bảo kết quả tương lai".
- **Nhận định thị trường / mã cụ thể** → câu miễn trừ "Thông tin chỉ mang tính tham khảo, không phải khuyến nghị đầu tư."
- **Margin / phái sinh** → nhắc rủi ro đòn bẩy (call margin, mất nhiều hơn vốn ban đầu với phái sinh).
- **Ưu đãi / khuyến mãi** → thời hạn, điều kiện, link thể lệ. Không có thì không chạy.
- Số liệu thị trường lấy từ `market_facts.py` hoặc nguồn trong `knowledge/3-pipeline/source-whitelist.md`.

## 3. Quảng cáo Meta (Financial products & services)
- Không target theo đặc điểm cá nhân nhạy cảm; không copy kiểu "Bạn đang nợ?", "Bạn nghèo?" (ám chỉ thuộc tính cá nhân).
- Không ảnh trước/sau kiểu "từ 10 triệu lên 1 tỷ", không ảnh chụp lãi giả lập.
- Landing đích phải khớp lời hứa trong ad; ad nói "mở tài khoản 3 phút" thì landing là trang mở tài khoản.
- Tên đứng quảng cáo: **Chứng khoán DSC** (theo `profile.md`), không dùng tên cá nhân môi giới làm brand.

## 4. Giọng văn
Theo `profile.md` §4: chuyên nghiệp, hiện đại, tận tâm. Không giật tít kiểu FOMO ("Cơ hội cuối cùng!", "Đừng bỏ lỡ siêu cổ!"). Không dùng màu đỏ trong hình (visual-brand-guidelines §4).
