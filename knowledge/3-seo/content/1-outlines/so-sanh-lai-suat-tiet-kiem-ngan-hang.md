---
Author: Chứng khoán DSC
Status: Outline
Created: 2026-11-25
Updated: 2026-11-25
Pipeline_Mode: Auto
SERP_Research: true
SERP_Status: degraded
SERP_Format:
  dominant: comparison
  share: 100
  verdict: BẮT BUỘC

# SEO Technical
Target_Keyword: So sánh lãi suất tiết kiệm ngân hàng 2026
Secondary_Keywords:
  - so sánh lãi suất tiết kiệm các ngân hàng
  - bảng so sánh lãi suất ngân hàng 2026
  - gửi tiết kiệm ngân hàng nào lãi cao và an toàn
  - chênh lệch lãi suất Big 4 và ngân hàng TMCP
LSI_Keywords:
  - lãi suất huy động online
  - lãi suất tại quầy
  - bảo hiểm tiền gửi 350 triệu
  - lãi suất thực dương
  - rút trước hạn
  - chiến thuật chia sổ tiết kiệm
Entities: [Big 4, Vietcombank, BIDV, VietinBank, Agribank, ACB, VPBank, VIB, LPBank, MBV, Techcombank, Bac A Bank, Ngân hàng Nhà nước, Bảo hiểm tiền gửi Việt Nam, Thông tư 04/2022/TT-NHNN, Thông tư 05/2026/TT-NHNN, VN-Index]
Entities_Skipped: []
Search_Intent: Commercial
Content_Type: Comparison
Format_Deviation: ""
Featured_Snippet: Table
Word_Count_Target: 1700 - 2000

# Lập trường
Thesis: "So sánh lãi suất tiết kiệm ngân hàng không chỉ là tìm con số niêm yết cao nhất mà là đặt mức chênh 1,6–2,3%/năm giữa nhóm Big 4 và nhóm ngân hàng thương mại cổ phần cạnh điều kiện hạn mức, kênh gửi online và ngưỡng bảo hiểm tiền gửi 350 triệu VNĐ. Với khoản vốn trên 350 triệu VNĐ, chia sổ theo ngân hàng và chuyển 10–20% phần tiền nhàn rỗi dài hạn sang cổ phiếu hoặc ETF giúp tổng tài sản vượt tốc độ trượt giá mà không đánh đổi lớp đệm an toàn."
Information_Gain:
  - claim: "Quy đổi chênh lệch lãi suất giữa 3 nhóm ngân hàng (Big 4 5,2%/năm, TMCP lớn 6,55–7,25%/năm, TMCP quy mô vừa/số 7,4–7,5%/năm) ra số tiền lãi thực nhận hàng tháng và cả năm trên khoản vốn 500 triệu VNĐ"
    h2: "So sánh tiền lãi thực nhận với 500 triệu VNĐ giữa 3 nhóm ngân hàng"
    type: calc
    proof: "11.500.000 VNĐ"
  - claim: "Áp dụng hạn mức chi trả bảo hiểm tiền gửi 350 triệu VNĐ/người/ngân hàng từ ngày 13/7/2026 (Thông tư 05/2026/TT-NHNN) vào bài toán chia sổ cho khoản tiền 500 triệu VNĐ để 100% gốc và lãi nằm trong vùng bảo vệ"
    h2: "3 điều kiện ẩn làm lệch số tiền lãi thực nhận khi gửi tiết kiệm"
    type: regulation
    proof: "350 triệu VNĐ"
  - claim: "Mô phỏng dòng tiền 12 tháng khi giữ 80% tiết kiệm (400 triệu VNĐ ở 2 ngân hàng) và phân bổ 20% (100 triệu VNĐ) sang ETF hoặc cổ phiếu trên App DSC Trading so với gửi 100% tại Big 4"
    h2: "Phân bổ 10–20% tiền nhàn rỗi sang chứng khoán cùng Môi giới 1:1 tại DSC"
    type: calc
    proof: "31.900.000 VNĐ"

