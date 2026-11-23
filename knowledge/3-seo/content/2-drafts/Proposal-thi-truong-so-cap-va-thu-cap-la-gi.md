---
# Khối máy đọc: qa_lint --outline / qa_gate đối chiếu bản Optimize với các trường này. Giữ đúng tên trường.
Target_Keyword: thị trường sơ cấp và thứ cấp là gì
Thesis: "Thị trường sơ cấp là nơi tiền đi vào doanh nghiệp (một lần, lúc phát hành), thị trường thứ cấp là nơi quyền sở hữu đổi tay giữa nhà đầu tư (hằng phiên, doanh nghiệp không nhận thêm đồng nào). Người mới thường mua cổ phiếu trên sàn HOSE/HNX/UPCoM, tức là đang giao dịch ở thị trường thứ cấp."
Entities: [phát hành, chào bán công khai, IPO, bảo lãnh phát hành, tổ chức phát hành, huy động vốn, quyền sở hữu, thanh khoản, nền kinh tế, Sở giao dịch chứng khoán, niêm yết, khớp lệnh, thị trường vốn, trái phiếu Chính phủ]
Entities_Skipped: [câu trắc nghiệm / lời giải / đăng nhập / nâng cấp VIP / giáo viên / học sinh / giá chỉ từ — boilerplate của trang đề thi Vietjack và Scribd, không phải chủ đề bài]
Information_Gain:
  - claim: "Bảng phân biệt 6 tiêu chí theo dòng tiền (tiền về ai, giá do ai quyết định, tần suất, nơi diễn ra, người mua, người bán) thay vì chỉ liệt kê đặc điểm bằng chữ"
    h2: "Bảng so sánh thị trường sơ cấp và thị trường thứ cấp"
    type: comparison
    proof: "Tiền thu được thuộc về"
  - claim: "Ví dụ số minh họa dòng tiền: doanh nghiệp giả định phát hành cổ phiếu thu 200 tỷ đồng ở sơ cấp, sau đó 1.000 cổ phiếu đổi tay ở thứ cấp thì doanh nghiệp nhận 0 đồng"
    h2: "Mối quan hệ giữa thị trường sơ cấp và thị trường thứ cấp (đoạn ví dụ ngắn)"
    type: calc
    proof: "200 tỷ đồng"
  - claim: "Gắn khái niệm với thao tác thật của người mới ở Việt Nam: mua trên sàn là thứ cấp, kèm quy tắc cấu trúc T+2, lô 100 cổ phiếu, biên độ 7% / 10% / 15%, ATO / ATC"
    h2: "Nguyên tắc hoạt động của thị trường chứng khoán (đoạn mở đầu nêu người mới giao dịch ở thứ cấp)"
    type: regulation
    proof: "T+2"
Featured_Snippet: Paragraph
PAA_Questions:
  - q: "[SERP không trả PAA — dùng câu từ GSC] Hoạt động của thị trường thứ cấp làm thay đổi điều gì?"
    placement: faq
  - q: "[GSC] Mua cổ phiếu trên sàn HOSE là thị trường sơ cấp hay thứ cấp?"
    placement: faq
  - q: "[GSC] Nhà đầu tư thứ cấp là gì?"
    placement: faq
  - q: "Thị trường sơ cấp hay thứ cấp quan trọng hơn?"
    placement: faq
---

# 📋 BÁO CÁO TỐI ƯU SEO (SEO Optimization Proposal)

## 0. Content Strategy Header ⚠️ ĐỌC TRƯỚC KHI XEM BẤT KỲ MỤC NÀO

| Thông số | Giá trị |
| :--- | :--- |
| **Target Keyword** | `thị trường sơ cấp và thứ cấp là gì` (key registry: `thị trường so cap va thu cap là gì`) |
| **Secondary Keywords** | `thị trường sơ cấp`, `thị trường thứ cấp là gì`, `thị trường sơ cấp là gì`, `thị trường chứng khoán sơ cấp`, `phân biệt thị trường sơ cấp và thứ cấp`, `so sánh thị trường sơ cấp và thị trường thứ cấp`, `sơ cấp là gì`, `thứ cấp là gì` |
| **LSI / Entities** | `IPO`, `chào bán công khai`, `bảo lãnh phát hành`, `Sở giao dịch chứng khoán`, `niêm yết`, `khớp lệnh ATO/ATC`, `thanh khoản`, `quyền sở hữu`, `thị trường vốn` |
| **Search Intent** | Informational — người tìm muốn phân biệt hai khái niệm và biết mình đang mua bán ở đâu. Một phần lớn query đến từ sinh viên (câu hỏi trắc nghiệm), nhưng người mới mở tài khoản cũng gõ cùng cụm. |
| **Persona** | P2 — F0 Nhà đầu tư mới — cần giải thích kỹ, ví dụ vốn nhỏ, nối khái niệm với hành động đầu tiên là mở tài khoản và đặt lệnh. |
| **Tone** | Thân thiện, xưng "bạn", ví dụ cụ thể; không dạy đời. |
| **DSC Product Bridge** | eKYC (3 phút, không cần ra văn phòng) + Môi giới 1:1 — góc: hiểu phân biệt hai thị trường chưa đủ, bước đầu là có tài khoản để giao dịch ở thị trường thứ cấp, có chuyên gia DSC khi cần hỏi. Không dùng DSC Invest. |
| **Featured Snippet** | Paragraph — đoạn sapo 2 câu định nghĩa song song (hiện bài chưa có sapo). AI Overview của Google đã trích DSC cho cụm này, nên sapo gọn sẽ củng cố vị trí được trích. |
| **Word Count hiện tại** | ~1.140 từ |
| **Word Count mục tiêu** | ~1.500–1.600 từ (hiện ~1.140, tăng 30–40%; VFS 2.086 từ, không cần đuổi theo) |

