# Phân tích content: VPBankS Trung tâm kiến thức vs DSC

*Ngày phân tích: 2026-11-03 · Phạm vi: content + internal link (bỏ qua backlink)*
*Dữ liệu: crawl 62/65 bài `vpbanks.com.vn/trung-tam-kien-thuc/` (`scripts/competitor_crawl.py` → `knowledge/raw/competitors/vpbanks/`), GSC `sc-domain:dsc.com.vn` (15/08–31/10/2026 so với cùng kỳ 2025), snapshot live DSC (`knowledge/raw/live/`).*

---

## TL;DR — 5 nguyên nhân chính (xếp theo mức ảnh hưởng)

1. **Mỗi head term có 1 trang "X là gì" đúng intent, còn DSC thường để trang lệch intent hoặc trang mỏng ra rank.** Ví dụ: "cách chơi chứng khoán" → DSC rank bằng bài "cách đầu tư… cho người mới"; "ETF là gì" → trang ETF của DSC nằm ở vị trí ~18; "bullish là gì" → bài DSC chỉ có **440 từ**, bài VPBankS có 3.656 từ.
2. **Outline phủ đủ intent theo một khuôn cố định:** định nghĩa → cơ chế/phân loại → công thức + ví dụ → ưu/nhược → so sánh với khái niệm gần → hướng dẫn từng bước → FAQ → "làm X cùng VPBankS". Bài DSC cùng chủ đề hay thiếu phần so sánh, ví dụ số, bước thực hành và FAQ.
3. **Bài dài gấp đôi, nhiều media:** median VPBankS **2.644 từ / 7 H2 / 7 ảnh / 1 bảng**, median DSC 1.282 từ. Ở các cặp bài DSC bị tụt, VPBankS dài hơn **2–8 lần**.
4. **Cụm bài dày, link nội bộ dồn vào pillar với anchor khớp chính xác keyword:** 88% anchor khớp với slug đích. Các pillar (`co-phieu-la-gi`, `cach-choi-chung-khoan`, `etf-la-gi`, `margin-la-gi`) nhận 17–25 inlink từ 62 bài.
5. **Đăng dồn theo đợt, rồi refresh bài trọng điểm:** 58/62 bài đăng trong 4 tháng (7–10/2026), theo từng đợt 4–16 bài/ngày. Ngày 30/10 có 5 bài pillar vừa được cập nhật.

> **Bằng chứng tương quan, chưa phải nhân quả:** trên toàn site DSC, các query **không** trùng chủ đề VPBankS có vị trí *tốt lên* YoY (7,84 → 7,13), mất click chủ yếu do CTR (AI Overview). Còn các query chứa keyword của 22 chủ đề VPBankS lớn nhất (chơi chứng khoán, ETF, CCQ, IPO, P/E, margin, lệnh LO/MP, cổ tức, OTC…) thì vị trí *tụt* (14,7 → 16,5) và mất **−87,6% click** (3.208 → 397). Chưa xác minh trực tiếp VPBankS đứng trên DSC ở từng SERP: cache SERP mới có 6/63 keyword và đã cũ 1–1,5 tháng (xem §7).

---

## 1. Tổng quan site đối thủ

| Chỉ số | VPBankS | DSC |
|---|---|---|
| Số bài kiến thức | **62** (sitemap 65, 3 URL là trang category) | 845 |
| Median từ/bài | **2.644** | 1.282 |
| Median H2 / H3 | 7 / 6 | — |
| Bài có FAQ | 21/62 (34%) | — |
| Bài có bảng | 41/62 (66%) | — |
| Median ảnh/bài | 7 | — |
| Tác giả hiển thị | 2 người (Nam Cao Hoàng: 57 bài) | — |
| Category | Kiến thức chung 37 · Sản phẩm đầu tư 22 · Tài khoản 3 | — |

- Kỹ thuật: Next.js + headless CMS. Thân bài nằm trong payload RSC, Google render được bình thường. **Không có schema Article / FAQPage / datePublished**, chỉ có Organization, WebSite và BreadcrumbList. Như vậy họ không thắng nhờ schema.
- Bài "Kiến thức liên quan" (3 bài) được render phía client, không có trong HTML ban đầu.
- 3 bài gần như rỗng (`cach-doc-bao-cao-tai-chinh`, `huong-dan-choi-chung-khoan-phai-sinh`: 0 từ trong body; `nhap-mon-chung-khoan`: 14 từ). Có thể nội dung nằm ở block khác, cần kiểm tay.

**Kết luận:** VPBankS **không** thắng nhờ số lượng (62 so với 845 bài). Họ thắng nhờ mỗi bài nhắm một head term lớn, viết rất sâu và gom link nội bộ vào đó.

---

## 2. Chủ đề — họ chọn gì

