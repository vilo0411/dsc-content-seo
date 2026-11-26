---
Author: Chứng khoán DSC
Status: Outline
Created: 2026-11-26
Updated: 2026-11-26
Pipeline_Mode: Auto
SERP_Research: true
SERP_Status: degraded
SERP_Format:
  dominant: toplist
  share: 42
  verdict: NGHIÊNG VỀ
  list_count_median: 6

# SEO Technical
Target_Keyword: thị trường sơ cấp và thứ cấp là gì
Secondary_Keywords: [thị trường sơ cấp là gì, thị trường thứ cấp là gì, thị trường sơ cấp và thị trường thứ cấp, phân biệt thị trường sơ cấp và thị trường thứ cấp, sơ cấp và thứ cấp là gì]
LSI_Keywords: [phát hành lần đầu, IPO, niêm yết, huy động vốn, thanh khoản, nhà phát hành, mua đi bán lại]
Entities: [phát hành, huy động vốn, nhà phát hành, bán chứng khoán, IPO, Luật Chứng khoán, Ủy ban Chứng khoán Nhà nước, HOSE, HNX, UPCoM, thanh khoản, T+2, công ty đại chúng, bảo lãnh phát hành, OTC]
Entities_Skipped: [câu trắc nghiệm, lời giải, k lượt thithi ngay, tiếp tục với google, đăng nhập bằng email, trải nghiệm miễn phí, giá chỉ từ k, nâng cấp vip, giao bài, bắt đầu thi, giáo viên, học sinh, cuối kì, tiếng anh, hà nội, liên kết, tốt nghiệp thpt, vietjackteam gmail, nhà nước — giao diện trang đề thi vietjack/scribd, không phải thuật ngữ chủ đề]
Search_Intent: Informational
Content_Type: Comparison
Format_Deviation: "SERP degraded: top 10 (DataForSEO, refetch 26/11/2026) toàn trang câu trắc nghiệm vietjack và PDF scribd, không có bài cùng loại; nhãn toplist đến từ tiêu đề 'Những đặc điểm…'. Keyword là cặp khái niệm cần phân biệt → khung Comparison (định nghĩa + bảng 6 điểm khác nhau). Chạy --auto theo yêu cầu user, không chờ duyệt."
Featured_Snippet: Table
Word_Count_Target: 1550 – 1800

# Lập trường
Thesis: "Ranh giới giữa sơ cấp và thứ cấp nằm ở chỗ tiền của bạn chảy vào doanh nghiệp hay vào túi nhà đầu tư khác. Gần như mọi lệnh mua trên app chứng khoán là thứ cấp, nên F0 cần hiểu thứ cấp trước, coi sơ cấp là cơ hội phụ có điều kiện."
Information_Gain:
  - claim: "Ví dụ dòng tiền bằng số: một đợt IPO 10 triệu cổ phiếu giá 20.000 VNĐ đưa 200 tỷ VNĐ vào doanh nghiệp, còn 750 tỷ VNĐ giao dịch sau niêm yết không mang thêm đồng nào cho doanh nghiệp"
    h2: "Tiền của nhà đầu tư đi về đâu ở mỗi thị trường"
    type: calc
    proof: "750 tỷ VNĐ"
  - claim: "Bảng 6 tình huống mua thường gặp của nhà đầu tư cá nhân và tình huống đó thuộc thị trường nào (IPO, quyền mua phát hành thêm, khớp lệnh trên HOSE, mua cổ phiếu OTC từ người khác, trái phiếu mua lần đầu, chứng chỉ ETF trên sàn)"
    h2: "Bạn đang mua ở thị trường nào: 6 tình huống thường gặp"
    type: comparison
    proof: "quyền mua cổ phiếu phát hành thêm"
  - claim: "Điều kiện pháp lý để cổ phiếu đi từ sơ cấp sang thứ cấp theo Luật Chứng khoán 2019: vốn điều lệ đã góp từ 30 tỷ VNĐ, tối thiểu 15% cổ phiếu có quyền biểu quyết bán cho ít nhất 100 nhà đầu tư không phải cổ đông lớn"
    h2: "Điều kiện để cổ phiếu đi từ thị trường sơ cấp sang thứ cấp"
    type: regulation
    proof: "ít nhất 100 nhà đầu tư không phải cổ đông lớn"

