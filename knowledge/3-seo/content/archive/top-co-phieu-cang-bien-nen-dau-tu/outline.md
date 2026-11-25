---
# Khối máy đọc: qa_lint --outline / qa_gate đối chiếu bản Optimize với các trường này. Giữ đúng tên trường.
Target_Keyword: cổ phiếu cảng biển
Thesis: "Danh sách mã chưa đủ để chọn cổ phiếu cảng biển: cùng một ngành nhưng GMD, PHP, VSC, HAH, CDN khác nhau rõ về nguồn thu, sàn niêm yết và thanh khoản (CDN khớp bình quân 20 phiên chỉ 2.313 cổ phiếu, GMD hơn 2,2 triệu), nên bài đặt từng mã cạnh nhau bằng số phiên ngày 19/11/2026 và dự báo lợi nhuận quý III/2026 có nguồn."
Entities: [hàng hóa, xuất nhập khẩu, vận tải biển, xếp dỡ, công ty cổ phần, triển vọng ngành, container, cảng nước sâu, Gemalink, Lạch Huyện, Cái Mép - Thị Vải, Đình Vũ, HOSE, HNX, vốn hóa, thanh khoản, GMD, HAH, CDN, VSC, PHP, SGP]
Entities_Skipped: ["bảo hiểm — thuộc bài ngành bảo hiểm, không liên quan intent", "khởi sắc / tích cực / cuối năm / đầu năm / đầu tháng — từ miêu tả chung, không phải thực thể", "hệ sinh thái — từ sáo, chỉ dùng khi gắn tên cụ thể (hệ sinh thái logistics của GMD)"]
Information_Gain:
  - claim: "Bảng so sánh thanh khoản và vùng giá của các mã cảng chính theo 44 phiên gần nhất (top 5 SERP không có số phiên nào, bài DSC hiện chỉ có vốn hóa 03/2023)"
    h2: "Top mã cổ phiếu theo ngành cảng biển có giá trị tốt"
    type: comparison
    proof: "KLGD bình quân 20 phiên"
  - claim: "Bảng dự báo lợi nhuận quý III/2026 của GMD, PHP, VSC, HAH kèm điều kiện (công suất khai thác, giá dịch vụ) để người đọc thấy mã nào tăng nhờ sản lượng, mã nào nhờ giá"
    h2: "Nhận định về ngành cảng biển"
    type: comparison
    proof: "quý III/2026"
  - claim: "Gắn từng mã với sàn, biên độ và giá trị 1 lô 100 cổ phiếu (CDN trên HNX biên độ 10%, GMD trên HOSE biên độ 7%) và hệ quả thanh khoản khi vào/ra lệnh"
    h2: "Top mã cổ phiếu theo ngành cảng biển có giá trị tốt"
    type: calc
    proof: "1 lô 100 cổ phiếu"
Featured_Snippet: Table
PAA_Questions:
  - q: "Mã cổ phiếu cảng Cái Mép là gì?"
    placement: faq
  - q: "Các mã cổ phiếu cảng biển nào niêm yết trên HOSE và HNX?"
    placement: faq
  - q: "Cổ phiếu cảng biển và cổ phiếu vận tải biển khác nhau thế nào?"
    placement: faq
  - q: "Các mã cổ phiếu ngành logistics gồm những mã nào?"
    placement: faq
# Ghi chú: SERP trả về 0 PAA. 4 câu trên lấy từ Related Searches của SERP (19/11/2026) + query GSC có impressions.
---

# 📋 BÁO CÁO TỐI ƯU SEO (SEO Optimization Proposal) — `top-co-phieu-cang-bien-nen-dau-tu`

URL: https://www.dsc.com.vn/kien-thuc/top-co-phieu-cang-bien-nen-dau-tu · Trạng thái: Optimizing · Gate 1 (chờ `/approve`)

## 0. Content Strategy Header ⚠️ ĐỌC TRƯỚC KHI XEM BẤT KỲ MỤC NÀO

| Thông số | Giá trị |
| :--- | :--- |
| **Target Keyword** | `cổ phiếu cảng biển` (GSC xác nhận: 56 clicks/287 impressions, vị trí 1,27, CTR 19,5%, 90 ngày) |
| **Secondary Keywords** | `cổ phiếu cảng`, `các cổ phiếu cảng biển`, `các mã cổ phiếu cảng biển`, `cổ phiếu vận tải biển`, `nhóm cổ phiếu cảng biển`, `cổ phiếu cảng cái mép` |
| **LSI / Entities** | GMD, HAH, CDN, VSC, PHP, SGP, Gemalink, Lạch Huyện, Cái Mép - Thị Vải, xuất nhập khẩu, xếp dỡ, container |
| **Search Intent** | Commercial / Informational — nhà đầu tư muốn có danh sách mã cảng biển niêm yết và biết mã nào đáng theo dõi trước khi đặt lệnh |
| **Persona** | P2 — F0: Nhà đầu tư mới — tìm "mã nào thuộc ngành cảng biển" theo ngành, sợ mua nhầm mã kém thanh khoản hoặc mua đỉnh; cần giải thích sàn, biên độ, lô giao dịch |
| **Tone** | Thân thiện nhưng giọng báo cáo, câu ngắn, mỗi nhận định một số liệu có mốc |
| **DSC Product Bridge** | eKYC 3 phút + Môi giới 1:1 — "một tài khoản giao dịch được cả mã HOSE (GMD, HAH, VSC, PHP) lẫn HNX (CDN)", chuyên gia DSC hỗ trợ khi cần hỏi về mã. Không nhắc DSC Invest (P2) |
| **Featured Snippet** | Table — bảng "Danh sách mã cổ phiếu theo ngành cảng biển" (SERP chưa có featured snippet; AI Overview đang trích DSC, giữ cấu trúc bảng để tiếp tục được trích) |
| **Word Count hiện tại** | ~1.100 từ (sync: 1.105; 909 từ chữ theo slop_check) |
| **Word Count mục tiêu** | ~1.600–1.800 từ (SERP: stockkisvn 935, diendandoanhnghiep ~990, fhsc 2.412, vnbusiness 3.130; median top 5 = 935. Tăng vì thêm 2 mã, rủi ro, FAQ; không vượt fhsc) |

