---
Title: Lệnh MAK là gì? Cơ chế khớp lệnh sàn HNX
Meta_Description: Tìm hiểu lệnh MAK là gì trên sàn HNX và chứng khoán phái sinh. Khám phá cơ chế Match And Kill, so sánh MAK với MOK, MTL, MP và kinh nghiệm đi lệnh thực chiến.
Target_Keyword: lệnh MAK là gì
Slug: lenh-mak-la-gi
---

# Lệnh MAK là gì? Cơ chế khớp lệnh trên sàn HNX và Phái sinh

Trong thời điểm thị trường chứng khoán biến động nhanh, việc đặt lệnh và kiểm soát lượng lệnh chờ là bài toán sống còn. Nếu bạn đang tìm hiểu **lệnh MAK là gì**, đây chính là loại lệnh thị trường giúp khớp ngay khối lượng sẵn có và tự động hủy phần dư. Lệnh giúp ngăn ngừa rủi ro treo lệnh ngoài ý muốn trên sàn HNX và thị trường phái sinh (cập nhật mới nhất năm 2026).

## Lệnh MAK trong chứng khoán là gì?

Lệnh MAK là viết tắt của cụm từ **Match And Kill** (nghĩa là "Khớp và Hủy"). Đây là một biến thể của lệnh thị trường (Market Order). Lệnh phục vụ nhu cầu vào và thoát hàng tức thì mà không để lại lượng lệnh chờ trên hệ thống.

Về bản chất, nguyên tắc vận hành của lệnh MAK dựa trên 3 đặc điểm cốt lõi:
- **Khớp lệnh ngay lập tức:** Ngay khi nhập vào hệ thống, lệnh MAK sẽ quét và đối ứng với mức giá tốt nhất trên sổ lệnh.
- **Cho phép khớp một phần:** Lệnh MAK không bắt buộc phải khớp đủ 100% khối lượng. Lệnh có thể khớp toàn bộ hoặc khớp một phần tùy theo thanh khoản đối ứng.
- **Hủy lập tức phần thừa:** Phần khối lượng chưa khớp ngay sẽ bị hệ thống tự động xóa bỏ (Kill). Lệnh hoàn toàn không treo lại dưới dạng lệnh giới hạn (LO).