EAV:
  - attribute: "người bán"
    entity: "Thị trường sơ cấp"
    value: "tổ chức phát hành"
    source: "https://vanban.chinhphu.vn/default.aspx?pageid=27160&docid=198541"
    type: root
    h2: "6 điểm khác nhau giữa thị trường sơ cấp và thứ cấp"
  - attribute: "người bán"
    entity: "Thị trường thứ cấp"
    value: "nhà đầu tư đang nắm giữ"
    source: "calc"
    type: root
    h2: "6 điểm khác nhau giữa thị trường sơ cấp và thứ cấp"
  - attribute: "thời điểm cổ phiếu về tài khoản"
    entity: "Thị trường thứ cấp"
    value: "13h ngày T+2"
    source: "market_facts"
    type: rare
    h2: "6 điểm khác nhau giữa thị trường sơ cấp và thứ cấp"
  - attribute: "biên độ dao động giá"
    entity: "Sàn HOSE"
    value: "±7%"
    source: "market_facts"
    type: rare
    h2: "6 điểm khác nhau giữa thị trường sơ cấp và thứ cấp"
  - attribute: "vốn điều lệ tối thiểu khi IPO"
    entity: "Công ty cổ phần"
    value: "30 tỷ VNĐ"
    source: "https://vanban.chinhphu.vn/default.aspx?pageid=27160&docid=198541"
    type: unique
    h2: "Điều kiện để cổ phiếu đi từ thị trường sơ cấp sang thứ cấp"

# Audience & Brand
Persona: P2 — F0 nhà đầu tư mới
Tone: giải thích bằng tiền thật, động từ trực tiếp, có lập trường
Writer_Profile: educational
Writing_Method: 4Cs
Core_Products:
  - product: "Mở tài khoản eKYC trên App DSC Trading"
    benefit: "vào thị trường thứ cấp (HOSE, HNX, UPCoM) trong 3 phút, phí giao dịch từ 0,1%"
  - product: "Môi giới 1:1"
    benefit: "có người hướng dẫn sàn, lô, cách đặt lệnh ở lệnh mua đầu tiên"

# Anti-AI
Anti_AI_Flags:
  - định nghĩa kiểu sách giáo khoa dịch ("đóng vai trò cầu nối", "huyết mạch nền kinh tế")
  - liệt kê chức năng rỗng không có số
  - ưu/nhược đối xứng giả giữa 2 thị trường
  - nhắc DSC bán cổ phiếu IPO (không có trong profile)

# GEO/AEO
GEO_Compliance: true
PAA_Questions:
  - q: "Thị trường sơ cấp là gì?"
    placement: body
    source: inferred
  - q: "Thị trường thứ cấp là gì?"
    placement: body
    source: inferred
  - q: "Mua cổ phiếu trên sàn HOSE là thị trường sơ cấp hay thứ cấp?"
    placement: faq
    source: inferred
  - q: "Thị trường mới nổi thứ cấp là gì?"
    placement: faq
    source: inferred
  - q: "Nhà đầu tư cá nhân có mua được cổ phiếu ở thị trường sơ cấp không?"
    placement: faq
    source: inferred
Related_Searches:
  same_intent: [thị trường sơ cấp, thị trường thứ cấp, sơ cấp và thứ cấp là gì, phân biệt thị trường sơ cấp và thị trường thứ cấp]
  spin_off: [thứ cấp nghĩa là gì, thị trường mới nổi thứ cấp là gì]