**Bài gốc đang phục vụ đúng intent/persona không?**
- [ ] ✅ Đúng
- [x] ⚠️ Lệch một phần: intent đúng (danh sách mã), nhưng bài viết như bản 2023: vốn hóa ngày 27/03/2023, doanh thu 2021 ("300,000 tỷ đồng" là số sai bậc), khẳng định "lợi nhuận cực khủng", "yên tâm". Chưa có số 2026 nào ngoài tiêu đề. Hướng chỉnh: giữ khung, thay toàn bộ số bằng dữ liệu 2026 có mốc, thêm tiêu chí chọn mã.

**Rủi ro thứ hạng (bắt buộc đọc):** keyword chính ở vị trí 1,27 (page-level 3,55 do các query ngách). Theo giới hạn tái cấu trúc: **không đổi H1, không đổi thứ tự/gộp/xóa H2 đang có, không đổi Title**. Chỉ `[GIỮ NGUYÊN]` / `[CẬP NHẬT]` / `[THÊM MỚI]`. Thêm mới đặt sau các H2/H3 hiện có, trước H2 Kết luận.

**Lưu ý đồng bộ live:** bản live vừa sync (19/11/2026) khác snapshot 11/11 ở 1 câu: đoạn H3 Gemadept cuối đã có thêm câu "Trước khi xuống tiền, nên so sánh GMD với các cổ phiếu tiềm năng…" kèm link `top-5-co-phieu-dang-dau-tu` (link do vòng link cụm). Final/Optimize đã lấy đúng bản này; link phải giữ. Meta live cũng đã đổi thành câu 192 ký tự (xem Section 1).

---

## 1. Đánh giá Tổng quan (Overall Health)

📊 GSC Performance Context (2026-08-19 → 2026-11-16, SEO Dashboard MCP):
- Page-level (không tách query): **735 clicks · 11.224 impressions · CTR 6,55% · vị trí TB 3,55**. Tổng theo query chỉ thấy 119 clicks / 1.106 impressions (CTR 10,76%, vị trí 3,26; kỳ trước 107 clicks, vị trí 4,66) vì ~84% clicks là query ẩn danh.
- Không cần rewrite Title vì CTR (query chính 19,5%) đã cao; flag duy nhất là CTR thấp ở các query ngách bên dưới.

| Query | Clicks | Impr. | Vị trí | CTR | Bài đang phục vụ? |
|---|---:|---:|---:|---:|---|
| cổ phiếu cảng biển | 56 | 287 | 1,3 | 19,5% | Có (H1, H2) |
| cổ phiếu cảng | 16 | 90 | 1,4 | 17,8% | Một phần (chỉ có "cảng biển") |
| các cổ phiếu cảng biển | 10 | 62 | 1,2 | 16,1% | Có |
| cổ phiếu vận tải biển | 9 | 105 | 2,4 | 8,6% | Yếu: "vận tải" chỉ là nhãn cột trong bảng |
| các mã cổ phiếu cảng biển | 5 | 16 | 1,1 | 31% | Có (bảng) |
| cổ phiếu cảng cái mép | 4 | 75 | 5,1 | 5,3% | **Không** — 0 lần nhắc "Cái Mép" |
| mã cổ phiếu cảng cái mép | 2 | 69 | 4,7 | 2,9% | **Không** |
| ngành cảng biển | 1 | 65 | 4,8 | 1,5% | Yếu — H2 "Nhận định" chỉ có 3 ý chung chung |
| báo cáo ngành cảng biển 2026 | 2 | 18 | 10,4 | 11% | **Không** (không có số 2026) |

- **Cannibalization:** không. Query `cổ phiếu cảng biển` chỉ có đúng 1 URL DSC (75 clicks / 406 impressions, vị trí 1,26). Các URL trùng chỉ là typo (`cphieu`, `dang-tu`, `kien-thux`, 1 impression mỗi URL). Bài `co-phieu-gmd/hah/vsc-...` là spoke của cùng cụm 5g, không có impressions ở query này.
- **SERP sanity check:** DSC xếp #1 trong SERP, khớp vị trí GSC 1,27; Related Searches (Cái Mép, Cảng Hải Phòng, Cát Lái, GMD, vận tải biển, logistics) khớp query GSC; ngày bài đối thủ có (6/10/2026 diendandoanhnghiep) hợp lý. Cảnh báo duy nhất của script: rank bị nhảy cóc (thiếu 3, 6) do loại kết quả Google nội bộ, không phải SERP sai. Có 7 organic hợp lệ. Không cần refetch. Cache: lần đầu gọi phải `--force` vì registry không khớp keyword (chi phí $0,002).
- **Word Count Gap:** ~1.100 vs median top 5 935 → đã trong range, thêm ~600 từ chỉ cho nội dung mới có giá trị.
- **Điểm On-page:** `qa_lint` baseline 71/100 (FAIL): CRITICAL: meta 192 ký tự, H1 không chứa cụm chính xác "cổ phiếu cảng biển", cụm cấm "Bài viết dưới đây". MAJOR: 4 mốc thời gian mơ hồ ("hiện nay", "những năm gần đây", "gần đây", "trong những năm qua"), 5 đoạn > 3 câu, dòng "Xem thêm" đặt rời. `slop_check` 87/100 trên Final-md (PASS với ngưỡng relative) nhưng có MAJOR `SLOP-vague` 3,3 câu/1000 từ (tối đa 1,1) và MINOR `uniform-run` 15 câu cùng nhịp. Điểm 77 ở corpus-wide cao hơn ngưỡng nên cần đối chiếu: baseline Final dùng 87, bản Optimize phải ≥ 87. `market_facts --verify`: 0 vấn đề (bài không có mốc chỉ số có ngày; số vốn hóa 2023 không bị bắt, nên không dựa vào FACT-stale mà vẫn phải thay).
- **Vi phạm Anti-AI/Brand:** Có. "lợi nhuận khủng", "lợi nhuận cực khủng", "yên tâm khi lựa chọn", "chuyên giá" (sai chính tả "chuyên gia") cộng "được chuyên gia đánh giá cao" không nêu chuyên gia nào, "cảng biến" (lỗi chính tả sapo), câu mở đầu vĩ mô "Cảng biển là ngành hàng đóng vai trò rất quan trọng đối với thương mại và kinh tế toàn cầu" (opener vĩ mô), "27/03/2023.." (hai dấu chấm). Khung H3 của 3 mã gần giống bài `top-co-phieu-cao-su-nen-dau-tu` (cùng mẫu "Công ty Cổ phần X" + đoạn vốn hóa + đoạn "nhờ vậy nhà đầu tư thu về kha khá lợi nhuận"), đó là nguồn của cờ `template`; chữa bằng khung Giới thiệu → Ưu → Nhược → Hợp với ai có số liệu riêng từng mã (I120).
- **Lỗi nội dung cần sửa (không phải slop mà là sai):**
  - "tổng doanh thu đã chạm mốc 300,000 tỷ đồng" (CDN 2021): sai bậc (CDN doanh thu cỡ vài trăm tỷ). `[CẦN XÁC NHẬN]` từ BCTC CDN trên hnx.vn hoặc bỏ.
  - "GMD và HAH niêm yết trên HoSE" và "tại sàn HSX" lẫn hai cách viết, thống nhất theo glossary.
  - Bảng liệt kê VTP (Bưu chính Viettel) là "Logistics ngành cảng biển" — lệch; cần ghi chú hoặc kiểm tra lại danh sách 18 mã (xem 4.2).
  - Số dữ liệu giá: bài diendandoanhnghiep (6/10/2026) ghi GMD ~77.800 đồng/cp, nhưng `market_facts` ngày 19/11/2026 cho GMD đóng cửa 51,10 (cao 57,90 ngày 22/10). Hai nguồn lệch lớn, **chỉ dùng `market_facts`**, không trích giá từ bài báo đó. Cần kiểm tra thêm nếu muốn nêu mức giảm.