**Bài gốc đang phục vụ đúng intent/persona không?**
- [x] ✅ Đúng intent, persona P2 hợp lý — GSC xác nhận bài đứng vị trí 1–2 cho gần như mọi query chính.
- [x] ⚠️ Lệch nhẹ ở chất lượng, không lệch hướng: bài hoàn toàn là định nghĩa, không có số, không có ví dụ, không có bảng; có lỗi chính tả và 1 lỗi sai nội dung (xem Section 1).

### Phạm vi (đã chốt với user): chạm nhẹ
Bài top 3, ranking ổn định; đòn bẩy chính là **CTR** (Title, Meta, sapo trả lời trực tiếp). Chỉ có **2 mục THÊM MỚI** là H2 mới (bảng so sánh, FAQ). Ví dụ dòng tiền (200 tỷ đồng) và đoạn "người mới tham gia thế nào" gộp thành đoạn ngắn trong H2 "Mối quan hệ…" và H2 "Nguyên tắc hoạt động…", không tạo H2 mới. Giữ nguyên các sửa lỗi sự thật (chính tả, câu "sơ cấp…sơ cấp").

### Hạn chế tái cấu trúc theo thứ hạng
GSC 90 ngày: vị trí trung bình 3,4 (kỳ trước 5,0); các query chính ở vị trí 1,5–2,0. Vị trí trung bình ≤ 5 nên Proposal này **chỉ** `[GIỮ NGUYÊN]` / `[CẬP NHẬT]` / `[THÊM MỚI]`. Không đổi H1, không đổi thứ tự, không gộp hay xoá H2 hiện có. Các H2 mới chỉ chèn vào khoảng trống giữa các H2 cũ.

### Phân biệt với bài cùng loại `phan-biet-thi-truong-tien-te-va-thi-truong-von-huong-dan-chi-tiet-cho-nha-dau-tu`
So sánh `knowledge/raw/live/html/` của hai bài:
- **Trùng lặp thực tế thấp.** Cụm 6 từ liên tiếp trùng nhau: 0; cụm 4 từ trùng: 17 (1,6% bài này), toàn là tên heading chung ("Khái niệm thị trường", "Kết luận thị trường"). Không có câu chép lại.
- **Cái giống là khung bài, không phải câu chữ:** cả hai theo cùng khuôn "Khái niệm → Đặc điểm → Chức năng → Mối quan hệ → Kết luận", cùng giọng định nghĩa trung tính, không có số, không có ví dụ. Đây là thứ cần phá, không phải sửa câu.
- **Hai bài trả lời hai câu hỏi khác nhau:** bài tiền tệ/vốn phân loại thị trường tài chính theo **kỳ hạn** (dưới / từ 1 năm: tiền gửi, giấy kho bạc vs cổ phiếu, trái phiếu dài hạn); bài này phân loại **thị trường vốn theo giai đoạn của chứng khoán** (phát hành lần đầu vs giao dịch lại). Bài này chỉ nằm trong "thị trường vốn" của bài kia.
- **Cách tách bạch khi viết (bắt buộc trong Bước 4):**
  1. Bảng so sánh dùng tiêu chí **dòng tiền, định giá, tần suất, nơi diễn ra, người mua, người bán**. Không dùng các hàng của bảng bên kia (kỳ hạn, thanh khoản cao/thấp, rủi ro thấp/cao, lợi nhuận thấp/cao).
  2. Không dùng lại các câu mẫu của bài kia ("đáp ứng nhu cầu vốn ngắn hạn/dài hạn", "duy trì thanh khoản hệ thống tài chính", "phân bổ nguồn lực", "giảm thiểu rủi ro bằng đa dạng hóa").
  3. Câu duy nhất nhắc thị trường tiền tệ giữ nguyên vị trí (cuối H2 "Mối quan hệ…") và chèn link về bài tiền tệ/vốn để chuyển phần so sánh sang bên đó, không viết lại ở đây.
  4. Ví dụ và số của bài này xoay quanh một cổ phiếu từ IPO đến sàn, bài kia không có ví dụ nào tương tự.
  5. Cannibalization: GSC `query_value = "thị trường sơ cấp"` cho thấy 99% impressions thuộc về bài này; bài tiền tệ/vốn không xuất hiện. Không cần xử lý gì thêm ngoài tách khung ở trên.