# Cluster
Cluster: 2f Thị trường, chủ thể & thuật ngữ
Cluster_Role: Cluster
Internal_Links:
  - anchor: "cách chơi chứng khoán cho người mới"
    url: "https://www.dsc.com.vn/kien-thuc/cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau"
    suggested_placement: "H2 Kết luận/ hoặc H2 tiền đi về đâu: câu nói F0 bắt đầu từ thứ cấp"
  - anchor: "niêm yết chứng khoán"
    url: "https://www.dsc.com.vn/kien-thuc/niem-yet-chung-khoan-ipo-la-gi-nhung-dieu-can-biet"
    suggested_placement: "H2 Điều kiện: câu về bước niêm yết sau IPO"
  - anchor: "mua cổ phiếu IPO"
    url: "https://www.dsc.com.vn/kien-thuc/cach-mua-co-phieu-ipo"
    suggested_placement: "FAQ nhà đầu tư cá nhân mua sơ cấp"
  - anchor: "biên độ giao dịch"
    url: "https://www.dsc.com.vn/kien-thuc/bien-do-giao-dich-san-chung-khoan-hose-hnx-upcom"
    suggested_placement: "H2 6 điểm khác nhau: dòng giá"
  - anchor: "thanh khoản"
    url: "https://www.dsc.com.vn/kien-thuc/thanh-khoan-la-gi"
    suggested_placement: "H2 Mối quan hệ: thanh khoản thứ cấp quyết định giá IPO"
  - anchor: "thị trường vốn"
    url: "https://www.dsc.com.vn/kien-thuc/thi-truong-von-la-gi-cach-tiep-can-cho-nha-dau-tu-ca-nhan"
    suggested_placement: "H2 định nghĩa: sơ cấp/thứ cấp là cách chia của thị trường vốn"
  - anchor: "mở tài khoản"
    url: "https://www.dsc.com.vn/mo-tai-khoan"
    suggested_placement: "H2 DSC + Kết luận"
---

# SEO Content Outline: Thị trường sơ cấp và thứ cấp là gì

- **Title:** Thị trường sơ cấp và thứ cấp là gì? 6 điểm khác nhau
- **H1:** Thị trường sơ cấp và thứ cấp là gì? 6 điểm khác nhau cho nhà đầu tư mới
- **Sapo (viết nguyên văn, duyệt cùng outline — I105):**
  - Đoạn 1: Thị trường sơ cấp và thứ cấp là gì? Thị trường sơ cấp là nơi tổ chức phát hành bán chứng khoán mới lần đầu để huy động vốn. Thị trường thứ cấp là nơi nhà đầu tư mua bán lại với nhau, chỉ quyền sở hữu đổi tay. Khi bạn đặt lệnh mua cổ phiếu trên HOSE với biên độ ±7% mỗi phiên, bạn đang ở thị trường thứ cấp.
  - Đoạn 2: Trong bài viết này, Chứng khoán DSC tóm tắt những điểm chính bạn cần nắm.
    - Thị trường sơ cấp là nơi tổ chức phát hành bán chứng khoán lần đầu, tiền thu được sau chi phí phát hành thuộc về doanh nghiệp.
    - Thị trường thứ cấp là nơi nhà đầu tư mua bán lại với nhau trên HOSE, HNX và UPCoM, doanh nghiệp không nhận thêm đồng nào.
    - Một đợt phát hành thu 200 tỷ VNĐ chỉ tăng vốn doanh nghiệp một lần, mọi giao dịch sau đó trên sàn chỉ đổi người sở hữu.
    - Doanh nghiệp IPO cần vốn điều lệ đã góp từ 30 tỷ VNĐ và bán cho ít nhất 100 nhà đầu tư không phải cổ đông lớn.
    - Mua cổ phiếu trên sàn là giao dịch ở thị trường thứ cấp, với lô chẵn 100 cổ phiếu, biên độ ±7% trên HOSE và thanh toán T+2.
  - Câu mời đọc: Nếu bạn sắp đặt lệnh mua cổ phiếu đầu tiên, đọc tiếp để biết tiền của mình thực sự đi về đâu.
- **Meta description:** Thị trường sơ cấp và thứ cấp là gì? Sơ cấp: doanh nghiệp bán chứng khoán mới lấy vốn. Thứ cấp: nhà đầu tư mua bán lại. Bảng 6 điểm khác nhau và ví dụ.

## 1. SERP & Intent

