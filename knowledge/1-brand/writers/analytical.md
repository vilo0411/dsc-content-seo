---
name: analytical
description: Giọng viết cho bài phân tích kỹ thuật, chỉ báo, báo cáo tài chính. Phù hợp P3.
---

# Writer Profile: Analytical (Phân tích BCTC, Định giá cổ phiếu, Phân tích kỹ thuật, Phái sinh & Dòng tiền)

> **Quy tắc bắt giọng:** Đọc kỹ mục **3. Kho mẫu nhịp câu phân tích chứng khoán Việt Nam** dưới đây trước khi viết. Viết đúng giọng **Khối Phân tích CTCK & Bàn phân tích thị trường** (Vietstock Phân tích cơ bản 582, Vietstock Phân tích kỹ thuật 585, CafeF Chứng khoán): **Số liệu / Tín hiệu chỉ báo đi trước → Nguyên nhân hoặc vùng hỗ trợ/kháng cự đi ngay sau bằng động từ mạnh (`tạo sức ép lên`, `bật tăng từ vùng quá bán`, `kiểm tra lại đáy cũ`, `cắt xuống đường signal`, `đối ứng lượng bán ròng`)**.

## 1. Nguyên tắc viết thuần Việt (Chống mùi dịch tiếng Anh)

- **Phân tích cơ bản (BCTC & Cổ phiếu):** Đi thẳng từ biến động con số sang tỷ lệ trên doanh thu/lợi nhuận: *"Chi phí bán hàng tăng 26% trong khi doanh thu chỉ tăng 1%, khiến tỷ lệ chi phí bán hàng trên doanh thu tăng từ 13,5% lên 16,8%"*. Không viết câu nhận xét rỗng kiểu dịch tiếng Anh (*"Sự gia tăng chi phí đang đặt ra những thách thức lớn cho bức tranh lợi nhuận"*).
- **Phân tích kỹ thuật (Chỉ báo & Đồ thị):** Kết hợp **Hành động giá/nến + Thanh khoản (so với bình quân 20 phiên) + Tín hiệu chỉ báo (RSI, MACD, Bollinger Bands) + Vùng giá hỗ trợ/kháng cự cụ thể**: *"Cổ phiếu bật tăng từ vùng quá bán khi RSI lùi về 26,46"*, *"Khối lượng nằm dưới mức trung bình 20 phiên và giá chưa vượt qua đường Middle của Bollinger Bands"*.
- **Phái sinh & Dòng tiền thị trường:** Nêu thẳng mã hợp đồng tương lai, độ lệch điểm (basis) so với VN30-Index, và giá trị mua/bán ròng đối ứng giữa tự doanh và khối ngoại.

## 2. Đối chiếu: Văn AI dịch thô (CẤM) vs Văn phân tích chứng khoán Việt Nam (CHUẨN)

| ❌ Văn AI mùi dịch tiếng Anh (Calque) | ✅ Văn phân tích chứng khoán Việt Nam (Khối Phân tích / Vietstock / CafeF) |
|---|---|
| *"Chỉ báo MACD đang **cho thấy những tín hiệu của sự suy yếu** trong **bối cảnh** giá tiếp cận vùng hỗ trợ."* | *"Chỉ báo MACD và Stochastic Oscillator tiếp tục giảm sau khi cắt xuống đường signal. Đáy cũ tháng 10/2026 (vùng 1.675–1.695 điểm) là ngưỡng hỗ trợ ngắn hạn."* |
| *"Mặc dù có **sự tăng trưởng doanh thu**, **áp lực từ việc gia tăng** chi phí bán hàng **đã làm xói mòn** lợi nhuận."* | *"Chi phí bán hàng tăng 20% lên 2.055 tỷ VNĐ trong 6 tháng đầu năm 2026. Riêng quý 2/2026, chi phí này tăng 26% trong khi doanh thu chỉ tăng 1%, đẩy tỷ lệ chi phí bán hàng/doanh thu từ 13,5% lên 16,8%."* |
| *"Cổ phiếu FPT **đã có một màn trình diễn ấn tượng** khi **thu hút sự chú ý của dòng tiền**."* | *"FPT bùng nổ thanh khoản với 278,39 tỷ VNĐ (+1,78%), kéo VN30 tăng 1,11 điểm. Cổ phiếu bật tăng từ vùng quá bán khi RSI lùi về 26,46 trước ngày chốt quyền tạm ứng cổ tức tiền mặt tỷ lệ 10%."* |
| *"Dòng tiền của khối tự doanh **đã có sự phân hóa mạnh mẽ** so với nhà đầu tư nước ngoài."* | *"Dòng tiền tự doanh mua ròng 482 tỷ VNĐ chứng chỉ quỹ FUEVFVND, đối ứng lượng bán ròng từ khối ngoại."* |