### Đề xuất cập nhật SEO Elements
- **Title hiện tại:** Danh sách cổ phiếu ngành cảng biển nên đầu tư 2026 (50 ký tự, chứa "cổ phiếu ... cảng biển" nhưng không đúng cụm liền).
- **Title đề xuất:** **Giữ nguyên.** Đang #1 với CTR 19,5% cho query chính; bài học rollback cho thấy đổi khung bài đang top 3 rủi ro hơn lợi. (Ghi chú cho lint: `CL1-h1`/`CL1-title` sẽ báo "không có cụm chính xác" — đây là miễn trừ có chủ đích. Phương án thay thế nếu user muốn: "Cổ phiếu cảng biển: danh sách mã nên đầu tư năm 2026" — 52 ký tự, **chỉ làm khi user đồng ý rủi ro** ở Section 0.)
- **Meta Description hiện tại:** "Nhà đầu tư trên thị trường có mối quan tâm đặc biệt tới các cổ phiếu ngành cảng biển. Bài viết hôm nay của DSC sẽ chia sẻ top 3 cổ phiếu cảng biến mà bạn có thể cân nhắc đầu tư trong năm 2026." (192 ký tự, lỗi chính tả "cảng biến", không có keyword chính xác)
- **Meta Description đề xuất (142 ký tự):** "Cổ phiếu cảng biển: bảng so sánh GMD, HAH, CDN, PHP, VSC theo giá, thanh khoản và dự báo lợi nhuận quý III/2026. Mở tài khoản DSC để theo dõi." Sửa meta không ảnh hưởng H1/H2 nên nằm trong giới hạn.

---

## 2. Phân tích Đối thủ SERP (Competitor Analysis)
Nguồn: `serp_research.py` (DataForSEO, 19/11/2026, cache `knowledge/raw/serp/co-phieu-cang-bien.json`) + `analyze_competitors.py` → `scratch/competitors-top-co-phieu-cang-bien-nen-dau-tu.json`. Organic hợp lệ 7; PAA 0; AI Overview có và trích dsc.com.vn.

### 2.1 Bảng so sánh tổng quan

| # | URL | Search Intent | Word Count | Điểm nổi bật |
| :--- | :--- | :--- | :--- | :--- |
| 1 | dsc.com.vn (bài mình) | Commercial | ~1.108 | Bảng 18 mã, 3 mã nổi bật, AI Overview trích |
| 2 | vnbusiness.vn/tag/co-phieu-cang-bien | News (trang tag) | ~3.130 | Tin cổ phiếu cảng biển giảm sau chu kỳ tăng "nóng" do cước vận tải |
| 3 | diendandoanhnghiep.vn (6/10/2026) | Informational/News | ~990 | Dự báo lợi nhuận quý III/2026 từng mã theo MBS, giá dịch vụ cảng nước sâu +10–15% |
| 4 | stockkisvn.vn/co-phieu-cang-bien/ | Informational | ~935–1.017 | 4 H2: ngành gồm công ty nào, tiềm năng, rủi ro, top mã; số liệu 2023 |
| 5 | fhsc.com.vn/co-phieu-cang-bien | Review | ~2.412 | Bài "năm 2025": tổng quan, thách thức, 4 mã (GMD, VSC, PHP, HAH), FAQ |
| — | simplize.vn, vietstock SGP | Dữ liệu mã/ngành | — | Trang dữ liệu, không phải bài; không so nội dung |

### 2.2 Cấu trúc outline từng đối thủ (chỉ ghi khác biệt)

**Đối thủ 1: vnbusiness.vn — https://vnbusiness.vn/tag/co-phieu-cang-bien**
- **Intent chính:** đọc tin diễn biến nhóm cảng biển (trang tag tổng hợp, không có outline).
- **Mục họ có mà bài mình chưa có:** diễn biến giá theo chu kỳ (tăng nóng khi cước tăng, giảm khi thị trường điều chỉnh) → góc "vì sao nhóm cảng biển biến động".
- **Yếu tố đặc biệt:** nhiều bài tin có ngày.
- **Content Gap:** bài DSC không có mốc giá hay biến động nào gần đây.

**Đối thủ 2: diendandoanhnghiep.vn — https://diendandoanhnghiep.vn/vi-sao-co-phieu-nganh-cang-bien-phan-hoa-10185457.html**
- **Intent chính:** vì sao cổ phiếu cảng biển phân hóa, mã nào hưởng lợi quý III/2026.
- **Mục họ có mà bài mình chưa có:** từng mã có lợi nhuận dự báo quý III/2026 theo MBS (GMD 587 tỷ, +86%; PHP 430 tỷ, +65%; VSC 146 tỷ, +82% nhưng cả năm chỉ +8,5%; HAH 339 tỷ, +12%); xuất nhập khẩu quý III +~30%, lượng hàng qua cảng +~22%; giá xếp dỡ cảng nước sâu +10–15%.
- **Yếu tố đặc biệt:** chia theo yếu tố (sản lượng, công suất khai thác, giá dịch vụ) thay vì liệt kê.
- **Content Gap:** bài DSC không có số 2026, không phân biệt mã nào tăng nhờ sản lượng/giá. Lưu ý: số giá GMD trong bài lệch `market_facts` (xem Section 1), chỉ mượn cách phân tích, không mượn giá.

