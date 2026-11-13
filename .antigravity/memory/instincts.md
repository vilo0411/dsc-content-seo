# Instincts

> Đọc trước khi viết; rule ở đây là đầy đủ. Sinh từ `instincts-archive.md` bằng `scripts/optimize_instincts.py` — không sửa tay. `(lint)` = có check máy bắt một phần.

> Theo topic, load thêm 1 file trong `instincts-by-scope/`: `chi-so-tai-chinh-bctc.md` (Chỉ số tài chính & BCTC), `giao-dich-co-ban-f0.md` (Giao dịch cơ bản (F0)), `phai-sinh.md` (Phái sinh), `phan-tich-co-phieu.md` (Phân tích cổ phiếu), `phan-tich-ky-thuat.md` (Phân tích kỹ thuật), `tai-chinh-ca-nhan.md` (Tài chính cá nhân), `vi-mo.md` (Vĩ mô)

## Văn phong & Ngôn từ (Style & Tone)

### [I105] Sapo: keyword + trả lời thẳng, đoạn 2 có DSC và câu dẫn vào bài (lint)
- Sapo 2 đoạn ngay dưới H1. Đoạn 1: chứa nguyên keyword dạng truy vấn, trả lời thẳng (how-to: tóm tắt số bước) kèm 1 mốc có ngày. Đoạn 2: có DSC + 1 câu nêu phạm vi bài + 1 câu mời đọc tiếp gắn lợi ích (“Trong bài viết này, DSC phân tích …”). Không mở bằng bối cảnh vĩ mô hay “Bạn chỉ cần…”.

### [I106] Văn phong định chế tài chính, từ cấm nằm trong blacklist (lint)
- Giọng định chế tài chính: mộc mạc, chính xác, đi thẳng vào số liệu. Không từ cường điệu, văn nói, từ lóng, ngoặc kép bọc từ thường, tiếng Anh thô khi có từ Việt chuẩn (trader → nhà đầu tư chủ động). Từ cấm cụ thể: anti-ai-rules-blacklist.md.

### [I107] Tiêu đề Sentence case, giọng báo cáo, có H2 chứa keyword (lint)
- Mọi tiêu đề (Title ≤ 59 ký tự, H1–H4) viết Sentence case, chỉ viết hoa tên riêng/mã (DSC, HOSE, VN-Index). H2/H3 là cụm danh từ mô tả, giọng báo cáo (“Các loại phí khi đầu tư chứng chỉ quỹ và mức ảnh hưởng đến lợi nhuận”); không văn nói (“ăn bao nhiêu”), không nhãn mở đầu kiểu “Số liệu 2026:”. Ít nhất 1 H2 chứa keyword hoặc câu hỏi keyword. H2/H3 lấy từ PAA giữ nguyên dạng câu hỏi.

### [I108] Câu ngắn phải mang dữ kiện, không nhân vật có tên (lint)
- Câu ≤ 7 từ dùng để ngắt nhịp phải mang dữ kiện (“MAGEF dẫn đầu với 64,31%.”); cấm câu nhận xét rỗng hoặc câu hỏi tu từ chuyển ý (“Kết quả này đáng chú ý.”, “Vậy nhà đầu tư nhận được gì?”) — xử lý hết SLOP-filler. Không dùng nhân vật có tên, tuổi, nghề (chị Lan, Minh 27 tuổi) ở mọi loại bài; viết “Ví dụ, với 500 triệu …”.

### [I110] Số liệu: 12 tháng gần nhất, kiểm bài gốc, có nguồn (lint)
- Ưu tiên số trong 12 tháng gần nhất (cuối 2026 thì số 2025 là cũ), mỗi số có nguồn + ngày. Số lấy qua WebSearch/AI Overview phải mở bài gốc kiểm năm, mốc, nguồn. Chỉ số/mã chạy lại market_facts.py, kể cả bài optimize đã có số. Quy định có số tiền tra văn bản hiện hành. Không lập bảng so sánh đối thủ khi không có nguồn công khai.

