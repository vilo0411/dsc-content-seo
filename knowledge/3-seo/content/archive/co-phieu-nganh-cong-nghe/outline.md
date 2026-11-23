---
# Khối máy đọc: qa_lint --outline / qa_gate đối chiếu bản Optimize với các trường này. Giữ đúng tên trường.
Target_Keyword: cổ phiếu ngành công nghệ
Thesis: "Sau 44 phiên điều chỉnh từ 21/09 đến 19/11/2026, cả 5 mã công nghệ của bài đều giảm 13–31% và FPT thấp nhất trong giai đoạn; nhóm này nay phân hóa theo sàn niêm yết, thanh khoản và mô hình doanh thu, không còn là câu chuyện vùng đỉnh lịch sử như đầu năm 2026."
Entities: [FPT, CMG, VGI, FOX, ELC, HOSE, HNX, UPCoM, biên độ dao động, thanh khoản, AI, Cloud, data center, 5G, chuyển đổi số, P/E, cổ tức, viễn thông]
Entities_Skipped:
  - "máy tính · di động · quảng cáo · bộ lọc · hồ sơ · trở thành · giá cao — nhiễu từ trang screener và trang cookie trong SERP, không thuộc chủ đề"
  - "mục tiêu giá · dự báo — DSC không tự đặt giá mục tiêu (I120); chỉ thêm nếu có báo cáo CTCK có ngày và user cung cấp nguồn"
Information_Gain:
  - claim: "Bảng biến động giá 5 mã công nghệ trong 44 phiên 21/09–19/11/2026: giá cao nhất kèm ngày, giá đóng cửa 19/11, % thay đổi, % cách đỉnh — SERP chỉ có tin tức và bộ lọc, không có bảng so sánh nhóm"
    h2: "Biến động giá 5 mã cổ phiếu công nghệ từ 21/09 đến 19/11/2026"
    type: comparison
    proof: "-30,5%"
  - claim: "Hai mã UPCoM (VGI, FOX) có biên độ 15%/phiên nhưng thanh khoản bình quân 20 phiên thấp hơn FPT hàng chục đến hàng trăm lần (FOX 52.114 cp so với FPT 10.113.045 cp, gấp khoảng 194 lần) — đối thủ không nói tới rủi ro thanh khoản theo sàn"
    h2: "Biến động giá 5 mã cổ phiếu công nghệ từ 21/09 đến 19/11/2026"
    type: calc
    proof: "52.114"
  - claim: "Vốn cần cho 100 cổ phiếu (1 lô) mỗi mã theo giá đóng cửa 19/11/2026, từ 963.000 đồng (ELC) đến 6.790.000 đồng (VGI), để nhà đầu tư vốn nhỏ biết điểm vào"
    h2: "Biến động giá 5 mã cổ phiếu công nghệ từ 21/09 đến 19/11/2026"
    type: calc
    proof: "4.615.000"
  - claim: "Bảng danh mục theo sàn có thêm cột biên độ dao động HOSE 7% / HNX 10% / UPCoM 15% gắn với từng mã"
    h2: "Danh mục mã cổ phiếu ngành công nghệ niêm yết"
    type: regulation
    proof: "UPCoM 15%"
Featured_Snippet: Table
PAA_Questions:
  - q: "[Không có PAA trong SERP — dùng truy vấn GSC] Cổ phiếu công nghệ AI Việt Nam gồm những mã nào?"
    placement: faq
  - q: "[Không có PAA trong SERP — dùng truy vấn GSC] Cổ phiếu công nghệ có nên mua khi giá giảm sâu?"
    placement: faq
  - q: "[Không có PAA trong SERP — dùng truy vấn GSC] Cổ phiếu ngành công nghệ niêm yết trên sàn nào?"
    placement: faq
---

# 📋 BÁO CÁO TỐI ƯU SEO (SEO Optimization Proposal) — `co-phieu-nganh-cong-nghe`

URL: https://www.dsc.com.vn/kien-thuc/co-phieu-nganh-cong-nghe · Soạn 19/11/2026 · Gate 1 (chưa rewrite)

## 0. Content Strategy Header ⚠️ ĐỌC TRƯỚC KHI XEM BẤT KỲ MỤC NÀO

| Thông số | Giá trị |
| :--- | :--- |
| **Target Keyword** | `cổ phiếu ngành công nghệ` (registry). Query thật mang click: `cổ phiếu công nghệ` (36 clicks, 477 impr, vị trí 1,5); giữ cả hai trong sapo/H2 |
| **Secondary Keywords** | `cổ phiếu công nghệ`, `cổ phiếu công nghệ việt nam`, `mã cổ phiếu công nghệ ai việt nam`, `các mã cổ phiếu công nghệ`, `cổ phiếu ai` |
| **LSI / Entities** | FPT, CMG, VGI, FOX, ELC, HOSE/HNX/UPCoM, biên độ, thanh khoản, AI, Cloud, data center, chuyển đổi số, cổ tức |
| **Search Intent** | Informational–Commercial: nhà đầu tư tìm danh sách mã công nghệ niêm yết để cân nhắc mua, giai đoạn so sánh lựa chọn. Google AI Overview đang trích bài DSC cho đoạn "định giá hợp lý hơn, động lực AI, Cloud, 5G, chuyển đổi số" |
| **Persona** | P2 — F0 Nhà đầu tư mới — người hỏi "mã nào" theo ngành, vốn nhỏ, cần số tiền cụ thể cho 1 lô và cảnh báo rủi ro; không dùng thuật ngữ nặng |
| **Tone** | Chuyên gia đồng hành, giọng báo cáo, có lập trường (không hô "thời điểm lý tưởng" khi giá đang giảm) |
| **DSC Product Bridge** | eKYC 3 phút + Môi giới 1:1 — nối từ vấn đề bài vừa nêu: mã công nghệ giảm 13–31% nên cần người hỏi trước lệnh đầu tiên. Không nhắc DSC Invest (ngưỡng 3 tỷ) |
| **Featured Snippet** | Table — bảng danh mục theo sàn (đã có) và bảng biến động 5 mã (thêm mới) |
| **Word Count hiện tại** | ~960 từ |
| **Word Count mục tiêu** | ~1.500 từ (đối thủ đọc được: aas.com.vn ~1.930, nguoiquansat ~1.480 nội dung; bài DSC đang ngắn nhưng đứng top 1–2 nên chỉ nở thêm ~550 từ) |

