---
Author: Chứng khoán DSC
Status: Outline
Pipeline_Mode: Guided
SERP_Research: true
SERP_Status: ok
SERP_Format:
  dominant: definition
  share: 50
  verdict: BẮT BUỘC

# SEO Technical
Target_Keyword: dòng tiền tự do là gì
Secondary_Keywords:
  - FCF là gì
  - free cash flow là gì
  - công thức tính dòng tiền tự do
  - FCFF và FCFE
LSI_Keywords:
  - lưu chuyển tiền thuần từ hoạt động kinh doanh
  - chi phí vốn CapEx
  - báo cáo lưu chuyển tiền tệ
  - mẫu B03-DN
  - lợi nhuận sau thuế
  - cổ tức tiền mặt
  - định giá DCF
Entities: [cổ tức, thanh toán, thể hiện, tổng thể, FCFF, FCFE, CapEx, Thông tư 200/2014/TT-BTC, Thông tư 99/2025/TT-BTC, HPG, VNM, FPT]
Entities_Skipped: []
Search_Intent: Informational
Content_Type: Definition
Format_Deviation: ""
Featured_Snippet: Paragraph
Word_Count_Target: 2100

# Lập trường
Thesis: "Dòng tiền tự do cho biết doanh nghiệp thật sự còn bao nhiêu tiền mặt sau khi nuôi bộ máy và đầu tư tài sản, nên đọc FCF cạnh lợi nhuận mới thấy lãi trên sổ sách có thành tiền hay không. FCF âm chỉ đáng lo khi dòng tiền kinh doanh yếu; FCF âm vì đang xây nhà máy là chuyện khác, và với ngân hàng thì không dùng chỉ số này."
Information_Gain:
  - claim: "Tính FCF năm 2025 từ BCTC hợp nhất kiểm toán của 3 doanh nghiệp niêm yết (HPG, VNM, FPT), đặt cạnh LNST để thấy tỷ lệ chuyển lợi nhuận thành tiền"
    h2: "Ví dụ tính FCF từ báo cáo tài chính 2025 của HPG, VNM và FPT"
    type: calc
    proof: "84,5%"
  - claim: "Chỉ đúng mã số dòng cần lấy trên mẫu B03-DN theo Thông tư 200/2014/TT-BTC (mã số 20 trừ mã số 21) và lưu ý BCTC năm tài chính từ 01/01/2026 lập theo Thông tư 99/2025/TT-BTC"
    h2: "Công thức tính dòng tiền tự do trên báo cáo tài chính Việt Nam"
    type: regulation
    proof: "mã số 21"
  - claim: "So sánh cổ tức tiền mặt đã trả năm 2025 với FCF cùng năm để kiểm tra cổ tức có được dòng tiền tự do chống lưng"
    h2: "Cách đọc FCF dương, âm và ngưỡng theo ngành"
    type: calc
    proof: "155,6%"

# Audience & Brand
Persona: P2 — F0 đang học phân tích cơ bản (đọc BCTC để chọn cổ phiếu đầu tiên)
Tone: Chính xác, đi thẳng vào số; giải thích thuật ngữ ngay lần đầu nhắc; có lập trường
Writer_Profile: analytical
Writing_Method: PAS
Core_Products:
  - product: "Môi giới 1:1"
    benefit: "Chuyên gia DSC cùng đọc báo cáo lưu chuyển tiền tệ của mã nhà đầu tư đang cân nhắc trước lệnh đầu tiên"
  - product: "eKYC trên App DSC Trading"
    benefit: "Mở tài khoản 3 phút để mua cổ phiếu sau khi đã lọc doanh nghiệp có FCF dương"

# Anti-AI
Anti_AI_Flags:
  - Gọi FCF là "chỉ số quan trọng nhất" mà không chứng minh
  - Liệt kê ưu/nhược FCF đối xứng giả
  - Ví dụ số giả định thay vì BCTC thật (I128)
  - Tự đặt giá mục tiêu hay khuyến nghị mua HPG/VNM/FPT
  - Nhắc FCF cho ngân hàng như doanh nghiệp thường