- Không sửa bài tiền tệ/vốn.

---

## 1. Đánh giá Tổng quan (Overall Health)

- **Baseline (bản live, cùng nội dung `Final-…md` tạo từ live):** `qa_lint` 79/100 FAIL (CRITICAL 3, MAJOR 1, MINOR 19) · `slop_check` 71/100 FAIL (MAJOR: evidence 0,18/100 từ, anchor 84% câu không mỏ neo; MINOR: sáo rỗng 0,9/1000 từ, đồng nghĩa 3 biến thể). `market_facts --verify`: 0 vấn đề. `news_feed`: không có tin khớp.
  - Ghi chú: kế hoạch ghi baseline slop 78; `slop_check` hôm nay chấm 71 trên bản live vừa đồng bộ. Gate so với 71, mục tiêu ≥ 80.
- **GSC cấp trang (90 ngày đến 20/11/2026):** 255 clicks, 17.081 impressions, CTR 1,49%, vị trí 3,78. 90 ngày trước: 270 clicks, 15.656 impr, vị trí 4,55 (clicks -6%, impr +9%). Cùng kỳ 2025: 1.356 clicks, 25.616 impr, CTR 5,29%, vị trí 4,55 (clicks -81%). _(Số ở bản trước cộng từ các dòng query bị cắt nên sai; đã thay.)_
- **Kết luận:** thứ hạng ổn định hoặc tốt hơn. Phần mất là **CTR**: các query vị trí 1–2 từ 26–30% xuống 2–7% (nhiều khả năng do AI Overview, vốn đang trích DSC), cộng một phần impressions. Vì vậy đòn bẩy chính là Title/Meta/sapo, không phải tái cấu trúc.

**Chẩn đoán keyword (so cùng kỳ 2025):**

| Query | Clicks | Vị trí | CTR |
| :--- | :--- | :--- | :--- |
| thị trường sơ cấp | 101 → 16 | 1,1 → 2,0 | 30% → 6,9% |
| thị trường sơ cấp và thứ cấp | 63 → 3 | 1,1 → 1,4 | 26% → 2% |
| thị trường thứ cấp là gì | 62 → 10 | — | 10,9% → 2,1% |
| thị trường sơ cấp và thị trường thứ cấp | 59 → 8 (impr 330 → 387) | — | 17,9% → 2,1% |
| thị trường mới nổi thứ cấp là gì | 51 → 5 | 2,0 → 4,1 | — |

Chỉ query cuối là mất thứ hạng thật, vì bài không phủ khái niệm đó (FTSE phân hạng thị trường, khác nghĩa).

**Cơ hội (90 ngày):**

| Query | Impr | Vị trí | CTR | Xử lý |
| :--- | :--- | :--- | :--- | :--- |
| thứ cấp là gì | 520 | 3,2 | 0,19% | Sapo định nghĩa trực tiếp |
| sơ cấp là gì | 444 | 4,2 | 0,23% | Sapo định nghĩa trực tiếp |
| sơ cấp và thứ cấp | 290 | 4,9 | — | Title/sapo |
| sơ cấp và thứ cấp là gì | 211 | 5,3 | — | Title/sapo |
| thứ cấp nghĩa là gì | 146 | — | — | Sapo |
| thị trường mới nổi thứ cấp là gì | 207 | 4,1 | — | FAQ chỉ khi có nguồn whitelist, nếu không **[CẦN XÁC NHẬN]** |
| nhà đầu tư thứ cấp là gì | 64 | 5,7 | — | FAQ |
- **Word Count Gap:** ~1.140 từ, đang trong range so với đối thủ thật (VFS 2.086, vietjack ~1.300–1.900 nhưng boilerplate). Thêm ~350–450 từ: sapo, bảng, FAQ, hai đoạn ngắn gộp.
- **Điểm On-page:** Cần cải thiện. Không có sapo; H2 "Khái niệm thị trường" và "Đặc điểm của thị trường" không chứa từ khóa. Ảnh đầu bài có alt chứa keyword.
- **Vi phạm Anti-AI:** Có. Câu cường điệu rỗng L63 ("có ý nghĩa rất quan trọng…"); 19 MINOR chủ yếu câu > 30 từ (câu dài nhất 64 từ ở đoạn Chức năng sơ cấp); 3 đoạn 4 câu; synonym (thị trường chứng khoán / sàn chứng khoán / thị trường vốn).
- **Lỗi chính tả / sai nội dung cần sửa (không phải anti-AI):**
  - "cháo bán công công khai lần lần đầu" → "chào bán công khai lần đầu" (anchor link IPO).
  - "chứng năng" → "chức năng"; "thông gia việc đấu giá" → "thông qua việc đấu giá"; "tên tiếng anh" → "tên tiếng Anh".
  - **Sai nội dung (quan trọng):** "thị trường sơ cấp có nhịp độ sôi động và khối lượng lớn hơn rất nhiều so với thị trường sơ cấp" — vế sau phải là thị trường thứ cấp. Ngoài ra khẳng định "sôi động hơn rất nhiều" không có số, nên chuyển thành khẳng định có cơ sở: sơ cấp xảy ra theo đợt, thứ cấp diễn ra mỗi phiên.
  - Phần "Nguyên tắc hoạt động" nằm trong H2 chung nhưng 3 đoạn nguyên tắc đều ghi "trên thị trường thứ cấp" — cần nói thẳng điều này ở câu mở đầu H2.
  - Câu "Đấu giá tự động thường được áp dụng trong các phiên ATO, ATC" nên ghi giờ: ATO 9h00–9h15, ATC 14h30–14h45 (HOSE; `market_facts.py --brief` 23/11/2026).
  - Câu "Dòng tiền gia tăng… doanh nghiệp vẫn có lợi vì gia tăng định giá" khẳng định không nguồn — viết lại thận trọng hoặc bỏ.