Tại thị trường chứng khoán Việt Nam năm 2026, lệnh MAK được áp dụng trong [phiên khớp lệnh liên tục](https://www.dsc.com.vn/kien-thuc/khop-lenh-dinh-ky-va-khop-lenh-lien-tuc) tại hai khu vực:
1. **Sàn HNX (Sở Giao dịch Chứng khoán Hà Nội):** Áp dụng cho các cổ phiếu niêm yết trên bảng HNX.
2. **Thị trường Chứng khoán Phái sinh:** Áp dụng cho Hợp đồng tương lai chỉ số VN30 (VN30F).

*Lưu ý quan trọng:* Sàn HOSE không hỗ trợ lệnh MAK mà sử dụng loại lệnh thị trường riêng là lệnh MP.

## Cơ chế hoạt động của lệnh MAK trên sàn HNX và Phái sinh

Để làm chủ lệnh MAK, nhà đầu tư lướt sóng cần hiểu rõ quy trình xử lý dữ liệu của hệ thống sàn giao dịch khi gửi lệnh.

### Luồng xử lý lệnh chi tiết

1. **Khởi tạo:** Nhà đầu tư phát lệnh MAK (Mua hoặc Bán) kèm theo số lượng chứng khoán cụ thể.
2. **Quét giá đối ứng:** Hệ thống tự động tìm mức giá bán thấp nhất (nếu Mua) hoặc mức giá mua cao nhất (nếu Bán) trên sổ lệnh.
3. **Thực thi khớp:** Lệnh tiến hành khớp theo thứ tự ưu tiên giá và thời gian. Nếu khối lượng giá tốt nhất chưa đủ, lệnh trượt sang các mức giá tiếp theo đến khi hết lượng đối ứng.
4. **Kích hoạt cơ chế Kill:** Khi không còn khối lượng đối ứng khả dụng, phần dư của lệnh MAK lập tức bị hủy bỏ hoàn toàn.

### Kịch bản thực tế minh họa

Giả sử nhà đầu tư đặt lệnh Mua MAK khối lượng 10.000 cổ phiếu PVS trên sàn HNX:

- Trên sổ lệnh hiện tại, bên Bán chỉ có sẵn 4.000 cổ phiếu giá 35,0 và 2.000 cổ phiếu giá 35,1. Tổng lượng bán giá tốt nhất là 6.000 cổ phiếu.
- **Kết quả:** Lệnh MAK khớp ngay 4.000 cổ phiếu giá 35,0 và 2.000 cổ phiếu giá 35,1. Tổng khớp đạt 6.000 cổ phiếu.
- **Xử lý phần dư:** 4.000 cổ phiếu PVS chưa khớp còn lại lập tức bị HỦY khỏi hệ thống. Tài khoản không bị treo 4.000 cổ phiếu ở giá 35,1 dưới dạng lệnh LO như khi dùng [lệnh MTL trong giao dịch chứng khoán](https://www.dsc.com.vn/kien-thuc/lenh-mtl-trong-giao-dich-chung-khoan-la-gi).

## Ưu điểm và hạn chế của lệnh MAK cho nhà giao dịch chủ động

Mặc dù là công cụ đắc lực, lệnh MAK vẫn có những điểm mạnh và điểm yếu riêng mà nhà đầu tư cần cân nhắc.

### Ưu điểm

- **Khớp lệnh với tốc độ tối đa:** Giúp nhà giao dịch chớp thời cơ trong các nhịp breakout hoặc thoát vị thế khẩn cấp.
- **Triệt tiêu rủi ro lệnh chờ bị khớp trễ:** Khi thị trường bất ngờ đảo chiều, lệnh LO treo trên sổ lệnh có thể khiến bạn bị kẹp hàng. Cơ chế "Kill" của MAK loại bỏ hoàn toàn mối lo này.
- **Thăm dò thanh khoản thị trường:** Bạn có thể dùng MAK để kiểm tra lực cầu và cung thực tế tại một vùng giá mà không lo bị chôn vốn.

### Hạn chế

- **Rủi ro trượt giá (Slippage):** Đặt khối lượng MAK quá lớn trong thị trường mỏng thanh khoản sẽ khiến lệnh quét qua nhiều bước giá. Điều này làm tăng giá vốn mua hoặc giảm giá bán.
- **Không đảm bảo khớp đủ khối lượng:** Bạn có thể chỉ mua hoặc bán được một phần mục tiêu ban đầu nếu lượng cung cầu đối ứng quá mỏng.

## Bảng so sánh lệnh MAK với MOK, MTL và MP

Các loại lệnh thị trường phổ biến thường gây nhầm lẫn cho nhà đầu tư. Bảng đối chiếu dưới đây giúp bạn đối soát kỹ 4 loại lệnh này:

| Đặc điểm so sánh | Lệnh MAK (Match And Kill) | Lệnh MOK (Match Or Kill) l| Lệnh MTL (Match To Limit) | Lệnh MP (Market Price) |
|---|---|---|---|---|
| **Cơ chế xử lý phần dư** | Khớp một phần hoặc toàn bộ, phần dư **HỦY NGAY** | Khớp **đủ 100%** hoặc **HỦY TOÀN BỘ** ngay lập tức | Khớp một phần/toàn bộ, phần dư **CHUYỂN THÀNH LỆNH LO** | Khớp một phần/toàn bộ, phần dư **CHUYỂN THÀNH LỆNH LO** |
| **Tính chất chấp nhận khớp 1 phần** | Có | Không | Có | Có |
| **Sàn giao dịch áp dụng** | HNX & [Chứng khoán phái sinh](https://www.dsc.com.vn/kien-thuc/chung-khoan-phai-sinh-la-gi-huong-dan-dau-tu-cho-nguoi-moi-bat-dau) | HNX & Phái sinh | HNX & Phái sinh | HOSE |
| **Phiên giao dịch** | Khớp lệnh liên tục | Khớp lệnh liên tục | Khớp lệnh liên tục | Khớp lệnh liên tục |
| **Mục đích sử dụng chính** | Thoát/Vào lệnh nhanh, không để lại dư lượng | Yêu cầu khớp đúng khối lượng quy định hoặc bỏ | Ưu tiên khớp nhanh nhưng giữ lệnh dư ở giá tốt nhất | Lệnh thị trường tiêu chuẩn trên HOSE |

Để tìm hiểu chi tiết về các nhóm lệnh điều kiện khác, nhà đầu tư có thể đọc thêm bài viết về [các loại lệnh ATO, ATC, LO, MP](https://www.dsc.com.vn/kien-thuc/lenh-ato-atc-lo-mp-la-gi).

## Khi nào nhà giao dịch chủ động nên và không nên dùng lệnh MAK?

### Trường hợp NÊN sử dụng

1. **Giao dịch Hợp đồng tương lai VN30F:** Khi phái sinh biến động mạnh chỉ trong vài phút, phát lệnh MAK giúp mở và đóng vị thế tức thì để chốt lời hoặc cắt lỗ khẩn cấp.
2. **Đánh Breakout cổ phiếu HNX:** Khi mã PVS, CEO, SHB hay IDC xuất hiện dòng tiền lớn, lệnh MAK đảm bảo bạn mua ngay lập tức. Lệnh giúp tránh việc dư lượng mua bị treo ở vùng giá cao.
3. **Quản trị rủi ro khi thị trường giảm biến động:** Khi thị trường quay đầu giảm bất ngờ, lệnh MAK hỗ trợ xả nhanh cổ phiếu sẵn có. Cơ chế giúp bạn tránh rủi ro lệnh dư bị kẹp lại trên bảng điện.

### Trường hợp KHÔNG NÊN sử dụng

1. **Giao dịch mã cổ phiếu thanh khoản thấp (Penny):** Đặt lệnh MAK ở mã kém thanh khoản có thể quét qua nhiều bước giá sàn. Việc này khiến tài khoản chịu thiệt hại nặng về giá.
2. **Cần mua hoặc bán ở mức giá cố định:** Khi bạn có chiến lược định giá cụ thể và chỉ muốn mua vùng hỗ trợ, lệnh giới hạn (LO) là lựa chọn tối ưu hơn.
3. **Giao dịch cổ phiếu thuộc sàn HOSE:** Lệnh MAK không hợp lệ trên sàn HOSE. Hệ thống sàn sẽ báo lỗi nếu bạn cố gửi lệnh này cho các mã FPT, HPG hay VNM.

## Tối ưu tốc độ giao dịch cổ phiếu HNX cùng App DSC Trading

Đối với nhà giao dịch chủ động, tốc độ xử lý hạ tầng và chi phí vốn là hai yếu tố then chốt tạo lợi thế cạnh tranh.

Hệ thống **App DSC Trading** được tối ưu hóa đường truyền tốc độ cao. Tính năng giúp lệnh MAK và MOK gửi thẳng tới sàn HNX mà không bị trễ hạ tầng khung giờ cao điểm (thống kê hiệu năng 2026).

Bên cạnh nền tảng công nghệ mạnh mẽ, Chứng khoán DSC mang tới hệ sinh thái hỗ trợ toàn diện:
- **Đội ngũ Môi giới 1:1 chuyên nghiệp:** Đồng hành phân tích kỹ thuật và xây dựng kịch bản giao dịch. Chuyên gia tư vấn điểm đi lệnh MAK tối ưu rủi ro trượt giá.
- **Gói Margin ưu đãi vượt trội:** Lãi suất vay ký quỹ linh hoạt từ **10% - 13,5%/năm**. Mức ưu đãi giúp tối ưu chi phí vốn cho chiến lược lướt sóng tần suất cao.
- **Hệ thống quản trị rủi ro real-time:** Cảnh báo biến động danh mục kịp thời. Tính năng giúp nhà đầu tư chủ động ứng phó trước mọi kịch bản thị trường.

👉 Trải nghiệm tốc độ khớp lệnh mượt mà và nhận tư vấn chiến lược 1:1 bằng cách [Mở tài khoản chứng khoán DSC online eKYC](https://www.dsc.com.vn/mo-tai-khoan) chỉ trong 3 phút.

<div style="background: linear-gradient(135deg, #0D1B2A 0%, #0A3D2E 100%); border-radius: 14px; padding: 34px 30px; margin: 36px 0; text-align: center; color: #ffffff;">
  <p style="font-size: 23px; line-height: 1.35; margin: 0 0 12px 0; font-weight: 700; color: #ffffff;">Tối Ưu Tốc Độ Khớp Lệnh & Biên Lợi Nhuận Giao Dịch</p>
  <p style="font-size: 15px; line-height: 1.6; margin: 0 0 22px 0; color: #E8F8F2; max-width: 520px; margin-left: auto; margin-right: auto;">Mở tài khoản chứng khoán DSC online eKYC trong 3 phút để nhận tư vấn 1:1 từ chuyên gia và trải nghiệm gói lãi suất Margin hấp dẫn từ 10%/năm.</p>
  <a href="https://www.dsc.com.vn/mo-tai-khoan" style="background: #2BE841; color: #0D1B2A; padding: 15px 38px; border-radius: 30px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block;">Mở Tài Khoản DSC Ngay</a>
</div>

## Câu hỏi thường gặp về lệnh MAK (FAQ)

### Lệnh MAK có được phép sửa hoặc hủy sau khi gửi không**?**
Không. Do đặc tính của lệnh MAK là khớp ngay và tự động hủy phần dư trong vài miligiây, bạn không thể thực hiện thao tác sửa giá hay hủy lệnh thủ công.

### Lệnh MAK có sử dụng được trong phiên ATO hoặc ATC không**?**
Không. Lệnh MAK chỉ có hiệu lực trong phiên khớp lệnh liên tục trên sàn HNX và phái sinh. Trong phiên khớp lệnh định kỳ mở cửa (ATO) và đóng cửa (ATC), lệnh MAK không được chấp nhận.

### Phí giao dịch khi đặt lệnh MAK bị hủy một phần được tính như thế nào**?**
Phí giao dịch chứng khoán chỉ tính trên khối lượng thực tế khớp thành công. Phần khối lượng chưa khớp bị hệ thống hủy (Kill) hoàn toàn không phát sinh bất kỳ khoản phí nào.