# GEO/AEO
GEO_Compliance: true
PAA_Questions:
  - q: "Dòng tiền tự do âm có phải doanh nghiệp đang gặp khó khăn?"
    placement: faq
    source: inferred
  - q: "FCF khác gì dòng tiền từ hoạt động kinh doanh?"
    placement: faq
    source: inferred
  - q: "Ngân hàng có tính dòng tiền tự do không?"
    placement: faq
    source: inferred
  - q: "FCF yield là gì?"
    placement: faq
    source: inferred
Related_Searches:
  same_intent:
    - Fcff là gì
    - Fcfe là gì
    - Fcff khác gì fcfe
    - Công thức tính FCFF
  spin_off:
    - Bài tập tính FCFF và FCFE
    - Dòng tiền thuần là gì
    - Cách tính dòng tiền thuần
    - Fcinv là gì

# Cluster
Cluster: "Cluster 1: So sánh Lãi suất & Tối ưu dòng vốn"
Cluster_Role: Cluster
Internal_Links:
  - anchor: "báo cáo lưu chuyển tiền tệ"
    url: "https://www.dsc.com.vn/kien-thuc/bao-cao-luu-chuyen-tien-te-la-gi"
    suggested_placement: "H2 Công thức — câu nói FCF lấy số từ báo cáo lưu chuyển tiền tệ"
  - anchor: "dòng tiền từ hoạt động kinh doanh (OCF)"
    url: "https://www.dsc.com.vn/kien-thuc/dong-tien-tu-hoat-dong-kinh-doanh-ocf-la-gi"
    suggested_placement: "H2 Định nghĩa — câu tách FCF khỏi OCF"
  - anchor: "chi phí vốn CapEx"
    url: "https://www.dsc.com.vn/kien-thuc/chi-phi-von-capex-la-gi-y-nghia-va-cach-tinh-chi-phi-von"
    suggested_placement: "H2 Công thức — câu giải thích dòng mã số 21"
  - anchor: "định giá DCF"
    url: "https://www.dsc.com.vn/kien-thuc/dcf-la-gi"
    suggested_placement: "H3 FCFF và FCFE — câu nói FCFF là đầu vào của mô hình chiết khấu dòng tiền"
  - anchor: "EBITDA"
    url: "https://www.dsc.com.vn/kien-thuc/ebitda-la-gi-giai-ma-chi-tiet-ve-chi-so-tai-chinh-quan-trong-nay"
    suggested_placement: "H2 Sai lầm — câu nói EBITDA không trừ CapEx"
  - anchor: "cổ tức"
    url: "https://www.dsc.com.vn/kien-thuc/co-tuc-la-gi"
    suggested_placement: "H2 Cách đọc FCF — câu so cổ tức tiền mặt với FCF"
  - anchor: "mở tài khoản chứng khoán DSC"
    url: "https://www.dsc.com.vn/mo-tai-khoan"
    suggested_placement: "H2 Bridge DSC + Kết luận"
---

# SEO Content Outline: Dòng tiền tự do là gì

- **Title:** Dòng tiền tự do là gì? Công thức FCF và ví dụ BCTC 2025
- **H1:** Dòng tiền tự do là gì? Cách tính FCF từ báo cáo tài chính
- **Sapo:** Đoạn 1: dòng tiền tự do là gì — trả lời thẳng (CFO trừ CapEx, tiền doanh nghiệp còn lại để trả cổ tức, trả nợ, tích lũy) + 1 số thật của BCTC 2025. Đoạn 2: DSC + phạm vi (công thức theo mẫu B03-DN, ví dụ 3 doanh nghiệp niêm yết, cách đọc FCF âm) + câu mời đọc tiếp gắn lợi ích: lọc được doanh nghiệp lãi thật trước khi mua cổ phiếu.
- **Meta description:** Dòng tiền tự do là gì? FCF bằng dòng tiền kinh doanh trừ CapEx. Cách lấy số trên mẫu B03-DN, ví dụ HPG, VNM, FPT năm 2025 và cách đọc FCF âm.

