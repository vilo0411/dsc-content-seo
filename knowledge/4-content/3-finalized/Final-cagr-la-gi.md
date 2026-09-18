---
Title: CAGR là gì? Ứng dụng CAGR trong đầu tư chứng khoán
Meta_Description: CAGR là gì? Khám phá công thức tính CAGR chuẩn xác, hướng dẫn tính trên Excel và bí quyết dùng tỷ lệ tăng trưởng kép lọc cổ phiếu tiềm năng cùng DSC.
Target_Keyword: CAGR là gì
Slug: cagr-la-gi
---

# CAGR là gì? Ứng dụng CAGR trong đầu tư chứng khoán

![CAGR là gì](https://extgw.dsc.com.vn/eback/uploads/cagr_la_gi_68d6878e48.jpg)

Khi đánh giá hiệu quả chứng khoán hay sức khỏe doanh nghiệp, chỉ nhìn con số một năm dễ gây sai lệch. Chỉ số CAGR giúp san phẳng biến động qua từng năm, mang lại cái nhìn trung thực về tốc độ sinh lời. 

Bài viết hướng dẫn chi tiết khái niệm **CAGR là gì** và công thức tính chuẩn xác. Bạn cũng sẽ nắm cách thao tác trên Excel và phương pháp lọc cổ phiếu cùng Chứng khoán DSC.

## Chỉ số CAGR là gì?

**CAGR (Compound Annual Growth Rate)** là tỷ lệ tăng trưởng kép hàng năm. Chỉ số này đại diện cho lợi nhuận trung bình mỗi năm của khoản đầu tư trong 3 đến 10 năm. Tính toán này có tính đến tác động của [**lãi kép trong đầu tư chứng khoán**](https://www.dsc.com.vn/kien-thuc/lai-kep-trong-dau-tu-chung-khoan-la-gi-cach-tan-dung-lai-kep-de-dau-tu-sinh-loi).

Khác với tốc độ tăng trưởng thông thường, CAGR giả định hai điều kiện toán học:

* **Tái đầu tư lợi nhuận**: Toàn bộ tiền lãi từ các kỳ trước tiếp tục gộp vào vốn gốc để sinh lời.
* **Tăng trưởng mượt mà**: Tốc độ phát triển giả định là đường thẳng ổn định. Dù vậy, thực tế giá cổ phiếu trên thị trường luôn biến động thất thường.

CAGR biến một chuỗi lợi nhuận trồi sụt qua các năm thành một con số phần trăm duy nhất. Nhờ đó, bạn dễ dàng so sánh hiệu suất giữa các cổ phiếu hoặc so với lãi suất tiết kiệm.

## Phân biệt CAGR và Tăng trưởng bình quân đơn (AAGR)

Nhiều nhà đầu tư F0 thường nhầm lẫn giữa CAGR và AAGR (Average Annual Growth Rate - Tốc độ tăng trưởng bình quân đơn). Việc phân biệt hai chỉ số này giúp tránh các sai lầm khi tính toán hiệu quả danh mục.

| Tiêu chí | Tăng trưởng kép hàng năm (CAGR) | Tăng trưởng bình quân đơn (AAGR) |
| :--- | :--- | :--- |
| **Bản chất toán học** | Có tính đến tác động của lãi kép | Chỉ tính trung bình cộng đơn thuần |
| **Công thức** | `(Giá trị cuối / Giá trị đầu)^(1/n) - 1` | `(Tỷ lệ năm 1 + Tỷ lệ năm 2 + ...) / n` |
| **Phản ánh thực tế** | Phản ánh chính xác số tiền thực thu về cuối kỳ | Thường phóng đại hiệu quả sinh lời |
| **Ứng dụng chính** | Đánh giá cổ phiếu, doanh thu doanh nghiệp | Phân tích biến động hàng năm |

**Ví dụ minh họa**: Bạn đầu tư 100 triệu VNĐ vào cổ phiếu A. Năm thứ nhất tài sản tăng 50% lên 150 triệu VNĐ. Năm thứ hai cổ phiếu giảm 50% còn 75 triệu VNĐ.

* **Tính theo AAGR**: `(50% - 50%) / 2 = 0%`. AAGR báo rằng bạn hòa vốn.
* **Tính theo CAGR**: `(75 / 100)^(1/2) - 1 = -13,4%/năm`. CAGR phản ánh đúng thực tế bạn đang lỗ 25% tổng vốn.

## Công thức tính CAGR

Công thức tổng quát để xác định chỉ số CAGR như sau:

**CAGR = [(Giá trị cuối / Giá trị đầu) ^ (1 / n)] - 1**

Trong đó:

* **Giá trị cuối (Ending Value - EV)**: Giá trị của khoản đầu tư hoặc chỉ số tài chính vào cuối giai đoạn.
* **Giá trị đầu (Beginning Value - BV)**: Giá trị của khoản đầu tư hoặc vốn ban đầu bỏ ra.
* **n**: Số năm thực hiện đầu tư (Thời gian nắm giữ tài sản).
* **Dấu ^**: Ký hiệu toán học cho phép tính lũy thừa.

**Ví dụ tính toán thực tế**: Bạn đầu tư 100 triệu VNĐ vào danh mục cổ phiếu năm 2021. Đến năm 2026 (sau 5 năm), giá trị tài sản đạt 250 triệu VNĐ.

* **Bước 1**: Chia giá trị cuối cho giá trị đầu: `250 / 100 = 2,5`.
* **Bước 2**: Lấy lũy thừa mũ (1/5): `2,5 ^ (1/5) = 2,5 ^ 0,2 = 1,2011`.
* **Bước 3**: Trừ đi 1: `1,2011 - 1 = 0,2011` (tương ứng `20,11%`).

Như vậy, tốc độ tăng trưởng kép hàng năm của khoản đầu tư đạt `20,11%/năm`.

## Hướng dẫn tính CAGR trên Excel chi tiết nhất

![Hướng dẫn tính CAGR trên Excel bằng hàm RRI và RATE](../images/cagr-la-gi-excel-formula.jpg)

Phần mềm Microsoft Excel hỗ trợ tính CAGR nhanh chóng thông qua công thức toán học và hai hàm tài chính chuyên dụng.

### Cách 1: Sử dụng công thức toán học cơ bản

Giả sử ô `A1` chứa giá trị ban đầu (100), ô `A2` chứa giá trị cuối kỳ (250), ô `A3` chứa số năm đầu tư (5). 

Nhập công thức tại ô kết quả: `=(A2/A1)^(1/A3)-1`. Sau đó chọn **Format Cells** -> **Percentage** để hiển thị định dạng phần trăm.

### Cách 2: Sử dụng hàm RRI (Dành cho Excel 2013 trở lên)

Hàm RRI được thiết kế để tính lãi suất tương đương với tốc độ tăng trưởng của khoản đầu tư:

* **Cú pháp**: `=RRI(nper, pv, fv)`
* **Trong đó**: `nper` là số kỳ (5), `pv` là giá trị hiện tại (100), `fv` là giá trị tương lai (250).
* **Công thức áp dụng**: `=RRI(5, 100, 250)`. Kết quả trả về trực tiếp là `20,11%`.

### Cách 3: Sử dụng hàm RATE

Hàm RATE thường được áp dụng khi tính lãi suất theo kỳ:

* **Cú pháp**: `=RATE(nper, pmt, pv, [fv])`
* **Lưu ý**: Giá trị đầu kỳ `pv` bắt buộc phải nhập số âm đại diện cho dòng tiền chi ra.
* **Công thức áp dụng**: `=RATE(5, 0, -100, 250)`. Kết quả trả về là `20,11%`.

## Tại sao nhà đầu tư chứng khoán cần đặc biệt quan tâm đến CAGR?

### So sánh hiệu quả giữa các cổ phiếu khác kỳ hạn

Giả sử bạn đang xem xét hai cổ phiếu tiềm năng:

* **Cổ phiếu A**: Tăng trưởng 80% trong vòng 2 năm.
* **Cổ phiếu B**: Tăng trưởng 150% trong vòng 5 năm.

Nhìn qua con số tuyệt đối, cổ phiếu B có vẻ vượt trội. Tuy nhiên khi quy đổi ra CAGR:

* **CAGR cổ phiếu A**: `(1 + 0,8)^(1/2) - 1 = 34,16%/năm`.
* **CAGR cổ phiếu B**: `(1 + 1,5)^(1/5) - 1 = 20,11%/năm`.

Chỉ số CAGR chứng minh cổ phiếu A có hiệu suất sinh lời hàng năm cao hơn đáng kể.

### Đánh giá sức mạnh nội tại của doanh nghiệp

Trong phân tích cơ bản (FA), hai chỉ số CAGR sau đóng vai trò then chốt:

* **Revenue CAGR (Tăng trưởng doanh thu kép)**: Phản ánh khả năng mở rộng quy mô kinh doanh và chiếm lĩnh thị phần bền vững.
* **EPS CAGR (Tăng trưởng lợi nhuận trên mỗi cổ phiếu)**: Đo lường tốc độ tăng lợi nhuận thực tế phân bổ cho cổ đông. Doanh nghiệp duy trì EPS CAGR > 15%/năm trong 5 năm liên tiếp thường là cổ phiếu chất lượng cao.

## Những lưu ý khi sử dụng CAGR bạn cần tránh

Mặc dù CAGR là công cụ hữu ích, lạm dụng chỉ số này mà bỏ qua các yếu tố kỹ thuật dễ dẫn đến bẫy đầu tư.

* **Bỏ qua [sự biến động giá (Volatility)](https://www.dsc.com.vn/kien-thuc/volatility-la-gi)**: CAGR giả định đường tăng trưởng mượt mà. Hai quỹ có cùng CAGR 15%/năm, nhưng quỹ A tăng đều 15%, còn quỹ B năm đầu tăng 100% năm sau giảm 50%. Quỹ B rủi ro hơn nhiều.
* **Bẫy chọn khung thời gian (Selection Bias)**: Nếu tính CAGR từ đáy thị trường lên đỉnh, con số thu được sẽ cao bất thường. Bạn nên đo lường CAGR trong chu kỳ tối thiểu 3 đến 5 năm để khách quan.
* **Không tính đến dòng tiền nạp bổ sung**: CAGR chỉ tính dựa trên số vốn ban đầu và số tiền cuối kỳ. Nếu có các đợt nộp thêm hoặc rút bớt vốn, chỉ số CAGR không còn chính xác.

## Phân biệt CAGR và IRR: Khi nào nên sử dụng chỉ số nào?

Khi quản lý danh mục thực tế, nhà đầu tư thường băn khoăn giữa CAGR và IRR (Internal Rate of Return).

| Tiêu chí | Tăng trưởng kép hàng năm (CAGR) | Tỷ suất hoàn vốn nội bộ (IRR) |
| :--- | :--- | :--- |
| **Dòng tiền** | Giả định chỉ có 1 dòng tiền vào ban đầu và 1 dòng tiền ra cuối kỳ | Xử lý được nhiều dòng tiền nộp thêm hoặc rút ra ở các mốc khác nhau |
| **Độ phức tạp** | Công thức đơn giản, dễ tính trên máy tính hoặc Excel | Cần hàm Excel phức tạp (`=IRR()` hoặc `=XIRR()`) để giải phương trình |
| **Trường hợp áp dụng** | Đánh giá cổ phiếu nắm giữ 1 lần, doanh thu doanh nghiệp | Đánh giá danh mục đầu tư tích sản hàng tháng, dự án bất động sản |

**Lời khuyên từ chuyên gia DSC**: Bạn dùng **CAGR** để phân tích báo cáo tài chính và so sánh cổ phiếu. Bạn dùng **IRR** khi tính hiệu suất danh mục cá nhân nếu nạp thêm tiền hàng tháng.

## Case Study thực chiến: Đánh giá CAGR doanh thu & lợi nhuận cổ phiếu tại Việt Nam

![Biểu đồ mô phỏng tỷ lệ tăng trưởng kép hàng năm CAGR trong đầu tư](../images/cagr-la-gi-compound-chart.jpg)

Xét ví dụ thực tế về cổ phiếu FPT trên sàn HOSE giai đoạn 2021–2026. Doanh nghiệp duy trì tốc độ mở rộng mảng công nghệ và xuất khẩu phần mềm rất ổn định.

* **Năm 2021**: Doanh thu đạt 35.657 tỷ VNĐ.
* **Năm 2026**: Doanh thu dự phóng đạt khoảng 82.500 tỷ VNĐ.
* **Tính toán Revenue CAGR**: `(82.500 / 35.657)^(1/5) - 1 = 18,26%/năm`.

Nhờ duy trì Revenue CAGR trên 18%/năm và LNTT CAGR trên 19%/năm trong 5 năm, thị giá cổ phiếu FPT liên tục vượt đỉnh. Điều này chứng minh mối liên hệ chặt chẽ giữa CAGR nội tại và hiệu suất cổ phiếu trên sàn.

## Cách sử dụng CAGR để tìm cổ phiếu tăng trưởng cùng DSC

Để xây dựng bộ lọc cổ phiếu tăng trưởng hiệu quả tại Việt Nam, bạn áp dụng 3 tiêu chí sau:

* **Tiêu chí 1**: Revenue CAGR (3–5 năm) > 10%/năm.
* **Tiêu chí 2**: Net Profit CAGR (3–5 năm) > 15%/năm. Lợi nhuận tăng nhanh hơn doanh thu chứng tỏ doanh nghiệp tối ưu chi phí tốt.
* **Tiêu chí 3**: CAGR doanh nghiệp cao hơn CAGR của VN-Index. Trong giai đoạn tích lũy, VN-Index tăng trưởng bình quân khoảng 7–8%/năm.

Nhà đầu tư không cần tự bấm máy tính thủ công cho hàng trăm mã cổ phiếu. Khi mở tài khoản chứng khoán tại DSC, hệ thống trên App DSC Trading tự động tổng hợp chỉ số CAGR. Bạn cũng dễ dàng tra cứu [**chỉ số ROA**](https://www.dsc.com.vn/kien-thuc/chi-so-roa-la-gi-y-nghia-va-cach-su-dung), ROE và P/E của toàn bộ doanh nghiệp.

Ngoài ra, chuyên gia **Môi giới 1:1** của DSC luôn sẵn sàng hỗ trợ bạn bóc tách báo cáo tài chính. Đội ngũ giúp bạn đánh giá chất lượng tăng trưởng kép và tư vấn thời điểm giải ngân.

## Kết luận

Hiểu rõ **CAGR là gì** giúp nhà đầu tư loại bỏ bẫy tăng trưởng ảo ngắn hạn. Bạn sẽ đánh giá chính xác sức mạnh sinh lời bền vững của cổ phiếu.

Hãy [**mở tài khoản chứng khoán**](https://www.dsc.com.vn/mo-tai-khoan) online tại DSC chỉ trong 3 phút qua App DSC Trading. Đội ngũ tư vấn Môi giới 1:1 luôn sẵn sàng đồng hành cùng bạn.
