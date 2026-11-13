# Gộp instincts 2026-11-09 — bản đề xuất để duyệt

- Bản đề xuất: `.antigravity/memory/instincts-archive.proposed.md` (archive thật chưa đổi; backup ID: `instincts-archive.bak-2026-11-09.md`).
- Xem trước: `python scripts/optimize_instincts.py --archive .antigravity/memory/instincts-archive.proposed.md --check`
- Kết quả: 102 rule ACTIVE → **26 rule chuẩn** (19 Global + 7 theo topic) + I045 giữ nguyên. `instincts.md` 26.800 ký tự (nội dung thật, hiện bị cắt còn 19.200) → **7.726 ký tự**, không rule nào bị cắt. Mỗi file topic: 1 rule (~500 ký tự).
- Rule cũ **không bị xoá chữ nào**: `DEPRECATED` + `Thay bởi:` (đã gộp hết), hoặc `ARTICLE` (ghi chú riêng 1 bài — tra khi /optimize đúng bài đó).

## Mâu thuẫn đã xử lý (theo phản hồi mới nhất của bạn)

| Rule cũ | Nói gì | Xử lý |
|---|---|---|
| I037 | thay “xương máu” bằng “sống còn”, “quý báu” | I004 + blacklist cấm “sống còn” → I106 chỉ trỏ blacklist |
| I093 | sapo không chèn DSC, không mời đọc tiếp | Ngược I098 + phản hồi 09/11 → I105: sapo có DSC + câu dẫn |
| I096 ý 3 | “ngoại lệ của quy tắc sapo không nhắc brand” | Quy tắc đó đã bỏ → không còn ngoại lệ |
| I033 | nhãn đậm trong list dùng “.” | I057 (bạn yêu cầu) + lint FMT-bold-label dùng “:” → I116 dùng “:” |
| I023 | “hiện tại là tháng 9/2026” | Bỏ mốc cứng → I109 “thời điểm thật” |
| I099 ý 2 | toplist: kết bài không cần heading | **Đã chốt 09/11:** mọi bài (kể cả toplist) có H2 Kết luận — ghi vào I120, I099 ý 2 đánh dấu đã bỏ |
| (lỗi định dạng) | “Ràng buộc thông tin sản phẩm…” không có Trạng thái → agent chưa từng thấy | Gán I104, gộp vào I111 |

## Rule chuẩn

