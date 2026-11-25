# Content Audit /kien-thuc: Xóa · Sửa · Gộp (GSC + GA4 + chuyển đổi)

- **Nguồn:** GSC Dashboard MCP, property `https://www.dsc.com.vn/`. Đã liên kết GA4 `properties/306412331` và Google Ads `1232517407`.
- **Mục tiêu chuyển đổi:** event `Mo_tai_khoan_thanh_cong` (goal event cấu hình trong dashboard).
- **Kỳ dữ liệu:** 90 ngày (2026-08-06 → 2026-11-03), so với 90 ngày trước (2026-05-08 → 2026-08-05).
- **Đối chiếu:** 845 bài live trong `knowledge/raw/live/pages.csv`.
- **Ngày lập:** 2026-11-05. **v3**: v2 đã bổ sung GA4 và chuyển đổi; v3 kiểm tra intent (GSC query overlap + SERP) cho mọi cặp gộp và chọn đích 301 cho từng bài xóa.

---

## 0. Những gì GA4 làm thay đổi so với bản v1

1. **Trang "cách mua cổ phiếu X" mang về phần lớn lượt mở tài khoản**, không phải bài "nên mua" hay "tổng quan". Bản v1 đề xuất 301 các bài *cách mua* sang bài *nên mua/tổng quan*. Làm vậy sẽ mất chuyển đổi, nên **đề xuất này đã bị hủy**.
2. **Nhiều bài /kien-thuc là trang đích của quảng cáo Dynamic Search Ads (DSA).** Ad DSA `813129083709` (campaign *Search_Mở tài khoản_T6*) không có final URL cố định: Google tự chọn trang trên site. Trong kỳ, ad này có 16.204 click và 286 conversion. Các bài chuyển đổi tốt có sessions cao hơn rất nhiều so với click GSC, ví dụ VCB có 2.680 sessions nhưng chỉ 92 click GSC. Như vậy phần lớn traffic của chúng đến từ Ads.
   → **Trước khi 301 hoặc sửa mạnh bất kỳ bài nào, phải kiểm tra báo cáo Landing pages trong Google Ads.** Đổi URL hay nội dung một trang DSA có thể làm giảm hiệu quả quảng cáo.
3. **Nhiều trang nhiều traffic SEO nhưng 0 chuyển đổi** (`lai-suat-ngan-hang-dong-a`, `co-phieu-nganh-*`, `tu-dien-30-mo-hinh-nen`…). Khi sửa nhóm này, giá trị nằm ở traffic và độ phủ thương hiệu, không phải lead. Thứ tự ưu tiên đã được xếp lại theo đó.

### Bức tranh chuyển đổi toàn site (90 ngày)

| Kênh | Sessions | Mở TK thành công | Tỷ lệ |
|---|---|---|---|
| Toàn site | 132.496 | 533 | 0,40% |
| Organic Search | 66.252 (50%) | 94 (18%) | 0,14% |
| Paid Search | 18.391 (14%) | 320 (60%) | 1,74% |
| Organic Social (Zalo) | 813 | 27 | 3,32% |

Các trang trong `/kien-thuc/` (mọi kênh) mang về **374 / 533** lượt mở tài khoản.

### Top bài /kien-thuc theo lượt mở tài khoản (mọi kênh)

| Bài | Mở TK | Sessions | Click GSC | Ghi chú |
|---|---|---|---|---|
| `cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau` | **118** | 9.450 | 610 | 22% chuyển đổi toàn site, phần lớn từ Ads |
| `cach-mua-co-phieu-vingroup-vic-huong-dan-moi-nhat-2024` | **77** | 2.379 | 290 | Slug có "2024", **giữ nguyên URL** |
| `cach-mua-co-phieu-vcb-ngan-hang-vietcombank` | **67** | 2.680 | 92 | Gần như toàn bộ từ Ads |
| `lam-the-nao-de-mua-co-phieu-mbb-ngan-hang-quan-doi` | **27** | 1.029 | 249 | |
| `top-5-co-phieu-dang-dau-tu` | 13 | 3.999 | 1.448 | Đang mất click (xem mục 2) |
| `cach-mua-co-phieu-hoa-phat-hpg-nhanh-chong-va-an-toan` | 11 | 311 | 46 | |
| `cach-mua-co-phieu-vinamilk-vnm-cho-nguoi-moi-bat-dau` | 8 | 517 | 135 | |
| `cach-mua-co-phieu-fpt-cong-ty-co-phan-tap-doan-fpt` | 8 | 337 | 54 | |
| `cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau` | 6 | 610 | 247 | |
| `cach-mua-co-phieu-ctg` | 5 | 160 | 65 | |
| `cach-mua-co-phieu-bid` | 4 | 250 | 80 | |

---

## 1. GỘP: đã kiểm tra cùng intent hay không (GSC + SERP)