**Bài gốc đang phục vụ đúng intent/persona không?**
- [ ] ✅ Đúng
- [x] ⚠️ Lệch một phần: intent đúng (danh sách mã công nghệ) nhưng (1) nội dung đã lỗi thời so với thị trường: bài viết VGI "đang ở vùng đỉnh lịch sử", FOX "vượt đỉnh lịch sử", kết luận "thời điểm lý tưởng để tái cơ cấu"; thực tế từ 21/09 đến 19/11/2026 FPT -30,5%, CMG -27,5%, ELC -26,5%, VGI -14,9%, FOX -13,1% (`market_facts.py --brief`); (2) mọi số liệu doanh nghiệp (P/E 15,2x, nhà máy AI 200 triệu USD, 1.000 GPU, biên lợi nhuận VGI 55%, lãi ròng ELC gấp đôi) không có nguồn và ngày; (3) không có bước chuyển sang hành động phù hợp P2.

### ⚠️ Rủi ro cần user biết trước khi duyệt
- Vị trí trung bình trang 3,7 (query chính 1,5): áp giới hạn tái cấu trúc. Proposal **không đổi H1, không đổi thứ tự, không gộp/xóa H2**. Chỉ có 2 H2 `[THÊM MỚI]` (Biến động giá + Câu hỏi thường gặp); cả hai nằm giữa các H2 hiện có, trước Kết luận. Cần user đồng ý (I121: thêm H2 mới phải hỏi).
- Hai mục sai thực tế cần sửa bắt buộc (không phải tùy chọn): các câu "đỉnh lịch sử" (VGI, FOX) và "thời điểm lý tưởng". Nếu giữ nguyên, bài mâu thuẫn dữ liệu giá công khai và dễ bị coi là gây hiểu lầm.
- Số doanh nghiệp (P/E, GPU, biên lợi nhuận…) chưa kiểm được: bản rewrite chỉ giữ số nào tìm được nguồn trong `source-whitelist.md`; không tìm được thì bỏ câu hoặc ghi `[CẦN XÁC NHẬN]`.

---

## 1. Đánh giá Tổng quan (Overall Health)

- **Word Count Gap:** ~960 từ. Đối thủ đọc được: aas.com.vn ~1.934, nguoiquansat.vn ~1.968 (gồm cả phần điều hướng), traderins ~7.881 (cổ phiếu Mỹ, khác intent). Cần thêm ~550 từ.
- **Điểm on-page:** Cần cải thiện. H1 có keyword; sapo không theo I105 (không có đoạn 2 "Trong bài viết này, Chứng khoán DSC…", chưa có số có ngày); chưa có FAQ; chưa có miễn trừ trách nhiệm đúng chỗ ở Kết luận; link "Xem thêm" đứng riêng; anchor CTA "đăng ký mở tài khoản chứng khoán" thiếu thương hiệu (`LINK-cta-anchor`).
- **Vi phạm Anti-AI:** Có. Ngoặc kép nhấn mạnh: "ông lớn", "cỗ máy in tiền", "chất xám", "đu đỉnh" (`CL2-quotes`, 4 chỗ); từ cường điệu: "tăng phi mã", "bùng nổ", "hùng hậu", "cực kỳ", "ấn tượng nhất"; 8 câu > 30 từ; 3/4 H2 không trả lời ngay ở câu đầu (`GEO-h2-answer`).
- **Baseline đo ngày 19/11/2026 (bản optimize không được tệ hơn):** `qa_lint` 84/100, FAIL, 0 CRITICAL, 6 MAJOR, 30 MINOR · `slop_check` 87/100 trong lần chạy riêng, MAJOR `SLOP-h2-open` (60% H2 mở bằng câu "X là…", tối đa 50%), MINOR `SLOP-table-thin` · `template_sim` 0,27 trong lần chạy riêng · `market_facts --verify` sạch (bài không có mốc chỉ số có ngày, nên không bắt được lỗi giá; lỗi thật nằm ở các câu "đỉnh lịch sử"). Điểm 77 của đợt quét toàn kho khác điểm 87 chạy riêng do ngưỡng relative và so sánh với `co-phieu-nganh-nhua`; sau rewrite cần chạy lại cả hai chế độ.
- **GSC (90 ngày 19/08–16/11/2026, nguồn SEO Dashboard MCP):** trang 646 clicks, 13.133 impressions, CTR 4,92%, vị trí 3,72; kỳ trước 828 clicks (-22,0%), impressions +0,3%, vị trí 3,82. Theo tháng CTR giảm 7,01% (07) → 4,80% (10) → 3,26% (11 đến ngày 16): impressions ổn định, CTR giảm dần, khớp với việc AI Overview đang chiếm câu trả lời. Phần lớn click là truy vấn ẩn danh; chỉ 84 clicks quy được về query (xem bảng dưới).

📊 GSC Performance Context (2026-08-19 → 2026-11-16, nguồn: SEO Dashboard MCP, phần quy được về query):
- Query: 84 clicks · 1.582 impressions · CTR 5,31% · vị trí 3,4 (kỳ trước 164 clicks, CTR 9,81%)
- Flag rewrite Title theo CTR trang: CTR tháng 11 = 3,26%, sát ngưỡng 3% → xem Meta bên dưới, chưa đổi Title/H1 vì vị trí ≤ 5.