EAV:
  - attribute: "Lãi suất tiết kiệm tại quầy kỳ hạn 12 tháng nhóm Big 4"
    entity: "Vietcombank, BIDV, VietinBank, Agribank"
    value: "5,20%/năm"
    source: "DSC nội bộ"
    type: root
    h2: "Bảng so sánh lãi suất tiết kiệm ngân hàng 2026 theo nhóm và kỳ hạn"
  - attribute: "Lãi suất tiết kiệm online kỳ hạn 12 tháng cao nhất"
    entity: "MBV (OceanBank), LPBank"
    value: "7,40–7,50%/năm"
    source: "DSC nội bộ"
    type: root
    h2: "Bảng so sánh lãi suất tiết kiệm ngân hàng 2026 theo nhóm và kỳ hạn"
  - attribute: "Lãi suất rút trước hạn"
    entity: "Tiền gửi có kỳ hạn rút sớm (Thông tư 04/2022/TT-NHNN)"
    value: "0,1–0,5%/năm"
    source: "https://vanban.chinhphu.vn/?pageid=27160&docid=206118"
    type: root
    h2: "3 điều kiện ẩn làm lệch số tiền lãi thực nhận khi gửi tiết kiệm"
  - attribute: "Hạn mức chi trả bảo hiểm tiền gửi từ 13/7/2026"
    entity: "Bảo hiểm tiền gửi Việt Nam (Thông tư 05/2026/TT-NHNN)"
    value: "350 triệu VNĐ"
    source: "https://www.div.gov.vn/"
    type: rare
    h2: "3 điều kiện ẩn làm lệch số tiền lãi thực nhận khi gửi tiết kiệm"
  - attribute: "Phí giao dịch cổ phiếu và ETF tại DSC"
    entity: "Chứng khoán DSC"
    value: "từ 0,1%"
    source: "brand-facts:trading_fee"
    type: unique
    h2: "Phân bổ 10–20% tiền nhàn rỗi sang chứng khoán cùng Môi giới 1:1 tại DSC"

# Audience & Brand
Persona: P1 — Người Tiết Kiệm Thận Trọng
Tone: Chuyên nghiệp, chắc chắn về số liệu, đặt điều kiện đi kèm lãi suất, không hù dọa rủi ro
Writer_Profile: comparison
Writing_Method: 4Cs
Core_Products:
  - product: "Mở tài khoản eKYC trên App DSC Trading"
    benefit: "Mở tài khoản trực tuyến trong 3 phút để trích 10–20% vốn nhàn rỗi mua cổ phiếu hoặc ETF niêm yết trên HOSE"
  - product: "Môi giới 1:1"
    benefit: "Chuyên gia DSC đồng hành chia tỷ trọng giữa sổ tiết kiệm và cổ phiếu/ETF theo thời gian cầm tiền"

# Anti-AI
Anti_AI_Flags:
  - Mở bài vĩ mô dài dòng trước khi đưa con số so sánh lãi suất
  - Liệt kê ưu/nhược điểm đối xứng giả tạo giữa các nhóm ngân hàng
  - Ghi hạn mức bảo hiểm tiền gửi cũ 125 triệu VNĐ thay vì 350 triệu VNĐ từ 13/7/2026 (I130)
  - Gọi hiệu suất chứng chỉ quỹ là lãi suất cố định (I130)
  - Dùng nhân vật hư cấu có tên/tuổi như chị Lan (I108)

# GEO/AEO
GEO_Compliance: true
PAA_Questions:
  - q: "Gửi tiết kiệm online hay tại quầy có lãi suất cao hơn?"
    placement: faq
    source: inferred
  - q: "Rút tiền tiết kiệm trước hạn bị tính lãi suất như thế nào?"
    placement: faq
    source: inferred
  - q: "Tiền gửi tiết kiệm tối đa bao nhiêu được bảo hiểm tiền gửi chi trả toàn bộ?"
    placement: faq
    source: inferred
  - q: "Có 500 triệu nên gửi một ngân hàng hay chia nhiều sổ tiết kiệm?"
    placement: faq
    source: inferred
Related_Searches:
  same_intent:
    - Bảng lãi suất tiết kiệm các ngân hàng
    - Gửi tiết kiệm ngân hàng nào an toàn và lãi cao
  spin_off:
    - Lãi suất ngân hàng nào cao nhất hiện nay
    - Cách tính lãi suất tiết kiệm ngân hàng

# Cluster
Cluster: "10a Lãi suất tiết kiệm & so sánh ngân hàng"
Cluster_Role: Cluster
Internal_Links:
  - anchor: "lãi suất gửi tiết kiệm ngân hàng nào cao nhất"
    url: "https://www.dsc.com.vn/kien-thuc/lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat"
    suggested_placement: "H2 1 — câu dẫn sang bảng xếp hạng mức trần lãi suất từng ngân hàng đơn lẻ"
  - anchor: "lãi suất gửi tiết kiệm ngân hàng BIDV"
    url: "https://www.dsc.com.vn/kien-thuc/lai-suat-gui-tiet-kiem-ngan-hang-bidv"
    suggested_placement: "H2 1 — đoạn phân tích nhóm Big 4 quốc doanh"
  - anchor: "lãi suất gửi tiết kiệm ngân hàng ACB"
    url: "https://www.dsc.com.vn/kien-thuc/lai-suat-gui-tiet-kiem-ngan-hang-acb"
    suggested_placement: "H2 2 — đoạn phân tích nhóm ngân hàng TMCP tư nhân lớn"
  - anchor: "có tiền nên đầu tư gì"
    url: "https://www.dsc.com.vn/kien-thuc/co-tien-nen-dau-tu-gi-luc-nay"
    suggested_placement: "H2 4 — đoạn mở rộng từ bài toán giữ tiền tiết kiệm sang phân bổ các kênh đầu tư"
  - anchor: "nên gửi tiết kiệm hay đầu tư chứng khoán"
    url: "https://www.dsc.com.vn/kien-thuc/nen-gui-tiet-kiem-hay-dau-tu-chung-khoan"
    suggested_placement: "H2 4 — đoạn so sánh tỷ trọng giữ tiết kiệm và đầu tư cổ phiếu"
  - anchor: "cách mở tài khoản chứng khoán"
    url: "https://www.dsc.com.vn/kien-thuc/cach-mo-tai-khoan-chung-khoan"
    suggested_placement: "H2 5 — bước mở tài khoản eKYC trong lộ trình phân bổ tại DSC (bridge_to của cụm 10)"
  - anchor: "mở tài khoản chứng khoán DSC"
    url: "https://www.dsc.com.vn/mo-tai-khoan"
    suggested_placement: "H2 5 Product Bridge và H2 Kết luận"