**Đối thủ 3: stockkisvn.vn — https://stockkisvn.vn/co-phieu-cang-bien/**
- **Intent chính:** có nên đầu tư cổ phiếu cảng biển.
- **Mục họ có mà bài mình chưa có:** H2 "Đầu tư vào cổ phiếu ngành cảng biển tồn tại rủi ro nào?" (~150 từ); H2 tiềm năng (~290 từ) gắn phục hồi vận chuyển sau Covid; chia danh sách theo sàn HSX/HNX.
- **Yếu tố đặc biệt:** hai bảng theo sàn niêm yết.
- **Content Gap:** DSC có 1 bảng, không tách sàn, không có phần rủi ro. Số liệu của họ cũng cũ (2023) nên cơ hội vượt bằng dữ liệu mới.

**Đối thủ 4: fhsc.com.vn — https://fhsc.com.vn/co-phieu-cang-bien**
- **Intent chính:** đánh giá cổ phiếu cảng biển năm 2025, mã nào đáng chú ý.
- **Mục họ có mà bài mình chưa có:** H3 "Những thách thức có thể ảnh hưởng đến cổ phiếu cảng biển" (~250 từ); H3 riêng cho VSC (~290 từ) và PHP (~160 từ), HAH (~340 từ), GMD (~285 từ); mục FAQs (~47 từ).
- **Yếu tố đặc biệt:** mỗi mã có đoạn riêng ~150–340 từ; FAQ cuối bài.
- **Content Gap:** họ chọn 4 mã (GMD, VSC, PHP, HAH) còn DSC chọn GMD, HAH, CDN; DSC thiếu VSC và PHP là hai mã nhóm cảng có thanh khoản cao (VSC KLGD bình quân 20 phiên ~11,5 triệu).

(`finance.vietstock.vn` và `simplize.vn` là trang dữ liệu/ngành, không đưa vào so sánh.)

### 2.3 Intent Gap — Bài hiện tại đang bỏ sót gì?
- **Intent SERP:** danh sách mã + đánh giá/triển vọng theo từng mã; đối thủ mới nhất (6/10/2026) so mã bằng dự báo lợi nhuận và yếu tố tăng trưởng.
- **Intent bài hiện tại:** đúng khung danh sách, nhưng không có tiêu chí so sánh và không có số mới.
- **Gap cần xử lý:** (1) số 2026 có mốc (giá, thanh khoản, lợi nhuận quý III/2026); (2) rủi ro ngành; (3) thêm VSC và PHP; (4) trả lời "Cái Mép", "cổ phiếu vận tải biển", "logistics" bằng bảng cụm cảng/phân loại; (5) FAQ (SERP 0 PAA nên lấy từ Related Searches).

---

## 3. Kết quả 8 Sweeps Audit

| Bước Quét | Đánh giá | Vấn đề chính | Ghi chú cải thiện |
| :--- | :---: | :--- | :--- |
| **Clarity** | 5/10 | Sapo mở bằng câu vĩ mô 33 từ; nhiều câu "có thể thấy được" | Sapo trả lời thẳng: số mã cảng niêm yết, 3 mã nổi bật, mốc dữ liệu |
| **Voice** | 5/10 | Giọng quảng cáo ("lợi nhuận cực khủng", "yên tâm") | Giọng báo cáo, nêu mã/số, không hứa lợi nhuận |
| **So What** | 4/10 | Nêu mã nhưng không nói người đọc làm gì với thông tin | Mỗi mã có "Hợp với ai" kèm giá trị 1 lô và hệ quả thanh khoản |
| **Prove It** | 2/10 | Vốn hóa 27/03/2023, doanh thu 2021 (có số sai), "chuyên gia đánh giá" không nguồn | Thay bằng `market_facts` (19/11/2026) + BCTC quý III/2026 + dự báo CTCK có tên và ngày |
| **Specificity** | 3/10 | "tiềm năng tốt", "khá tốt", "nhiều kinh nghiệm" | Thay bằng số: sản lượng, công suất, KLGD, biên độ |
| **Emotion** | 4/10 | Không chạm nỗi lo F0 | Đoạn rủi ro/thanh khoản đánh thẳng nỗi sợ "mua mã khó bán" |
| **Zero Risk** | 5/10 | Có lưu ý cuối bài nhưng nằm sau CTA | Giữ lưu ý, thêm "Hợp với ai/Rủi ro" từng mã; DSC không đặt giá mục tiêu |
| **GEO/AEO** | 4/10 | 3/4 H2 đã trả lời thẳng nhưng 0 FAQ, 4 mốc thời gian mơ hồ, bảng không có sàn/cụm cảng | Thêm FAQ ≤ 60 từ/câu đầu, đổi 4 mốc mơ hồ thành ngày cụ thể, thêm cột Sàn + Cụm cảng |

---

## 4. Phân tích Chi tiết (Heading-by-Heading Analysis)

### GIỮ NGUYÊN

| Heading | Lý do giữ |
| :--- | :--- |
| H1: Danh sách cổ phiếu ngành cảng biển nên đầu tư 2026 | Vị trí 1,27, CTR 19,5%; giới hạn tái cấu trúc (position ≤ 5). Miễn trừ lint CL1-h1 có chủ đích |
| H2: Kết luận | Giữ vị trí cuối, vẫn kèm CTA mở tài khoản + lưu ý miễn trừ (nội dung đoạn CTA được `[CẬP NHẬT]` nhẹ, xem dưới) |

### XÓA BỎ
Không xóa heading nào. Chỉ bỏ câu/số liệu lỗi ở các mục CẬP NHẬT (vốn hóa 03/2023, doanh thu CDN 2021, "300,000 tỷ", "lợi nhuận cực khủng", "yên tâm").

### CẬP NHẬT