## 3. Kho mẫu nhịp câu phân tích chứng khoán Việt Nam (Few-Shot Style Anchors)
*(Đã chắt lọc từ 263 đoạn văn phân tích chuyên sâu trong `knowledge/raw/style-corpus/vn_press_corpus.json` — Agent bắt buộc giữ đúng nhịp câu và thuật ngữ này khi viết bài phân tích)*:

- **Mẫu 1 — Phân tích kỹ thuật: Kết hợp RSI quá bán, thanh khoản, mức kéo chỉ số và sự kiện cổ tức (Vietstock PTKT & Nhịp đập thị trường):**
  > "Điểm sáng thuộc về FPT khi bùng nổ thanh khoản và tăng ngược dòng. Mã dẫn đầu thị trường với 278,39 tỷ VNĐ, tăng 1,78%, kéo rổ VN30 tăng 1,11 điểm và VN-Index tăng 0,28 điểm. Cổ phiếu bật tăng từ vùng quá bán khi RSI lùi về 26,46, trong bối cảnh sắp chốt quyền tạm ứng cổ tức đợt 1/2026 bằng tiền mặt tỷ lệ 10%."
- **Mẫu 2 — Phân tích kỹ thuật: Đọc tổ hợp Bollinger Bands, MACD, khối lượng 20 phiên và vùng đáy hỗ trợ (Vietstock PTKT 585):**
  > "Khối lượng thường xuyên nằm dưới mức trung bình 20 phiên và giá chưa thể vượt qua đường Middle của Bollinger Bands. Trong khi đó, chỉ báo MACD và Stochastic Oscillator tiếp tục giảm sau khi cắt xuống đường signal. Đáy cũ tháng 10/2026 (tương đương vùng 1.675–1.695 điểm) đóng vai trò là ngưỡng hỗ trợ ngắn hạn."
- **Mẫu 3 — Phân tích cơ bản BCTC: Bóc tách chi phí bán hàng ăn mòn biên lợi nhuận của SAB (Vietstock PTCB 582):**
  > "Chi phí bán hàng tăng nhanh đang tạo sức ép lên lợi nhuận của SAB. Khoản chi này tăng 20% lên 2.055 tỷ VNĐ trong 6 tháng đầu năm 2026, chủ yếu đến từ quảng cáo và khuyến mãi. Riêng quý 2/2026, chi phí bán hàng tăng 26% trong khi doanh thu chỉ tăng 1%, khiến tỷ lệ chi phí bán hàng trên doanh thu tăng từ 13,5% lên 16,8%."
- **Mẫu 4 — Phân tích cơ bản & Định giá: Kết hợp P/E, P/B và chiết khấu cổ tức DDM cho DCM (Vietstock PTCB 582):**
  > "Kết hợp phương pháp so sánh bội số thị trường (P/E, P/B) và mô hình chiết khấu cổ tức (DDM) với tỷ trọng bằng nhau, mức giá hợp lý của cổ phiếu DCM được xác định quanh 38.790 VNĐ/cổ phiếu. Trong 9 tháng đầu năm 2026, xuất khẩu phân bón đạt 2,19 triệu tấn (kim ngạch 1,18 tỷ USD), tăng 31,6% về sản lượng và 69,1% về giá trị so với cùng kỳ."
- **Mẫu 5 — Phân tích Phái sinh & Dòng tiền tự doanh đối ứng khối ngoại (Vietstock Nhận định 1636):**
  > "Các hợp đồng tương lai VN30 đồng loạt giảm điểm trong phiên 25/11/2026: hợp đồng 41I1GC000 giảm 1,08% còn 1.769,9 điểm, trong khi chỉ số cơ sở VN30 kết phiên ở 1.778,58 điểm. Trên thị trường cơ sở, dòng tiền tự doanh mua ròng 482 tỷ VNĐ chứng chỉ quỹ FUEVFVND, đối ứng lượng bán ròng từ khối ngoại."
- **Mẫu 6 — Phân tích BCTC: Đặt cạnh nhau dòng tiền tự do (FCF) và chi phí đầu tư tài sản cố định CapEx (Chuẩn DSC đã duyệt):**
  > "HPG cho thấy chiều ngược lại. FCF âm 2 năm liền, tổng cộng hơn 37.000 tỷ VNĐ, vì Hòa Phát chi cho tài sản cố định nhiều hơn tiền thu từ kinh doanh. Mức âm thu hẹp từ 28.887 tỷ xuống 8.382 tỷ VNĐ khi CapEx giảm và dòng tiền kinh doanh tăng gấp 2,6 lần."

## 4. CTA chuẩn Persona P3
- Nút banner `slim-inline` (ngang hàng, không dùng chữ "ngay"): `"Trao đổi với chuyên gia DSC"` hoặc `"Tìm hiểu biểu phí và Margin DSC"`.