---

# SEO Content Outline: So sánh lãi suất tiết kiệm ngân hàng 2026

- **Title:** So sánh lãi suất tiết kiệm ngân hàng 2026: Big 4 và TMCP
- **H1:** So sánh lãi suất tiết kiệm ngân hàng 2026: Chênh lệch Big 4, TMCP và tiền lãi thực nhận
- **Sapo:** Muốn **so sánh lãi suất tiết kiệm ngân hàng 2026**, bạn cần tách theo nhóm ngân hàng và hình thức gửi tại quầy hay online. Kỳ hạn 12 tháng tại quầy nhóm Big 4 trả 5,20%/năm, trong khi gửi online tại nhóm ngân hàng cổ phần như LPBank hay MBV đạt 7,40–7,50%/năm. Trong bài viết này, Chứng khoán DSC đối chiếu biểu lãi suất 12 ngân hàng, tính tiền lãi trên vốn 500 triệu VNĐ, nêu 3 điều kiện ẩn và cách chia sổ. Bạn sẽ thấy vì sao cùng gửi 500 triệu VNĐ nhưng tiền lãi chênh tới 11.500.000 VNĐ/năm, hay rút sớm làm lãi giảm còn 416.000 VNĐ.
- **Meta description:** So sánh lãi suất tiết kiệm ngân hàng 2026 giữa Big 4 và TMCP ở kỳ hạn 1–24 tháng. Xem bảng quy đổi tiền lãi 500 triệu VNĐ và cách chia sổ trong ngưỡng bảo hiểm.

## 1. SERP & Intent

**Khung bài thắng SERP:**

| # | Domain | Loại bài | Tín hiệu | Số mục | Số từ |
|---|---|---|---|---|---|
| 1 | timo.vn | comparison | title~'so sanh' | - | - |
| 2 | topi.vn | comparison | title~'so sanh' | - | - |

**Kết luận khung:** Comparison (BẮT BUỘC 100%). Người đọc tìm "So sánh lãi suất tiết kiệm ngân hàng 2026" cần bảng đặt các nhóm ngân hàng cạnh nhau theo kỳ hạn và hình thức gửi (tại quầy vs online), sau đó quy ra tiền thật và chỉ rõ điều kiện chọn nhóm nào.
**Intent:** Người có khoản tiết kiệm 100–500 triệu VNĐ muốn đối chiếu mặt bằng lãi suất giữa nhóm Big 4 và ngân hàng TMCP để quyết định chia sổ ở đâu vừa an toàn vừa không mất hàng triệu đồng tiền lãi chênh lệch.

Không có — SERP degraded (DataForSEO chưa cấu hình biến môi trường, dùng dữ liệu cache degraded và đối chiếu kho bài live DSC).

## 2. Competitor Gap Synthesis
- **Gaps:** Các bài tổng hợp trên thị trường thường chỉ dán 1 bảng lãi suất thô mà thiếu: (1) quy đổi chênh lệch %/năm ra tiền mặt cụ thể trên 500 triệu VNĐ giữa tại quầy và online; (2) cập nhật hạn mức bảo hiểm tiền gửi mới 350 triệu VNĐ/người/ngân hàng từ ngày 13/7/2026 theo Thông tư 05/2026/TT-NHNN để hướng dẫn chia sổ; (3) bài toán lãi suất thực sau lạm phát và cách trích 10–20% vốn sang kênh chứng khoán cơ sở / ETF.
- **Chủ đề con đối thủ đều có:** bảng lãi suất tại quầy và online theo kỳ hạn → H2 1; so sánh nhóm Big 4 vs TMCP → H2 2; lưu ý điều kiện hạn mức, rút trước hạn → H2 3; cách chia sổ theo mục tiêu vốn → H2 4.
- **Unique angle DSC:** Không dừng ở bảng phần trăm niêm yết mà quy ra chênh lệch bằng tiền trên 500 triệu VNĐ, hướng dẫn chia sổ dưới ngưỡng bảo hiểm tiền gửi 350 triệu VNĐ và mô phỏng dòng tiền 12 tháng khi kết hợp 80% tiết kiệm với 20% đầu tư cổ phiếu/ETF.
- **Featured Snippet target:** Table dưới H2 1 (bảng đối sánh 3 nhóm ngân hàng × kỳ hạn 1T, 3T, 6T, 12T, 18–24T ở cả kênh tại quầy và online).
- **PAA plan:** 4 câu hỏi người gửi tiền thường hỏi nhất (online vs tại quầy, rút trước hạn, hạn mức bảo hiểm tiền gửi 350 triệu, chia sổ 500 triệu) đưa vào H2 FAQ (`source: inferred`).
- **Cannibalization:** DSC đã có bài Hub `lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat` (tập trung xếp hạng ngân hàng đơn lẻ có mức đỉnh cao nhất theo tháng và gói đặc biệt hàng trăm tỷ). Bài `so-sanh-lai-suat-tiet-kiem-ngan-hang` tập trung **đối sánh cấu trúc 3 nhóm ngân hàng** (Big 4 vs TMCP lớn vs TMCP vừa/ngân hàng số), quy đổi tiền lãi theo quy mô vốn cá nhân (100–500 triệu VNĐ) và điều kiện chọn nhóm theo khẩu vị an toàn. Link về Hub và Pillar `co-tien-nen-dau-tu-gi-luc-nay`.