| Query | Clicks | Impr | Vị trí | CTR | Phục vụ trong bài hiện tại? |
| :--- | ---: | ---: | ---: | ---: | :--- |
| cổ phiếu công nghệ | 36 (kỳ trước 37) | 477 | 1,5 | 7,55% | Có ở H2 "Những lưu ý…" và Kết luận; chưa có trong sapo dạng nguyên cụm |
| mã cổ phiếu công nghệ ai việt nam | 15 (19) | 71 | 1,3 | 21,13% | Chỉ ngầm qua FPT/CMG; chưa có câu trả lời trực tiếp → FAQ + câu trong H3 FPT/CMG |
| cổ phiếu công nghệ việt nam | 9 (18) | 88 | 1,4 | 10,23% | Chưa có "Việt Nam" trong H2; thêm vào câu mở H2 Top 5 |
| cổ phiếu ngành công nghệ | 7 (13) | 25 | 1,5 | 28,00% | H1, H2 |
| cổ phiếu ai | 3 | 189 | 4,2 | 1,59% | Chưa có; FAQ "cổ phiếu công nghệ AI" |
| cổ phiếu blue chip việt nam 2026 | 2 | 132 | 4,2 | 1,52% | Lệch intent (blue chip), không chạy theo |
| cổ phiếu công ty sản xuất chip việt nam | 3 | 32 | 4,2 | 9,38% | Bài không có mã sản xuất chip niêm yết trong danh sách; không có dữ liệu xác minh → ghi vào FAQ chỉ khi có nguồn, hiện **bỏ qua** |

- **Cannibalization:** `cổ phiếu công nghệ`: URL này 66 clicks/821 impr (vị trí 1,9). `top-5-co-phieu-dang-dau-tu` (hub cha) có 93 impr, vị trí 1,86, 0 clicks cho cùng query; các URL còn lại < 10 impr. Mức thấp, không cần xử lý; chỉ lưu ý khi viết lại hub cha không dùng anchor/heading "cổ phiếu công nghệ" cạnh tranh. Query "cổ phiếu ngành công nghệ": 1 URL duy nhất (DSC này).

### Đề xuất cập nhật SEO Elements
- **Title hiện tại:** Top 5 mã cổ phiếu ngành công nghệ tiềm năng 2026 — 48 ký tự
- **Title đề xuất:** Giữ nguyên (H1 = Title, vị trí ≤ 5 nên không đổi). Ghi chú: nếu user muốn đổi sau khi đo lại, hướng phù hợp là bỏ "tiềm năng" vì không còn khớp dữ liệu giá; cần user đồng ý rủi ro.
- **Meta Description hiện tại:** "Đâu là những mã cổ phiếu ngành công nghệ tiềm năng 2026 để giải ngân trong giai đoạn này? Cùng DSC phân tích chi tiết trong bài viết hôm nay" — 140 ký tự, câu hỏi mở, không có dữ kiện.
- **Meta Description đề xuất:** "Cổ phiếu ngành công nghệ giảm 13–31% từ 21/09 đến 19/11/2026. Xem 5 mã FPT, CMG, VGI, ELC, FOX: giá, biên độ, thanh khoản. Mở tài khoản DSC để theo dõi." — 152 ký tự, có keyword, có số có ngày trong 50 ký tự đầu (I121), có CTA.

---

## 2. Phân tích Đối thủ SERP (Competitor Analysis)

> ⚠️ **SERP sanity check.** `serp_research.py` cho keyword "cổ phiếu ngành công nghệ" trả `SERP_CHECK: không có PAA lẫn related searches`; 9 organic nhưng hỗn tạp: bài báo 2024, trang screener Ấn Độ (investing.com), trang giá hodl/tradingview/cotuc, bài tổng hợp SHS 2018. Không có DSC (bị loại khỏi so sánh) nên không đối chiếu được vị trí qua list. Chạy thêm keyword "cổ phiếu công nghệ" (query mang click, `--force` vì guard registry không nhận chuỗi có dấu từ dòng lệnh) cho SERP khác nhưng cùng kiểu nhiễu (pexels, investing.com, traderins cổ phiếu Mỹ). Cả hai lần đều ghi nhận AI Overview trích `www.dsc.com.vn` và `aas.com.vn`. Kết luận: SERP **không sai** (GSC cho thấy DSC vị trí 1,5 trên cả hai query, khớp việc không có đối thủ bài chuyên sâu), nhưng **rất ít đối thủ đọc được**: chỉ `aas.com.vn/cac-co-phieu-cong-nghe/` là bài cùng dạng, lấy từ nguồn AIO. Chưa refetch `--no-cache` vì dữ liệu đối chiếu GSC đã đủ.

### 2.1 Bảng so sánh tổng quan

| # | URL | Search Intent | Word Count | Điểm nổi bật |
| :--- | :--- | :--- | :--- | :--- |
| 1 | aas.com.vn/cac-co-phieu-cong-nghe/ | Informational–Commercial | ~1.930 | Bài cùng dạng; có tiêu chí chọn, cơ hội/rủi ro, FAQ 3 câu; được AI Overview trích |
| 2 | nguoiquansat.vn (xu-huong-ai-bung-no-…) | Tin khuyến nghị 1 mã | ~1.480 | Tin có ngày 30/12/2024: dự báo lãi sau thuế 6.900 tỷ, khuyến nghị MUA, kỳ vọng tăng 16% — đã cũ |
| 3 | tinnhanhchungkhoan.vn (suc-ben-co-phieu-cong-nghe) | Tin phân tích | ~1.870 | Bài 13/08/2024 về cổ phiếu công nghệ toàn cầu; trang crawl lẫn mục tin khác |
| 4 | nmquan.vn/data/nganh/phan-mem-va-dich-vu-cong-nghe | Dữ liệu | ~1.070 | Danh sách 4 mã HOSE ngành Phần mềm và dịch vụ công nghệ (phân ngành HOSE, chuẩn GICS), giá cập nhật mỗi phiên, vốn hóa |
| 5 | hodl.vn/co-phieu/nganh/cong-nghe-va-thong-tin | Dữ liệu | ~30 (bảng) | 29 mã ngành Công nghệ và thông tin trên HOSE, HNX, UPCoM với giá, RSI14, xu hướng |