**Khung bài thắng SERP:** SERP degraded. Refetch `--no-cache` ngày 26/11/2026 cho cả 2 biến thể keyword: 9/9 kết quả là trang câu trắc nghiệm khoahoc.vietjack.com, PDF scribd.com, tailieu.vn, plo.vn; không có PAA, không có related searches. GSC 90 ngày cho thấy URL DSC đang ở vị trí 1,8 cho keyword nhưng không có trong list → SERP DataForSEO lệch so với SERP thật.
**Kết luận khung:** Comparison: định nghĩa ngắn (Featured Snippet đoạn) → dòng tiền bằng ví dụ số → bảng 6 điểm khác nhau (Featured Snippet bảng) → điều kiện chuyển thị trường → bảng 6 tình huống. AI Overview trả lời bằng 1 câu định nghĩa đối sánh, trích vfs.com.vn, dsc.com.vn, topi.vn → sapo và câu đầu H2 1 phải trả lời đúng dạng này.
**Intent:** người đọc (F0, sinh viên) muốn phân biệt 2 khái niệm và biết mình đang mua cổ phiếu ở thị trường nào.

### Competitor 1: khoahoc.vietjack.com
- URL: https://khoahoc.vietjack.com/question/1634051/nhung-dac-diem-nao-thuoc-ve-thi-truong-so-cap-nom99
- Khung: câu trắc nghiệm · 1772 từ (phần lớn là giao diện)
- Điểm: Độ sâu 2 · Trình bày 3 · SEO 5 · UX 3 = 13/40
- Mạnh: khớp đúng câu hỏi đặc điểm sơ cấp · Thiếu: không giải thích, không ví dụ, không bảng

### Competitor 2: scribd.com
- URL: https://www.scribd.com/document/864858395/Chu-o-ng-6-TTCK-thu-ca-p-PDF
- Khung: tài liệu chương giáo trình · 969 từ
- Điểm: Độ sâu 5 · Trình bày 3 · SEO 4 · UX 2 = 14/40
- Mạnh: cấu trúc thứ cấp tập trung/phi tập trung · Thiếu: số liệu Việt Nam hiện hành, không đọc được trên mobile

### Competitor 3: tailieu.vn
- URL: https://tailieu.vn/doc/thi-truong-chung-khoan-so-cap-1223116.html
- Khung: tài liệu giáo trình · 797 từ
- Điểm: Độ sâu 5 · Trình bày 2 · SEO 4 · UX 2 = 13/40
- Mạnh: IPO, đối tượng mua cổ phần lần đầu · Thiếu: chữ lỗi font, không có thứ cấp, không ví dụ

## 2. Competitor Gap Synthesis
- **Gaps:** không trang nào quy ra tiền dòng chảy vốn; không có bảng tình huống thực tế; không ai nêu điều kiện IPO theo Luật Chứng khoán 2019; không ai nói F0 mua trên app là thứ cấp.
- **Chủ đề con đối thủ đều có:** đặc điểm sơ cấp (H2 1, H2 3) · đặc điểm thứ cấp (H2 1, H2 3) · tập trung/phi tập trung (H2 3 dòng "Nơi diễn ra") · IPO (H2 4).
- **Unique angle DSC:** góc nhà đầu tư cầm app — "lệnh của bạn rơi vào thị trường nào, tiền về ai".
- **Featured Snippet target:** Table (bảng 6 điểm khác nhau) + đoạn định nghĩa 40–60 từ.
- **PAA plan:** SERP không có PAA; câu hỏi suy từ query GSC của URL (thị trường sơ cấp là gì 246 impr, thị trường thứ cấp là gì 471 impr, thị trường mới nổi thứ cấp là gì 207 impr) → body/faq như YAML.
- **Cannibalization:** URL `/kien-thuc/thi-truong-so-cap-va-thu-cap-la-gi` (vị trí 3,4 trung bình, 6.593 impr / 90 ngày). Bản này viết lại toàn bộ bài trên chính URL đó, không tạo URL mới.

## 3. Dữ liệu dùng trong bài

