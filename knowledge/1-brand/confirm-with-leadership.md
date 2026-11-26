# Sổ Theo dõi Quyết định & Câu hỏi Chờ Lãnh đạo / Pháp chế Xác nhận

**Cập nhật gần nhất:** 2026-11-25
**Liên kết với:** `knowledge/1-brand/brand-facts.json` (các mục có `status: "needs_confirmation"`) và các câu hỏi mở từ `/market-research`, `/setup`.

---

## 1. Mục tiêu
Tài liệu này là **Open Decisions & Pending Confirmations Log** duy nhất trong `1-brand/`:
- Ghi nhận các điểm chiến lược đã được Ban lãnh đạo chốt (`[Resolved ✅]`).
- Theo dõi các số liệu sản phẩm trong `brand-facts.json` hoặc các câu hỏi chiến lược đang chờ xác nhận (`[Pending ⏳]`) trước khi được phép dùng trong quảng cáo trả phí (Google Ads / Meta Ads) và Email.

---

## 2. Các quyết định chiến lược đã chốt (`[Resolved ✅]`)

### A. Định vị & Phạm vi Sản phẩm (Chốt 2026-05-11 & 2026-11-19)
1. **Dịch vụ Môi giới 1:1:** Tập trung vào sự đồng hành của chuyên gia môi giới (tư vấn chọn mã, hướng dẫn sàn, lô giao dịch, cách đặt lệnh; không tự đặt giá mục tiêu trong bài SEO). `[Resolved ✅]`
2. **Quản lý tài sản (DSC Invest):** Tập trung vào khách hàng vốn lớn ($\ge 3$ tỷ VNĐ/hợp đồng), phí quản lý 1,5%/năm, phí thưởng hiệu quả 20% trên phần lợi nhuận vượt 8%/năm. `[Resolved ✅]`
3. **Mở tài khoản & Digital Onboarding:** Tập trung vào trải nghiệm eKYC 100% online ~3 phút, nạp tiền định danh BIDV `963369`. `[Resolved ✅]`
4. **Loại bỏ sản phẩm cũ / ngoài phạm vi:** Đã loại bỏ hoàn toàn **Tư vấn số**, **Đào tạo** và **Chứng khoán phái sinh** khỏi phạm vi sản phẩm bán lẻ của dự án. `[Resolved ✅]`

### B. Hệ thống Persona & Nhận diện (Chốt 2026-05-15 & 2026-11-25)
1. **Hệ thống 4 Persona (`personas.md` v2.0):** P1 Tiết kiệm · P2 F0 · P3 Active Trader · P4 Vốn lớn. `[Resolved ✅]`
2. **Danh sách đối thủ theo dõi (`2-market/`):** Chia 2 nhóm rõ ràng: Đối thủ Thị phần & Ads (VPS, TCBS, SSI, DNSE, VPBankS) và Đối thủ SEO Content Hub (`competitors.json`: VPBankS, VCBS, DNSE, ACBS, Vietcap, VFS). `[Resolved ✅]`
3. **Hệ thống Nhận diện Thương hiệu (`DESIGN.md` v1.0 & `brand.json`):** Palette chuẩn Gunmetal `#272D2B` · Pine Teal `#1D4130` · Lime `#2AD03D` · Emerald `#1BBE72` · Frosted Mint `#8CFFCC` · White `#FFFFFF`; font duy nhất `Plus Jakarta Sans`. `[Resolved ✅]`

---

## 3. Các số liệu & chính sách đang chờ xác nhận (`[Pending ⏳]`)

> **Quy tắc an toàn:** Các mục dưới đây dùng được trong bài kiến thức SEO dưới dạng khoảng tham khảo kèm điều kiện, nhưng **cần owner xác nhận (`status: "verified"` trong `brand-facts.json`)** trước khi chạy chiến dịch Ads cam kết cố định. Kiểm tra hạn rà soát bằng: `python scripts/fact_consistency.py --due`.

| ID (`brand-facts.json`) | Nội dung hiện tại | Điểm cần lãnh đạo / nghiệp vụ xác nhận | Trạng thái |
|---|---|---|---|
| `trading_fee` | `từ 0,1%` | Xác nhận biểu phí bậc thang chính thức hiện hành trên web để dẫn link thể lệ trong quảng cáo. | `[Pending ⏳]` |
| `margin_rate` | `10–13,5%/năm` | Xác nhận tên các gói vay Margin đang mở mới (ví dụ gói S9 hay gói ưu đãi Tết 2027) và điều kiện đi kèm. | `[Pending ⏳]` |
| `ekyc_time` | `3 phút` | Xác nhận claim thời gian mở tài khoản eKYC dùng trên headline quảng cáo. | `[Pending ⏳]` |
| `free_nice_account_number` | Miễn phí chọn số tài khoản đẹp | Đang dùng trong `account-opening-comparison.md` và brief `CMP-261124` — cần xác nhận điều kiện dải số áp dụng miễn phí. | `[Pending ⏳]` |