### Cách kiểm tra

Mỗi cặp bài định gộp được kiểm tra bằng 3 tín hiệu:

1. **Trùng query trên GSC (16 tháng):** trong tổng lượt hiển thị của bài sẽ bị gộp, bao nhiêu % nằm trên những query mà bài giữ lại cũng đang nhận.
2. **SERP Google VN (DataForSEO, desktop, top 10 organic):**
   - Lấy *query chính thật* của mỗi bài trên GSC rồi so số URL trùng nhau giữa hai SERP.
   - Ghi lại bài nào của DSC đang được Google xếp cho query đó.
3. **Loại trang Google ưu tiên:** trang dữ liệu mã (vietstock, cafef, simplize), bài phân tích/khuyến nghị (báo cáo CTCK, tin tức) hay bài giải thích khái niệm.

> ⚠️ **Đã hiệu chỉnh độ tin cậy của SERP.** SERP tiếng Việt trong lĩnh vực này rất phân mảnh: hai query rõ ràng cùng chủ đề là *"bollinger bands"* và *"cách sử dụng chỉ báo bollinger bands"* cũng chỉ trùng **0/10** URL.
> Vì vậy **số URL trùng thấp không đủ để kết luận khác intent**. SERP chỉ được dùng làm bằng chứng mạnh khi:
> - tỷ lệ trùng từ 3/10 trở lên, **hoặc**
> - SERP cho thấy Google đang xếp **chính bài A** của DSC cho query chính của bài B.
>
> Nếu không, quyết định dựa vào mức trùng query GSC và loại trang.
>
> Chi phí SERP: khoảng $0,31 (depth 30). Dữ liệu lưu ở thư mục tạm, không ghi đè cache `knowledge/raw/serp/`.

**Quy tắc quyết định:**

| Gộp ✅ | Không gộp ❌, tách intent |
|---|---|
| Từ 60% lượt hiển thị của bài phụ trùng query với bài chính, và query chính của hai bài giống nhau hoặc Google đã chọn một bài cho cả hai | Dưới 50% trùng, hoặc mỗi bài đang giữ một query riêng có click |
| Cả hai bài ~0 chuyển đổi | Bài phụ có chuyển đổi |

### 1a. Bài theo mã cổ phiếu ("nên mua" và "tổng quan")

Bài **"cách mua cổ phiếu X" không nằm trong diện gộp**: đây là intent giao dịch và là trang chuyển đổi (xem mục 0).

Ký hiệu trong bảng:
- **% trùng GSC:** phần lượt hiển thị của bài bị gộp nằm trên query mà bài giữ lại cũng nhận.
- **SERP:** số URL trùng giữa SERP query chính của hai bài.