### [I112] Product Bridge nối từ kết luận bài, nói lợi ích bằng tiền (lint)
- 1) Câu mở H2 DSC nêu lý do cụ thể người đọc cần sản phẩm (vd ETF niêm yết → cần tài khoản CK), không tham chiếu ngược “ví dụ ở bước X”, nói rõ điều DSC KHÔNG làm. 2) Trả lời vì sao chọn DSC: bảng so DSC với kênh thay thế (CTCK khác, công ty quản lý quỹ/đại lý) bằng tiền trên ví dụ của bài; DSC không rẻ nhất thì nói thẳng, nhấn Môi giới 1:1 hỗ trợ tư vấn đầu tư. 3) Không list tính năng rời.

### [I114] Banner CTA: headline hành động, 3 dữ kiện thật, đoạn dẫn phía trên (lint)
- Headline banner nêu hành động/lợi ích gắn chủ đề, không câu hỏi mồi; dòng phụ 3 dữ kiện thật (eKYC 3 phút, miễn phí mở/duy trì, phí từ 0,1%, 963369). Banner giữa ở ~35–40% thân bài sau phần sản phẩm DSC; banner cuối khác ý banner giữa. Ngay trên banner là 1 đoạn văn dẫn (≥ 10 từ), không phải list. Màu Dark Navy #0D1B2A + nút #2BE841.

### [I116] Định dạng Markdown để lint và CMS đọc đúng (lint)
- Heading `##`/`###` (không giữ `### H2:` của outline). 1 dòng trống trước/sau list, bảng và giữa câu hỏi–đáp FAQ. Dấu ?/. đặt ngoài `**…**`; câu dẫn vào list liền kề kết thúc bằng “.”; nhãn đậm đầu bullet dùng “:”. Số thập phân dấu phẩy. Không LaTeX (công thức in đậm), callout `> [!NOTE]`, `---`, ký tự `|` trong ô bảng, ngoặc kép trong YAML.

### [I118] Một URL một intent, chủ đề đã có bài riêng thì chỉ link
- Trước khi viết, find_links.py xem bài DSC cùng cụm. Bài lựa chọn chỉ nhắc quy trình 2–3 câu + link sang bài hướng dẫn (và ngược lại); bài how-to mua mã không chứa phân tích BCTC. Chủ đề đã có bài riêng (rủi ro, phí…) → 1 câu + link, không dựng H2 riêng. Anchor dạng hướng dẫn chỉ trỏ bài hướng dẫn, dạng lựa chọn chỉ trỏ bài lựa chọn.

### [I119] Bài how-to: cùng cỡ đối thủ, H3 là bước, web/app theo ảnh
- Giữ số từ, số H2 cùng cỡ 2 đối thủ top; cắt phần lệch intent. H3 dưới H2 hướng dẫn là bước đánh số. Bước đã minh họa bằng sản phẩm DSC thì không thêm H2 “tại DSC”; H1 có DSC. Web hay app xác định từ chính ảnh chụp; khác quy trình thì tách H2 cho app.

## Cấu trúc & Định dạng (Structure & Formatting)

### [I109] Mốc thời gian chỉ đi với số liệu biến động (lint)
- Chỉ gắn mốc thời gian (thời điểm thật) vào câu có số liệu biến động: phí, lãi suất, chỉ số. Không lặp “Tính đến tháng M/Y,” đầu câu hay đầu H2; phần lý thuyết, quy định chung không cần mốc.

### [I113] H2 Kết luận + CTA mở tài khoản, miễn trừ cho bài khuyến nghị (lint)
- Bài kết thúc bằng H2 “Kết luận”: 1 nhận định + checklist hành động 3 mục + CTA có link https://www.dsc.com.vn/mo-tai-khoan; không mở bằng “Tóm lại”. Bài khuyến nghị/đánh giá mã thêm câu miễn trừ trách nhiệm.