### Đề xuất cập nhật SEO Elements
> Trong snapshot live chỉ có phần body nên Title/Meta thực tế lấy từ registry; meta hiện tại **[CẦN XÁC NHẬN trên CMS]**.

- **Title hiện tại:** Thị trường sơ cấp và thứ cấp: Phân biệt đặc điểm và chức năng — 61 ký tự (> 59, dễ bị cắt).
- **Title đề xuất (viết cho CTR, giữ cụm chính):** Thị trường sơ cấp và thứ cấp là gì? Phân biệt qua 1 bảng — 56 ký tự. _(Rủi ro thấp: giữ nguyên "thị trường sơ cấp và thứ cấp là gì"; không đổi H1.)_
- **Meta Description hiện tại:** [CẦN XÁC NHẬN trên CMS]
- **Meta Description đề xuất:** Thị trường sơ cấp là nơi chứng khoán phát hành lần đầu, thứ cấp là nơi mua bán lại. Xem bảng phân biệt, ví dụ dòng tiền và cách tham gia cùng DSC. — 146 ký tự.

---

## 2. Phân tích Đối thủ SERP (Competitor Analysis)
> Nguồn: `serp_research.py` cho `thị trường sơ cấp và thứ cấp là gì` và `thị trường sơ cấp và thị trường thứ cấp` (`--force --no-cache`, vì key này chưa có trong registry), và `analyze_competitors.py` (in console). `⚠️ SERP_CHECK`: SERP không có PAA lẫn related searches; top organic toàn là trang đề thi (Vietjack ×5, Scribd ×3, tailieu.vn) vì intent học thuật. DSC không nằm trong 10 organic vì script tự loại domain dsc, và xác nhận được từ AI Overview đang trích DSC + GSC vị trí 1–2 cho gần như mọi query. SERP này **không đủ để học khung bài**, chỉ để biết đối thủ nội dung thật nằm trong AI Overview.

### 2.1 Bảng so sánh tổng quan

| # | URL | Search Intent | Word Count (ước tính) | Điểm nổi bật |
| :--- | :--- | :--- | :--- | :--- |
| 1 | khoahoc.vietjack.com/question/… (5 trang) | Informational (trắc nghiệm sinh viên) | ~1.280–1.912 (phần lớn là giao diện đăng nhập) | Câu hỏi trắc nghiệm + đáp án; không có bài giải thích |
| 2 | vfs.com.vn/phan-biet-thi-truong-so-cap-va-thi-truong-thu-cap | Informational | ~2.086 | Được AI Overview trích; khuôn Khái niệm / Đặc điểm / Vai trò / Nguyên tắc / Mối quan hệ |
| 3 | wiki.batdongsan.com.vn/wiki/thi-truong-thu-cap-la-gi-110210 | Informational → Commercial (bất động sản) | ~2.818 | Được AI Overview trích; nói về BĐS sơ cấp/thứ cấp, không phải chứng khoán |

(`plo.vn/post-753276` là trang chủ tin tức, crawl ra nội dung không liên quan, loại.)

### 2.2 Cấu trúc Outline từng đối thủ

**Đối thủ 1: vfs.com.vn — https://www.vfs.com.vn/phan-biet-thi-truong-so-cap-va-thi-truong-thu-cap**
- **Intent chính:** Phân biệt hai thị trường chứng khoán cho người mới.
- **Mục họ có mà bài mình chưa có:** H2 "1. Phân biệt… chi tiết" mở bằng đoạn tổng quan ~260 từ trước khi vào H3 (bài mình không có sapo); H3 "1.2. Đặc điểm" có đoạn riêng cho từng thị trường.
- **Yếu tố đặc biệt:** Cùng khuôn với bài DSC (khái niệm, đặc điểm, vai trò, nguyên tắc), không bảng, không số ví dụ.
- **Content Gap (so với bài của mình):** Gần như không có gì mình thiếu; điểm khác duy nhất là đoạn mở đầu. Điểm DSC có thể vượt: bảng, ví dụ số, thao tác thật.