| Dữ kiện | Số liệu | Mốc thời gian | Nguồn | Trạng thái |
|---|---|---|---|---|
| Biên độ dao động giá | HOSE ±7%, HNX ±10%, UPCoM ±15% | quy định hiện hành | market_facts | ✓ đã kiểm |
| Chu kỳ thanh toán, lô | T+2 (cổ phiếu về 13h ngày T+2), lô 100 cổ phiếu | quy định hiện hành | market_facts | ✓ đã kiểm |
| Khối lượng khớp lệnh VN-Index phiên cuối | 410.637.498 cổ phiếu | 25/11/2026 | market_facts | ✓ đã kiểm |
| KLGD bình quân 20 phiên VN-Index | 544,9 triệu cổ phiếu | đến 25/11/2026 | market_facts | ✓ đã kiểm |
| VN-Index đóng cửa | 1.687,45 điểm | 25/11/2026 | market_facts | ✓ đã kiểm |
| Chào bán ra công chúng / riêng lẻ, điều kiện IPO: vốn điều lệ đã góp từ 30 tỷ VNĐ, ít nhất 15% cổ phiếu có quyền biểu quyết bán cho ít nhất 100 nhà đầu tư không phải cổ đông lớn | Luật Chứng khoán số 54/2019/QH14 | hiệu lực 01/01/2021 | https://vanban.chinhphu.vn/default.aspx?pageid=27160&docid=198541 | ✓ đã kiểm |
| Phí giao dịch DSC | từ 0,1% | 11/2026 | DSC nội bộ | ✓ đã kiểm |
| eKYC DSC | 3 phút | 11/2026 | DSC nội bộ | ✓ đã kiểm |
| Ví dụ dòng tiền IPO 10 triệu cp × 20.000 VNĐ = 200 tỷ VNĐ; 10 triệu cp đổi chủ 3 lần × 25.000 VNĐ = 750 tỷ VNĐ | calc | — | DSC nội bộ | ✓ đã kiểm |

## 4. Brand Context (output Brand Guardian)
- **Writer Profile:** educational — 3 đặc điểm tone: giải thích bằng tiền thật và quy định sàn Việt Nam · câu 12–22 từ, động từ làm trụ · thuật ngữ giải thích ngay trong câu.
- **USP bắt buộc:** eKYC 3 phút, phí từ 0,1% kèm Môi giới 1:1 (đúng chỗ F0 vào thứ cấp lần đầu).
- **Lỗi cũ cần tránh với chủ đề này:** I118 (IPO đã có bài riêng → 1 câu + link, không dựng hướng dẫn mua IPO); I111 (không nói DSC phân phối IPO / quỹ mở); I108 (không nhân vật có tên — persona P2 có "anh Minh", không dùng); I127 (T+2 về 13h).
- **Xung đột instinct ↔ phản hồi user:** không có.

## 5. Cấu trúc nội dung

### H1: Thị trường sơ cấp và thứ cấp là gì? 6 điểm khác nhau cho nhà đầu tư mới

### H2: Thị trường sơ cấp và thứ cấp là gì?
- **Câu hỏi người đọc:** hai khái niệm này nghĩa là gì, nói ngắn.
- **Ý chính:** sơ cấp = bán lần đầu, tiền vào tổ chức phát hành; thứ cấp = mua bán lại, tiền vào nhà đầu tư bán. Cả hai là hai tầng của thị trường vốn.
- **Nội dung chính:** đoạn trả lời 40–60 từ; link thị trường vốn.
- **GEO_Load_Bearing:** Luật Chứng khoán số 54/2019/QH14 chia việc phát hành thành chào bán ra công chúng và chào bán riêng lẻ.
- **Chuyển ý → H2 sau:** định nghĩa xong, xem tiền thật chảy thế nào.
- **Không viết:** chức năng vĩ mô kiểu sách giáo khoa.
- **Target:** 60

#### H3: Thị trường sơ cấp là gì?
- **Nội dung chính:** người bán = doanh nghiệp, Chính phủ, ngân hàng; hình thức IPO, phát hành thêm, chào bán riêng lẻ; bảo lãnh phát hành; giá do tổ chức phát hành định (đấu giá / giá cố định).
- **Target:** 110

#### H3: Thị trường thứ cấp là gì?
- **Nội dung chính:** người bán = nhà đầu tư khác; tập trung (HOSE, HNX, UPCoM qua CTCK) và phi tập trung (OTC); giá khớp theo cung cầu trong biên độ.
- **Target:** 110