Gần như toàn bộ là **head term định nghĩa cho F0** (dạng "X là gì"), volume cao:

- **Sản phẩm:** cổ phiếu, trái phiếu, trái phiếu chuyển đổi, chứng chỉ quỹ, ETF, quỹ mở/đóng/cân bằng, chứng quyền, phái sinh, hàng hóa phái sinh, cổ phiếu ưu đãi/penny/bluechip, OTC
- **Chỉ số:** P/E, P/B, EPS, ROE, ROA, EBIT, GDP, VN-Index, Bollinger
- **Giao dịch:** lệnh LO/MP/MOK/ACT, phiên giao dịch, giá trần/sàn, bảng giá, phí giao dịch, thanh khoản, margin, tỷ lệ ký quỹ, bắt đáy, tự doanh
- **Hành trình F0 + sản phẩm:** cách chơi chứng khoán (+ trên điện thoại), mở tài khoản (+ "không dùng có sao không"), app chứng khoán, nguyên nhân không mua bán được cổ phiếu, đánh giá VPBankS

### Đối chiếu với DSC (map theo slug)

| Tình trạng | Chủ đề |
|---|---|
| **DSC chưa có bài riêng** | P/B, lệnh MP, lệnh MOK, lệnh ACT, VN-Index "là gì" (chỉ có bài dài về ý nghĩa), tỷ lệ ký quỹ (chỉ có `/huong-dan/`), cổ phiếu bluechip, bắt đáy, quỹ cân bằng, quỹ đóng, các phiên giao dịch, đọc bảng giá, cho vay cầm cố trái phiếu, trái phiếu vs gửi tiết kiệm, nguyên nhân không mua bán được, chơi chứng khoán trên điện thoại, công thức tính GDP |
| **DSC có bài nhưng mỏng hơn nhiều** | bullish (440 so với 3.656 từ), OTC (611 so với 5.189), trái phiếu chuyển đổi (1.058 so với 3.958), so sánh cổ phiếu–CCQ (1.114 so với 2.584), lệnh LO (gộp chung vào bài ATO/ATC/LO/MP), IPO (1.329 so với 3.162), thanh khoản (1.386 so với 3.331), phí giao dịch (1.390 so với 3.839) |
| **DSC có bài tương đương** | margin, EPS, EBIT, ROE, cổ tức, chứng chỉ quỹ, ETF, trái phiếu, mở tài khoản: độ dài gần bằng; khác biệt nằm ở intent, outline và link (xem §3) |

---

## 3. So sánh từng cặp bài (trang DSC bị tụt)

GSC, 15/08–31/10/2026 so với cùng kỳ 2025:

| Query | Trang DSC đang rank | Vị trí LY → nay | Click LY → nay | DSC (từ / H2) | VPBankS (từ / H2 / bảng / FAQ) |
|---|---|---|---|---|---|
| cách chơi chứng khoán | cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau | 2,85 → **4,74** | 498 → 71 | 3.357 / 6 | 2.673 / 7 / 0 / – |
| bullish là gì | bullish-la-gi-xu-huong-… | 2,20 → 3,53 | 14 → 0 | **440** / 6 | 3.656 / 7 / 2 / – |
| ipo là gì | niem-yet-chung-khoan-ipo-la-gi-… | 7,29 → **17,37** | — | 1.329 / 7 | 3.162 / 8 / 2 / – |
| chứng khoán phái sinh là gì | chung-khoan-phai-sinh-la-gi-huong-dan-… | 7,30 → **15,91** | — | — | 3.500 / 7 |
| p/e là gì | chi-so-p-e-la-gi-… | 9,09 → 12,79 | 13 → 0 | 2.099 / 8 | 1.944 / 7 / 0 / ✓ |
| lệnh lo là gì | lenh-ato-atc-lo-mp-la-gi (bài gộp) | 8,12 → **26,63** | 5 → 0 | 1.668 | 2.439 / 8 / ✓ |
| vnindex là gì | chi-so-vn-index-va-y-nghia-… | 6,75 → 13,21 | — | — | 2.506 / 6 |
| etf (cụm) | cach-dau-tu-etf-… (lệch intent) | 8,58 → **25,61** | 188 → 8 | 1.459 / 4 | 3.410 / 9 / 2 / ✓ |
| chứng chỉ quỹ (cụm) | top-chung-chi-quy-… (lệch intent) | 14,1 → 14,2 | 120 → 22 | 1.305 / **3** | 4.212 / 8 / 1 / – |

Một số trang DSC lại **đang lên**: `margin-la-gi` (36,8 → 9,4), `etf-la-gi` (33,3 → 17,7), `co-tuc-la-gi` (60,9 → 13,5). Tức là khi DSC có trang đúng intent thì Google vẫn đẩy lên. Vấn đề là trang đúng intent của DSC còn yếu, hoặc đang bị trang khác của chính DSC chiếm query (cannibalization).