**Đối thủ 2: wiki.batdongsan.com.vn — https://wiki.batdongsan.com.vn/wiki/thi-truong-thu-cap-la-gi-110210**
- **Intent chính:** Người xem BĐS muốn biết nhà sơ cấp / thứ cấp khác gì và có nên mua thứ cấp.
- **Mục họ có mà bài mình chưa có:** H3 "Phân biệt giữa thị trường thứ cấp và sơ cấp" (~250 từ) đặt riêng, rõ ràng như một mục so sánh; H2 "Có nên đầu tư vào… thứ cấp?" (~970 từ) trả lời câu hỏi hành động.
- **Yếu tố đặc biệt:** Mục so sánh tách riêng; kết thúc bằng khuyến nghị hành động.
- **Content Gap:** Bài mình không có mục so sánh riêng và không có phần "làm gì tiếp theo"; học cách tách mục so sánh và phần hành động (cho chứng khoán, không lấy BĐS).

### 2.3 Intent Gap — Bài hiện tại đang bỏ sót gì?
- **Intent SERP:** Informational, định nghĩa + phân biệt; top organic là trang đề thi (người học cần đáp án ngắn), AI Overview trả lời bằng 2 câu định nghĩa song song.
- **Intent bài hiện tại:** Đúng intent định nghĩa, nhưng thiếu câu trả lời 2 câu ở đầu bài, thiếu bảng phân biệt (query `phân biệt…`, `so sánh…` đang ở vị trí 2,8 và 5,1, ít click) và thiếu ví dụ cho người mới.
- **Gap cần xử lý:** (1) sapo định nghĩa song song, (2) bảng so sánh, (3) ví dụ dòng tiền, (4) phần "bạn tham gia ở đâu" nối với hành động mở tài khoản, (5) FAQ lấy từ query GSC (không có PAA).

---

## 3. Kết quả 8 Sweeps Audit

| Bước Quét | Đánh giá (1-10) | Vấn đề chính | Ghi chú cải thiện |
| :--- | :--- | :--- | :--- |
| **Clarity** | 5/10 | 19 câu quá dài (đến 64 từ), lỗi chính tả làm khó đọc, 3 đoạn 4 câu | Tách câu, sửa chính tả, mỗi đoạn tối đa 3 câu |
| **Voice** | 4/10 | Giọng giáo trình, không có góc nhìn DSC, không xưng "bạn" | Giọng đồng hành P2: "bạn mua cổ phiếu trên sàn là đang ở thị trường thứ cấp" |
| **So What** | 4/10 | Chỉ nêu khái niệm, không nói người mới được gì khi hiểu | Thêm phần tham gia hai thị trường |
| **Prove It** | 2/10 | 0 số liệu, 0 nguồn, evidence 0,18/100 từ | Quy tắc cấu trúc (T+2, lô 100, biên độ, giờ ATO/ATC) lấy từ `market_facts.py --brief` kèm mốc 23/11/2026 |
| **Specificity** | 3/10 | "sôi động hơn rất nhiều", "rất quan trọng" không số | Ví dụ giả định 200 tỷ đồng, ghi rõ là ví dụ minh họa |
| **Emotion** | 3/10 | Không chạm nỗi lo F0 (mua nhầm chỗ, không biết mình ở thị trường nào) | Một câu mở: người mới thường tự hỏi mình đang mua ở thị trường nào |
| **Zero Risk** | 4/10 | CTA cuối chung chung, anchor "Mở tài khoản" thiếu thương hiệu | Anchor "mở tài khoản DSC", nhắc eKYC 3 phút |
| **GEO/AEO** | 4/10 | Không có sapo, H2 chung chung, không bảng; AI Overview vẫn trích nhờ vị trí 1–2 | Sapo 2 câu định nghĩa song song, bảng, FAQ câu đầu ≤ 60 từ có số + mốc |

---

## 4. Phân tích Chi tiết (Heading-by-Heading Analysis)

### GIỮ NGUYÊN

| Heading | Lý do giữ |
| :--- | :--- |
| H1 (tiêu đề bài trên CMS) | Vị trí 1–2, không đổi H1. |
| Thứ tự toàn bộ H2/H3 hiện có | Giới hạn tái cấu trúc theo thứ hạng. |
| H3: Thị trường sơ cấp là gì? / H3: Thị trường thứ cấp là gì? | Khớp trực tiếp query `thị trường sơ cấp là gì`, `thị trường thứ cấp là gì` (vị trí 1,6 / 1,9). Chỉ sửa nội dung bên dưới (xem CẬP NHẬT), không đổi tên heading. |
| H3: Chức năng của thị trường chứng khoán sơ cấp / thứ cấp | Tên heading giữ; nội dung CẬP NHẬT. |

### XÓA BỎ

| Heading | Lý do xóa |
| :--- | :--- |
| (không có) | Không xóa H2/H3 nào. Chỉ xóa câu: "Việc phân định hai cấp… có ý nghĩa rất quan trọng…" (sáo rỗng, không ý mới) và câu "Dòng tiền gia tăng… gia tăng định giá doanh nghiệp" nếu không tìm được nguồn. |

### CẬP NHẬT