| ID | Phạm vi | Rule | Gộp từ | Máy kiểm |
|---|---|---|---|---|
| I105 | Global | Sapo: keyword + trả lời thẳng, đoạn 2 có DSC và câu dẫn vào bài | I004, I024, I030, I034, I075, I093, I096, I098 | partial |
| I106 | Global | Văn phong định chế tài chính, từ cấm nằm trong blacklist | I004, I025, I031, I032, I037, I043, I073, I094 | partial |
| I107 | Global | Tiêu đề Sentence case, giọng báo cáo, có H2 chứa keyword | I010, I053, I075, I094, I102 | partial |
| I108 | Global | Câu ngắn phải mang dữ kiện, không nhân vật có tên | I075, I102 | partial |
| I109 | Global | Mốc thời gian chỉ đi với số liệu biến động | I023, I064 | partial |
| I110 | Global | Số liệu: 12 tháng gần nhất, kiểm bài gốc, có nguồn | I009, I048, I086, I089, I103 | partial |
| I111 | Global | Chỉ nhắc sản phẩm DSC thật có (không phái sinh, không quỹ mở) | I010, I036, I037, I099, I104 | partial |
| I112 | Global | Product Bridge nối từ kết luận bài, nói lợi ích bằng tiền | I026, I034, I044, I049, I101 | partial |
| I113 | Global | H2 Kết luận + CTA mở tài khoản, miễn trừ cho bài khuyến nghị | I030, I034, I052, I101 | partial |
| I114 | Global | Banner CTA: headline hành động, 3 dữ kiện thật, đoạn dẫn phía trên | I002, I076, I082, I085 | partial |
| I115 | Global | Trình bày: bảng/list cho so sánh và quy trình, ngắt đoạn theo ý | I029, I038, I039, I040, I049, I050, I060 | partial |
| I116 | Global | Định dạng Markdown để lint và CMS đọc đúng | I028, I033, I035, I041, I042, I043, I046, I047, I057, I058, I060, I063, I066, I067 | partial |
| I117 | Global | Internal link tuyệt đối, khớp sitemap, đặt trong câu | I051, I052, I054, I055, I056, I068 | full |
| I118 | Global | Một URL một intent, chủ đề đã có bài riêng thì chỉ link | I074, I085, I096 | - |
| I119 | Global | Bài how-to: cùng cỡ đối thủ, H3 là bước, web/app theo ảnh | I075, I095, I096 | - |
| I120 | Global | Toplist: N mục là nội dung chính, mỗi mục cùng khung | I014, I072, I097, I099 | partial |
| I121 | Global | Khi /optimize: giữ xương bài gốc, dùng query GSC | I086, I089, I090, I093, I097 | - |
| I122 | Global | Phản hồi “ko có X” nghĩa là đang thiếu X | I098, I100 | - |
| I123 | Global | Bài BCTC/chỉ báo/công cụ có phần nền và phần thực hành | I027, I063 | - |
| I124 | Phân tích cổ phiếu | Bài phân tích mã: số quý mới nhất, tách khoản bất thường | I003, I008, I009, I012, I084, I091, I092 | - |
| I125 | Phân tích kỹ thuật | Bài chỉ báo/mô hình: bảng phân biệt mẫu dễ nhầm, tín hiệu có xác nhận | I005, I016, I021, I022, I079, I082, I087 | - |
| I126 | Vĩ mô | Vĩ mô: số Việt Nam gần nhất, biến số quốc tế gắn tác động trong nước | I001, I007, I019, I044, I048, I069, I088, I089 | - |
| I127 | Giao dịch cơ bản (F0) | F0: thông số giao dịch chuẩn và khái niệm dễ nhầm | I002, I006, I010, I013, I015, I064, I080, I081 | - |
| I128 | Chỉ số tài chính & BCTC | Chỉ số tài chính: ví dụ từ BCTC thật, ngưỡng theo ngành | I020, I059, I061, I065, I070 | - |
| I129 | Phái sinh | Phái sinh: bài kiến thức, Bridge về cổ phiếu cơ sở | I017, I018, I083 | - |
| I130 | Tài chính cá nhân | Tài chính cá nhân: CCQ dùng NAV, ví dụ dòng tiền theo tháng | I062, I071, I072, I078, I103 | - |

## Chuyển sang ARTICLE (ghi chú riêng 1 bài, không load khi viết bài mới)

I001, I002, I003, I005, I006, I007, I008, I009, I012, I013, I014, I015, I016, I017, I018, I019, I020, I021, I022, I044, I048, I059, I061, I062, I064, I065, I069, I070, I071, I072, I078, I079, I080, I081, I082, I083, I084, I086, I087, I088, I089, I090, I091, I092, I093, I094, I099, I103

Phần dùng chung của các rule này đã nằm trong rule chuẩn (cột “Gộp từ”). Phần riêng (bảng GRDP các tỉnh, mã BCM/KBC, Nhơn Trạch 3&4, số quỹ…) chỉ cần khi optimize lại đúng bài đó.

## Chi tiết không đưa vào rule chuẩn (vẫn còn nguyên trong archive)

- I049 ý 2: danh sách tính năng DSC cụ thể (App phân loại vốn hóa, báo cáo phân tích miễn phí) → đã có trong `profile.md`.
- I099 ý 4: lấy dữ kiện app từ App Store listing → ARTICLE (bài app-mua-chung-chi-quy); áp lại khi viết toplist app khác.
- I077: quy ước `**Target:**` trong outline → chuyển vào `brief-template.md`.
- I097 ý 2 phần “liệt kê chỗ lệch gốc vì QA” → không còn cần vì /optimize đã hỏi trước khi thêm H2.

## Việc sau khi bạn duyệt

1. Thay archive thật bằng bản đề xuất, chạy `optimize_instincts.py --check` → ghi `instincts.md` mới.
2. Rút gọn Claude memory `article-structure-preferences` thành 1 dòng trỏ về I105/I107/I108/I112/I113/I118 (rule đã nằm trong instincts, agent Antigravity cũng đọc được).
3. Thêm quy ước Target vào `brief-template.md`; /optimize tra ARTICLE theo slug.
4. Sau vài bài: `optimize_instincts.py --stats` xem rule nào còn tái diễn.
