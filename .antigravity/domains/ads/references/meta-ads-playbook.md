# Meta Ads playbook — Chứng khoán DSC

## 1. Mục tiêu → objective → KPI
| Mục tiêu kinh doanh | Objective Meta | KPI chính | KPI phụ |
|---|---|---|---|
| Mở tài khoản (P2 F0) | Leads hoặc Sales (sự kiện mở TK trên web/app) | CPL / CPA mở TK | CTR link, tỷ lệ eKYC hoàn tất |
| Đặt lịch tư vấn (P3, P4) | Leads (form) | CPL đủ điều kiện | tỷ lệ liên hệ được |
| Traffic về bài SEO / landing | Traffic | CPC link, thời gian trên trang | CTR |
| Nhận diện | Awareness | CPM, reach | ThruPlay (video) |

Không chạy Leads cho DSC Invest khi chưa có quy trình lọc ≥ 3 tỷ — CPL rẻ nhưng lead không đạt.

## 2. Khung copy (mỗi biến thể chọn 1 khung, ghi tên khung trong heading)
- **PAS** — Problem (nỗi sợ của persona) → Agitate nhẹ, không dọa → Solution (sản phẩm + điều kiện).
- **Proof** — 1 con số kiểm chứng được (phí từ 0,1%, eKYC 3 phút) → lợi ích → CTA.
- **Question-hook** — câu hỏi thật của F0 (lấy từ PAA / GSC query) → trả lời 1 câu → CTA đọc tiếp.
- **Expert** — góc nhìn chuyên gia môi giới 1:1 → mời trao đổi.

Trigger theo persona: `python scripts/persona.py --matrix` (dòng Trigger sợ / kỳ vọng / CTA).

## 3. Giới hạn biên tập (mkt_lint)
| Trường | MINOR khi > | MAJOR khi > | Ghi chú |
|---|---|---|---|
| Primary text | 125 ký tự | 500 | Câu đầu phải đứng được một mình khi bị cắt |
| Headline | 40 | 255 | Lợi ích cụ thể, không lặp primary |
| Description | 30 | 255 | Hay bị ẩn trên mobile — không đặt thông tin bắt buộc ở đây |

Điều kiện / thời hạn ưu đãi → đặt ở primary text hoặc landing, không chỉ ở description.

## 4. Đọc số (`/ads-review`)
Thứ tự: tình trạng phân phối (đang chạy / learning / limited) → chi tiêu so ngân sách → KPI chính so mục tiêu brief → phễu (CTR → landing → chuyển đổi) để biết hỏng ở tầng nào → creative fatigue (frequency > 3 và CTR giảm 3 ngày liền).
Ngưỡng tham chiếu: lấy `ads_insights_industry_benchmark` / `ads_insights_performance_vs_peers`, không tự đặt con số.
Kết luận chỉ khi đủ dữ liệu: ≥ 1.000 impression và ≥ 3 ngày ở ad set; thiếu thì ghi "chưa đủ dữ liệu".

## 5. Creative brief (cho `/image` hoặc designer)
Mỗi ad: tỷ lệ (1080×1350 feed, 1080×1920 story/reel, 1200×628 link), style S01–S04 (`visual-styles.md`), dòng chữ trên ảnh ≤ 8 từ, logo trên trái, không màu đỏ, không ảnh chụp lãi/lỗ.