### [I115] Trình bày: bảng/list cho so sánh và quy trình, ngắt đoạn theo ý (lint)
- Số liệu so sánh, phí, quy trình → bảng hoặc list; khái niệm dễ nhầm → bảng đối sánh. Phần ngắn 2–3 câu gộp thành bullet có nhãn đậm, không tách H3. Ngắt đoạn theo ý (≤ 3 câu), không bẻ câu máy móc; 2 list liền nhau phải có câu nối. Lưu đồ, code → bảng hoặc list đánh số. Bài glossary chia nhóm H2 theo chủ đề.

### [I120] Toplist: N mục là nội dung chính, mỗi mục cùng khung (lint)
- N mục là nội dung chính, tối đa 3 H2 hỗ trợ (bảng tóm tắt, cách chọn, FAQ) + H2 Kết luận như mọi bài (I113, chốt 09/11). Mỗi H3 ~200 từ: Giới thiệu → Ưu → Nhược → Hợp với ai, mỗi ý 1 dữ kiện đã xác minh; mục DSC cũng có nhược điểm thật. Bài khuyến nghị mã: chọn theo đồng thuận báo cáo CTCK có ngày, ghi nguồn cạnh giá mục tiêu; DSC không tự đặt giá mục tiêu.

### [I121] Khi /optimize: giữ xương bài gốc, dùng query GSC
- Giữ thứ tự H2 và mẫu block bản gốc, chỉ thay nội dung; thêm H2 mới phải hỏi. Query GSC của URL: biến thể nhiều click vào sapo/H2, câu hỏi nhiều impression thành H2. CTR thấp dù hiển thị cao → Title có con số/giải pháp, 50 ký tự đầu Meta trả lời thẳng.

### [I045] Bỏ qua tạo ảnh fallback khối vuông khi gặp lỗi Quota
- Khi công cụ sinh ảnh AI (`generate_image`) bị báo lỗi Quota (429 RESOURCE_EXHAUSTED), tuyệt đối không sinh các hình ảnh fallback khối vuông 3D bằng script Python PIL. Hãy bỏ qua việc tạo ảnh mới, bảo toàn 100% hình ảnh gốc của bài viết và trình bày bài viết chuẩn văn bản/bảng biểu trực quan.

## Sản phẩm & Thương hiệu (Products & Brand Context)

### [I111] Chỉ nhắc sản phẩm DSC thật có (không phái sinh, không quỹ mở) (lint)
- Chỉ nhắc tính năng DSC có trong profile.md / service-operations.md, không tự suy (đặt lệnh 24/7…). DSC KHÔNG có phái sinh và KHÔNG phân phối quỹ mở (chỉ ETF niêm yết): bài về các sản phẩm này không kêu gọi mở tài khoản cho chúng, hướng về cổ phiếu cơ sở/ETF + Môi giới 1:1. eKYC luôn ghi “3 phút”.

### [I122] Phản hồi “ko có X” nghĩa là đang thiếu X
- Phản hồi ngắn “ko có X”, “chưa có X” = bài đang THIẾU X, cần thêm. Chỉ hiểu là bỏ khi user viết rõ “bỏ”, “xóa”, “đừng”. Cách hiểu đi ngược rule hiện có hoặc làm mất nội dung đang có → hỏi lại 1 câu trước khi sửa.

### [I123] Bài BCTC/chỉ báo/công cụ có phần nền và phần thực hành
- Ngoài phần chiến lược, có phần nền (cách lập, cấu tạo, công thức) để khớp truy vấn học thuật. Bài cho nhà đầu tư chủ động (P3) thêm hướng dẫn thực hành từng bước và sai lầm thường gặp.

## ✅ Đã tự động hoá (vẫn phải tuân thủ khi viết)

| Bản năng | Check |
|---|---|
| [I117] Internal link tuyệt đối, khớp sitemap, đặt trong câu | `qa_lint:LINK-sitemap, qa_lint:LINK-relative, qa_lint:LINK-local, qa_lint:LINK-anchor, qa_lint:LINK-xemthem, qa_lint:LINK-cta` |