## 1. SERP & Intent

**Khung bài thắng SERP:**

| # | Domain | Loại bài | Số từ |
|---|---|---|---|
| 1 | studocu.vn | guide (tài liệu, bị chặn) | - |
| 2 | bizzi.vn | definition (FCFE) | 2012 |
| 3 | topi.vn | definition (cash flow) | 3137 |
| 4 | nghiencuu.tapchikinhtetaichinh.vn | guide (nghiên cứu) | 3898 |
| 6 | ub.edu.vn | definition | - |
| 9 | vimo.cuthongthai.vn | definition | - |

**Kết luận khung:** Definition (X là gì). Top 3 thật đều mở bằng định nghĩa rồi tới công thức; không ai làm toplist hay how-to. Bài theo khung định nghĩa → công thức → ví dụ → cách đọc.
**Intent:** Nhà đầu tư mới gặp chữ FCF trong báo cáo phân tích, muốn biết nó là gì, tự tính được từ BCTC và dùng để loại doanh nghiệp lãi trên giấy.

### Competitor 1: bizzi.vn
- URL: https://bizzi.vn/fcfe-la-gi/
- Khung: definition (FCFE) · 2012 từ
- Điểm: Độ sâu 6 · Trình bày 7 · SEO 6 · UX 6 = 25/40
- Mạnh: bảng phân biệt FCFE với FCFF, NI, cổ tức, EBITDA · Thiếu: chỉ nói FCFE, không có ví dụ doanh nghiệp niêm yết, góc nhìn kế toán doanh nghiệp chứ không phải nhà đầu tư

### Competitor 2: topi.vn
- URL: https://topi.vn/cash-flow-la-gi.html
- Khung: definition (cash flow) · 3137 từ
- Điểm: Độ sâu 5 · Trình bày 6 · SEO 6 · UX 6 = 23/40
- Mạnh: phân loại CFO/CFI/CFF đầy đủ · Thiếu: FCF chỉ 99 từ, không ví dụ số, lệch sang dự báo dòng tiền nội bộ

### Competitor 3: nghiencuu.tapchikinhtetaichinh.vn
- URL: https://nghiencuu.tapchikinhtetaichinh.vn/dong-tien-tu-do-trong-cac-phan-khuc-dich-vu-logistics-tai-viet-nam-phan-tich-so-sanh-duoi-goc-do-fcff-va-fcfe-138625.html
- Khung: bài nghiên cứu · 3898 từ
- Điểm: Độ sâu 8 · Trình bày 4 · SEO 4 · UX 4 = 20/40
- Mạnh: có số liệu FCFF/FCFE ngành logistics · Thiếu: văn học thuật, không có heading, không hướng dẫn nhà đầu tư cá nhân

## 2. Competitor Gap Synthesis
- **Gaps:** Không đối thủ nào tính FCF từ BCTC thật của doanh nghiệp niêm yết năm 2025; không ai chỉ mã số dòng trên mẫu B03-DN; không ai nói FCF không áp dụng cho ngân hàng; không ai so cổ tức tiền mặt với FCF.
- **Chủ đề con đối thủ đều có:** định nghĩa → H2 1; công thức → H2 2; FCFF/FCFE → H3; so với lợi nhuận/EBITDA/cổ tức → H2 4 và H2 5. Dự báo dòng tiền nội bộ (topi) bỏ: lệch intent nhà đầu tư.
- **Unique angle DSC:** đọc FCF từ góc nhà đầu tư cổ phiếu, với số BCTC 2025 thật và bảng ngưỡng theo ngành.
- **Featured Snippet target:** Paragraph 40–60 từ ngay dưới H2 định nghĩa; AI Overview đang trích định nghĩa "tiền mặt còn lại sau chi phí hoạt động và CapEx".
- **PAA plan:** SERP không có PAA → 4 câu FAQ tự suy (source: inferred). FCFF/FCFE (related) → H3 thân bài. Bài tập FCFF/FCFE, dòng tiền thuần → spin-off.
- **Cannibalization:** GSC 90 ngày: chỉ `dong-tien-tu-hoat-dong-kinh-doanh-ocf-la-gi` có 1 impression ở vị trí 59 cho cụm này. Ranh giới: bài OCF giải thích dòng tiền kinh doanh; bài này lấy OCF làm đầu vào, link chéo 2 chiều.