| Mã | Query chính (giữ / gộp) | % trùng GSC | SERP | Bằng chứng thêm | Quyết định |
|---|---|---|---|---|---|
| **LPB** | "cổ phiếu lpb" / "cổ phiếu lpb" | **100%** | Cùng query | Bài tổng quan ở vị trí 15, 0 click. **GSC 06/11 (16 tháng):** nên mua 557 click, tổng quan 76; tổng quan không giữ query nào có click đáng kể | ✅ Gộp tổng quan → **nên mua** (đã xác nhận) |
| **PLX** | "plx" / "plx" | **95%** | Cùng query | Bài tổng quan có 26,5K imp "plx" nhưng chỉ 33 click. **GSC 06/11 (16 tháng):** đây là cặp lớn nhất, nên mua 875 click, tổng quan 694 (90 ngày: 100 và 70). Nên mua thắng "cổ phiếu plx" (74 so với 33 click), "nhận định" (vị trí 4,4 so với 5,2) và cụm Petrolimex/xăng dầu. Tổng quan thắng "plx" (94 so với 43 click, 55K so với 17K imp) và cụm phân tích: "phân tích cổ phiếu plx" vị trí 3,1 so với 9,4, "định giá" vị trí 4,3 so với 6,3 | ✅ Gộp tổng quan → **nên mua** (đã xác nhận). ⚠️ Phải chuyển phần phân tích/định giá/KQKD của tổng quan sang và thêm "phân tích" vào title. Cặp nhiều click nhất nên **làm sau** khi đã đo kết quả LPB/VJC |
| **VJC** | "vjc" / "vjc" | **91%** | Cùng query | **GSC 06/11 (16 tháng):** nên mua 460 click, tổng quan 258 (90 ngày: 39 và 7). Nên mua giữ "nhận định cổ phiếu vjc" (69 click, vị trí 4,2) và "cổ phiếu vjc". Tổng quan chỉ còn hơn ở "phân tích cổ phiếu vjc" (vị trí 3,7 so với 10,2; 10 click) và nhiều imp hơn cho "vjc" (13,9K so với 4,7K, cả hai ở vị trí 11) | ✅ Gộp tổng quan → **nên mua** (đã xác nhận). Chuyển phần phân tích sang |
| **ACB** | "cổ phiếu acb" / "cổ phiếu acb" | **88%** | Cùng query | SERP "cổ phiếu acb": Google xếp bài *nên mua* ở #6 | ✅ Gộp tổng quan → **nên mua** |
| **VPB** | "cổ phiếu vpb" / "cổ phiếu vpb" | **83%** | Cùng query | Cả hai bài đều không vào top 10 | ✅ Gộp tổng quan → **nên mua** |
| **GAS** | "cổ phiếu gas" / "cổ phiếu gas" | **81%** | Cùng query | Cả hai bài đều không vào top 10 | ✅ Gộp tổng quan → **nên mua** |
| **MWG** | "cổ phiếu mwg" / "cổ phiếu mwg" | **78%** | Cùng query | **GSC 06/11 (16 tháng):** tổng quan 346 click, nên mua 153. Google chọn rõ tổng quan cho cụm phân tích: "phân tích cổ phiếu mwg" vị trí 5,6 (27 click) so với 18,5; "định giá cổ phiếu mwg" 5,9 so với 36,9; "đánh giá" 5,4 so với 11,3; "nhận định" 6,6 so với 11,1. Nên mua chỉ giữ query thực thể ("mwg là gì", "mwg là cổ phiếu gì", "cổ phiếu thế giới di động"). 90 ngày gần nhất nên mua nhỉnh hơn (30 so với 17 click) vì tổng quan đang tụt | ✅ Gộp, **đảo chiều: giữ tổng quan**, gộp nên mua vào. Đưa phần "MWG là gì / Thế giới Di động" của bài nên mua thành một mục, thêm "có nên mua" vào title |
| **VIB** | "cổ phiếu vib" / "cổ phiếu vib" | **73%** | Cùng query | **GSC 06/11 (16 tháng):** nên mua 496 click, tổng quan 205 (90 ngày: 85 và 16). Nên mua giữ "nhận định cổ phiếu vib" (58 click) và "cổ phiếu vib" (36 so với 8). Tổng quan thắng "phân tích" (vị trí 3,7, 22 click, so với 4,8) và "định giá cổ phiếu vib" (vị trí 4,2, 22 click, so với 9,6) | ✅ Gộp tổng quan → **nên mua** (đã xác nhận). Chuyển phần phân tích/định giá sang |
| **HPG** | "cổ phiếu hpg" / "phân tích cổ phiếu hpg" | 67% | 0/10 | SERP "phân tích cổ phiếu hpg": Google xếp **bài nên mua ở #1**, tức đã chọn bài nên mua cho intent của bài tổng quan | ✅ Gộp tổng quan → **nên mua** |
| **SSI** | "có nên mua cổ phiếu ssi" / "cổ phiếu ssi" | 75% | 1/10 | SERP "phân tích cổ phiếu ssi": Google xếp **bài nên mua ở #1** | ✅ Gộp tổng quan → **nên mua** |
| **DIG** | "cổ phiếu dig" / "dig" | 79% | **3/10** | SERP "dig": bài tổng quan ở #1. GSC: tổng quan ở vị trí 3 cho "nhận định cổ phiếu dig" (82 click) | ✅ Gộp. ⚠️ Chọn bài giữ: tổng quan đang xếp tốt hơn trên SERP, nên mua có nhiều click hơn (172 so với 129). **Đề xuất giữ tổng quan** (đang giữ query "dig" và "nhận định"), gộp nên mua vào |
| **BID** | "bid" / "cổ phiếu bidv" | 61% | 0/10 | "bid" là từ tiếng Anh nên SERP bị lẫn. **Kiểm tra lại GSC (06/11, 16 tháng):** query của bài nên mua chỉ khác tên gọi ("bidv" thay vì "bid"): "cổ phiếu bidv" (6 click, vị trí 9,5), "cổ phiếu ngân hàng bidv" (2 click), "mã cổ phiếu bidv"… Bài tổng quan cũng nhận chính các query này ("cổ phiếu bidv" vị trí 13, "cổ phiếu ngân hàng bidv" vị trí 9,3). Bài nên mua chỉ có khoảng 15 click trong 16 tháng, so với khoảng 100 click của tổng quan. Query giao dịch duy nhất là "cách mua cổ phiếu bidv" (3 click), đã có bài `cach-mua-co-phieu-bid` phục vụ | ✅ Gộp nên mua → **tổng quan** (đã xác nhận). Khi gộp: thêm "BIDV" vào title/H1 bài tổng quan và link sang `cach-mua-co-phieu-bid` |
| **REE** | "cổ phiếu ree" / "nhận định cổ phiếu ree" | 80% | 1/10 | **Kiểm tra lại GSC (06/11, 16 tháng):** query "riêng" của bài tổng quan không thật sự riêng, vì bài nên mua cũng có mặt ở đó: "nhận định cổ phiếu ree" (tổng quan vị trí 5,4 với 20 click, nên mua vị trí 6 với 4 click) và "phân tích cổ phiếu ree" (tổng quan vị trí 4,1, nên mua vị trí 4,3). Hai bài cannibal nhau trên cả cụm. Bài nên mua giữ query đầu "cổ phiếu ree" (25 click, vị trí 11,9; tổng quan ở vị trí 21). Bài tổng quan xếp tốt hơn cho "ree là gì" (vị trí 2,3 so với 5,6) và "ree là công ty gì" (1,8 so với 5,3). Click hai bài gần ngang nhau (~45 và ~50) | ✅ Gộp, **giữ tổng quan** (đã xác nhận). Đưa "cổ phiếu REE" lên đầu title/H1 để bài giữ lại nhận query đầu từ bài nên mua. Ưu tiên thấp vì traffic nhỏ |
| **PNJ** | "cổ phiếu pnj" / "co phieu pnj" | **42%** | — | Bài nên mua giữ riêng **"cách mua cổ phiếu pnj"** (vị trí 2, 31 click) và có **3 mở TK**. Bài tổng quan giữ "nhận định/phân tích pnj" (vị trí 5–7) | ❌ **Không gộp.** Đổi title bài nên mua sang hướng "cách mua / có nên mua PNJ", bài tổng quan sang "nhận định PNJ" |
| **FRT** | "frt" / "frt là gì" | **34%** | 1/10 | Bài nên mua giữ "frt là gì" (vị trí 6) và "cổ phiếu long châu"; bài tổng quan giữ "frt" | ❌ **Không gộp.** Tách title: tổng quan = "cổ phiếu FRT", nên mua = "FRT là gì / Long Châu" |