🔄 **Sapo (dưới H1)** — `[CẬP NHẬT]`
- **Vấn đề:** mở bằng câu vĩ mô 33 từ ("đóng vai trò rất quan trọng đối với thương mại và kinh tế toàn cầu…"), "lợi nhuận khủng", lỗi "cảng biến", cụm cấm "Bài viết dưới đây", chưa có keyword chính xác.
- **Hướng xử lý (I105):** đoạn 1 trả lời thẳng: "Cổ phiếu cảng biển trên sàn Việt Nam gồm [N] mã niêm yết (CẦN XÁC NHẬN theo danh sách ngành tại 19/11/2026); GMD, PHP, VSC, HAH là các mã có thanh khoản cao nhất, CDN thấp nhất" kèm 1 số có ngày. Đoạn 2: "Trong bài viết này, Chứng khoán DSC so sánh …" nêu phạm vi (danh sách, so sánh mã theo giá/thanh khoản/lợi nhuận quý III/2026, rủi ro) và câu cuối là 1 con số có trong bài (CDN khớp bình quân 20 phiên chỉ 2.313 cổ phiếu).
- **Entities cần có:** `cổ phiếu cảng biển`, `GMD`, `HAH`, `CDN`, `PHP`, `VSC`
- **Word count target:** ~110 từ (hiện ~75)

🔄 **H2: Nhận định về ngành cảng biển** — `[CẬP NHẬT]`
- **Vấn đề:** 3 ý chung chung không số ("đang trên đà tăng trưởng", "đầu tư mạnh", "dần thặng dư"), một dòng thừa "Xem thêm" rời, đoạn rút gọn lỗi định dạng (3 ý nằm trong 2 đoạn không list). Query `ngành cảng biển` (65 impr, vị trí 4,8, CTR 1,5%) và `báo cáo ngành cảng biển 2026` (vị trí 10,4) đang không được phục vụ.
- **Hướng xử lý:** giữ câu mở trả lời trực tiếp, đổi 3 ý thành list có số + mốc: xuất nhập khẩu quý III/2026 tăng gần 30% cùng kỳ, lượng hàng qua cảng dự báo tăng gần 22% (cả hai theo MBS, tháng 9/2026), giá xếp dỡ cảng nước sâu có thể tăng 10–15% (dự báo thị trường 2026). **Bắt buộc** mở báo cáo/bản tin gốc kiểm năm, mốc, tên tổ chức (I110); số nào không xác minh được → bỏ, không dán lại từ bài báo. Thêm **bảng "Dự báo lợi nhuận quý III/2026"** (GMD 587 tỷ +86%, PHP 430 tỷ +65%, VSC 146 tỷ +82%, HAH 339 tỷ +12% — nguồn MBS, `[CẦN XÁC NHẬN]`); nếu BCTC thực tế quý III/2026 đã công bố (hạn 30/10) thì ưu tiên số thực tế từ công bố thông tin trên hsx.vn/hnx.vn và ghi "dự báo vs thực tế". Nguồn MBS không có trong whitelist: ghi tên + tháng trong câu, không link (link ngoài chỉ tới whitelist).
- **Giữ:** link `top-5-co-phieu-dang-dau-tu` (chuyển từ dòng "Xem thêm" vào 1 câu có ngữ cảnh), ảnh gốc ngay dưới (alt đổi, URL giữ).
- **Entities cần có:** `xuất nhập khẩu`, `hàng hóa`, `xếp dỡ`, `cảng nước sâu`, `triển vọng ngành`
- **Word count target:** ~260 từ (hiện ~120)

🔄 **H2: Danh sách mã cổ phiếu theo ngành cảng biển** — `[CẬP NHẬT]`
- **Vấn đề:** "Hiện nay" (mốc mơ hồ); bảng chỉ có Mã/Tên/Phân loại, không có sàn, không có cụm cảng nên không trả lời được `cổ phiếu cảng cái mép`, `cổ phiếu vận tải biển`, `các mã cổ phiếu ngành logistics`; bảng lẫn VTP, SWC (lệch intent "cảng biển").
- **Hướng xử lý:** giữ nguyên 18 hàng và thứ tự cột 1–3, **thêm 2 cột: Sàn niêm yết** (HOSE/HNX/UPCoM, kiểm tra ngày 19/11/2026) và **Khu vực/cụm cảng** (Hải Phòng–Lạch Huyện–Đình Vũ, Cái Mép–Thị Vải, Sài Gòn–Cát Lái, Đà Nẵng… — mỗi ô `[CẦN XÁC NHẬN]` bằng báo cáo thường niên/công bố thông tin trên hsx.vn/hnx.vn, ô nào chưa xác minh thì để trống). Câu mở dẫn "Tại 19/11/2026, ngành có [N] mã niêm yết" thay "Hiện nay…". Thêm 1 câu giải thích 3 nhóm Cảng / Vận tải / Logistics khác nhau thế nào (tăng độ phủ `cổ phiếu vận tải biển`, `logistics`). Hàng nào không còn niêm yết hoặc đổi nhóm: ghi chú, **không xóa hàng** nếu chưa xác minh.
- **Định dạng:** giữ bảng (Featured Snippet = Table).
- **Entities cần có:** `HOSE`, `HNX`, `Cái Mép - Thị Vải`, `Hải Phòng`, `vận tải biển`, `logistics`
- **Word count target:** ~190 từ + bảng

🔄 **H2: Top mã cổ phiếu theo ngành cảng biển có giá trị tốt** — `[CẬP NHẬT]`
- **Vấn đề:** "được chuyên giá đánh giá cao" (sai chính tả và không nguồn); không nêu tiêu chí chọn 3 mã; không có bảng so sánh.
- **Hướng xử lý:** đoạn mở nêu tiêu chí chọn (sản lượng/công suất khai thác, thanh khoản, sàn) thay cho "chuyên gia đánh giá cao"; đoạn mở là câu trả lời thẳng "Trong nhóm cảng biển, GMD, PHP, VSC, HAH có thanh khoản cao, CDN thấp". **Thêm bảng so sánh các mã** (Information_Gain 1 và 3): Mã · Sàn · Biên độ · Giá đóng cửa 19/11/2026 · Vùng giá 44 phiên · KLGD bình quân 20 phiên · Giá trị 1 lô 100 cổ phiếu — dữ liệu `market_facts.py --brief` (21/09–19/11/2026): GMD 51,10 (thấp 49,05 ngày 03/11, cao 57,90 ngày 22/10; KLGD bq 2.232.536); HAH 46,15 (44,90–53,50; 369.155); CDN 25,10 (24,70–26,90; **2.313**); VSC 13,05 (12,65–15,50; 11.475.813); PHP 44,50 (41,00–51,90; 478.376); SGP 18,20 (18,00–23,10; 29.356; **phiên 19/11 -8,1%** — kiểm nguyên nhân (quyền/cổ tức?) trước khi đưa số vào bài). Chạy lại `market_facts.py` ngay trước khi viết (I110).
- **Giữ:** link "mở một tài khoản chứng khoán" (`cach-mo-tai-khoan-chung-khoan`); câu "nhà đầu tư chỉ cần mở một tài khoản là giao dịch được cả ba mã" nới thành 5 mã; Product Bridge lồng vào đây (P2: eKYC 3 phút + Môi giới 1:1), nêu rõ DSC không đặt giá mục tiêu (I120).
- **Entities cần có:** `vốn hóa`, `thanh khoản`, `HOSE`, `HNX`, `biên độ`, `lô 100 cổ phiếu`
- **Word count target:** ~170 từ + bảng