### 2.2 Cấu trúc & khoảng trống từng đối thủ (mỗi đối thủ một block)

**Đối thủ 1: aas.com.vn — https://aas.com.vn/cac-co-phieu-cong-nghe/**
- **Intent chính:** nhà đầu tư tìm danh sách cổ phiếu công nghệ Việt Nam năm 2026 và cách chọn.
- **Mục họ có mà bài mình chưa có:** H2 "Tiêu chí lựa chọn cổ phiếu công nghệ" (4 H3: tăng trưởng doanh thu–lợi nhuận, R&D, thị trường–khách hàng, định giá); H2 "Cơ hội và rủi ro" (rủi ro ~116 từ); H2 "Câu hỏi thường gặp" (cổ phiếu công nghệ là gì, vốn hóa lớn, có nên dồn toàn bộ danh mục); H3 SGT.
- **Yếu tố đặc biệt:** FAQ, giọng giải thích chung; không có giá, không có số theo ngày.
- **Content Gap so với DSC:** DSC có bức tranh vĩ mô + 5 mã + bảng theo sàn nhưng thiếu FAQ và tiêu chí rõ. Ngược lại aas thiếu mọi dữ liệu giá. Hướng: giữ khung DSC, thêm FAQ và nâng bullet "Lưu ý" thành tiêu chí có số.

**Đối thủ 2: nguoiquansat.vn — https://nguoiquansat.vn/xu-huong-ai-bung-no-mot-co-phieu-cong-nghe-duoc-khuyen-nghi-mua-ky-vong-tang-16-188905.html**
- **Intent chính:** tin khuyến nghị mua 1 cổ phiếu công nghệ (30/12/2024).
- **Mục họ có mà bài mình chưa có:** dẫn nguồn khuyến nghị CTCK kèm giá mục tiêu và mức tăng kỳ vọng.
- **Yếu tố đặc biệt:** list, trích dẫn báo cáo; tin cũ hơn 22 tháng.
- **Content Gap:** DSC không tự đặt giá mục tiêu (I120); bài này không cần theo hướng khuyến nghị. Chỉ ghi nhận: nhà đầu tư có nhu cầu "khuyến nghị CTCK" nhưng nguồn đã cũ, nên DSC có cơ hội cập nhật nếu user cung cấp báo cáo có ngày.

**Đối thủ 3: tinnhanhchungkhoan.vn — https://www.tinnhanhchungkhoan.vn/suc-ben-co-phieu-cong-nghe-post351258.html**
- **Intent chính:** phân tích cổ phiếu công nghệ toàn cầu nửa đầu 2024.
- **Mục họ có mà bài mình chưa có:** "Ngành công nghệ thông tin – cơ hội từ nhu cầu chuyển đổi số" (mục liên quan trực tiếp tới nhóm VN).
- **Yếu tố đặc biệt:** bài báo có chữ ký ngày; crawl nhiễu cả mục tin hôm nay (nên không dùng làm cấu trúc).
- **Content Gap:** gần như không có; bài cũ, thiên về thế giới.

**Đối thủ 4: nmquan.vn — https://nmquan.vn/data/nganh/phan-mem-va-dich-vu-cong-nghe**
- **Intent chính:** tra giá, vốn hóa nhóm ngành theo phân ngành HOSE.
- **Mục họ có mà bài mình chưa có:** bảng theo phân ngành chuẩn (4 mã Phần mềm và dịch vụ công nghệ) cập nhật mỗi phiên.
- **Yếu tố đặc biệt:** bảng dữ liệu sống; không có phân tích.
- **Content Gap:** DSC không cạnh tranh được về dữ liệu sống nhưng có thể thêm ngữ cảnh mà trang dữ liệu không có: biên độ theo sàn, vốn cho 1 lô, rủi ro thanh khoản.

**Đối thủ 5: hodl.vn — https://hodl.vn/co-phieu/nganh/cong-nghe-va-thong-tin**
- **Intent chính:** danh sách 29 mã Công nghệ và thông tin trên 3 sàn với giá đóng cửa, ±%, khối lượng, RSI14, xu hướng.
- **Mục họ có mà bài mình chưa có:** danh sách đầy đủ 29 mã (bài DSC bảng 18 mã), cột xu hướng, RSI.
- **Yếu tố đặc biệt:** bộ lọc theo sàn; không có bài phân tích dài.
- **Content Gap:** bảng DSC thiếu số mã đối chiếu và thiếu cột dữ liệu. Chưa đủ nguồn xác minh để nâng lên 29 mã; chỉ cập nhật bảng hiện có khi `market_facts` hoặc nguồn whitelist xác nhận mã còn niêm yết đúng sàn (`[CẦN XÁC NHẬN]`).

### 2.3 Intent Gap — Bài hiện tại đang bỏ sót gì?
- **Intent SERP:** tra danh sách mã công nghệ niêm yết và giá, kèm vài bài phân tích/tin; AI Overview trả lời bằng câu "thị trường điều chỉnh định giá hợp lý hơn, động lực từ AI, Cloud, 5G, chuyển đổi số" lấy gần nguyên từ bài DSC.
- **Intent bài hiện tại:** khớp nhưng ở dạng "top 5 tiềm năng" có tính khuyến nghị, dữ kiện lỗi thời.
- **Gap cần xử lý:** (1) dữ liệu giá có ngày thay cho "đỉnh lịch sử"; (2) FAQ trả lời truy vấn AI/Việt Nam; (3) tiêu chí chọn và rủi ro theo sàn/thanh khoản; (4) Kết luận có checklist + miễn trừ. **Giữ nguyên câu "định giá hợp lý hơn… AI, Cloud, 5G" trong sapo để không mất vị trí nguồn của AI Overview**, chỉ thêm số có ngày bên cạnh.

---

## 3. Kết quả 8 Sweeps Audit