**Lưu ý chung cho nhóm gộp mã cổ phiếu:**
- Với query chính "cổ phiếu X", Google ưu tiên **trang dữ liệu mã** (vietstock, cafef, simplize, cophieu68). Cả hai bài của DSC đều chỉ ở vị trí 8–12.
- Khi gộp, bài giữ lại nên có thêm **khối dữ liệu nhanh** (giá, P/E, vốn hóa, KQKD quý gần nhất) đặt ở đầu bài, để khớp với loại trang Google đang ưu tiên.
- Bài giữ lại có link hoặc CTA sang bài *cách mua X* (nếu có).
- **Kiểm tra GSC ngày 06/11 cho mọi cặp:** bài *tổng quan* thường được Google xếp tốt hơn cho cụm "phân tích / định giá / đánh giá cổ phiếu X" (gặp ở PLX, VJC, VIB, MWG, REE). Khi gộp tổng quan vào nên mua, **bắt buộc chuyển phần phân tích, định giá và KQKD** sang bài giữ lại. Nếu chỉ 301 mà không chuyển nội dung, bài giữ lại sẽ mất cụm query này.

#### Bài "cách mua" và "tổng quan" cùng mã: **không gộp** (giữ như v2)

VCB, CTG, BID, VHM, TPB, PVD, SAB, STB, BVH, HDB: hai bài khác intent (giao dịch và phân tích), và bài *cách mua* có chuyển đổi. Chỉ cần tách title và thêm link chéo.

### 1b. Các cụm chủ đề: phần lớn **không gộp** sau khi kiểm tra intent