## 3. Dữ liệu dùng trong bài

| Dữ kiện | Số liệu | Mốc thời gian | Nguồn | Trạng thái |
|---|---|---|---|---|
| Mẫu báo cáo lưu chuyển tiền tệ B03-DN: lưu chuyển tiền thuần từ HĐKD = mã số 20; tiền chi mua sắm, xây dựng TSCĐ = mã số 21; tiền thu thanh lý TSCĐ = mã số 22 | mã số 20, 21, 22 | 22/12/2014 | https://vanban.chinhphu.vn/?pageid=27160&docid=178998 | ✓ đã kiểm |
| Thông tư 99/2025/TT-BTC thay Thông tư 200, áp dụng cho năm tài chính bắt đầu từ 01/01/2026 | 01/01/2026 | 27/10/2025 | https://portal.mof.gov.vn/hoidapcstc/home/cthoidap/159102 | ✓ đã kiểm |
| HPG 2025: CFO 17.365,86 · CapEx (25.748,32) · LNST 15.514,93 tỷ VNĐ → FCF −8.382,46 tỷ, FCF/LNST −54,0% | 2024: CFO 6.608,32 · CapEx (35.495,03) · LNST 12.020,02 → FCF −28.886,71 | BCTC hợp nhất kiểm toán 2025, công bố 27/03/2026 | https://file.hoaphat.com.vn/hoaphat-com-vn/2026/03/20260327-hpg-bctc-hop-nhat-nam-2025-sau-kiem-toan.pdf | ✓ đã kiểm |
| VNM 2025: CFO 8.948,88 · CapEx (1.762,01) · LNST 8.505,22 · cổ tức tiền mặt đã trả 11.181,26 tỷ VNĐ → FCF 7.186,87 tỷ, FCF/LNST 84,5%, cổ tức/FCF 155,6% | 2024: CFO 9.770,59 · CapEx (1.741,50) · LNST 8.686,25 · cổ tức 8.046,33 → FCF 8.029,09, FCF/LNST 92,4%, cổ tức/FCF 100,2% | BCTC hợp nhất 2025 trong Báo cáo thường niên 2025, 19/03/2026 | https://www.vinamilk.com.vn/investor/reports/annual | ✓ đã kiểm |
| FPT 2025: CFO 10.136,04 · CapEx (5.097,92) · LNST 11.232,34 · cổ tức tiền mặt đã trả 4.573,75 tỷ VNĐ → FCF 5.038,12 tỷ, FCF/LNST 44,9%, cổ tức/FCF 90,8% | 2024: CFO 11.703,78 · CapEx (3.275,31) · LNST 9.427,42 · cổ tức 3.291,86 → FCF 8.428,47, FCF/LNST 89,4%, cổ tức/FCF 39,1% | BCTC hợp nhất kiểm toán 2025, ký 18/03/2026 | https://fpt.com/api/media/20260319_fpt_audited_consolidated_financial_statements_for_2025_f29f536732.pdf | ✓ đã kiểm |

## 4. Brand Context (output Brand Guardian)
- **Writer Profile:** analytical — 3 đặc điểm tone: data trước, giải thích sau · có nhận định rõ (nói thẳng khi nào FCF âm đáng lo) · súc tích, không khen chỉ số. Persona P2 nên mỗi thuật ngữ (CapEx, CFO, FCFF) giải thích 1 mệnh đề ở lần đầu nhắc.
- **USP bắt buộc:** Môi giới 1:1 (cùng đọc BCTC mã đang cân nhắc); eKYC 3 phút trên App DSC Trading; phí giao dịch từ 0,1%. Không nhắc DSC Invest (P2), không nhắc phái sinh/quỹ mở (I111).
- **Lỗi cũ cần tránh với chủ đề này:** I128 ví dụ phải từ BCTC thật + bảng ngưỡng theo ngành; I123 có phần nền (công thức, cấu tạo) và phần thực hành; I108 không nhân vật có tên; I110 số có nguồn + ngày; I120 không tự đặt giá mục tiêu hay khuyến nghị mã.
- **Xung đột instinct ↔ phản hồi user:** Không có.