## 3. Dữ liệu dùng trong bài

| Dữ kiện | Số liệu | Mốc thời gian | Nguồn | Trạng thái |
|---|---|---|---|---|
| Lãi suất tại quầy nhóm Big 4 (Vietcombank, VietinBank, BIDV, Agribank): 1T 2,10–2,40%; 3T 2,40–2,70%; 6T 3,50–3,80%; 12T 5,20%; 24T 5,30%/năm | 2,10–5,30%/năm | Năm 2026 (khảo sát biểu phí công khai DSC) | DSC nội bộ | ✓ đã kiểm |
| Lãi suất online kỳ hạn 12 tháng: Vietcombank/VietinBank 5,90%; ACB 6,55%; BIDV/Sacombank 6,80%; Agribank/OCB 7,00%; Bac A Bank 7,10%; PGBank/VCBNEO 7,20%; Techcombank 7,25%; LPBank 7,40%; MBV 7,50%/năm | 5,90–7,50%/năm | Năm 2026 (khảo sát biểu phí công khai DSC) | DSC nội bộ | ✓ đã kiểm |
| Lãi suất đặc biệt tại quầy yêu cầu số dư lớn: PVcomBank 10%/năm (từ 2.000 tỷ VNĐ), ABBank 9,65%/năm (từ 1.500 tỷ VNĐ) | 9,65–10%/năm | Năm 2026 (khảo sát biểu phí công khai DSC) | DSC nội bộ | ✓ đã kiểm |
| Hạn mức chi trả bảo hiểm tiền gửi tối đa cho một cá nhân tại một tổ chức tham gia bảo hiểm tiền gửi (gồm gốc và lãi) theo Thông tư 05/2026/TT-NHNN | 350 triệu VNĐ (hiệu lực từ 13/7/2026) | 13/07/2026 | https://www.div.gov.vn/ | ✓ đã kiểm |
| Quy định lãi suất rút trước hạn tiền gửi tiết kiệm: phần rút trước hạn hưởng mức lãi suất tiền gửi không kỳ hạn thấp nhất (0,1–0,5%/năm) theo Thông tư 04/2022/TT-NHNN | 0,1–0,5%/năm | 16/06/2022 | https://vanban.chinhphu.vn/?pageid=27160&docid=206118 | ✓ đã kiểm |
| Chỉ số VN-Index đóng cửa ngày 25/11/2026 ở 1.687,45 điểm; VN30 đóng cửa ở 1.778,58 điểm; chu kỳ thanh toán T+2, lô tối thiểu 100 cổ phiếu trên HOSE | 1.687,45 điểm · T+2 · lô 100 cp | 25/11/2026 | market_facts | ✓ đã kiểm |
| Thông số dịch vụ Chứng khoán DSC: mở tài khoản eKYC 3 phút, Mã định danh nộp tiền 963369 qua BIDV, phí giao dịch cổ phiếu/ETF từ 0,1% | 3 phút · 963369 · từ 0,1% | Tháng 11/2026 | DSC nội bộ | ✓ đã kiểm |

