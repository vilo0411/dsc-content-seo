---
Author: Research Agent
Status: Verified ✅
Last_Updated: 2026-11-25
Sources: dsc.com.vn, knowledge/1-brand/brand-facts.json
---

# Company Profile — Chứng khoán DSC

## 0. Định vị nội dung (Source Context) & Thực thể trung tâm (Central Entity)
<!-- Nguồn duy nhất cho 2 khái niệm này. Dashboard (mục Bản đồ chiến lược) đọc nguyên văn 2 dòng in đậm dưới đây. -->
- **Định vị nội dung:** Chứng khoán DSC là công ty chứng khoán; mọi bài viết từ góc nhìn "nhà đầu tư cá nhân làm việc này thế nào khi có tài khoản chứng khoán" — không viết như báo tin tức hay ngân hàng.
- **Thực thể trung tâm:** Đầu tư chứng khoán cá nhân tại Việt Nam.
- **DSC kiếm tiền từ:** mở tài khoản + phí giao dịch (Môi giới 1:1), margin, DSC Invest (mục 2). Số liệu: `brand-facts.json`.
- **Áp dụng:** chủ đề ngoài thực thể trung tâm (vàng, bạc, lãi suất ngân hàng, nghề nghiệp) chỉ viết khi có góc so sánh / dẫn về đầu tư chứng khoán. Cụm nào core / outer / off, bài Outer dẫn về đâu (`bridge_to`): `knowledge/3-seo/strategy/taxonomy.json` → `topics` (xem nhanh: `python scripts/registry.py cluster`).

## 1. Tổng quan & Bằng chứng tin cậy (Proof Points)
- **Tên đầy đủ:** Công ty Cổ phần Chứng khoán DSC.
- **Trụ sở chính:** Tầng 2, tòa nhà Thành Công (Thành Công Tower), số 80 Dịch Vọng Hậu, Quận Cầu Giấy, Hà Nội.
- **Pháp lý & Niêm yết:** Thành viên chính thức của HOSE, HNX, VSDC; cổ phiếu **DSC** niêm yết trên sàn **HOSE** (chuyển sàn từ UPCoM sang HOSE ngày 24/10/2024).
- **Lịch sử:** Tiền thân là Công ty Cổ phần Chứng khoán Đà Nẵng (thành lập 2006), sau khi tái cấu trúc toàn diện từ năm 2021 và đổi tên thành DSC, công ty đã có bước nhảy vọt về quy mô vốn điều lệ và hạ tầng công nghệ số.
- **Định vị thương hiệu:** Ngân hàng Đầu tư (Investment Bank) hiện đại và Quản lý tài sản (Wealth Management) dựa trên nền tảng công nghệ số.
- **Hạ tầng thanh toán:** Kết nối nộp/rút tiền nhanh qua mã định danh với **BIDV** (`963369`) và liên kết trực tiếp với các ngân hàng lớn (Vietcombank, VietinBank, Techcombank, VIB).

## 2. Các mảng dịch vụ trọng tâm
> **Quy tắc MECE:** Mọi con số cụ thể (biểu phí, lãi suất margin, thời gian eKYC, vốn tối thiểu…) chỉ lưu tại **1 nguồn duy nhất** là `knowledge/1-brand/brand-facts.json` (có trạng thái `verified` / `needs_confirmation` và kiểm tra tự động qua `qa_lint.py` `CL5-fact`). Quy trình thao tác kỹ thuật step-by-step lưu tại `knowledge/1-brand/service-operations.md`.

DSC tập trung nguồn lực vào 3 trụ cột dịch vụ chính trên nền tảng công nghệ **DSC Trading**:

### 2.1. Dịch vụ Môi giới chứng khoán 1:1 (Personal Brokerage) — Persona P1, P2, P3
- **Đội ngũ chuyên gia:** Mỗi khách hàng được gán một chuyên gia môi giới hỗ trợ 1:1, đồng hành tư vấn chọn mã, hướng dẫn sàn/lô/cách đặt lệnh và quản trị rủi ro danh mục.
- **Biểu phí & Margin:** Xem `trading_fee` và `margin_rate` trong `brand-facts.json`.

### 2.2. Quản lý tài sản & Ủy thác đầu tư (DSC Invest) — Persona P4
- **Định vị sản phẩm:** Dịch vụ ủy thác quản lý tài sản chuyên biệt dành cho khách hàng vốn lớn (Wealth Client) muốn tăng trưởng bền vững.
- **Tính minh bạch:** Khách hàng theo dõi hiệu quả đầu tư real-time qua App DSC Trading trong khi danh mục được quản lý bởi đội ngũ chuyên gia DSC.
- **Vốn tối thiểu & Biểu phí:** Xem `dsc_invest_min_capital` và `dsc_invest_fees` trong `brand-facts.json`.

### 2.3. Mở tài khoản & Giao dịch trực tuyến (Digital Onboarding) — Persona P1, P2
- **Mở tài khoản eKYC:** 100% online qua App DSC Trading hoặc Web (`https://www.dsc.com.vn/mo-tai-khoan`), kích hoạt ngay tài khoản dạng `024Cxxxxxx` (tiểu khoản đuôi `1` giao dịch thường, đuôi `6` giao dịch ký quỹ/Margin).
- **Thời gian hoàn tất & Mã nạp tiền:** Xem `ekyc_time` và `deposit_code` trong `brand-facts.json`.
- **Phạm vi sản phẩm:** DSC hiện tập trung vào chứng khoán cơ sở và ủy thác đầu tư; **chưa cung cấp dịch vụ giao dịch phái sinh** cho khách hàng cá nhân.

## 3. Lợi thế cạnh tranh (USPs)
- **Phí cạnh tranh kèm Chuyên gia 1:1:** Giải quyết bài toán đánh đổi của thị trường (các bên phí 0% thường cắt bỏ môi giới, các bên có môi giới thường thu phí cao 0,15%–0,35%). DSC giữ mức phí thấp nhưng vẫn có chuyên gia đồng hành 1:1.
- **Cá nhân hóa theo quy mô vốn:** Kết hợp liền mạch từ tự giao dịch có môi giới hỗ trợ (P1–P3) lên ủy thác quản lý tài sản chuyên nghiệp DSC Invest (P4).
- **Hệ thống nạp/rút tiền định danh 24/7:** Liên kết định danh `963369` cùng BIDV và các ngân hàng lớn, tiền vào tiểu khoản ngay lập tức.
- **Hạ tầng công nghệ DSC Trading & Báo cáo phân tích:** Giao diện tối giản cho F0, tốc độ khớp lệnh ổn định, tích hợp báo cáo phân tích vĩ mô & doanh nghiệp từ khối Ngân hàng Đầu tư (IB).

## 4. Tone of Voice (Giọng văn thương hiệu)
- **Chuyên nghiệp (Professional):** Chính xác, có số liệu và nguồn kiểm chứng trong mọi phân tích tài chính.
- **Hiện đại & Sáng tạo (Innovative):** Trực diện, rõ ràng, ưu tiên bảng biểu và hướng dẫn thực hành trên nền tảng số.
- **Tận tâm (Dedicated):** Đứng ở góc nhìn bảo vệ và đồng hành cùng nhà đầu tư cá nhân; cảnh báo rủi ro minh bạch.
- **Ngôn ngữ:** Gần gũi nhưng giữ chuẩn mực tài chính; điều chỉnh độ sâu thuật ngữ theo từng Persona (`python scripts/persona.py --matrix`).

## 5. Từ khóa thương hiệu chính
- Chứng khoán DSC, App DSC Trading, DSC Invest, Môi giới 1:1 DSC.