## 5. Cấu trúc nội dung

### H1: Dòng tiền tự do là gì? Cách tính FCF từ báo cáo tài chính
- **Max word count:** 110

### H2: Dòng tiền tự do (FCF) là gì?
- **Câu hỏi người đọc:** FCF là gì và khác gì lợi nhuận tôi vẫn thấy trên báo cáo?
- **Ý chính:** FCF là tiền mặt thật còn lại sau khi trả chi phí hoạt động và đầu tư tài sản; lợi nhuận là số kế toán, có thể dương trong khi tiền mặt đang chảy ra.
- **Nội dung chính:** định nghĩa 40–60 từ (snippet) → tách FCF khỏi OCF (OCF chưa trừ CapEx) → tách khỏi LNST (khoản phải thu, hàng tồn kho làm lợi nhuận chưa thành tiền) → doanh nghiệp dùng FCF để làm gì: trả cổ tức, trả nợ, mua lại cổ phiếu, tích lũy.
- **Bằng chứng thực tế:** HPG 2025: lãi 15.515 tỷ nhưng FCF −8.382 tỷ (dòng HPG mục 3).
- **GEO_Load_Bearing:** FCF bằng lưu chuyển tiền thuần từ hoạt động kinh doanh trừ tiền chi mua sắm TSCĐ, hai dòng có sẵn trên báo cáo lưu chuyển tiền tệ của mọi doanh nghiệp niêm yết.
- **Chuyển ý → H2 sau:** biết định nghĩa rồi thì cần biết lấy 2 con số đó ở dòng nào của BCTC.
- **Không viết:** giải thích chi tiết 3 nhóm dòng tiền (đã có bài báo cáo lưu chuyển tiền tệ — chỉ link).
- **Target:** 230

### H2: Công thức tính dòng tiền tự do trên báo cáo tài chính Việt Nam
- **Câu hỏi người đọc:** Tôi mở BCTC ra thì lấy số ở đâu, cộng trừ thế nào?
- **Ý chính:** Với BCTC Việt Nam, FCF = mã số 20 + mã số 21 (mã số 21 đã mang dấu âm) trên mẫu B03-DN; cộng mã số 22 nếu muốn tính FCF ròng sau thanh lý tài sản.
- **Nội dung chính:** công thức FCF = CFO − CapEx (in đậm, không LaTeX) → bảng 3 dòng mã số 20/21/22 với tên dòng nguyên văn → lưu ý dấu âm trong ngoặc đơn → lưu ý TT99 áp dụng từ năm tài chính 2026, tên dòng/mã số cần đối chiếu khi đọc BCTC 2026.
- **Bằng chứng thực tế:** dòng 1–2 mục 3.
- **GEO_Load_Bearing:** Theo mẫu B03-DN ban hành kèm Thông tư 200/2014/TT-BTC, lưu chuyển tiền thuần từ hoạt động kinh doanh nằm ở mã số 20 và tiền chi mua sắm, xây dựng TSCĐ nằm ở mã số 21.
- **Chuyển ý → H2 sau:** công thức có 2 biến thể FCFF và FCFE mà báo cáo phân tích hay dùng.
- **Không viết:** cách lập báo cáo lưu chuyển tiền tệ theo phương pháp trực tiếp/gián tiếp.
- **Target:** 230

#### H3: FCFF và FCFE khác nhau thế nào?
- **Nội dung chính:** bảng đối sánh FCFF (dòng tiền cho toàn bộ chủ nợ và cổ đông, đầu vào định giá DCF theo WACC) vs FCFE (phần còn lại cho cổ đông sau trả nợ gốc, lãi vay; đầu vào định giá theo chi phí vốn chủ). Công thức rút gọn: FCFF = CFO + lãi vay × (1 − thuế suất) − CapEx; FCFE = CFO − CapEx + vay mới − trả nợ gốc. Nhà đầu tư cá nhân dùng FCF đơn giản là đủ để lọc.
- **Target:** 200