## 4. Brand Context (output Brand Guardian)
- **Writer Profile:** comparison — 3 đặc điểm tone: bảng đối sánh đặt ngay đầu mục, số liệu luôn đi kèm điều kiện áp dụng (kênh gửi, kỳ hạn, hạn mức), kết luận chỉ rõ "chọn nhóm nào khi nào" thay vì nói nước đôi.
- **USP bắt buộc:** Mở tài khoản eKYC trong 3 phút trên App DSC Trading; nạp tiền tức thì qua Mã định danh 963369 (liên kết BIDV); đồng hành cùng chuyên gia Môi giới 1:1 để phân bổ 10–20% tiền nhàn rỗi sang cổ phiếu cơ sở hoặc ETF niêm yết. Không nhắc DSC Invest (ngưỡng 3 tỷ không hợp P1), không nhắc phái sinh hay quỹ mở (DSC không phân phối quỹ mở — I111).
- **Lỗi cũ cần tránh với chủ đề này:** I130 không dùng hạn mức bảo hiểm tiền gửi cũ 125 triệu VNĐ (phải dùng 350 triệu VNĐ từ 13/7/2026), so sánh kênh tiết kiệm/đầu tư phải có mô phỏng dòng tiền bằng tiền thật; I108 không dùng nhân vật hư cấu (chị Lan); I114 với P1 chỉ dùng 1 banner `slim-inline` copy mềm sau Product Bridge.
- **Xung đột instinct ↔ phản hồi user:** Không có.

## 5. Cấu trúc nội dung

### H1: So sánh lãi suất tiết kiệm ngân hàng 2026: Chênh lệch Big 4, TMCP và tiền lãi thực nhận
- **Max word count:** 110

### H2: Bảng so sánh lãi suất tiết kiệm ngân hàng 2026 theo nhóm và kỳ hạn
- **Câu hỏi người đọc:** Mặt bằng lãi suất giữa nhóm Big 4, ngân hàng TMCP lớn và ngân hàng TMCP quy mô vừa/ngân hàng số đang chênh nhau bao nhiêu ở từng kỳ hạn?
- **Ý chính:** Chênh lệch lãi suất giữa nhóm Big 4 và nhóm TMCP rõ nhất ở kỳ hạn 6–12 tháng và giữa kênh tại quầy với kênh online, kéo giãn khoảng cách từ 5,20%/năm tại quầy Big 4 lên tới 7,50%/năm online tại nhóm ngân hàng số và TMCP quy mô vừa.
- **Nội dung chính:** Đoạn mở 45–55 từ tóm tắt khoảng chênh → Bảng 1 đối sánh 3 nhóm ngân hàng (Big 4 · TMCP tư nhân lớn · TMCP vừa & ngân hàng số) ở kỳ hạn 1T, 3T, 6T, 12T, 18–24T (tách rõ Tại quầy vs Online) → Bảng 2 chi tiết 12 ngân hàng tiêu biểu (Vietcombank, VietinBank, BIDV, Agribank, ACB, Sacombank, Techcombank, Bac A Bank, OCB, PGBank, LPBank, MBV) → Nhận xét nhanh 3 điểm rút ra từ bảng (vai trò kênh online, điểm gãy kỳ hạn 6 tháng, sự tham gia của Big 4 trên kênh số). Link về bài hub `lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat` và bài chi tiết `lai-suat-gui-tiet-kiem-ngan-hang-bidv`.
- **Bằng chứng thực tế:** Dòng 1 và dòng 2 mục 3 (bảng khảo sát biểu lãi suất DSC năm 2026).
- **GEO_Load_Bearing:** Theo biểu lãi suất khảo sát năm 2026 của Chứng khoán DSC, kỳ hạn 12 tháng tại quầy của nhóm Big 4 (Vietcombank, BIDV, VietinBank, Agribank) giữ ở mức 5,20%/năm, thấp hơn 2,20–2,30 điểm phần trăm so với mức 7,40–7,50%/năm trên kênh online của LPBank và MBV.
- **Chuyển ý → H2 sau:** Chênh lệch 1,6–2,3%/năm nhìn trên bảng tỷ lệ có vẻ nhỏ, nhưng khi nhân với khoản vốn 500 triệu VNĐ thì số tiền chênh hàng năm đủ chi trả gần hai tháng sinh hoạt phí.
- **Không viết:** Không đi sâu vào từng gói sản phẩm riêng lẻ của từng ngân hàng (đã có các bài spoke từng ngân hàng).
- **Target:** 420