### H2: Tiền của nhà đầu tư đi về đâu ở mỗi thị trường
- **Câu hỏi người đọc:** khác nhau thì ảnh hưởng gì tới tôi?
- **Ý chính:** chỉ thị trường sơ cấp mang vốn mới cho doanh nghiệp; thứ cấp chỉ đổi người sở hữu, nhưng tạo thanh khoản giúp đợt sơ cấp bán được.
- **Nội dung chính:** ví dụ calc 200 tỷ / 750 tỷ VNĐ; khối lượng khớp lệnh 25/11/2026 410,6 triệu cổ phiếu; link cách chơi chứng khoán cho người mới.
- **Bằng chứng thực tế:** dòng calc + market_facts.
- **GEO_Load_Bearing:** Phiên 25/11/2026, VN-Index khớp 410,6 triệu cổ phiếu, toàn bộ là giao dịch thứ cấp.
- **Chuyển ý → H2 sau:** gom khác biệt thành bảng.
- **Target:** 190

### H2: 6 điểm khác nhau giữa thị trường sơ cấp và thứ cấp
- **Câu hỏi người đọc:** phân biệt nhanh bằng tiêu chí nào?
- **Ý chính:** 6 tiêu chí: người bán, tiền về ai, cách định giá, số lần giao dịch, nơi diễn ra, thời điểm có cổ phiếu/bán được.
- **Nội dung chính:** bảng 3 cột × 6 dòng; 2 đoạn giải thích dòng giá (biên độ ±7%) và dòng thời điểm (13h T+2); link biên độ giao dịch.
- **GEO_Load_Bearing:** Trên HOSE, giá cổ phiếu thứ cấp chỉ dao động ±7% mỗi phiên so với giá tham chiếu.
- **Chuyển ý → H2 sau:** cổ phiếu sang thứ cấp phải qua điều kiện gì.
- **Target:** 200

### H2: Điều kiện để cổ phiếu đi từ thị trường sơ cấp sang thứ cấp
- **Câu hỏi người đọc:** doanh nghiệp nào cũng IPO rồi lên sàn được không?
- **Ý chính:** phải đủ điều kiện chào bán ra công chúng rồi niêm yết/đăng ký giao dịch; khoảng trống giữa 2 bước là rủi ro của người mua sơ cấp.
- **Nội dung chính:** 3 điều kiện IPO (Luật 54/2019, link nguồn) dạng list; sau IPO: niêm yết HOSE/HNX hoặc đăng ký UPCoM (link niêm yết chứng khoán); người mua IPO chưa bán được cho tới khi cổ phiếu lên sàn.
- **GEO_Load_Bearing:** Luật Chứng khoán số 54/2019/QH14 yêu cầu doanh nghiệp IPO có vốn điều lệ đã góp từ 30 tỷ VNĐ.
- **Chuyển ý → H2 sau:** áp vào tình huống mua của bạn.
- **Không viết:** quy trình niêm yết chi tiết (bài riêng).
- **Target:** 180

### H2: Bạn đang mua ở thị trường nào: 6 tình huống thường gặp
- **Câu hỏi người đọc:** lệnh tôi đặt hôm nay là sơ cấp hay thứ cấp?
- **Ý chính:** chỉ 3/6 tình huống là sơ cấp và đều cần đăng ký trước, có thời hạn.
- **Nội dung chính:** bảng tình huống · thị trường · tiền về ai; 1 đoạn nhận xét quyền mua cổ phiếu phát hành thêm.
- **GEO_Load_Bearing:** Quyền mua cổ phiếu phát hành thêm là giao dịch sơ cấp dù bạn thực hiện qua tài khoản chứng khoán.
- **Chuyển ý → H2 sau:** vì sao hai tầng phụ thuộc nhau.
- **Target:** 180

### H2: Mối quan hệ giữa thị trường sơ cấp và thị trường thứ cấp
- **Câu hỏi người đọc:** thị trường nào quan trọng hơn?
- **Ý chính:** không có thứ cấp thanh khoản thì không ai mua sơ cấp; giá thứ cấp là mốc định giá đợt phát hành thêm.
- **Nội dung chính:** 2 đoạn; link thanh khoản; KLGD bình quân 20 phiên 544,9 triệu cp. Tiêu đề trong bài: "Vì sao thanh khoản thứ cấp quyết định đợt phát hành sơ cấp" (tránh DUP-h2).
- **GEO_Load_Bearing:** Bình quân 20 phiên đến 25/11/2026, VN-Index khớp 544,9 triệu cổ phiếu mỗi phiên.
- **Chuyển ý → H2 sau:** F0 vào thứ cấp cần tài khoản.
- **Target:** 110