### H2: Ví dụ tính FCF từ báo cáo tài chính 2025 của HPG, VNM và FPT
- **Câu hỏi người đọc:** Áp vào doanh nghiệp thật thì số ra sao?
- **Ý chính:** Cả 3 doanh nghiệp đều lãi năm 2025, nhưng VNM chuyển 84,5% lợi nhuận thành tiền tự do, FPT 44,9%, còn HPG âm vì vẫn rót 25.748 tỷ vào tài sản cố định.
- **Nội dung chính:** bảng 3 mã: CFO · CapEx · FCF · LNST · FCF/LNST, năm 2025 (có thêm 2024 nếu cần thấy xu hướng) → 1 đoạn đọc bảng theo từng nhóm. Không khuyến nghị mua/bán.
- **Bằng chứng thực tế:** dòng BCTC 2025 mục 3.
- **GEO_Load_Bearing:** Năm 2025, Vinamilk (VNM) chuyển 84,5% lợi nhuận sau thuế thành dòng tiền tự do, trong khi Hòa Phát (HPG) có FCF âm 8.382 tỷ VNĐ dù lãi 15.515 tỷ VNĐ, theo BCTC hợp nhất kiểm toán của hai doanh nghiệp.
- **Chuyển ý → H2 sau:** có số rồi, câu hỏi tiếp theo là FCF âm hay dương thì nghĩa là gì với từng ngành.
- **Không viết:** phân tích toàn diện từng doanh nghiệp (đã có bài cổ phiếu HPG riêng — chỉ link nếu cần).
- **Target:** 320

### H2: Cách đọc FCF dương, âm và ngưỡng theo ngành
- **Câu hỏi người đọc:** FCF âm có phải dấu hiệu xấu không, và ngành nào nhìn khác?
- **Ý chính:** FCF âm do CFO âm là cảnh báo; FCF âm do CapEx mở rộng trong khi CFO dương là đầu tư, cần xem dự án đã chạy chưa. Ngân hàng, công ty chứng khoán không dùng FCF.
- **Nội dung chính:** bảng 4 tình huống (CFO dương/âm × CapEx lớn/nhỏ) → bảng ngưỡng theo ngành (bán lẻ, tiêu dùng, công nghệ, thép/BĐS, ngân hàng) → so cổ tức tiền mặt đã trả với FCF 2025 của 3 mã: cổ tức lớn hơn FCF nhiều năm liền = đang trả bằng tiền vay hoặc tiền tích lũy.
- **Bằng chứng thực tế:** dòng cổ tức tiền mặt 2025 mục 3.
- **GEO_Load_Bearing:** Vinamilk trả 11.181 tỷ VNĐ cổ tức tiền mặt năm 2025, bằng 155,6% dòng tiền tự do cùng năm theo BCTC hợp nhất 2025.
- **Chuyển ý → H2 sau:** đọc đúng chiều rồi vẫn có những lỗi phổ biến khi dùng FCF.
- **Không viết:** chiến lược đầu tư cổ tức (có bài riêng — 1 câu + link).
- **Target:** 300

### H2: Sai lầm thường gặp khi phân tích dòng tiền tự do
- **Câu hỏi người đọc:** Tôi dễ đọc sai FCF ở đâu?
- **Ý chính:** Một năm FCF không nói lên gì; cần chuỗi 3–5 năm và đọc cùng nợ vay.
- **Nội dung chính:** list 4–5 lỗi có nhãn đậm: nhìn 1 năm; dùng EBITDA thay FCF (EBITDA không trừ CapEx); quên dấu âm mã số 21; áp FCF cho ngân hàng; coi FCF dương nhờ cắt CapEx bảo trì là tốt.
- **Bằng chứng thực tế:** FPT: FCF/LNST giảm từ 89,4% (2024) xuống 44,9% (2025) khi CapEx tăng từ 3.275 lên 5.098 tỷ.
- **GEO_Load_Bearing:** EBITDA không trừ chi phí đầu tư tài sản cố định nên một doanh nghiệp có EBITDA dương vẫn có thể có FCF âm.
- **Chuyển ý → H2 sau:** đọc dòng tiền cho từng mã tốn thời gian; đây là chỗ có người cùng đọc giúp ích.
- **Không viết:** rủi ro đầu tư cổ phiếu nói chung.
- **Target:** 200