🔄 **Phần mở đầu (trước H2 đầu, không phải heading)** — [THÊM sapo, không đổi heading]
- **Vấn đề:** Bài mở thẳng bằng ảnh rồi H2; không có đoạn trả lời, không chứa keyword, không có hook cho F0.
- **Hướng xử lý:** Định nghĩa trực tiếp cả hai thuật ngữ trong **≤ 40 từ** (sơ cấp: chứng khoán phát hành lần đầu, tiền về tổ chức phát hành; thứ cấp: mua bán lại giữa nhà đầu tư, quyền sở hữu đổi tay) để trả lời "sơ cấp là gì / thứ cấp là gì"; thêm 1 câu nói rõ mua cổ phiếu trên sàn là thứ cấp. Nhắc giữ nguyên vị trí ảnh. Không nhắc brand ở sapo.
- **Entities cần có:** `phát hành`, `quyền sở hữu`, `huy động vốn`
- **Word count target:** ~60 từ (định nghĩa ≤ 40 từ)

🔄 **H2: Khái niệm thị trường** (+ H3 sơ cấp / thứ cấp)
- **Vấn đề:** Lỗi "cháo bán công công khai lần lần đầu", "tên tiếng anh"; câu 35 từ; synonym lẫn lộn.
- **Hướng xử lý:** Sửa chính tả, tách câu, chốt 1 thuật ngữ ("thị trường chứng khoán"). Ở H3 sơ cấp: giữ link IPO; thêm một dòng nêu phương thức phát hành (chào bán công khai, chào bán riêng lẻ, bảo lãnh phát hành) **[CẦN XÁC NHẬN theo Luật Chứng khoán hiện hành trước khi viết; nếu không xác nhận được thì chỉ nêu IPO]**. Ở H3 thứ cấp: nêu nơi diễn ra là HOSE, HNX, UPCoM.
- **Entities cần có:** `IPO`, `chào bán công khai`, `Sở giao dịch chứng khoán`, `niêm yết`
- **Word count target:** ~200 từ

🔄 **H2: Chức năng của thị trường chứng khoán** (+ 2 H3)
- **Vấn đề:** "chứng năng"; câu 64 từ (chính phủ/doanh nghiệp huy động vốn); câu "doanh nghiệp vẫn có lợi vì gia tăng định giá" không nguồn.
- **Hướng xử lý:** Tách câu 64 từ thành 3 câu (Chính phủ phát hành trái phiếu để bù ngân sách; doanh nghiệp phát hành cổ phiếu hoặc trái phiếu để mở rộng; tiền thuộc về tổ chức phát hành). Ở H3 thứ cấp: giữ ý thanh khoản, bỏ khẳng định định giá hoặc viết thận trọng ("giá trên sàn là thước đo nhà đầu tư dùng khi doanh nghiệp huy động vốn lần sau") không kèm số.
- **Entities cần có:** `huy động vốn`, `thanh khoản`, `tổ chức phát hành`, `trái phiếu Chính phủ`
- **Word count target:** ~230 từ

🔄 **H2: Đặc điểm của thị trường**
- **Vấn đề:** **Sai nội dung**: "thị trường sơ cấp … hơn rất nhiều so với thị trường sơ cấp". Khẳng định "sôi động hơn rất nhiều" không có cơ sở số.
- **Hướng xử lý:** Sửa thành so sánh đúng và có cơ sở: sơ cấp diễn ra theo từng đợt phát hành, thứ cấp diễn ra mỗi phiên giao dịch. Bỏ cụm "rất nhiều". Phần bảng so sánh mới đặt ngay sau H2 này (xem mục 5).
- **Entities cần có:** `phiên giao dịch`, `đợt phát hành`
- **Word count target:** ~120 từ

🔄 **H2: Nguyên tắc hoạt động của thị trường chứng khoán**
- **Vấn đề:** "thông gia"; 3 nguyên tắc đều nói về thứ cấp nhưng câu mở đầu không nói; câu ATO/ATC thiếu giờ; câu 45 từ.
- **Hướng xử lý:** Thêm câu mở "ba nguyên tắc dưới đây áp dụng cho thị trường thứ cấp". Sửa chính tả, tách câu. Thêm giờ ATO 9h00–9h15, ATC 14h30–14h45 (HOSE, mốc 23/11/2026, `market_facts.py --brief`). Giữ link "mở tài khoản giao dịch chứng khoán" và "cách chơi chứng khoán cho người mới".
- **Entities cần có:** `khớp lệnh`, `ATO`, `ATC`, `môi giới`, `Sở giao dịch`
- **Gộp thêm (thay H2 "tham gia" riêng):** 1 đoạn ngắn nói người mới gần như luôn giao dịch ở thứ cấp: mở tài khoản, đặt lệnh trên HOSE/HNX/UPCoM; T+2, lô 100 cổ phiếu HOSE, biên độ 7% / 10% / 15% (mốc 23/11/2026, `market_facts --brief`). Proof: "T+2". Mua ở sơ cấp (IPO) theo lịch từng đợt, cũng cần tài khoản.
- **Word count target:** ~320 từ