🔄 **H3: Công ty Cổ phần Gemadept** — `[CẬP NHẬT]`
- **Vấn đề:** vốn hóa 15 520,96 tỷ cập nhật 27/03/2023; "yên tâm khi lựa chọn"; "có giá trị thanh khoản và tiềm năng khá tốt" không số; đoạn 2 mở bằng câu thiếu chủ ngữ; câu link mới "Trước khi xuống tiền, nên so sánh GMD…" là câu `[định tính không tiêu chí]` (SLOP-vague).
- **Hướng xử lý (I120):** khung Giới thiệu → Ưu → Nhược → Hợp với ai, mỗi ý 1 dữ kiện đã xác minh: Gemalink (cảng nước sâu Cái Mép, sản lượng +27% theo MBS), GMD dự báo LNST quý III/2026 587 tỷ (+86%), giá 51,10 và KLGD bq 2,23 triệu (19/11/2026), vốn hóa mới (chạy `market_facts`/công bố thông tin, bỏ số 2023); nhược: giá giảm khỏi đỉnh 57,90 (22/10) xuống 49,05 (03/11); liên doanh/liên kết đóng góp lợi nhuận. **Giữ nguyên link** `co-phieu-gmd-...` và link `top-5-co-phieu-dang-dau-tu` (viết lại câu quanh link để có tiêu chí: "so sánh P/E và tăng trưởng lợi nhuận với cổ phiếu ngành khác", link bọc trong câu đó).
- **Entities cần có:** `GMD`, `Gemalink`, `Cái Mép - Thị Vải`, `Nam Đình Vũ`, `HOSE`
- **Word count target:** ~190 từ (hiện ~150)

🔄 **H3: Công ty Cổ phần Vận tải và Xếp dỡ Hải An** — `[CẬP NHẬT]`
- **Vấn đề:** vốn hóa 2314,34 tỷ ngày 27/03/2023 (lỗi hai dấu chấm); "lợi thế cạnh tranh cao hơn hẳn so với các cảng biển khác" không nguồn, HAH thực tế là mã vận tải/khai thác tàu container hơn là cảng đơn thuần; "lợi nhuận cực khủng" là hứa hẹn (vi phạm nguyên tắc không hứa lợi nhuận); "máy móc mới tiên tiến hơn" không số.
- **Hướng xử lý:** giữ khung; nêu đúng mô hình kinh doanh (khai thác tàu container, cảng, logistics `[CẦN XÁC NHẬN]` từ công bố thông tin HAH), LNST dự báo quý III/2026 339 tỷ (+12%, thấp hơn nhóm khai thác cảng vì chi phí nhiên liệu), giá 46,15 (19/11/2026), vùng 44,90–53,50, KLGD bq 369.155; nhược: phụ thuộc giá cước thuê tàu và nhiên liệu. Bỏ "cực khủng", "dự đoán". **Giữ link** `co-phieu-hah-...`.
- **Entities cần có:** `HAH`, `vận tải biển`, `container`, `giá cước`
- **Word count target:** ~190 từ (hiện ~170)

🔄 **H3: Công ty Cổ phần cảng Đà Nẵng** — `[CẬP NHẬT]`
- **Vấn đề:** vốn hóa 03/2023; "doanh thu 300,000 tỷ đồng" và "lợi nhuận sau thuế tăng 61 tỷ, gấp 4 lần" nghi sai (cùng một câu mâu thuẫn quy mô), số năm 2021 đã cũ 5 năm; "thu về kha khá lợi nhuận" là cường điệu.
- **Hướng xử lý:** thay bằng BCTC năm gần nhất + quý III/2026 từ hnx.vn (`[CẦN XÁC NHẬN]`; nếu không xác minh được thì bỏ số, chỉ giữ thông tin xác định: HNX, IPO 2016, trực thuộc Bộ Giao thông Vận tải khi thành lập). Điểm mới có giá trị: **thanh khoản thấp** (KLGD bq 20 phiên 2.313 cổ phiếu, giá 25,10 → ~58 triệu đồng/phiên) và biên độ HNX 10%; "Hợp với ai": nhà đầu tư dài hạn vốn nhỏ, không phù hợp lệnh lớn (kết hợp ví dụ 1 lô 100 cổ phiếu = 2,51 triệu đồng).
- **Entities cần có:** `CDN`, `HNX`, `thanh khoản`, `biên độ 10%`
- **Word count target:** ~190 từ (hiện ~165)

🔄 **Đoạn ">> Xem thêm" dưới H3 cuối (ngành Dược, dệt may)** — `[CẬP NHẬT]` nhẹ
- **Hướng xử lý:** giữ 2 link (đang có trên live, bắt buộc giữ); chuyển thành 1 câu ngữ cảnh ("Cùng chọn cổ phiếu theo ngành, xem thêm danh sách cổ phiếu ngành dược và dệt may") theo `LINK-xemthem`. Thứ tự dòng không đổi.