| Bước Quét | Đánh giá | Vấn đề chính | Ghi chú cải thiện |
| :--- | :---: | :--- | :--- |
| **Clarity** | 6/10 | 8 câu > 30 từ, bullet gộp nhiều ý (ELC 3 câu/1 bullet) | Tách câu ≤ 30 từ; mỗi bullet 1 ý; nhãn đậm dùng ":" ngoài bold |
| **Voice** | 5/10 | Giọng quảng bá ("ông lớn", "cỗ máy in tiền", "gương mặt tiêu biểu"), ngoặc kép nhấn mạnh | Giọng báo cáo, gọi tên mã và số; bỏ ngoặc kép |
| **So What** | 5/10 | Điểm nhấn là tính năng doanh nghiệp, không nói lợi ích/rủi ro cho nhà đầu tư | Mỗi mã thêm dòng "Hợp với ai / Cần lưu ý" (I120), có 1 dữ kiện |
| **Prove It** | 3/10 | P/E 15,2x vs 23,2x, GPU 1.000, biên lợi nhuận 55%, nhà máy AI 200 triệu USD không nguồn, không ngày; "đỉnh lịch sử" mâu thuẫn giá 19/11/2026 | Số giá lấy `market_facts.py`; số doanh nghiệp chỉ giữ khi có nguồn whitelist, nếu không bỏ hoặc `[CẦN XÁC NHẬN]` |
| **Specificity** | 4/10 | "ổn định", "mạnh mẽ", "rất lớn" | Thay bằng số: giá, % từ đỉnh, vốn cho 1 lô, KLGD bình quân |
| **Emotion** | 4/10 | Không chạm nỗi lo hiện tại (giá giảm 13–31%) | Mở đoạn Tổng quan bằng tình huống giá giảm có số |
| **Zero Risk** | 3/10 | Kết luận "thời điểm lý tưởng", miễn trừ nhỏ ở cuối | Nhận định thận trọng, checklist 3 mục, miễn trừ đứng cạnh nhận định |
| **GEO/AEO** | 5/10 | 3/4 H2 không trả lời ngay ở câu đầu; H2 mở bằng "Dưới đây là…", "Năm 2025 là…"; không có FAQ; 0 nguồn ngoài | Câu đầu mỗi H2 gọi tên chủ đề + 1 số có ngày; thêm FAQ; 1–2 link nguồn whitelist |

---

## 4. Phân tích Chi tiết (Heading-by-Heading Analysis)

> Giới hạn vị trí ≤ 5: toàn bộ H1/H2 hiện có giữ nguyên chữ, thứ tự, số lượng. H3 cổ phiếu giữ tên.

### GIỮ NGUYÊN

| Heading | Lý do giữ |
| :--- | :--- |
| H1: Top 5 mã cổ phiếu ngành công nghệ tiềm năng 2026 | Vị trí ≤ 5, không đổi H1 (ghi chú "tiềm năng" ở Title phía trên). |
| Ảnh 1 và ảnh 2 (2 `<img>`) | Bảo toàn 100% cú pháp và vị trí; chỉ cập nhật alt (xem 7.1). |
| Block "Xem thêm" 2 link | Giữ cả 2 link, chuyển vào câu văn trong H2 Lưu ý (không mất link); bỏ dòng ">> Xem thêm:" rời. |

### XÓA BỎ
Không xóa H2/H3 nào. Chỉ xóa câu (không xóa heading): các câu "đỉnh lịch sử" (VGI, FOX), "thời điểm lý tưởng để tái cơ cấu danh mục", "cực kỳ ổn định" và 4 cụm trong ngoặc kép nhấn mạnh.

### CẬP NHẬT

🔄 **Sapo (dưới H1)** — `[CẬP NHẬT]`
- **Vấn đề:** 1 đoạn, 46 từ/câu, không có số có ngày, không có đoạn 2 theo I105; mở bằng bối cảnh vĩ mô; "Hãy cùng DSC phân tích chi tiết" là câu rỗng.
- **Hướng xử lý:** Đoạn 1: nguyên cụm `cổ phiếu ngành công nghệ`/`cổ phiếu công nghệ Việt Nam` + trả lời thẳng: gồm FPT, CMG, ELC (HOSE), VGI, FOX (UPCoM); cả 5 mã giảm 13–31% trong 44 phiên 21/09–19/11/2026. Giữ nguyên cụm "định giá hợp lý hơn… AI, Cloud, 5G, chuyển đổi số" (nguồn AI Overview). Đoạn 2: "Trong bài viết này, Chứng khoán DSC phân tích 5 mã theo biến động giá, biên độ sàn và thanh khoản, kèm bảng danh mục theo sàn." + câu cuối là con số trong bài (vd 100 cổ phiếu FPT cần 4.615.000 đồng tại giá 19/11/2026). Giữ link `top-5-co-phieu-dang-dau-tu` ở cụm "mã cổ phiếu tiềm năng".
- **Entities:** `FPT`, `CMG`, `ELC`, `VGI`, `FOX`, `HOSE`, `UPCoM`
- **Word count target:** ~90 từ

🔄 **H2: Tổng quan bức tranh thị trường ngành công nghệ**
- **Vấn đề:** mở bằng "Năm 2025 là một khoảng lặng…" (câu nhận định không có số, kiểu "X là"); P/E 15,2x vs 23,2x và "đỉnh lịch sử" không nguồn; "tăng phi mã", "bùng nổ".
- **Hướng xử lý:** câu đầu gọi tên "Cổ phiếu ngành công nghệ Việt Nam" + số có ngày (5 mã giảm 13–31% từ 21/09 đến 19/11/2026; FPT -30,5% còn 46.150 đồng). Giữ 3 bullet (định giá / hạ tầng viễn thông / chuyển đổi số) nhưng: bullet 1 bỏ P/E không nguồn, thay bằng giá và % từ đỉnh (số `market_facts`), P/E chỉ giữ khi có nguồn; bullet 2 bỏ "bùng nổ", ghi 5G và data center kèm VGI/FOX/ELC; bullet 3 "Chuyển đổi số quốc gia 2025–2030": cần nguồn văn bản chính phủ (`[CẦN XÁC NHẬN]`). Nhịp: thêm câu ngắn mang dữ kiện ("FPT đóng cửa 46.150 đồng." ).
- **Entities cần có:** `FPT`, `VGI`, `FOX`, `ELC`, `AI`, `5G`, `chuyển đổi số`
- **Word count target:** ~170 từ