| Cụm | % trùng GSC | SERP | Bằng chứng | Quyết định |
|---|---|---|---|---|
| **Bollinger**: `chien-luoc-giao-dich-ket-hop-bollinger-bands-va-duong-ma` → `bollinger-bands-la-gi-...` | 66% | 0/10 (bị nhiễu, xem hiệu chỉnh) | Query của bài chiến lược đều là query của bài chính: "bollinger bands", "cách sử dụng chỉ báo bollinger bands", "bollinger band chuyên sâu". Bài chỉ có 425 chữ, 0 chuyển đổi | ✅ **Gộp**: đưa phần chiến lược kết hợp MA thành một H2 trong bài chính |
| **Người mới**: `cac-kinh-nghiem-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau` → `cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau` | 73% | **0/10** ("cách chơi chứng khoán" so với "kinh nghiệm đầu tư chứng khoán" / "cách đầu tư chứng khoán hiệu quả") | Bài kinh nghiệm giữ riêng "kinh nghiệm đầu tư chứng khoán" (vị trí 14) và "kinh nghiem dau tu" (vị trí 4). SERP 2 query khác hẳn (hướng dẫn nhập môn so với kinh nghiệm/chiến lược). Bài đích là trang chuyển đổi số 1 (118 mở TK), gộp vào có rủi ro | ❌ **Không gộp** (đảo v2). Đổi hướng bài kinh nghiệm sang "kinh nghiệm/chiến lược đầu tư", bỏ "cho người mới bắt đầu" khỏi title/H1 để thôi tranh với bài chính, thêm link sang bài chính |
| **Trái phiếu ngân hàng** → `trai-phieu-la-gi` | **8%** | 1/10 | Bài trái phiếu ngân hàng giữ riêng "trái phiếu ngân hàng là gì" (vị trí 9) | ❌ **Không gộp** (đảo v2). Thêm link từ `trai-phieu-la-gi` |
| **Tại sao nên đầu tư trái phiếu** → `trai-phieu-la-gi` | **17%** | 0/10 | Giữ riêng "có nên đầu tư trái phiếu" (vị trí 5, 7 click) và "lợi ích khi mua trái phiếu" (vị trí 2) | ❌ **Không gộp** (đảo v2) |
| **Quỹ**: `nen-dau-tu-quy-mo-hay-quy-etf` ↔ `nen-dau-tu-quy-etf-nao` | 49% | 1/10 | Bài quỹ mở/ETF giữ riêng intent so sánh: "quỹ mở và quỹ etf" (vị trí 6), "chứng chỉ quỹ etf" (vị trí 5). Phần trùng là "nên đầu tư quỹ etf nào", nơi bài kia đứng vị trí 2 còn bài này ở vị trí 16 | ❌ **Không gộp.** Bỏ "nên đầu tư quỹ ETF nào" khỏi title/H2 của bài quỹ mở để nhường query cho bài kia |
| **"Có X tiền nên đầu tư gì"** | — | — | Chuỗi bài có chuyển đổi (5 triệu: 2, 40 triệu: 1, 300 triệu: 1, có tiền: 1) | ❌ Không gộp (như v2) |
| `cho-nguoi-moi-bat-dau`, `dau-tu-hieu-qua` | — | — | Kiểm tra trực tiếp: đây là **trang danh mục** (title "Cho người mới bắt đầu", "Đầu tư hiệu quả"), không phải bài viết | ❌ Không 301. Nếu danh mục mỏng, cân nhắc `noindex` và viết mô tả danh mục |

**Kết luận mục 1:**
- Gộp **13 cặp mã cổ phiếu** và **1 cặp Bollinger**.
- Hủy 5 đề xuất gộp của v2 vì khác intent: người mới, 2 cặp trái phiếu, quỹ, PNJ/FRT.

---

## 2. SỬA: xếp lại ưu tiên theo giá trị chuyển đổi

### Ưu tiên 1: bài vừa mất traffic vừa có chuyển đổi

| Bài | Click 90 ngày trước → nay | Mở TK | Việc cần làm |
|---|---|---|---|
| `top-5-co-phieu-dang-dau-tu` | 2.458 → 1.448 | 13 | Làm mới danh mục và mốc thời gian, giữ CTA |
| `cach-mua-co-phieu-vingroup-vic-huong-dan-moi-nhat-2024` | (290 click) | **77** | Cập nhật năm trong title/H1/nội dung, **không đổi slug**. Kiểm tra lại các bước mở TK có còn đúng không. |
| `cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau` | 429 → 247 | 6 | Đã có bản Final mới, kiểm tra đã đăng lên CMS chưa |
| `top-5-co-phieu-dau-khi-se-huong-loi-trong-nam-2024-khi-gia-dau-tang` | 331 → 194 | 1 | Cập nhật năm và danh mục |
| `cac-co-phieu-niem-yet-thuoc-tap-doan-vingroup-...-2024` | 1.190 → 752 | 1 | Cập nhật năm trong title/H1, giữ URL, thêm link sang bài *cách mua VIC* (77 mở TK) |
| `cach-mua-co-phieu-flc` | — | 1 (4 key event) | **Không xóa** (đảo ngược v1). Viết lại theo góc "FLC hủy niêm yết, cổ đông làm gì" và giữ CTA. |

### Ưu tiên 2: nhiều traffic, 0 chuyển đổi (cần SEO kèm CRO)

Đây là các trang "trap": nhiều người đọc nhưng không ai mở tài khoản. Sửa SEO để giữ traffic, đồng thời chạy `/cro <slug>` để thêm cầu nối sang sản phẩm (ví dụ bài lãi suất → so sánh lãi suất gửi tiết kiệm với đầu tư).