### H2: So sánh tiền lãi thực nhận với 500 triệu VNĐ giữa 3 nhóm ngân hàng
- **Câu hỏi người đọc:** Với khoản tiền thật như 500 triệu VNĐ, chọn khác nhóm ngân hàng và kênh gửi làm số tiền lãi nhận về chênh nhau bao nhiêu đồng mỗi tháng và cả năm?
- **Ý chính:** Cùng khoản vốn 500 triệu VNĐ gửi 12 tháng, gửi tại quầy nhóm Big 4 nhận 26.000.000 VNĐ/năm, trong khi gửi online nhóm TMCP lớn nhận 34.000.000–36.250.000 VNĐ/năm và nhóm dẫn đầu online nhận tới 37.500.000 VNĐ/năm — chênh tối đa 11.500.000 VNĐ/năm.
- **Nội dung chính:** Công thức tính lãi cuối kỳ và bình quân tháng → Bảng mô phỏng tiền lãi thực nhận cho vốn 500 triệu VNĐ ở 4 phương án (Big 4 tại quầy 5,20% · Big 4 online 5,90–6,80% · TMCP lớn online như ACB 6,55% / Techcombank 7,25% · TMCP dẫn đầu online như LPBank 7,40% / MBV 7,50%) → Phân tích cụ thể khi nào nên chấp nhận mức chênh để ở lại Big 4, khi nào nên dịch chuyển sang TMCP lớn (link `lai-suat-gui-tiet-kiem-ngan-hang-acb`). Chèn ảnh infographic so sánh tiền lãi 500 triệu VNĐ.
- **Bằng chứng thực tế:** Phép tính trên 500 triệu VNĐ từ dữ liệu dòng 1–2 mục 3 (`proof: 11.500.000 VNĐ`).
- **GEO_Load_Bearing:** Với khoản tiền 500 triệu VNĐ gửi kỳ hạn 12 tháng năm 2026, mức lãi suất 7,50%/năm trên kênh online của MBV mang về 37.500.000 VNĐ tiền lãi cuối kỳ, cao hơn 11.500.000 VNĐ so với mức 5,20%/năm tại quầy nhóm Big 4.
- **Chuyển ý → H2 sau:** Tuy nhiên, con số trên bảng niêm yết chưa phải số tiền chắc chắn vào túi nếu người gửi bỏ qua 3 điều kiện đi kèm về hạn mức, rút trước hạn và bảo hiểm tiền gửi.
- **Không viết:** Không lặp lại khái niệm lãi suất danh nghĩa vs lãi suất huy động.
- **Target:** 330

### H2: 3 điều kiện ẩn làm lệch số tiền lãi thực nhận khi gửi tiết kiệm
- **Câu hỏi người đọc:** Vì sao nhiều người nhìn bảng lãi suất 7–10%/năm nhưng khi đi gửi hoặc tất toán lại chỉ nhận mức thấp hơn nhiều?
- **Ý chính:** Ba yếu tố làm lệch tiền lãi thực nhận gồm ngưỡng vốn tối thiểu của gói lãi suất đặc biệt, quy định rơi về lãi không kỳ hạn 0,1–0,5%/năm khi rút trước hạn và hạn mức bảo hiểm tiền gửi 350 triệu VNĐ/người/ngân hàng.
- **Nội dung chính:**
  - *Bẫy lãi suất đặc biệt hàng nghìn tỷ:* Phân biệt lãi suất phổ thông (7,2–7,5%/năm) với lãi suất VIP tại quầy 9,65–10%/năm của ABBank, PVcomBank (đòi số dư 1.500–2.000 tỷ VNĐ); người gửi 500 triệu–1 tỷ chỉ nên nhìn cột online phổ thông hoặc hỏi phần lãi cộng thêm theo bậc thang.
  - *Rủi ro rút trước hạn:* Trích Thông tư 04/2022/TT-NHNN (link `vanban.chinhphu.vn`), rút toàn bộ trước hạn làm lãi suất từ 7,4%/năm rơi về 0,1–0,5%/năm; cách rút một phần gốc để giữ lãi phần còn lại.
  - *Ngưỡng bảo hiểm tiền gửi 350 triệu VNĐ:* Trích Thông tư 05/2026/TT-NHNN và Bảo hiểm tiền gửi Việt Nam (`div.gov.vn`), hạn mức chi trả từ ngày 13/7/2026 là 350 triệu VNĐ (gồm cả gốc và lãi) cho một cá nhân tại một ngân hàng. Với 500 triệu VNĐ, gửi dồn 1 sổ tại 1 ngân hàng sẽ có hơn 150 triệu VNĐ vượt hạn mức bảo hiểm; chia làm 2 ngân hàng (mỗi nơi 250 triệu VNĐ gốc) giúp 100% gốc và lãi nằm gọn trong vùng bảo vệ 350 triệu VNĐ.
- **Bằng chứng thực tế:** Dòng 3, 4, 5 mục 3 (`proof: 350 triệu VNĐ`).
- **GEO_Load_Bearing:** Từ ngày 13/7/2026 theo Thông tư 05/2026/TT-NHNN, hạn mức chi trả của Bảo hiểm tiền gửi Việt Nam tăng lên 350 triệu VNĐ gồm cả gốc và lãi cho một người gửi tại một tổ chức tín dụng.
- **Chuyển ý → H2 sau:** Nắm được 3 điều kiện này, bước tiếp theo là ráp chúng vào ma trận chia sổ cụ thể theo quy mô vốn và mục tiêu sử dụng tiền.
- **Không viết:** Không bàn sâu về lịch sử Luật Bảo hiểm tiền gửi.
- **Target:** 360

