---
ID: CMP-261124-mo-tai-khoan-tet-2027
Title: Mở tài khoản Tết 2027
Created: 2026-11-24
Channels: seo, social, ads, landing
Owner: Chứng khoán DSC
---
Status: Chờ duyệt

# Mở tài khoản Tết 2027

## 1. Mục tiêu
- Mục tiêu kinh doanh: tăng số tài khoản mới mở online (eKYC) trong mùa Tết 2027, nhắm người có tiền thưởng / tiền lì xì muốn bắt đầu đầu tư.
- KPI chính: số tài khoản mở mới ghi nhận qua sự kiện Meta pixel/dataset — mục tiêu: **[chưa có baseline — xem dưới]**
  - Baseline Meta (24/11/2026, read-only): chưa lấy được. Tài khoản `768269981943615` chưa có campaign nào và chưa có phương thức thanh toán; `1410210783429265` chưa được bật Ads MCP (Meta rollout dần). Chi tiết: `knowledge/raw/ads/2026-11-24-baseline-check.json`.
  - Đề xuất: chạy 7 ngày đầu (22–28/12) như giai đoạn test 2–3 angle, lấy CPL thực tế làm baseline rồi chốt KPI cho phần còn lại. User cần chỉ rõ tài khoản quảng cáo của DSC sẽ dùng.
- KPI phụ: CPL/CPA mở TK (ads); clicks GSC cụm "mở tài khoản" (SEO); reach + click link (social).
- Thời gian chạy: **22/12/2026 – 21/02/2027** (user chốt 24/11/2026). Tết Nguyên đán 06/02/2027 — lịch nghỉ giao dịch HOSE/HNX cần xác minh khi sở công bố.
- Ngân sách ads: **[user chốt sau khi xem baseline — agent không tự đặt]**

## 2. Đối tượng
- Persona chính: **P2 — F0** (vốn 10–100 triệu). Phụ: P1 (tiết kiệm, cân nhắc chuyển một phần tiền gửi).
- Nỗi sợ / kỳ vọng (`persona.py --matrix`): P2 sợ "mua nhầm đỉnh", kỳ vọng "có người đồng hành"; P1 sợ "mất gốc", kỳ vọng "an toàn + hơn ngân hàng".
- Góc dẫn (P2 bridge): "Không cần biết hết mới bắt đầu — có chuyên gia DSC ở đó khi bạn cần hỏi". Tránh DSC Invest.
- Insight từ dữ liệu (`page-audit.csv`, cập nhật 13/11/2026; kỳ đo theo audit gần nhất):
  - "mở tài khoản chứng khoán ở đâu tốt nhất" — bài `nen-mo-tai-khoan-chung-khoan-o-dau`: 12.235 lượt hiển thị, CTR 0,89%, vị trí TB 11,0; 33 query trong vùng 11–20 → câu hỏi lớn nhất của nhóm này là **chọn công ty nào**.
  - "mở tài khoản chứng khoán có mất phí không" — vị trí 2,3 nhưng bài bị gắn nhãn `rank-drop` → lo ngại về **chi phí**.
  - Pillar `cach-mo-tai-khoan-chung-khoan`: 75 inlink ngữ cảnh nhưng vị trí TB 26,7, 18 clicks → trang chính đang yếu.
  - Chưa có bài nào về Tết / tiền lì xì / tiền thưởng (`topic_status --find` 0 kết quả) → khoảng trống nội dung mùa vụ.
  - Chưa có số GSC mới (SEO Dashboard MCP chưa xác thực, cache trống).

## 3. Thông điệp
- Thông điệp chính (13 từ): **Mở tài khoản 3 phút, có chuyên gia đồng hành từ lệnh đầu tiên.**
- Bằng chứng (nguồn `profile.md`):
  1. eKYC 100% online, khoảng 3 phút, không cần ra văn phòng.
  2. Môi giới 1:1 — mỗi khách hàng có chuyên gia hỗ trợ.
  3. Phí giao dịch từ 0,1% — phải kèm "theo biểu phí áp dụng từ …" (compliance-finance §2).
- Offer / ưu đãi Tết: **không** (user xác nhận 24/11/2026) — chỉ dùng USP sẵn có, không viết "ưu đãi Tết", "quà Tết", "lì xì từ DSC".
- Claim cần pháp chế duyệt:
  - "Miễn phí chọn số tài khoản đẹp" — lấy từ `account-opening-comparison.md` (05/2026), chưa có trong `profile.md`.
  - Mọi so sánh phí với VPS/TCBS/SSI — số đối thủ từ 05/2026, đã cũ; mặc định **không** so sánh đích danh trong ads.

## 4. Kênh & việc con
Thứ tự chạy: landing → ads → social → SEO (SEO chạy song song vì cần thời gian để index).

| Kênh | Việc | Lệnh | File | Trạng thái |
|---|---|---|---|---|
| Landing | Landing "Mở tài khoản đầu năm" cho P2 — hero khớp thông điệp chính, FAQ từ query "ở đâu tốt", "có mất phí không" | `/landing CMP-261124-mo-tai-khoan-tet-2027 --persona P2` | landing/ | Chờ brief duyệt |
| Ads | Brief Meta: mục tiêu Leads/Sales mở TK, baseline CPL từ campaign cũ, Ad Library đối thủ mùa Tết | `/ads-brief` → `/meta-ads-copy` (5 biến thể, khung Proof + Question-hook) | ads/ | Chờ brief duyệt |
| Social | 6–8 post Fanpage/Zalo từ 22/12 → 21/02: tiền thưởng/lì xì nên làm gì, lịch nghỉ giao dịch Tết, 3 bước mở TK, câu hỏi "có mất phí không" | `/social-plan 2026-12` + `/social-plan 2027-01` (gắn job này) → `/social-post` | social/ | Chờ brief duyệt |
| SEO | (1) Tối ưu `nen-mo-tai-khoan-chung-khoan-o-dau` (33 query vùng 11–20) | `/optimize` | 3-seo | Đề xuất |
| SEO | (2) Tối ưu pillar `cach-mo-tai-khoan-chung-khoan` (vị trí 26,7) | `/optimize` | 3-seo | Đề xuất |
| SEO | (3) Bài mới mùa vụ, ví dụ "tiền lì xì nên đầu tư gì" / "lịch nghỉ Tết chứng khoán 2027" — **cần kiểm volume trước** (`/keyword-plan` hoặc `/outlining`) | `/outlining <kw>` | 3-seo | Đề xuất |

## 5. Đo lường
- Nguồn số: GSC (SEO Dashboard MCP — cần xác thực), Meta Ads MCP, social export / `syndication/ledger.csv`.
- Cách đếm: **sự kiện Meta pixel/dataset** cho mở tài khoản (user chọn 24/11/2026). UTM vẫn tắt. Cần kiểm dataset đã có sự kiện mở TK và chất lượng khớp sự kiện trước khi chạy ads (`ads_get_datasets` / `ads_get_dataset_quality`). SEO và social không đếm được theo pixel → đo bằng clicks GSC và click link.
- Ngày đo: +7 / +14 / +28 ngày sau Live; báo cáo cuối sau 21/02/2027 bằng `/campaign-report`.