🔄 **H2: Top 5 mã cổ phiếu ngành công nghệ tiềm năng nhất 2026** (+ 5 H3 mỗi mã, tên H3 giữ nguyên)
- **Vấn đề:** câu mở "Dựa trên sức mạnh nội tại… 5 gương mặt tiêu biểu:" là câu dẫn, chưa trả lời; mỗi mã chỉ có "Điểm nhấn/Tăng trưởng/Khuyến nghị" không có giá, không có nhược điểm; khuyến nghị "Phù hợp dài hạn" không dẫn chứng; VGI/FOX "đỉnh lịch sử" sai so với giá hiện tại.
- **Hướng xử lý:** Câu mở: "Cổ phiếu công nghệ Việt Nam đáng theo dõi gồm FPT, CMG, ELC (HOSE) và VGI, FOX (UPCoM), chọn theo mô hình doanh thu: dịch vụ IT xuất khẩu, hạ tầng số, viễn thông." Mỗi H3 (I120): 1 câu định vị + `Điểm nhấn` (1 dữ kiện có nguồn) + `Giá` (đóng cửa 19/11/2026 và % từ đỉnh 21/09–19/11) + `Hợp với ai` + `Cần lưu ý` (nhược điểm thật). Dữ liệu cụ thể:
  - FPT: đóng cửa 46.150 đồng, đỉnh 67.000 (22/09/2026), cách đỉnh -31,1%; KLGD bq 20 phiên 10.113.045. CafeF 17–18/11/2026 đưa tin giá về đáy 3 năm: dùng khi nguồn nằm trong whitelist.
  - CMG: 16.450 đồng, đỉnh 23.700 (22/09), -30,6%; thấp nhất kỳ ngay 19/11.
  - VGI (UPCoM): 67.900 đồng, đỉnh 85.700 (24/09), -20,8%; bỏ câu "vùng đỉnh lịch sử".
  - ELC: 9.630 đồng, đỉnh 13.850 (24/09), -30,5%; bỏ "lãi ròng gấp đôi" nếu không có nguồn (BCTC 2025).
  - FOX (UPCoM): 53.300 đồng, đỉnh 64.000 (24/09), -16,7%; bỏ "vượt đỉnh lịch sử"; cổ tức chỉ giữ nếu có tỷ lệ và ngày từ nguồn.
  - Bỏ "ông lớn", "cỗ máy in tiền" (CL2-quotes); "nhà máy AI 200 triệu USD", "1.000 GPU", "biên lợi nhuận 55%", "6 thị trường": giữ khi tìm được nguồn; không thì bỏ.
- **Entities cần có:** `FPT`, `CMG`, `VGI`, `ELC`, `FOX`, `HOSE`, `UPCoM`, `Cloud`, `data center`
- **Word count target:** ~420 từ (hiện ~330)

🔄 **H2: Danh mục mã cổ phiếu ngành công nghệ niêm yết**
- **Vấn đề:** câu mở "Dưới đây là danh sách…" không trả lời; bảng 2 cột 3 dòng (SLOP-table-thin); không nguồn/ngày đối chiếu niêm yết.
- **Hướng xử lý:** Câu mở có số: nhóm ngành công nghệ và viễn thông trong bài gồm 18 mã trên 3 sàn: HOSE 7, HNX 5, UPCoM 6. Bảng 4 cột × 3 dòng: Sàn · Mã tiêu biểu · Biên độ dao động/phiên (HOSE 7%, HNX 10%, UPCoM 15%) · Số mã. Dữ liệu biên độ từ `market_facts` (cấu trúc, không hết hạn). Danh sách mã giữ nguyên; đối chiếu sàn từng mã chỉ khi có nguồn (`[CẦN XÁC NHẬN]`).
- **Entities cần có:** `HOSE`, `HNX`, `UPCoM`, `biên độ dao động`
- **Word count target:** ~110 từ

🔄 **H2: Những lưu ý khi đầu tư cổ phiếu công nghệ**
- **Vấn đề:** mở bằng câu "Đầu tư vào nhóm ngành "chất xám"…" (ngoặc kép, không trả lời); 4 bullet đều là câu 36–37 từ; "P/E không bao giờ rẻ" tuyên bố tuyệt đối, P/E 20x–30x không nguồn; "Tránh đu đỉnh" dùng ví dụ VGI đầu 2026 đã lỗi thời.
- **Hướng xử lý:** Câu mở: "Cổ phiếu công nghệ cần 4 tiêu chí: doanh thu lặp lại, định giá, đầu tư AI thật và vị thế thanh khoản." Giữ thứ tự 4 bullet, đổi nội dung: (1) doanh thu lặp lại (giữ, tách câu); (2) định giá: giữ ý P/E theo trung bình 5 năm nhưng chỉ khi có nguồn số, kèm link `chi-so-p-e-la-gi-cach-ap-dung-de-tim-co-phieu-tot`; (3) AI: tiêu chí nhìn vào hạ tầng thật, bỏ "làm màu"; (4) thay "đu đỉnh" bằng nhịp ngược lại: sau khi giảm 13–31%, đợi tín hiệu thay vì bắt đáy, dẫn link `khi-nao-nen-mua-co-phieu` (giữ nguyên link cũ, chuyển vào trong câu) và link `top-5-co-phieu-dang-dau-tu`/`top-co-phieu-hang-khong-nen-dau-tu` (2 link "Xem thêm" cũ) vào câu văn. Thêm 1 ví dụ vốn nhỏ P2: 100 cổ phiếu ELC hết 963.000 đồng, 100 cổ phiếu VGI hết 6.790.000 đồng (giá 19/11/2026). Giữ ảnh 2 ngay dưới.
- **Entities cần có:** `P/E`, `doanh thu lặp lại`, `AI`, `thanh khoản`
- **Word count target:** ~280 từ (hiện ~190)