### Ví dụ outline: "ETF là gì"
- **DSC** (trang đang rank cho cụm "etf"): *Cách đầu tư ETF cho người mới / Chiến lược DCA / 5 lưu ý / Kết luận*. Bài bỏ qua phần định nghĩa.
- **VPBankS:** *1. Quỹ ETF là gì · 2. Cơ chế hoạt động · 3. Đặc điểm · 4. Ưu/nhược · 5. Các quỹ ETF phổ biến tại VN · 6. So sánh ETF với quỹ mở và cổ phiếu · 7. Hướng dẫn mua · 8. Giao dịch trên NEO Invest · 9. FAQ*

### Ví dụ outline: "Bullish là gì"
- **DSC (440 từ):** định nghĩa / nguồn gốc / dấu hiệu / chiến lược / lưu ý / kết luận. Mỗi H2 chỉ 1–2 đoạn.
- **VPBankS (3.656 từ):** + *Phân biệt bullish và bearish, bull và bear market* · *Các giai đoạn của thị trường bullish* · *Mô hình nến bullish* · 2 bảng.

---

## 4. Khuôn outline của VPBankS

- **97% H2 có đánh số** ("1. … 2. …"), 7–9 H2 mỗi bài. **Không bài nào có H2 "Kết luận".**
- Thứ tự cố định: định nghĩa → phân loại/cơ chế → công thức + ví dụ số → ý nghĩa → "bao nhiêu là tốt / có nên…" → so sánh → hướng dẫn từng bước → sai lầm cần tránh → FAQ.
- **H2 cuối là product bridge** ở 18/58 bài: "Giao dịch ETF trên app NEO Invest", "Đầu tư chứng chỉ quỹ cùng VPBankS".
- 39/62 bài có **link trỏ về chính nó** ngay câu đầu (anchor là keyword chính). Không có tác dụng SEO rõ ràng, nhưng cho thấy câu mở bài luôn đặt keyword chính lên đầu.
- 2/3 bài có bảng, thường là bảng so sánh hoặc phân loại. Đây là dạng nội dung hay được lấy làm featured snippet hoặc trích trong AI Overview.

---

## 5. Internal link

| | VPBankS (62 bài) | DSC (845 bài) |
|---|---|---|
| Link sang bài kiến thức khác / bài (không tính tự link) | ~5,4 | ~3,8 |
| Tỷ lệ link "Xem thêm" / tổng link KB | **56%** (207/370) | 34% (1.100/3.228) |
| Anchor khớp slug đích | **88%** | — |
| Median inlink / bài | 3 | 2 |
| Bài 0 inlink | 15/62 | 92/845 |
| Link từ section khác vào bài kiến thức | **0** (mẫu 300 trang `/post`, `/trung-tam-phan-tich`, `/khoa-hoc`…; menu chỉ link về trang hub) | — |

- Hub nhỏ và khép kín, nên mỗi pillar nhận inlink từ **25–40% số bài trong hub**: `co-phieu-la-gi` 25, `cach-choi-chung-khoan` 24, `dau-tu-co-phieu` 22, `etf-la-gi` 21, `margin-la-gi` 19, `chung-chi-quy-la-gi` 17. Với DSC, `cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau` có 68 inlink nhưng nằm trong 845 bài, nên tỷ lệ tương đối thấp hơn nhiều.
- Họ **vẫn dùng "Xem thêm" nhiều**, cuối mỗi section. Như vậy internal link không phải lợi thế kỹ thuật lớn của họ. Lợi thế là tín hiệu rõ: anchor khớp chính xác và mọi link trong cụm dồn về một trang cho mỗi khái niệm.
- Link ra: trang chủ (38), `/trung-tam-phan-tich` (16), trang app NEO Invest (9), link mở tài khoản onelink (11), nguồn ngoài rất ít (thuvienphapluat 4, dantri 1).

---

## 6. Tần suất đăng & cập nhật

| Tháng | Bài mới | Ghi chú |
|---|---|---|
| ≤ 2025 | 4 | bài cũ migrate sang CMS mới |
| 07/2026 | 20 | 4 đợt: 07/07, 16/07, 21/07, 23/07 |
| 08/2026 | 20 | 13/08, 15/08, **22/08 (11 bài/ngày)** |
| 09/2026 | 15 | **27/09 (15 bài cùng ngày)** |
| 10/2026 | 3 | + **refresh 30/10**: margin, app chứng khoán, sàn giao dịch, chơi CK trên điện thoại, VN-Index |