| Bài | Sessions | Click (trước → nay) | Mở TK |
|---|---|---|---|
| `top-5-co-phieu-nganh-chung-khoan-dang-dau-tu-nhat` | 1.571 | 1.879 → 1.293 | 1 |
| `lai-suat-ngan-hang-dong-a` | 1.275 | 2.489 → 1.180 | 0 |
| `tu-dien-30-mo-hinh-nen-pho-bien-tren-thi-truong-chung-khoan` | 1.161 | 740 | 0 |
| `top-co-phieu-cang-bien-nen-dau-tu` | 969 | 778 | 0 |
| `lai-suat-gui-tiet-kiem-ngan-hang-lpbank` | 943 | 877 | 0 |
| `co-phieu-nganh-cong-nghe` | 850 | 870 → 687 | 0 |
| `co-phieu-nganh-*` (năng lượng, y tế, thực phẩm, nông nghiệp…) | 70–365 mỗi bài | | 0 |

> `lai-suat-ngan-hang-dong-a` mất nhiều click nhất (−1.309) nhưng **0 chuyển đổi**, nên bị hạ từ ưu tiên số 1 (v1) xuống nhóm này. Vẫn nên sửa: Đông Á Bank có thể đã đổi tên thành Vikki Bank (cần kiểm tra lại).

### Ưu tiên 3: CTR thấp, chỉ cần viết lại title và meta

Giữ nguyên danh sách v1: `margin-la-gi`, `chi-so-dow-jones-...`, `cir-...`, `chi-bao-moving-average-envelope-...`, `tieu-san-la-gi`, `bullish-la-gi`, `dong-tien-nong-la-gi`, `uptrend-la-gi`, `bear-trap-la-gi`, `ce-trong-chung-khoan-la-gi`, `duong-phan-tu-quadrant-line-la-gi`, `cagr-la-gi`, `chi-bao-distance-from-moving-average-la-gi`, `backtest-la-gi`.

Các bài này đều dưới 66 sessions hoặc 0 chuyển đổi, nên quyết định theo SEO.

### Ưu tiên 4: bài nền tảng xếp hạng kém, cần viết lại sâu

Giữ nguyên danh sách v1: `co-phieu-la-gi-...`, `chi-so-roe-...`, `san-giao-dich-chung-khoan-la-gi`, `trai-phieu-la-gi`, `chi-so-eps-la-gi`, `cach-dau-tu-chung-khoan-phai-sinh-tai-viet-nam`, `mo-hinh-kinh-doanh-la-gi`, `uy-thac-dau-tu-la-gi`, `lam-phat-nen-dau-tu-gi-...`, `cach-dau-tu-chung-quyen-co-bao-dam-...`, `diem-hoa-von-la-gi`, `cac-thuat-ngu-trong-chung-khoan`, `huong-dan-mo-tai-khoan-chung-chi-quy`.

---

## 3. XÓA: đề xuất đích 301 cho từng bài

**Nguyên tắc chọn đích 301:**
1. Bài đích phải trả lời được **query mà bài bị xóa đang nhận** (lấy từ GSC 16 tháng).
2. Ưu tiên bài **cùng loại intent**: giao dịch → bài hướng dẫn mua, khái niệm → bài khái niệm.
3. Không có đích phù hợp thì **không 301 bừa**. Redirect sang trang không liên quan sẽ bị Google coi là soft-404 và không chuyển được giá trị. Khi đó dùng **410** hoặc giữ lại để sửa.

### 3a. Đã xử lý từ trước (kiểm tra HTTP ngày 05/11/2026), không cần làm gì

| URL cũ | Hiện trạng | Nhận xét |
|---|---|---|
| `quy-trinh-hoan-doi-danh-muc-etf` | 301 → `etf-la-gi` | ✅ Đúng: hai bài trùng nội dung (cùng title, cùng 1.821 chữ); query "quỹ hoán đổi danh mục" = ETF |
| `cach-mua-co-phieu-pdr` | 301 → `cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau` | ✅ Đúng intent (giao dịch) |
| `cach-mua-co-phieu-msn` | 301 → `co-phieu-msn` | ⚠️ Lệch intent (giao dịch → phân tích). Nên đổi đích sang `cach-mua-co-phieu-tren-san-hose` (MSN niêm yết HOSE; bài này có 3 mở TK) |
| `cach-mua-co-phieu-bcm` | 301 → `co-phieu-bcm` | ⚠️ Như trên, nên đổi đích sang `cach-mua-co-phieu-tren-san-hose` |

### 3b. Đề xuất 301 mới