🔄 **H2: Kết luận**
- **Vấn đề:** "Năm 2026 là thời điểm lý tưởng để tái cơ cấu danh mục" mâu thuẫn dữ liệu giá và có tính khuyến nghị; "dư địa tăng trưởng dài hạn rất lớn" không căn cứ; anchor CTA "đăng ký mở tài khoản chứng khoán" thiếu thương hiệu, "ngay hôm nay" là kêu gọi gấp; miễn trừ đặt cuối, 1 câu.
- **Hướng xử lý (I113):** 1 nhận định: nhóm công nghệ đang điều chỉnh sâu (13–31% trong 44 phiên), nhà đầu tư vốn nhỏ nên chia nhỏ lệnh và chọn mã thanh khoản cao trước (FPT, CMG, ELC hơn VGI, FOX). Checklist 3 mục: (a) chọn mã theo mô hình doanh thu; (b) kiểm biên độ sàn và KLGD bình quân 20 phiên trước khi đặt lệnh; (c) chia vốn thành nhiều đợt. CTA P2: "mở tài khoản DSC — eKYC 3 phút, hoàn toàn online" có link https://www.dsc.com.vn/mo-tai-khoan + nhắc Môi giới 1:1 (nối từ rủi ro vừa nêu). Miễn trừ: bài tham khảo, không phải khuyến nghị mua bán.
- **Entities cần có:** `eKYC`, `Môi giới 1:1`
- **Word count target:** ~170 từ

---

## 5. Đề xuất Thêm mới (Content Gaps)

✨ **[THÊM MỚI] H2: Biến động giá 5 mã cổ phiếu công nghệ từ 21/09 đến 19/11/2026**
- **Học từ đối thủ:** Competitor 4 (nmquan.vn) và 5 (hodl.vn): họ có bảng giá/% nhưng không có phân tích; không đối thủ nào đặt biên độ và thanh khoản cạnh nhau.
- **Vị trí chèn:** Ngay dưới H2 "Top 5 mã cổ phiếu ngành công nghệ tiềm năng nhất 2026" (sau H3 FOX), trước H2 "Danh mục mã cổ phiếu ngành công nghệ niêm yết". Không đổi thứ tự các H2 hiện có.
- **Nội dung chính:** Câu mở có số: 5 mã giảm 13,1–30,5% trong 44 phiên. Bảng: Mã · Sàn · Đỉnh 21/09–19/11 (ngày) · Đóng cửa 19/11 · % từ đỉnh · % cả kỳ · KLGD bq 20 phiên · Vốn cho 100 cp. Đoạn nhận định: 3 mã HOSE thanh khoản cao, 2 mã UPCoM thanh khoản thấp (FOX 52.114 cp so với FPT 10.113.045 cp, ~194 lần; VGI 138.941 cp ~73 lần) dù biên độ UPCoM 15%/phiên so với HOSE 7%: biên độ rộng cộng thanh khoản mỏng làm giá dao động mạnh hơn khi vào lệnh lớn. Giọng có lập trường: vốn nhỏ, F0 nên bắt đầu với mã HOSE.
- **Entities cần có:** `FPT`, `CMG`, `VGI`, `FOX`, `ELC`, `biên độ dao động`, `thanh khoản`, `HOSE`, `UPCoM`
- **Bằng chứng / Số liệu cần có:** toàn bộ từ `python scripts/market_facts.py --brief --tickers FPT,CMG,VGI,FOX,ELC` (19/11/2026), chạy lại lúc rewrite vì số đổi theo phiên; mốc 21/09–19/11 sẽ thành mốc mới nếu chạy lại. % từ đỉnh tính từ cột cao/đóng cửa (FPT -31,1%, CMG -30,6%, VGI -20,8%, ELC -30,5%, FOX -16,7%).
- **Định dạng:** Bảng 8 cột (có thể tách 2 bảng 4–5 cột nếu quá rộng trên CMS mobile) + 2 đoạn văn ngắn.
- **Word count ước tính:** ~230 từ

✨ **[THÊM MỚI] H2: Câu hỏi thường gặp về cổ phiếu ngành công nghệ**
- **Học từ đối thủ:** Competitor 1 — aas.com.vn (H2 "Câu hỏi thường gặp", 3 câu).
- **Vị trí chèn:** Dưới H2 "Những lưu ý khi đầu tư cổ phiếu công nghệ" (sau ảnh 2), trước H2 "Kết luận".
- **Nội dung chính:** 3 câu hỏi dạng H3 (I107), câu trả lời ≤ 60 từ, câu đầu có số + mốc: (1) Cổ phiếu công nghệ AI Việt Nam gồm những mã nào? → FPT và CMG gắn với AI/Cloud; trả lời bằng thông tin có nguồn (`[CẦN XÁC NHẬN]` cho hợp tác Nvidia/GPU); (2) Cổ phiếu công nghệ có nên mua khi giá giảm sâu? → số giảm 13–31%, chia lệnh, ưu tiên thanh khoản; (3) Cổ phiếu ngành công nghệ niêm yết trên sàn nào? → HOSE 7 mã, HNX 5, UPCoM 6 theo bảng + biên độ. Nguồn câu hỏi: truy vấn GSC (`mã cổ phiếu công nghệ ai việt nam`, `cổ phiếu ai`, `cổ phiếu công nghệ`), **không phải PAA** (SERP không có PAA).
- **Entities cần có:** `AI`, `FPT`, `CMG`, `HOSE`, `HNX`, `UPCoM`
- **Bằng chứng / Số liệu cần có:** giá và biên độ từ `market_facts`; số doanh nghiệp chỉ dùng khi có nguồn.
- **Định dạng:** FAQ (3 H3 + đoạn trả lời; không JSON-LD vì CMS không hỗ trợ)
- **Word count ước tính:** ~170 từ