🔄 **H2: Mối quan hệ giữa thị trường sơ cấp và thị trường thứ cấp**
- **Vấn đề:** Đoạn 4 câu; kết bằng câu sáo rỗng; "Vậy… quan trọng hơn?" trả lời lòng vòng.
- **Hướng xử lý:** Giữ câu trả lời "không bên nào quan trọng hơn" nhưng thêm lý do cụ thể một câu: người mua chấp nhận giá phát hành vì biết sau này bán lại được ở thứ cấp. Giữ link "thị trường tài chính". Đổi câu nhắc thị trường tiền tệ thành link tới bài tiền tệ/vốn (xem phần phân biệt ở trên).
- **Entities cần có:** `thanh khoản`, `thị trường vốn`
- **Gộp thêm (thay H2 ví dụ riêng):** 1 đoạn 3 câu ví dụ giả định, ghi rõ là minh họa: công ty chào bán 10 triệu cổ phiếu giá 20.000 đồng, thu 200 tỷ đồng ở sơ cấp; sau đó 1.000 cổ phiếu đổi tay trên sàn, người bán nhận tiền còn công ty nhận 0 đồng. Proof: "200 tỷ đồng".
- **Word count target:** ~230 từ

🔄 **H2: Kết Luận**
- **Vấn đề:** Câu 42 từ; CTA anchor "Mở tài khoản" thiếu thương hiệu (qa_lint `LINK-cta-anchor`).
- **Hướng xử lý:** Tóm tắt trong 2 câu (sơ cấp = tiền vào doanh nghiệp, thứ cấp = đổi tay giữa nhà đầu tư); CTA P2: "Mở tài khoản DSC — eKYC 3 phút, hoàn toàn online" (anchor có thương hiệu), thêm lựa chọn môi giới 1:1 khi cần hỏi. Không hứa lợi nhuận.
- **Word count target:** ~80 từ

---

## 5. Đề xuất Thêm mới (Content Gaps)

✨ **[THÊM MỚI] H2: Bảng so sánh thị trường sơ cấp và thị trường thứ cấp**
- **Học từ đối thủ:** Competitor 2 — wiki.batdongsan.com.vn (tách mục so sánh riêng); cùng khuôn "phân biệt" của vfs.com.vn nhưng DSC thêm bảng.
- **Vị trí chèn:** Ngay sau H2 "Đặc điểm của thị trường" (trước H2 "Nguyên tắc hoạt động"). Không đổi thứ tự H2 cũ.
- **Nội dung chính:** Bảng 3 cột × 6 hàng theo dòng tiền: Tiền thu được thuộc về (tổ chức phát hành / người bán lại); Ai quyết định giá (tổ chức phát hành và đơn vị bảo lãnh, hoặc đấu giá / cung cầu từng phiên); Tần suất (theo đợt / mỗi phiên); Nơi diễn ra (đợt chào bán, IPO / HOSE, HNX, UPCoM); Người mua (nhà đầu tư mua lần đầu / nhà đầu tư mua lại); Làm tăng vốn cho doanh nghiệp (có / không). Không dùng hàng kỳ hạn, thanh khoản cao/thấp, rủi ro, lợi nhuận (đã thuộc bài tiền tệ/vốn).
- **Entities cần có:** `tổ chức phát hành`, `quyền sở hữu`, `Sở giao dịch chứng khoán`
- **Bằng chứng / Số liệu cần có:** Bảng cấu trúc, không cần số; hàng "giá do ai quyết định" ở sơ cấp **[CẦN XÁC NHẬN: nêu cơ chế đấu giá / bảo lãnh theo quy định hiện hành, hoặc bỏ hàng này]**.
- **Định dạng:** Bảng so sánh (Featured Snippet dạng Table cho query `phân biệt`, `so sánh`).
- **Word count ước tính:** ~120 từ

✨ **[THÊM MỚI] H2: Câu hỏi thường gặp**
- **Học từ đối thủ:** Competitor 1 (Vietjack) — các câu hỏi trắc nghiệm là query thật sinh viên gõ; lấy từ GSC.
- **Vị trí chèn:** Trước "Kết Luận" (sau phần tham gia thị trường).
- **Nội dung chính:** 3 câu, câu đầu ≤ 60 từ, có số hoặc mốc:
  1. "Hoạt động của thị trường thứ cấp làm thay đổi điều gì?" (GSC: query trắc nghiệm, 42 impr, vị trí 2,7): chỉ đổi quyền sở hữu giữa nhà đầu tư, không tăng vốn cho tổ chức phát hành.
  2. "Mua cổ phiếu trên sàn HOSE là thị trường sơ cấp hay thứ cấp?": thứ cấp; trừ khi mua trong đợt chào bán lần đầu.
  3. "Nhà đầu tư thứ cấp là gì?" (GSC 64 impr, vị trí 5,7): nhà đầu tư mua lại chứng khoán từ nhà đầu tư khác ở thị trường thứ cấp, không mua từ tổ chức phát hành.
  4. "Thị trường sơ cấp hay thứ cấp quan trọng hơn?": chuyển ý đã có ở H2 Mối quan hệ thành câu trả lời ngắn; không lặp nguyên văn trong cùng bài (tránh trùng nội dung nội bộ).
  - Tùy chọn **[CẦN XÁC NHẬN]**: query `thị trường mới nổi thứ cấp là gì` (207 impr, 5 clicks, vị trí 4,1) là khái niệm khác (phân hạng thị trường của tổ chức chỉ số, không phải sơ cấp/thứ cấp theo nghĩa chứng khoán). Chỉ thêm một câu phân biệt nếu xác nhận được từ nguồn trong whitelist; không nêu trạng thái nâng hạng của Việt Nam khi chưa có nguồn.