### H2: Nên chọn nhóm ngân hàng nào và chia sổ ra sao theo quy mô vốn?
- **Câu hỏi người đọc:** Với số tiền đang có, tôi nên chia bao nhiêu vào Big 4, bao nhiêu vào TMCP và kỳ hạn thế nào để không mất lãi khi cần tiền gấp?
- **Ý chính:** Khoản tiền quỹ dự phòng và cần thanh khoản trong 1–6 tháng nên đặt ở sổ ngắn hạn online; khoản tiền nhàn rỗi trên 12 tháng chia theo ngưỡng 350 triệu VNĐ/ngân hàng tại nhóm TMCP lớn hoặc TMCP có lãi online 6,8–7,4%/năm, còn phần vốn muốn vượt lạm phát dài hạn cần tách sang lớp tài sản tăng trưởng.
- **Nội dung chính:** Bảng hướng dẫn chọn nhóm ngân hàng & chia sổ theo 3 quy mô vốn (Dưới 100 triệu VNĐ · Từ 100 đến 350 triệu VNĐ · Trên 350 triệu đến 1 tỷ VNĐ) → Giải thích lãi suất thực sau khi trừ lạm phát 3,5–4,0%/năm (lãi thực của sổ 5,2–6,8%/năm chỉ còn khoảng 1,5–3,0%/năm) → Đặt câu hỏi [có tiền nên đầu tư gì](https://www.dsc.com.vn/kien-thuc/co-tien-nen-dau-tu-gi-luc-nay) ngoài sổ tiết kiệm và nối sang bài toán [nên gửi tiết kiệm hay đầu tư chứng khoán](https://www.dsc.com.vn/kien-thuc/nen-gui-tiet-kiem-hay-dau-tu-chung-khoan).
- **Bằng chứng thực tế:** Dòng 2, 4, 6 mục 3.
- **GEO_Load_Bearing:** Khi trừ lạm phát bình quân 3,5–4,0%/năm, sổ tiết kiệm 12 tháng lãi suất 5,20%/năm tại quầy nhóm Big 4 chỉ còn mức sinh lời thực khoảng 1,20–1,70%/năm.
- **Chuyển ý → H2 sau:** Khi đã khóa xong lớp đệm tiết kiệm trong hạn mức bảo hiểm 350 triệu VNĐ, người gửi tiền thận trọng có thể dùng phần vốn nhàn rỗi còn lại như thế nào trên tài khoản chứng khoán mà không phải đánh cược toàn bộ tiền tích lũy?
- **Không viết:** Không phân tích vàng hay bất động sản chi tiết.
- **Target:** 280

### H2: Phân bổ 10–20% tiền nhàn rỗi sang chứng khoán cùng Môi giới 1:1 tại DSC
- **Câu dẫn từ kết luận bài:** Giữ 80–90% tiền trong sổ tiết kiệm giúp bảo toàn gốc tuyệt đối, nhưng để nâng hiệu suất của toàn bộ danh mục vượt xa mức trượt giá, bạn có thể trích 10–20% phần vốn chưa cần dùng trong 2–3 năm sang cổ phiếu doanh nghiệp đầu ngành hoặc chứng chỉ quỹ ETF niêm yết trên sàn HOSE. Để mua cổ phiếu hay ETF niêm yết, bạn cần thực hiện [cách mở tài khoản chứng khoán](https://www.dsc.com.vn/kien-thuc/cach-mo-tai-khoan-chung-khoan) chính chủ; lưu ý DSC chỉ cung cấp giao dịch cổ phiếu cơ sở và ETF niêm yết, không nhận gửi tiết kiệm ngân hàng và không phân phối chứng chỉ quỹ mở.
- **Bước cụ thể tại DSC:**
  - Bảng mô phỏng dòng tiền 12 tháng trên vốn 500 triệu VNĐ (I112 + I130): Phương án A (100% gửi tại quầy Big 4 ở 5,20%/năm = 26.000.000 VNĐ tiền lãi, bình quân 2.166.667 VNĐ/tháng) vs Phương án B (400 triệu VNĐ chia 2 sổ online TMCP ở 6,80%/năm thu 27.200.000 VNĐ + 100 triệu VNĐ phân bổ vào ETF/cổ phiếu cổ tức trên App DSC Trading; với kịch bản hiệu suất thận trọng 12%/năm trừ phí mua bán 0,2% và thuế bán 0,1% còn 11,7%, phần 100 triệu thu 11.700.000 VNĐ → tổng sinh lời cả danh mục đạt 38.900.000 VNĐ/năm, cao hơn 12.900.000 VNĐ so với gửi quầy Big 4; ngay cả ở kịch bản thận trọng hơn hay giữ 1 sổ Big 4 200 triệu ở 5,90% + 1 sổ TMCP 200 triệu ở 7,00% + 100 triệu cổ phiếu cổ tức tiền mặt 6,1%/năm sau phí thì tổng thu về 31.900.000 VNĐ/năm).
  - 3 bước bắt đầu nhỏ cho người gửi tiết kiệm: (1) Mở tài khoản eKYC 3 phút trên App DSC Trading; (2) Chuyển khoản phần vốn 10–20% qua Mã định danh 963369 (kết nối trực tiếp BIDV, tiền vào ngay tiểu khoản thường đuôi 1); (3) Trao đổi với chuyên gia Môi giới 1:1 (phí giao dịch từ 0,1% giá trị lệnh — tức 100.000 VNĐ cho khoản giải ngân 100 triệu VNĐ) để chọn danh mục ETF VN30 hoặc cổ phiếu trả cổ tức tiền mặt đều đặn.
  - Đoạn Product Bridge 2–3 câu + 1 banner `slim-inline` đúng chuẩn P1.
- **Target:** 250

### H2: Câu hỏi thường gặp khi so sánh lãi suất tiết kiệm ngân hàng
- `#### Câu hỏi?` → câu đầu ≤ 60 từ, có entity + số/mốc.
- **Q1:** Gửi tiết kiệm online hay tại quầy có lãi suất cao hơn? · **Q2:** Rút tiền tiết kiệm trước hạn bị tính lãi suất như thế nào? · **Q3:** Tiền gửi tiết kiệm tối đa bao nhiêu được bảo hiểm tiền gửi chi trả toàn bộ? · **Q4:** Có 500 triệu nên gửi một ngân hàng hay chia nhiều sổ tiết kiệm?
- **Target:** 180

### H2: Kết luận
- **Ý chính:** Chênh lệch 1,6–2,3%/năm giữa nhóm Big 4 và nhóm TMCP tạo ra khoảng cách tới 11.500.000 VNĐ/năm trên mỗi 500 triệu VNĐ, nên người gửi tiền không nên gửi theo thói quen tại quầy một ngân hàng duy nhất. Checklist 3 việc cần làm ngay: (1) Chuyển sổ tại quầy sang kênh online để nhận thêm 0,4–1,6%/năm; (2) Chia khoản tiền trên 350 triệu VNĐ sang ít nhất 2 ngân hàng và tách 1 sổ ngắn hạn 1–3 tháng để không bao giờ mất lãi do rút trước hạn; (3) Trích 10–20% phần vốn nhàn rỗi từ 2–3 năm sang cổ phiếu hoặc ETF niêm yết để nâng lợi suất thực của cả danh mục.
- **CTA:** Tìm hiểu và [mở tài khoản chứng khoán DSC](https://www.dsc.com.vn/mo-tai-khoan) qua eKYC trong 3 phút để có chuyên gia Môi giới 1:1 cùng thiết lập tỷ trọng tích lũy an toàn.
- **Target:** 110

## 6. Liên kết & yếu tố trực quan
- **External links:** Thông tư 04/2022/TT-NHNN trên Cổng văn bản Chính phủ (`https://vanban.chinhphu.vn/?pageid=27160&docid=206118`) tại câu quy định rút tiền tiết kiệm trước hạn; Bảo hiểm tiền gửi Việt Nam (`https://www.div.gov.vn/`) tại câu nêu hạn mức chi trả 350 triệu VNĐ theo Thông tư 05/2026/TT-NHNN.
- **Bằng chứng thực tế (first-hand):** Bảng khảo sát biểu lãi suất 12 ngân hàng tại quầy và online năm 2026 của DSC; phép tính quy đổi tiền lãi thực nhận trên vốn 500 triệu VNĐ và mô phỏng phân bổ 80/20.
- **Spin-off candidates:** `lãi suất ngân hàng nào cao nhất hiện nay` (đã có bài Hub `lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat`), `cách tính lãi suất tiết kiệm ngân hàng` (đã có bài `cach-tinh-lai-suat-tiet-kiem-ngan-hang`).
- **Yếu tố trực quan:**
  1. Ảnh bìa `so-sanh-lai-suat-tiet-kiem-ngan-hang-featured.jpg` (1000×600) vẽ bằng `dsc_design.py`.
  2. Infographic 1 `so-sanh-lai-suat-tiet-kiem-ngan-hang-500-trieu.jpg` (800×500): So sánh tiền lãi 12 tháng của 500 triệu VNĐ giữa 3 nhóm ngân hàng (26,0 triệu vs 32,75 triệu vs 37,5 triệu VNĐ) và ngưỡng bảo hiểm 350 triệu VNĐ.
  3. Infographic 2 `so-sanh-lai-suat-tiet-kiem-ngan-hang-phan-bo-80-20.jpg` (800×500): Mô phỏng dòng tiền 500 triệu VNĐ giữa gửi 100% tại quầy Big 4 (26,0 triệu VNĐ) và công thức 80% tiết kiệm online + 20% đầu tư tại DSC (31,9–38,9 triệu VNĐ).
  4. Banner CTA `slim-inline` chuẩn Persona P1.

## 7. Revision Log
- **v1.0 (2026-11-25):** Khởi tạo outline theo khung Comparison (`SERP_Status: degraded`), tổng hợp biểu lãi suất từ kho dữ liệu live DSC năm 2026, cập nhật hạn mức BHTG 350 triệu VNĐ (Thông tư 05/2026/TT-NHNN) và cầu nối `bridge_to: cach-mo-tai-khoan-chung-khoan`.