🔄 **H2: Kết luận** — nội dung CẬP NHẬT, heading `[GIỮ NGUYÊN]`
- **Vấn đề:** kết luận nhắc lại "tiềm năng tốt" không số; không còn đúng khi thêm PHP/VSC. CTA "Mở tài khoản DSC ngay để truy cập công cụ phân tích thị trường" — "công cụ phân tích" không có trong profile/service-operations (I111).
- **Hướng xử lý (I113):** 1 nhận định + checklist 3 mục (chọn mã theo sàn/thanh khoản/lợi nhuận; kiểm tra BCTC; đặt lệnh theo lô 100) + CTA có link https://www.dsc.com.vn/mo-tai-khoan; CTA đúng P2: "Mở tài khoản — 3 phút" + Môi giới 1:1. Giữ lưu ý miễn trừ (đặt trước CTA hoặc ngay sau, không dùng ngoặc kép nhấn mạnh).
- **Word count target:** ~130 từ

---

## 5. Đề xuất Thêm mới (Content Gaps)

✨ **[THÊM MỚI] H3: Công ty Cổ phần Cảng Hải Phòng**
- **Học từ đối thủ:** Competitor fhsc.com.vn (H3 PHP ~160 từ) + diendandoanhnghiep.vn (PHP lãi quý III/2026 ~430 tỷ, +65%; cả năm 1.240 tỷ, +50,6%; bến 3–4 Lạch Huyện hiệu suất ~48% sau 9 tháng).
- **Vị trí chèn:** ngay sau H3 "Công ty Cổ phần cảng Đà Nẵng", trước dòng ">> Xem thêm" (không đổi thứ tự 3 H3 cũ).
- **Nội dung chính:** khung Giới thiệu → Ưu → Nhược → Hợp với ai. Query `cổ phiếu cảng biển hải phòng` (related) được phục vụ.
- **Entities cần có:** `PHP`, `Lạch Huyện`, `HNX` (CẦN XÁC NHẬN sàn PHP; nguồn SERP stockkis ghi HNX), `cảng Hải Phòng`
- **Bằng chứng / Số liệu cần có:** giá 44,50, KLGD bq 478.376 (19/11/2026, `market_facts`); dự báo lợi nhuận MBS `[CẦN XÁC NHẬN]`.
- **Định dạng:** Đoạn văn + list Ưu/Nhược
- **Word count ước tính:** ~170 từ

✨ **[THÊM MỚI] H3: Công ty Cổ phần Container Việt Nam**
- **Học từ đối thủ:** Competitor fhsc.com.vn (H3 VSC ~290 từ) + diendandoanhnghiep.vn (VSC quý III/2026 +82% nhưng cả năm chỉ +8,5%; công suất Nam Hải Đình Vũ 73,6% vs 51,5%; giá dịch vụ +6,5%).
- **Vị trí chèn:** sau H3 Hải Phòng.
- **Nội dung chính:** VSC là mã khớp mạnh nhất nhóm (KLGD bq 11,48 triệu) nhưng lợi nhuận cả năm tăng thấp hơn quý III — chi tiết giúp người đọc không nhầm tăng trưởng 1 quý với cả năm. Link spoke có sẵn `co-phieu-vsc-tong-quan-danh-gia-va-ket-qua-kinh-doanh-moi-nhat`.
- **Entities cần có:** `VSC`, `Đình Vũ`, `container`, `công suất khai thác`
- **Bằng chứng / Số liệu cần có:** giá 13,05, vùng 12,65–15,50, KLGD bq 11.475.813 (19/11/2026); số quý III/2026 MBS `[CẦN XÁC NHẬN]`.
- **Định dạng:** Đoạn văn + list Ưu/Nhược
- **Word count ước tính:** ~170 từ

✨ **[THÊM MỚI] H2: Rủi ro khi đầu tư cổ phiếu cảng biển**
- **Học từ đối thủ:** Competitor stockkisvn.vn (H2 rủi ro ~150 từ), fhsc.com.vn (H3 thách thức ~250 từ).
- **Vị trí chèn:** sau H3 mới cuối cùng (sau VSC) và dòng ">> Xem thêm", **trước H2 Kết luận**.
- **Nội dung chính:** 4 rủi ro, mỗi rủi ro 1 số/ví dụ: phụ thuộc xuất nhập khẩu và giá cước; cạnh tranh công suất cảng mới (Cần Giờ, Lạch Huyện mở rộng `[CẦN XÁC NHẬN]`); giá nhiên liệu (HAH); thanh khoản thấp (CDN, SGP — KLGD bq 29.356). Link ngữ cảnh: `chu-ky-co-phieu-la-gi`, `bien-do-giao-dong-gia-co-phieu-la-gi` (Cluster 5j/1b). Không dựng thêm H2 cho nội dung đã có bài riêng (I118).
- **Entities cần có:** `giá cước`, `xuất nhập khẩu`, `thanh khoản`, `chu kỳ ngành`
- **Bằng chứng / Số liệu cần có:** SGP -8,1% phiên 19/11/2026 và KLGD thấp; HAH vùng giá thấp 44,90; mọi số khác `market_facts` hoặc `[CẦN XÁC NHẬN]`.
- **Định dạng:** List đậm nhãn (I115) + 1 câu dẫn
- **Word count ước tính:** ~150 từ

✨ **[THÊM MỚI] H2: Câu hỏi thường gặp về cổ phiếu cảng biển**
- **Học từ đối thủ:** Competitor fhsc.com.vn (FAQ cuối bài, 47 từ, quá ngắn); SERP không có PAA nên lấy Related Searches + GSC.
- **Vị trí chèn:** sau H2 Rủi ro, trước H2 Kết luận.
- **Nội dung chính:** 4 câu hỏi, câu đầu mỗi đáp án ≤ 60 từ, có số + mốc:
  1. Mã cổ phiếu cảng Cái Mép là gì? (GSC: 75 + 69 impressions, vị trí ~5; AI Overview nêu GMD qua Gemalink và SGP — **`[CẦN XÁC NHẬN]`** từ công bố thông tin hoặc báo cáo thường niên)
  2. Các mã cổ phiếu cảng biển nào niêm yết trên HOSE và HNX? (dùng cột Sàn của bảng)
  3. Cổ phiếu cảng biển và cổ phiếu vận tải biển khác nhau thế nào? (phục vụ `cổ phiếu vận tải biển`, 105 impr)
  4. Các mã cổ phiếu ngành logistics gồm những mã nào? (nhóm Logistics của bảng; Related Search)
- **Entities cần có:** `Cái Mép - Thị Vải`, `Cát Lái`, `HOSE`, `HNX`, `logistics`
- **Bằng chứng / Số liệu cần có:** đều rút từ bảng bài + `market_facts`; không câu nào dùng số chưa kiểm.
- **Định dạng:** FAQ (1 dòng trống giữa hỏi–đáp, I116)
- **Word count ước tính:** ~220 từ