| Bài xóa | Query GSC (16 tháng) | Đích 301 đề xuất | Lý do chọn | Điều kiện trước khi làm |
|---|---|---|---|---|
| `cach-mua-co-phieu-vre` | "cách mua cổ phiếu vingroup" (71 imp, vị trí 11), đây là query duy nhất | `cach-mua-co-phieu-vingroup-vic-huong-dan-moi-nhat-2024` | Khớp đúng query đang nhận và cùng intent giao dịch. VRE thuộc hệ sinh thái Vingroup. Bài đích có **77 mở TK** | Kiểm tra Google Ads Landing pages: không có traffic Ads thì 301 |
| `cach-mua-co-phieu-pow` | 3 click / 90 ngày, không có query đáng kể | `cach-mua-co-phieu-tren-san-hose` | Cùng intent giao dịch (POW niêm yết HOSE). Không chọn `co-nen-mua-co-phieu-pow` vì đó là intent phân tích | Như trên |
| `khoa-hoc-chung-khoan-tan-thu` | 14 imp | `khoa-hoc-chung-khoan` | Trang tổng khóa học "cho người mới, lộ trình chi tiết cho F0", cùng đối tượng tân thủ | Hỏi Marketing: link có đang dùng trong email/Zalo/sự kiện không (301 vẫn giữ được link cũ) |
| `khoa-hoc-ky-thuat-thuc-chien` | 4 imp | `khoa-hoc-phan-tich-ky-thuat-chung-khoan` | Cùng chủ đề phân tích kỹ thuật | Như trên |
| `chinh-sach-cong-la-gi` | 0–1 imp (16 tháng) | `so-sanh-chinh-sach-tai-khoa-va-chinh-sach-tien-te` | Góc bài là "5 điều nhà đầu tư cần biết về chính sách công". Bài đích bao quát cả hai trụ chính sách vĩ mô và có traffic (251 click / 90 ngày). Phương án 2: `chinh-sach-tai-khoa-la-gi` | Không có |

### 3c. Bỏ khỏi danh sách xóa

| Bài | Lý do |
|---|---|
| `rua-tien-la-gi-hau-qua-va-cach-phong-chong` | GSC theo tháng: **11/2025–4/2026 đứng vị trí 2,8–4, khoảng 3–9,7K imp/tháng** cho "rửa tiền là gì" (29K imp). **Rớt từ 5/2026** xuống vị trí 13–17. Bài chỉ có 407 chữ, CTR thấp (0,1–0,2%, query định nghĩa). **Không có đích 301 phù hợp** trên site. → **SỬA**: mở rộng theo góc chứng khoán (rửa tiền qua chứng khoán, quy định phòng chống rửa tiền, KYC/eKYC khi mở tài khoản), qua đó có cầu nối tự nhiên sang mở tài khoản. Nếu không muốn giữ: dùng **410**, không 301. |
| `cach-mua-co-phieu-flc` | 1 mở TK (110 sessions). Chuyển sang mục SỬA |
| `co-phieu-la-gi-cac-loai-co-phieu-...` | Bài nền tảng có 16 inlink. Chuyển sang mục SỬA (ưu tiên 4) |
| `cho-nguoi-moi-bat-dau`, `dau-tu-hieu-qua` | Là trang danh mục, không phải bài viết |

**Không xóa:** bài mới đăng chưa đủ 90 ngày dữ liệu: `krx-la-gi`, `100-trieu-gui-ngan-hang-lai-bao-nhieu-1-thang`, `50-trieu-nen-gui-tiet-kiem-ngan-hang-nao`, `sinh-vien-nen-dau-tu-gi`, `1-hop-dong-phai-sinh-bao-nhieu-tien`, `chi-so-s-p-500-la-gi`, `lenh-stop-limit-la-gi`, `chi-so-dar-la-gi`.

### Quy trình áp dụng cho mọi 301 (gộp và xóa)

1. Đưa nội dung còn giá trị của bài bị gộp sang bài đích (với các cặp gộp).
2. Đặt 301 trên CMS.
3. Sửa toàn bộ internal link đang trỏ vào URL cũ cho trỏ thẳng đích, không đi qua redirect: `python scripts/find_links.py --backfill <slug-cũ>` kết hợp `scripts/link_plan.py` (op `href`).
4. Chạy `python scripts/sync_live.py --only <slug-đích>`, sau đó `scripts/link_plan.py verify`.
5. Gỡ URL cũ khỏi sitemap. Theo dõi query của bài cũ trên bài đích sau 2–4 tuần.

---

## 4. Lỗi kỹ thuật

1. **URL sai chính tả trả về 200 (soft-404):** khoảng 700 URL. Đã thử 3 URL, cả 3 đều chuyển về `/kien-thuc` với mã 200. Đề xuất dev cho slug không tồn tại trả 404, hoặc 301 về bài có slug gần nhất.
2. **GA4: referral nội bộ** (theo dashboard `source_issues`).
   - `accounts.hvsvn.com` (12.445 sessions) và các host `*.dsc.com.vn` (trading, wetrade, accounts…) đang bị ghi là Referral, khiến chuyển đổi sau đăng nhập bị gán sai nguồn.
   - Cần thêm các host này vào **GA4 → Admin → Data streams → Configure tag settings → List unwanted referrals**.
   - Chưa sửa thì con số "Organic chỉ có 0,14% chuyển đổi" có thể đang bị đánh giá thấp.