- Hub mới ra mắt (CMS tạo 09/2025, nội dung đổ vào từ 07/2026). Thời điểm DSC tụt trên các chủ đề trùng khớp với các đợt đăng này.
- **DSC không thua về tần suất:** từ 07/2026 DSC đã thêm 115 bài finalized. Nhưng chỉ 6 bài cũ được sửa, trong khi các trang DSC bị tụt ở §3 chính là bài cũ chưa refresh.

---

## 7. Giới hạn của phân tích

- Chưa xác minh trực tiếp thứ hạng VPBankS trên từng SERP. Cache SERP (09–10/2026) mới thấy VPBankS ở 6/63 keyword: app đầu tư chứng khoán #4, cách mở tài khoản #4, ngày đáo hạn phái sinh #4, cổ phiếu vs CCQ #6, full margin #7, cách bán cổ phiếu cho người mới #7. Muốn khẳng định cần chạy `serp_research.py` cho ~10 query ở §3 (**tốn phí DataForSEO**).
- Impression của một số query giảm mạnh (bullish 6.055 → 961) nên một phần thiệt hại là do nhu cầu tìm kiếm / SERP feature, không chỉ vì đối thủ.
- Ngày `updated_at` lấy từ CMS (đáng tin). `lastmod` trong sitemap là thời điểm deploy, không dùng.
- Phân loại CTA trong `links.csv` đếm nhầm link tới bài `app-chung-khoan` / `mo-tai-khoan-chung-khoan` thành CTA (regex khớp chữ `mo-tai-khoan`, `/app`).

---

## 8. Hành động cho DSC

### A. `/optimize` ngay: bài cũ đang mất vị trí (ưu tiên theo click mất)
1. `cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau`: thêm H2 "chơi chứng khoán là gì", "chuẩn bị gì", "sai lầm cần tránh"; đưa từ "chơi" vào title/H1 (query chính là "cách chơi chứng khoán", −427 click).
2. `bullish-la-gi-…`: viết lại lên ~2.500 từ; thêm bull/bear, các giai đoạn, mô hình nến, bảng so sánh.
3. `niem-yet-chung-khoan-ipo-la-gi-…`: thêm "nhà đầu tư có nên mua IPO, cách tham gia" + các thương vụ IPO nổi bật ở VN (bảng).
4. `chung-khoan-phai-sinh-la-gi-…`, `chi-so-p-e-la-gi-…` (thêm "P/E bao nhiêu là tốt ở VN" + FAQ), `chi-so-vn-index-…`.
5. Cụm ETF và chứng chỉ quỹ: **sửa cannibalization**. Đổi anchor/link nội bộ cho query "là gì" trỏ về `etf-la-gi` và `chung-chi-quy-la-gi` (2 trang này đang lên), bài "cách đầu tư ETF" và "top CCQ" link ngược về. Kiểm tra bằng `get_cannibalization` trước khi sửa.

### B. Bài mới (`/keyword-plan` / `/outlining`)
Tách bài riêng cho các chủ đề DSC chưa có hoặc đang gộp: **lệnh LO, lệnh MP, lệnh MOK, lệnh ACT** (tách từ bài ATO/ATC gộp), **P/B là gì**, **VN-Index là gì**, **tỷ lệ ký quỹ là gì**, **cổ phiếu bluechip**, **bắt đáy**, **các phiên giao dịch**, **cách đọc bảng giá**, **quỹ đóng / quỹ cân bằng**, **nguyên nhân không mua bán được cổ phiếu**, **trái phiếu hay gửi tiết kiệm**.

### C. Chuẩn outline cho bài định nghĩa (bổ sung vào skill outlining)
- Đủ các khối: định nghĩa → phân loại/cơ chế → công thức + ví dụ số VN → "bao nhiêu là tốt / có nên" → so sánh với khái niệm gần (bảng) → hướng dẫn từng bước → FAQ (lấy từ PAA) → product bridge DSC.
- Độ dài mục tiêu cho head term: **2.200–3.000 từ**. Không đặt sàn cứng cho long-tail.
- Mỗi bài ít nhất 1 bảng so sánh hoặc phân loại.

### D. Internal link
- Mỗi khái niệm chỉ có **1 trang đích**. Anchor đúng keyword trỏ về trang "X là gì", không trỏ về bài hướng dẫn.
- Chạy `find_links.py --backfill <slug>` cho các trang ở mục A sau khi sửa, để kéo inlink ngữ cảnh từ cụm bài liên quan.

### E. Nhịp refresh
- Trích **10–15% công suất** sang refresh bài cũ có head term, đặc biệt các trang ở §3. Hiện chỉ 6 bài cũ được sửa so với 115 bài mới.
- Theo dõi: chạy lại `python scripts/competitor_crawl.py` mỗi tháng (~3 phút), diff `pages.csv` để thấy bài mới / refresh của VPBankS.