> Nếu user duyệt: tổng H2 sau optimize = 4 cũ + 2 mới (Rủi ro, FAQ); H3 = 3 cũ + 2 mới. Không xóa/gộp/đổi thứ tự H2 hiện có. Không thêm H2 riêng cho Cái Mép (xử lý qua FAQ + cột bảng); nếu sau 4–6 tuần `cổ phiếu cảng cái mép` vẫn ở vị trí ~5 thì cân nhắc spoke riêng.

---

## 6. Chiến lược Internal Links
> Dùng URL tuyệt đối từ `find_links.py`; chỉ đặt trong câu có ngữ cảnh. Link live hiện có (bắt buộc giữ): `top-5-co-phieu-dang-dau-tu` (×2), `cach-mo-tai-khoan-chung-khoan`, `co-phieu-gmd-…`, `co-phieu-hah-…`, `top-co-phieu-nganh-duoc-nen-dau-tu`, `co-phieu-nganh-det-may`, `mo-tai-khoan`.

| Anchor Text đề xuất | Bài đích (slug) | Vị trí chèn |
| :--- | :--- | :--- |
| cổ phiếu VSC | co-phieu-vsc-tong-quan-danh-gia-va-ket-qua-kinh-doanh-moi-nhat | H3: Công ty Cổ phần Container Việt Nam (mới) |
| vốn hóa | von-hoa-thi-truong-la-gi | H2: Top mã cổ phiếu… (câu nói về vốn hóa) |
| biên độ dao động giá | bien-do-giao-dong-gia-co-phieu-la-gi | H2: Top mã… hoặc H3 CDN |
| chu kỳ của cổ phiếu | chu-ky-co-phieu-la-gi | H2: Rủi ro khi đầu tư cổ phiếu cảng biển |
| cách chọn cổ phiếu tốt | 3-cach-chon-co-phieu-tot-va-co-tiem-nang-tang-gia-de-dau-tu | H2: Kết luận (checklist) |

Không có spoke riêng cho PHP, CDN, SGP, MVN trong registry → không tạo link tới URL chưa có. **Backfill link tới bài này:** `find_links.py --backfill` báo "Không có bài nào phù hợp" → bỏ qua. Bài `co-phieu-gmd/hah/vsc-...` (cùng cụm 5g) hiện đã link lên bài này (đang là hub); không sửa trong phạm vi bài này.

📎 **Backfill Link Suggestions:** (không có).

---

## 7. Chiến lược Hình ảnh (Image Strategy & Preservation)

### 7.1 Danh sách hình ảnh GỐC cần bảo toàn (BẮT BUỘC) — toàn bộ 1 ảnh
| Cú pháp Markdown ảnh gốc | Vị trí hiện tại | Hướng xử lý |
| :--- | :--- | :--- |
| `![Tổng quan ngành cảng biển](https://extgw.dsc.com.vn/eback/uploads/danh_sach_co_phieu_cang_bien_733c1465ab.jpg)` | Dưới H2: Nhận định về ngành cảng biển (trước H2 Danh sách mã) | Giữ URL và vị trí; đổi alt thành "Tổng quan cổ phiếu ngành cảng biển Việt Nam" (chứa keyword). Khi sang CMS HTML, URL tự đổi sang `/uploads/` theo `md_to_cms_html.py` |

### 7.2 Gợi ý vị trí đặt ảnh mới (skill `/image`, bước Optimize)
| Vị trí đề xuất | Concept ảnh gợi ý | Alt text tối ưu SEO chứa keyword |
| :--- | :--- | :--- |
| Dưới bảng so sánh ở H2: Top mã cổ phiếu… | Biểu đồ cột ngang KLGD bình quân 20 phiên của 6 mã (số khớp bảng; infographic vẽ bằng code, 800×500) | `Thanh khoản các cổ phiếu cảng biển GMD, HAH, VSC, PHP, CDN (20 phiên đến 19/11/2026)` |
| Dưới H2: Danh sách mã… (sau bảng) — tùy chọn | Sơ đồ ba cụm cảng (Hải Phòng–Lạch Huyện, Cái Mép–Thị Vải, Sài Gòn–Cát Lái) gắn mã cổ phiếu; chỉ vẽ sau khi xác minh cột Cụm cảng | `Các mã cổ phiếu cảng biển theo cụm cảng Hải Phòng, Cái Mép và Sài Gòn` |

---

## 8. Điều cần user quyết trước `/approve`
1. Đồng ý **giữ nguyên Title/H1** (miễn trừ lint `CL1-h1`) và chỉ đổi Meta? Hay muốn thử Title có cụm "Cổ phiếu cảng biển" (có rủi ro, ghi ở Section 0)?
2. Đồng ý thêm 2 H3 (PHP, VSC) trong H2 "Top mã" và 2 H2 mới (Rủi ro, FAQ) đặt trước Kết luận?
3. Nguồn dự báo quý III/2026 là MBS qua bài báo, không có trong whitelist: duyệt cách "ghi tên + tháng, không link, bắt buộc kiểm lại bản gốc"; nếu không kiểm được thì thay bằng BCTC quý III/2026 từ hsx.vn/hnx.vn?
4. Giá/vốn hóa lấy từ `market_facts` (19/11/2026) và phải chạy lại ngay trước khi viết.

## Danh sách số cần xác nhận khi viết (không bịa)
- Số mã cảng biển niêm yết hiện tại (bài ghi 18) và sàn từng mã; VTP, SWC có nên nằm trong bảng.
- Cụm cảng của từng mã; mã gắn với cảng Cái Mép/Cát Lái (AI Overview và SERP nêu GMD, SGP, TCL — chưa xác minh).
- Số dự báo MBS quý III/2026 (GMD 587 tỷ +86%, PHP 430 tỷ +65%, VSC 146 tỷ +82%, HAH 339 tỷ +12%), tăng trưởng XNK ~30%, lượng hàng ~22%, giá xếp dỡ +10–15%.
- Số CDN 2021 ("300,000 tỷ", +61 tỷ, gấp 4 lần) — nghi sai.
- SGP -8,1% ngày 19/11/2026 (lý do).
- Giá GMD trong bài báo (77.800) lệch `market_facts` (51,10): chỉ dùng `market_facts`.