### H2: Đọc báo cáo dòng tiền trước lệnh đầu tiên cùng Môi giới 1:1 tại DSC
- **Câu dẫn từ kết luận bài:** lọc FCF xong mới chỉ loại được doanh nghiệp yếu; mua mã nào, giá nào vẫn cần tài khoản và người đối chiếu. DSC không đặt giá mục tiêu hay quyết định thay nhà đầu tư.
- **Bước cụ thể tại DSC:** mở tài khoản eKYC 3 phút trên App DSC Trading → gửi Môi giới 1:1 mã đang cân nhắc để cùng đọc báo cáo lưu chuyển tiền tệ 3–5 năm → đặt lệnh với phí giao dịch từ 0,1% (ví dụ lệnh 50 triệu = phí 50.000 VNĐ). Bảng so tự làm một mình vs có Môi giới 1:1 (I112), không so phí với CTCK khác khi không có nguồn công khai.
- **Target:** 200

### H2: Câu hỏi thường gặp về dòng tiền tự do
- `#### Câu hỏi?` → câu đầu ≤ 60 từ, có entity + số/mốc.
- **Q1:** Dòng tiền tự do âm có phải doanh nghiệp đang gặp khó khăn? · **Q2:** FCF khác gì dòng tiền từ hoạt động kinh doanh? · **Q3:** Ngân hàng có tính dòng tiền tự do không? · **Q4:** FCF yield là gì?
- **Word count:** ~220 (không ghi Target: count_words.py không cộng H3 câu hỏi vào H2 FAQ)

### H2: Kết luận
- **Ý chính:** FCF là phép thử lợi nhuận có thành tiền hay không; đọc chuỗi nhiều năm, tách FCF âm do đầu tư khỏi FCF âm do kinh doanh yếu, bỏ qua với ngân hàng. Checklist 3 mục: lấy mã số 20 và 21 của 3–5 năm · tính FCF/LNST · so cổ tức tiền mặt với FCF.
- **CTA:** mở tài khoản chứng khoán DSC — 3 phút, hoàn toàn online.
- **Target:** 100

## 6. Liên kết & yếu tố trực quan
- **External links:** Thông tư 200/2014/TT-BTC (vanban.chinhphu.vn) tại câu mã số 20/21; hỏi đáp Bộ Tài chính về Thông tư 99/2025/TT-BTC (mof.gov.vn) tại câu hiệu lực 01/01/2026; file BCTC trên trang IR của HPG, VNM, FPT tại bảng ví dụ (thêm hoaphat.com.vn, vinamilk.com.vn, fpt.com vào source-whitelist mục doanh nghiệp).
- **Bằng chứng thực tế (first-hand):** phép tính FCF, FCF/LNST, cổ tức/FCF do DSC tự tính từ BCTC kiểm toán 2025.
- **Spin-off candidates:** bài tập FCFF/FCFE, dòng tiền thuần là gì → chưa có bài, ghi serp-opportunities.
- **Yếu tố trực quan:** bảng mã số B03-DN, bảng FCFF vs FCFE, bảng 3 doanh nghiệp, bảng tình huống CFO × CapEx, bảng ngưỡng theo ngành, banner CTA.

## 7. Revision Log
- **v1.0 (2026-11-10):** SERP DataForSEO 9 organic, extract 5 (3 hợp lệ). Số liệu BCTC 2025 đọc từ file gốc; MWG bỏ vì chỉ tìm được bản lưu trên trang tổng hợp (24hmoney), ngoài whitelist. Keyword chọn sau khi loại quantitative trading (đã live) và ROAA (Google gộp intent với ROA).