### H2: Bắt đầu giao dịch trên thị trường thứ cấp tại Chứng khoán DSC
- **Câu dẫn từ kết luận bài:** mọi lệnh trên HOSE/HNX/UPCoM đi qua tài khoản tại công ty chứng khoán thành viên → cần tài khoản.
- **Bước cụ thể tại DSC:** eKYC 3 phút trên App DSC Trading → nạp tiền qua mã định danh 963369 → Môi giới 1:1 hướng dẫn lệnh mua lô 100 cổ phiếu đầu tiên. Bảng so phí trên lệnh 100 triệu VNĐ: DSC từ 0,1% (100.000 VNĐ) vs CTCK có môi giới 0,15–0,35% (150.000–350.000 VNĐ) vs CTCK phí 0% (không có môi giới). DSC không tự đặt giá mục tiêu.
- **Target:** 170

### H2: Câu hỏi thường gặp về thị trường sơ cấp và thứ cấp
- `###` mỗi câu, câu đầu ≤ 60 từ.
- **Q1:** Mua cổ phiếu trên sàn HOSE là thị trường sơ cấp hay thứ cấp? · **Q2:** Thị trường mới nổi thứ cấp là gì? · **Q3:** Nhà đầu tư cá nhân có mua được cổ phiếu ở thị trường sơ cấp không?
- **Word count:** ~180 (không ghi Target: count_words.py không cộng H3 câu hỏi vào H2 FAQ)

### H2: Kết luận
- **Ý chính:** tiền về ai là tiêu chí duy nhất cần nhớ; F0 bắt đầu ở thứ cấp, coi IPO là cơ hội phụ có thời gian chờ.
- **CTA:** checklist 3 mục + link https://www.dsc.com.vn/mo-tai-khoan
- **Target:** 110

## 6. Liên kết & yếu tố trực quan
- **External links:** Luật Chứng khoán số 54/2019/QH14 — vanban.chinhphu.vn (H2 1 và H2 Điều kiện).
- **Bằng chứng thực tế (first-hand):** phép tính dòng tiền 200/750 tỷ; bảng 6 tình huống.
- **Spin-off candidates:** thị trường mới nổi thứ cấp (FTSE) → FAQ ngắn, chưa có bài riêng.
- **Yếu tố trực quan:** ảnh bìa 1000×600 (`thi-truong-so-cap-va-thu-cap-la-gi-featured.jpg`); infographic 800×500 dòng tiền (`thi-truong-so-cap-va-thu-cap-la-gi-dong-tien-ipo.jpg`); bảng 6 điểm; bảng 6 tình huống; banner giữa + cuối.

## 7. Revision Log
- **v1.6 (2026-11-26):** gộp v2 vào slug gốc, thay bản Final cũ (sao lưu: archive/thi-truong-so-cap-va-thu-cap-la-gi/final-v1-2026-11-26.md). Outline dựng lại sau khi article_snapshot xoá nhầm (lỗi đã vá); outline cũ 23/11 ở outline.prev.md.
- **v1.5 (2026-11-26):** user chọn sapo v1 (khung điểm chính) → chép v1 + 1 bullet điều kiện IPO.
- **v1.4 (2026-11-26):** bỏ giới hạn 110 từ, đoạn 2 sapo nêu đủ các H2.
- **v1.3 (2026-11-26):** user bỏ khối điểm chính, sapo về 2 đoạn văn xuôi (sau đó đảo lại ở v1.5).
- **v1.2 (2026-11-26):** sapo thử khung điểm chính với câu dẫn tự viết (user chê câu dẫn).
- **v1.1 (2026-11-26):** sapo viết lại theo khung Comparison (tiêu chí: tiền về ai).
- **v1.0 (2026-11-26):** bản viết lại để so sánh với Final cũ, chạy /write --auto. SERP DataForSEO refetch 2 biến thể đều lệch (trang trắc nghiệm) → degraded, khung theo intent.