*Không đề xuất thêm H2 "Tiêu chí chọn" và "Cơ hội, rủi ro" như aas.com.vn: nội dung này đã nằm trong H2 "Những lưu ý…" và Kết luận; thêm riêng sẽ lặp (I118, I115).*

---

## 6. Chiến lược Internal Links
> Chỉ dùng URL có Sitemap ✓ từ `find_links.py`; chèn trong câu, URL tuyệt đối. Link hiện có giữ nguyên (5 link, 0 link "chỉ có trên live").

| Anchor Text đề xuất | Bài đích (slug) | Vị trí chèn |
| :--- | :--- | :--- |
| cách mua cổ phiếu FPT | cach-mua-co-phieu-fpt-cong-ty-co-phan-tap-doan-fpt | H3: Cổ phiếu FPT (câu Hợp với ai) |
| chỉ số P/E | chi-so-p-e-la-gi-cach-ap-dung-de-tim-co-phieu-tot | H2: Những lưu ý (bullet định giá) |
| biên độ dao động giá | bien-do-giao-dong-gia-co-phieu-la-gi | H2: Biến động giá 5 mã (đoạn nhận định) |
| cổ phiếu ngành truyền thông | co-phieu-nganh-truyen-thong | H3: VGI hoặc FOX (1 câu về viễn thông/truyền hình) |
| Giữ: `co-phieu-fpt`, `top-5-co-phieu-dang-dau-tu` (sapo), `khi-nao-nen-mua-co-phieu`, `top-co-phieu-hang-khong-nen-dau-tu`, `mo-tai-khoan` | — | Chuyển 2 link "Xem thêm" vào câu; CTA đổi anchor thành "mở tài khoản DSC" |

**📎 Backfill Link Suggestions (bài khác → bài này; thực hiện trên CMS, không thuộc bản Optimize):**

| Bài nguồn | Đoạn | Anchor | Clicks |
| :--- | :--- | :--- | ---: |
| top-5-co-phieu-sieu-dau-co-cua-tung-nhom-nganh-rui-ro-cao-loi-nhuan-cao | Dòng "Top cổ phiếu ngành công nghệ" đang là link ở dòng Xem thêm | Chuyển vào câu: "cổ phiếu ngành công nghệ" | 24 |
| co-phieu-nganh-thuy-san | ">> Xem thêm: Top 5 mã cổ phiếu ngành công nghệ tiềm năng nhất" | Chuyển vào câu trong mục "Chiến lược đầu tư…" | 12 |
| day-la-5-co-phieu-tich-san-cuc-tot-se-khien-ban-kiem-duoc-bon-tien | Tiêu chí lựa chọn: "…ngân hàng, công nghệ, hàng tiêu dùng…" | bọc cụm "công nghệ" (không exact-match) | 79 |
| top-co-phieu-cao-su-nen-dau-tu | Đoạn DPR (201 clicks) | chỉ nên chèn nếu có câu so sánh ngành tự nhiên; ưu tiên thấp | 201 |

---

## 7. Chiến lược Hình ảnh (Image Strategy & Preservation)

### 7.1 Danh sách hình ảnh GỐC cần bảo toàn (BẮT BUỘC)
| Cú pháp Markdown ảnh gốc | Vị trí hiện tại | Hướng xử lý |
| :--- | :--- | :--- |
| `![Tổng quan bức tranh thị trường ngành công nghệ](https://extgw.dsc.com.vn/eback/uploads/co_phieu_nganh_cong_nghe_1_f025ab69e3.jpg)` | Dưới H2: Tổng quan bức tranh thị trường ngành công nghệ | Giữ nguyên; đề xuất alt: "Biểu đồ cổ phiếu ngành công nghệ Việt Nam năm 2026" (chỉ khi user muốn đổi alt) |
| `![Những lưu ý khi đầu tư cổ phiếu công nghệ](https://extgw.dsc.com.vn/eback/uploads/co_phieu_nganh_cong_nghe_2_590eeca2df.jpg)` | Dưới H2: Những lưu ý khi đầu tư cổ phiếu công nghệ | Giữ nguyên; alt giữ hoặc thêm "cổ phiếu ngành công nghệ" |

Ghi chú: ảnh trên bản Final giữ URL tuyệt đối `extgw.dsc.com.vn` đúng bản gốc live (không sửa trong Gate 1). Quy ước CMS là đường dẫn tương đối `/uploads/`; xử lý ở bước đưa lên CMS.

### 7.2 Gợi ý vị trí đặt ảnh mới
| Vị trí đề xuất | Concept ảnh gợi ý | Alt text chứa keyword |
| :--- | :--- | :--- |
| Dưới bảng ở H2 "Biến động giá 5 mã cổ phiếu công nghệ…" | Biểu đồ cột ngang % từ đỉnh của 5 mã (800×500, vẽ bằng `dsc_design.py`, không đỏ, số khớp bảng) | `Biến động giá 5 mã cổ phiếu ngành công nghệ từ 21/09 đến 19/11/2026` |

---

## 8. Checklist trước khi sang Bước 4 (sau `/approve`)
- Chạy lại `market_facts.py --brief --tickers FPT,CMG,VGI,FOX,ELC` lúc rewrite và dùng số mới nhất (mốc ngày sẽ đổi; giữ công thức % tính ở trên).
- Số doanh nghiệp (P/E, GPU, nhà máy AI, biên lợi nhuận, lãi ròng, cổ tức): tìm nguồn trong `source-whitelist.md`; không có thì bỏ câu hoặc `[CẦN XÁC NHẬN]` và báo user.
- Bản Optimize không được tệ hơn baseline: qa_lint 84, slop 87 (và sạch `SLOP-h2-open`), không `FACT-*`.
- Thêm 2 H2 (Biến động giá, FAQ) cần user đồng ý.