- **Entities cần có:** `quyền sở hữu`, `tổ chức phát hành`, `HOSE`
- **Định dạng:** FAQ (H3 hoặc đoạn đậm cho từng câu, theo `seo-formatting.md`).
- **Word count ước tính:** ~180 từ

---

## 6. Chiến lược Internal Links
> Giữ nguyên 100% link hiện có (IPO, NYSE, Chứng khoán là gì, mở tài khoản giao dịch chứng khoán, cách chơi chứng khoán cho người mới, thị trường tài chính, /mo-tai-khoan). URL lấy từ `find_links.py`, không đoán slug; `qa_gate` kiểm sitemap.

| Anchor Text đề xuất | Bài đích (slug) | Vị trí chèn |
| :--- | :--- | :--- |
| thị trường tiền tệ và thị trường vốn | phan-biet-thi-truong-tien-te-va-thi-truong-von-huong-dan-chi-tiet-cho-nha-dau-tu | H2: Mối quan hệ… (câu nhắc thị trường tiền tệ) |
| thị trường vốn | thi-truong-von-la-gi-cach-tiep-can-cho-nha-dau-tu-ca-nhan | H2: Mối quan hệ… |
| khớp lệnh định kỳ | khop-lenh-dinh-ky-va-khop-lenh-lien-tuc | H2: Nguyên tắc hoạt động (đoạn ATO/ATC) |
| phái sinh | phan-biet-thi-truong-chung-khoan-co-so-va-phai-sinh | H2: Nguyên tắc hoạt động… (đoạn người mới, nếu hợp ngữ cảnh) |

### 📎 Backfill Link Suggestions (`find_links.py --backfill`, snapshot live 23/11/2026)

| Bài nguồn | Đoạn | Anchor | Clicks |
| :--- | :--- | :--- | ---: |
| khop-lenh-dinh-ky-va-khop-lenh-lien-tuc | H2 "Khớp lệnh là gì?" — hiện link qua dòng ">> Xem thêm" | cụm "thị trường sơ cấp và thứ cấp" nếu có sẵn trong câu; chưa có thì bọc cụm có sẵn gần nhất, không đổi chữ | 76 |
| thi-truong-von-la-gi-cach-tiep-can-cho-nha-dau-tu-ca-nhan | H2 "Thị trường vốn là gì?" — hiện link qua dòng ">> Xem thêm" | cụm tương tự trong câu mô tả thị trường vốn | 0 |

Backfill chỉ thực hiện sau khi bài này lên CMS (bước `/link` riêng), không sửa hai bài nguồn trong phiên optimize.

---

## 7. Chiến lược Hình ảnh (Image Strategy & Preservation)

### 7.1 Danh sách hình ảnh GỐC cần bảo toàn (BẮT BUỘC)
| Cú pháp Markdown ảnh gốc | Vị trí hiện tại | Hướng xử lý |
| :--- | :--- | :--- |
| `![Thị trường sơ cấp và thứ cấp là gì](https://extgw.dsc.com.vn/eback/uploads/thi_truong_so_cap_va_thu_cap_94fb0c5b5a.jpg)` | Đầu bài, trước H2 "Khái niệm thị trường" | Giữ nguyên vị trí; sapo mới đặt **trước** ảnh hoặc ngay sau ảnh (không chuyển ảnh sang chỗ khác); alt đã chứa keyword nên giữ. Khi đưa lên CMS dùng đường dẫn tương đối `/uploads/…`. |

### 7.2 Gợi ý vị trí đặt ảnh mới (Tối ưu SEO & UX)
| Vị trí đề xuất | Concept ảnh gợi ý | Alt text tối ưu SEO chứa keyword |
| :--- | :--- | :--- |
| Dưới đoạn ví dụ trong H2: Mối quan hệ giữa thị trường sơ cấp và thị trường thứ cấp | Infographic ngang 2 bước: doanh nghiệp → nhà đầu tư (sơ cấp, 200 tỷ đồng vào doanh nghiệp) và nhà đầu tư ↔ nhà đầu tư (thứ cấp, doanh nghiệp nhận 0 đồng). Theo `image-design-system`, không chữ dài, không dùng màu đỏ. | `dòng tiền thị trường sơ cấp và thứ cấp qua ví dụ phát hành cổ phiếu` |