3. **`(not set)` landing page:** 7.702 sessions, 2 chuyển đổi. Có thể do event không gắn page. Nên kiểm tra cấu hình GA4.

---


## 5. Thứ tự làm

1. **Trước mọi 301:** xuất báo cáo **Google Ads → Landing pages (90 ngày)**. URL nào đang là trang đích của quảng cáo Dynamic Search Ads thì không 301.
   - ✅ **Đã kiểm tra ngày 06/11/2026 qua GSC Dashboard MCP (06/08 → 03/11):** GA4 kênh Paid Search có 109 landing page, tổng 18.395 sessions, khớp tổng kênh nên danh sách là đầy đủ. Trong 19 URL sẽ 301 (13 bài gộp mã cổ phiếu, Bollinger và 5 bài ở mục 3b), chỉ `co-phieu-ssi-tong-quan-…` có 4 sessions, 0 mở TK. 18 URL còn lại không có session Paid nào. Báo cáo PMax landing pages trong Google Ads cũng không có URL nào trong số này. **Kết luận: không URL nào là trang đích Ads, có thể 301.**
   - Chưa kiểm tra được kênh Cross-network trong GA4 (4.082 sessions) vì tool lỗi. Bài giữ lại `cach-mua-co-phieu-tren-san-hose` (đích 301 của pow/msn/bcm) có 56 sessions Paid và 1 mở TK, nên vẫn giữ nguyên.
2. **Tuần 1:** sửa ưu tiên 1 (top-5 cổ phiếu, cách mua VIC, Vingroup 2024). Đổi đích 301 của msn/bcm sang `cach-mua-co-phieu-tren-san-hose`.
3. **Tuần 1–2:** gộp 13 cặp mã cổ phiếu (mục 1a). Bắt đầu với các cặp mà bài phụ yếu rõ: LPB, VJC, ACB, VIB. **PLX làm sau cùng** (hai bài đều có ~700–900 click) khi đã thấy kết quả đợt đầu. Thêm khối dữ liệu nhanh và CTA sang *cách mua*.
4. **Tuần 2:**
   - Tách intent cho các cặp không gộp: PNJ, FRT, bài kinh nghiệm/người mới, quỹ mở/ETF (sửa title/H1, link chéo).
   - Viết lại title/meta cho ưu tiên 3.
5. **Tuần 3:**
   - Gộp Bollinger.
   - 301 các bài ở mục 3b sau khi có xác nhận từ Ads và Marketing.
   - Sửa `rua-tien-la-gi`.
6. **Song song:** dev xử lý soft-404, Analytics xử lý unwanted referrals.
7. **Đo lại:** 4–6 tuần sau mỗi đợt.
   - Click GSC của bài đích, theo dõi query của bài cũ đã chuyển sang chưa.
   - `Mo_tai_khoan_thanh_cong` theo trang.

---

## Giới hạn dữ liệu

- **Chuyển đổi theo URL** chỉ có cho 300 trang có nhiều sessions nhất (từ 66 sessions trở lên). Các trang ít hơn ghi "<66 ph." là **không có số**, không phải bằng 0.
- **Chưa tách được kênh theo từng trang.** Bộ lọc `channel` của `get_conversion_breakdown` đang lỗi phía server. Ước lượng phần traffic không phải organic bằng *sessions GA4 − click GSC*. Muốn số chính xác, xem GA4 Explore: Landing page × Session default channel group × `Mo_tai_khoan_thanh_cong`.
- **Hai loại số chuyển đổi khác nhau:** `ga4_conversions` trong Content Matrix tính mọi key event (ví dụ VCB = 428), còn bảng chuyển đổi trong file này chỉ tính `Mo_tai_khoan_thanh_cong` (VCB = 67). File này dùng số `Mo_tai_khoan_thanh_cong`.
- **Cannibalization** lấy từ 500 cặp query–trang có nhiều impressions nhất (trong khoảng 25.000 cặp).
- **Không dùng % trong báo cáo "content decay"** vì kỳ cuối chưa đủ ngày. Mọi so sánh trong file là 90 ngày so với 90 ngày.
- **Trước khi đặt 301:** cập nhật internal link bằng `python scripts/find_links.py --backfill <slug>` và `scripts/link_plan.py`, sau đó chạy `sync_live.py` để kiểm tra.
- **SERP:** DataForSEO, Google VN desktop, lấy ngày 05/11/2026, chụp tại một thời điểm. Kết quả video (`google.com/goto`, YouTube) đã bị loại khỏi organic. SERP trong lĩnh vực này rất phân mảnh nên chỉ dùng làm tín hiệu phụ (xem phần hiệu chỉnh ở mục 1).
- **Trùng query GSC** tính trên 1.000 cặp page×query có nhiều impressions nhất của các bài cần xét (16 tháng). Bài nhỏ có ít query nên tỷ lệ % dao động hơn.
