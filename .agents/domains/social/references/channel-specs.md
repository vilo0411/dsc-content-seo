# Channel specs — Social chủ

> Giới hạn dưới đây là **giới hạn biên tập** mà `mkt_lint.py` dùng, không phải giới hạn kỹ thuật chắc chắn của nền tảng. Nền tảng đổi giao diện thường xuyên — kiểm lại khi đăng.

| Kênh | Persona hợp | Độ dài | Câu mở | Hashtag | Hình | CTA |
|---|---|---|---|---|---|---|
| Facebook Fanpage | P1, P2 | 80–250 từ (lint: MINOR > 2000 ký tự) | ≤ 125 ký tự, chứa ý chính trước "Xem thêm" | 1–3 (lint: > 5) | 1080×1350 hoặc carousel 1080×1080; S01/S03 | link bài web hoặc "Mở tài khoản — 3 phút" |
| Zalo OA | P1, P2 (khách hiện hữu) | 60–200 từ, câu ngắn | tiêu đề bài viết OA rõ lợi ích | 0–2 | ảnh bìa 16:9 | nút / link trang đích |
| LinkedIn (Page) | P3, P4 | 150–300 từ (lint: MAJOR > 3000 ký tự) | ≤ 210 ký tự trước "…xem thêm" | 2–3 | 1200×1500 hoặc PDF carousel; S02/S03 | đọc phân tích / đặt lịch tư vấn |

## Format post
- **Giáo dục 1 ý** (pillar Kiến thức): hook = hiểu lầm / câu hỏi thật của F0 → 3 ý ngắn → link bài SEO.
- **Carousel** (5–8 slide): slide 1 luận điểm, slide cuối CTA + logo; mỗi slide ≤ 25 từ.
- **Số liệu tuần** (pillar Thị trường): 1 con số từ `market_facts.py` + ý nghĩa + câu miễn trừ.
- **Sản phẩm** (pillar Sản phẩm): 1 lợi ích cụ thể + điều kiện + CTA. Tối đa 1/4 tổng số post.

## Quy tắc viết
- Một post = một ý. Không dồn 5 mẹo.
- Lấy chất liệu từ bài đã **live** (`publish-ledger.csv`), không chế số mới.
- Không mở bằng câu hỏi tu từ chung chung ("Bạn có biết…?") — blacklist.
- Emoji: tối đa 2, không dùng 🚀💰🔥 cạnh claim lợi nhuận.
