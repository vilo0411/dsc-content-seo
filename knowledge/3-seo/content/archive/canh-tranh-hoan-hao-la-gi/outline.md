---
# Khối máy đọc: qa_lint --outline / qa_gate đối chiếu bản Optimize với các trường này.
Target_Keyword: cạnh tranh hoàn hảo là gì
Thesis: "Cạnh tranh hoàn hảo là mô hình chuẩn để đo các thị trường khác: một doanh nghiệp chỉ là người chấp nhận giá, lợi nhuận kinh tế về 0 ở dài hạn, và thị trường cổ phiếu niêm yết gần với mô hình này ở số lượng người mua bán và giá công khai nhưng lệch ở thông tin và biên độ giá."
Entities: [thị trường cạnh tranh hoàn hảo, thị trường cạnh tranh hoàn toàn, thị trường hoàn hảo, perfect competition, người chấp nhận giá, hàng hóa đồng nhất, gia nhập và rút lui, rào cản gia nhập, doanh thu cận biên, chi phí cận biên, lợi nhuận kinh tế, điểm đóng cửa, hiệu quả phân bổ, độc quyền, cạnh tranh độc quyền, độc quyền nhóm, kinh tế vi mô]
Entities_Skipped: []   # "nội dung", "tiêu chuẩn" (Topic Coverage "nên có") bỏ: từ chung, không phải thuật ngữ miền
Information_Gain:
  - claim: "Ví dụ số 3 bước (giá, chi phí cận biên, chi phí trung bình) cho thấy doanh nghiệp chọn sản lượng tại P = MC, lãi kinh tế ở ngắn hạn và về 0 ở dài hạn; top 5 chỉ nêu lý thuyết, không có phép tính"
    h2: "Sự vận động của thị trường cạnh tranh hoàn hảo trong ngắn và dài hạn"
    type: calc
    proof: "P = MC"
  - claim: "Bảng đối chiếu 5 điều kiện cạnh tranh hoàn hảo với thị trường cổ phiếu niêm yết trên HOSE (số người mua bán, hàng hóa đồng nhất, thông tin công khai, rào cản, biên độ giá ±7%): thị trường này gần mô hình ở đâu và lệch ở đâu; không đối thủ nào nối khái niệm với đầu tư chứng khoán"
    h2: "Thị trường cổ phiếu có phải là cạnh tranh hoàn hảo không?"
    type: comparison
    proof: "biên độ ±7%"
  - claim: "Tiêu chí pháp lý thị phần từ 30% trở lên là dấu hiệu doanh nghiệp có vị thế thống lĩnh theo Luật Cạnh tranh 2018 (Luật số 23/2018/QH14), làm thước đo mức lệch của Việt Nam khỏi cạnh tranh hoàn hảo [CẦN XÁC NHẬN điều khoản và mức % tại văn bản gốc trước khi viết]"
    h2: "Thực trạng thị trường cạnh tranh hoàn hảo tại Việt Nam"
    type: regulation
    proof: "Luật Cạnh tranh 2018"
Featured_Snippet: Paragraph
PAA_Questions:   # SERP không có khối PAA; lấy từ Related Searches + query GSC
  - q: "Thị trường hoàn hảo là gì?"
    placement: faq
  - q: "Cạnh tranh hoàn hảo có tồn tại trong thực tế không?"
    placement: faq
  - q: "Cạnh tranh hoàn hảo khác cạnh tranh không hoàn hảo như thế nào?"
    placement: faq
  - q: "Đặc điểm của doanh nghiệp cạnh tranh hoàn hảo"
    placement: body
---

# BÁO CÁO TỐI ƯU SEO — canh-tranh-hoan-hao-la-gi

Nguồn bản gốc: live `https://www.dsc.com.vn/kien-thuc/canh-tranh-hoan-hao-la-gi` (độ giống Final 99%, 0 link chỉ có trên live). Baseline: slop 70/100 FAIL (`SLOP-evidence` 0,1/100 từ, `SLOP-anchor` 82%, `SLOP-vague` 1,9/1000 từ); qa_lint 78/100 (3 CRITICAL: thiếu Meta, Title 66 ký tự, thiếu link mở tài khoản; MAJOR: thiếu link pillar, dòng "Xem thêm", GEO-h2-answer 3/5). `market_facts --verify`: sạch, không có số liệu thị trường. `news_feed`: không có tin. Bài không có FAQ, không nguồn, không số.

## 0. Content Strategy Header

| Thông số | Giá trị |
| :--- | :--- |
| **Target Keyword** | `cạnh tranh hoàn hảo là gì` (registry ghi `canh tranh hoan hao là gì`, thiếu dấu; đề xuất sửa `key_chinh` sau khi duyệt, không đụng pages.csv ở bước này) |
| **Secondary Keywords** | `thị trường cạnh tranh hoàn hảo`, `thị trường cạnh tranh hoàn hảo là gì`, `thị trường cạnh tranh hoàn toàn`, `thị trường hoàn hảo là gì`, `ví dụ thị trường cạnh tranh hoàn hảo` |
| **LSI / Entities** | người chấp nhận giá, hàng hóa đồng nhất, rào cản gia nhập, doanh thu cận biên, chi phí cận biên, lợi nhuận kinh tế, điểm đóng cửa, độc quyền, kinh tế vi mô |
| **Search Intent** | Informational — định nghĩa + đặc điểm + ví dụ cho sinh viên kinh tế và người mới học kinh tế vi mô, giai đoạn tìm hiểu khái niệm |
| **Persona** | P2 — F0 — người mới, cần giải thích thuật ngữ kỹ, tone thân thiện; bài thuộc cụm vĩ mô (hub `kinh-te-hoc-vi-mo-la-gi-y-nghia-trong-dau-tu-chung-khoan`), cầu nối sang đầu tư chứng khoán |
| **Tone** | Chuyên gia đồng hành, giải thích từng thuật ngữ, câu ngắn, có phép tính |
| **DSC Product Bridge** | eKYC mở tài khoản 3 phút + Môi giới 1:1. Góc dẫn: nhà đầu tư cá nhân trên thị trường cổ phiếu là người chấp nhận giá, nên cần thông tin và người đồng hành (I111, I112; không nhắc phái sinh/quỹ mở) |
| **Featured Snippet** | Paragraph — câu định nghĩa đầu H2 "Cạnh tranh hoàn hảo là gì?" (hiện 51 từ, rút còn ≤ 40 từ); List phụ cho 5 đặc điểm |
| **Word Count hiện tại** | ~1.570 từ (live crawl ~1.780 gồm bảng) |
| **Word Count mục tiêu** | ~1.700–1.850 từ. Đối thủ: stockmap 963, wikipedia 986, andrews 1.207, luatminhkhue 2.197 (nhiều trắc nghiệm), lavn 2.004 (bài cạnh tranh không hoàn hảo). Median top 5 chỉ 750 nhưng bài hiện tại đã dài hơn và đang top 1–2, nên chỉ thêm ~200 từ dữ kiện và cắt câu thừa |

**Bài gốc đang phục vụ đúng intent/persona không?**
- [x] Đúng intent (định nghĩa + ví dụ khớp 8/8 kết quả SERP dạng definition). Lệch nhẹ về persona/độ chặt: bài không nối với đầu tư, không có CTA, không số, giọng sách giáo khoa dài; sửa bằng nội dung, không đổi khung.

**Giới hạn thứ hạng (SKILL Bước 3):** GSC 90 ngày cho `cạnh tranh hoàn hảo là gì` vị trí 1,3, bài vị trí trung bình 2,15 (≤ 5) → chỉ `[GIỮ NGUYÊN]` / `[CẬP NHẬT]` / `[THÊM MỚI]`; không đổi H1, không đổi thứ tự, không gộp/xoá H2 hiện có. Hai H2 `[THÊM MỚI]` ở dưới chèn giữa các H2 sẵn có (không xê dịch H2 cũ). Rủi ro: thêm H2 vào bài top 1 có thể làm lệch khung; giảm thiểu bằng chỉ thêm 2 H2 ngắn (~120–150 từ) và giữ nguyên toàn bộ H2/H3 cũ. Cần user đồng ý (xem mục 8).

---

## 1. Đánh giá Tổng quan

📊 GSC Performance Context (2026-08-19 → 2026-11-16, nguồn: SEO Dashboard MCP, cache `knowledge/raw/gsc/dashboard/page-queries-canh-tranh-hoan-hao-la-gi.json`):
- Clicks 140, impressions 4.096, CTR 3,42%, position 2,1 (kỳ trước: 88 clicks, CTR 3,84%, pos 3,6; clicks +59,1%). Lưu ý: số này khác con số 341 clicks / 14.748 impressions / pos 3,7 coordinator đưa; MCP 90 ngày mới nhất trả số trên (có thể bên kia dùng cửa sổ dài hơn).
- Flag rewrite Title theo CTR: KHÔNG (CTR ≥ 3%). Nhưng CTR `thị trường cạnh tranh hoàn hảo` chỉ 3,26% ở vị trí 1,7 và `thị trường hoàn hảo là gì` 1,34% ở vị trí 2,2 (224 impressions) — AI Overview trích DSC, có thể nuốt click.
- Query mang click: `cạnh tranh hoàn hảo là gì` 43 clicks (pos 1,3, CTR 7,78%) · `thị trường cạnh tranh hoàn hảo` 38 (1,7; 1.164 impr) · `thị trường cạnh tranh hoàn hảo là gì` 17 (1,5) · `cạnh tranh hoàn hảo` 11 (1,5) · `thị trường cạnh tranh hoàn toàn` 8 (pos 3,5 — tụt từ 2,9; bài chưa dùng cụm "cạnh tranh hoàn toàn" ngoài một lần) · `thị trường hoàn hảo` 5 · `ví dụ về thị trường cạnh tranh hoàn hảo` 5 (CTR 7,25%).
- Việc rút ra: đưa các biến thể "thị trường cạnh tranh hoàn toàn", "thị trường hoàn hảo" vào câu định nghĩa và FAQ; giữ "ví dụ".
- Cannibalization (MCP, query chứa `cạnh tranh hoàn hảo`, 90 ngày): bài này 123 clicks / 2.888 impr / pos 1,63; `canh-tranh-doc-quyen-la-gi` 0 clicks / 48 impr / pos 7,3; `canh-tranh-khong-hoan-hao-phan-tich-chi-tiet-cac-mo-hinh` 0 clicks / 67 impr / pos 6,3. Không đáng kể, intent khác (độc quyền, không hoàn hảo) → chỉ link qua lại (I118), không dựng H2 riêng cho chủ đề đó.
- SERP sanity check: SERP mới fetch (`--force`, keyword có dấu, $0,002) đặt DSC #1, khớp GSC pos 1,3; related searches đúng chủ đề; AI Overview trích dsc.com.vn. Không có dấu hiệu SERP sai. Cache còn thiếu `PAA`, DataForSEO không trả khối này.
- **Word Count Gap:** 1.570 từ so median 750 (top 5 hợp lệ) → dài hơn; không cần thêm độ dài, cần thêm dữ kiện.
- **On-page:** Title 66 ký tự (> 59), chưa có Meta; keyword có ở sapo đoạn 2 nhưng đoạn 1 không trả lời thẳng; 2/5 H2 trả lời ngay câu đầu; không có FAQ, 0 data point, 0 nguồn, 0 mốc thời gian.
- **Vi phạm Anti-AI:** Có. `SLOP-vague` ×3 ("rất nhiều người mua và người bán" ở dòng 20, 52, 72); sapo mở bằng câu chung ("Cạnh tranh hoàn hảo là một khái niệm quan trọng…"), "chúng tôi sẽ cung cấp cho bạn một số thông tin"; kết luận mở bằng "Tóm lại"; 26 câu > 30 từ (dài nhất 98 từ ở Kết luận, 76 từ ở đặc điểm thứ tư); 3 đoạn dài; câu hỏi tu từ liệt kê ở sapo đoạn 2.

### Đề xuất cập nhật SEO Elements
- **Title hiện tại:** Cạnh tranh hoàn hảo là gì? Ví dụ về thị trường cạnh tranh hoàn hảo — 66 ký tự (vượt giới hạn 59).
- **Title đề xuất:** Cạnh tranh hoàn hảo là gì? Đặc điểm, điều kiện và ví dụ — 55 ký tự, giữ nguyên cụm đầu đang rank 1,3 và "ví dụ". **H1 trong bài giữ nguyên** (không đổi H1); chỉ đổi front matter Title / thẻ title. Nếu user muốn zero rủi ro cho bài đang top 1: chọn "Giữ nguyên" và chấp nhận `CL1-title` còn ở lint.
- **Meta Description hiện tại:** không có trong snapshot live (chỉ lấy phần thân bài); coi như chưa xác nhận → cần user kiểm tra trên CMS.
- **Meta Description đề xuất (155 ký tự):** Cạnh tranh hoàn hảo là thị trường nhiều người mua bán, hàng hóa đồng nhất, giá do cung cầu quyết định. Xem 5 đặc điểm, ví dụ và bảng so sánh với độc quyền.

---

## 2. Phân tích Đối thủ SERP

SERP "cạnh tranh hoàn hảo là gì" (Google VN, 8 organic hợp lệ). Khung thống trị: Định nghĩa (X là gì) 45%. DSC là #1. Crawl hợp lệ: stockmap, luatminhkhue, andrews, lavn (studocu bị chặn Cloudflare; scribd là trang tải tài liệu; wikipedia chỉ 1 H2). JSON: `scratch/competitors-canh-tranh-hoan-hao-la-gi.json`.

### 2.1 Bảng so sánh

| # | URL | Intent | Từ | Điểm nổi bật |
| :--- | :--- | :--- | :--- | :--- |
| 1 | stockmap.vn/blog/thi-truong-canh-tranh-hoan-hao-khai-niem-… | Informational | ~963 | Nối với nhà đầu tư; "5 đặc điểm nhận diện", bảng "so sánh nhanh 4 cấu trúc thị trường", H3 khả năng hiện thực hóa tại VN |
| 2 | luatminhkhue.vn/thi-truong-canh-tranh-hoan-hao-la-gi.aspx | Informational | ~2.197 | Đặc điểm doanh nghiệp (người chấp nhận giá) + bài tập trắc nghiệm/tự luận |
| 3 | andrews.edu.vn/su-khac-biet-giua-canh-tranh-hoan-hao-va-canh-tranh-doc-quyen/ | Informational | ~1.207 | Bảng so sánh với độc quyền, "công ty là người chấp nhận giá" |
| 4 | lavn.com.vn/thi-truong-canh-tranh-khong-hoan-hao-la-gi-… | Informational (cạnh tranh không hoàn hảo) | ~2.004 | Phân loại 3 dạng thị trường không hoàn hảo, ví dụ thực tế |
| 5 | vi.wikipedia.org/wiki/Cạnh_tranh_hoàn_hảo | Informational | ~986 | Danh sách giả thiết chuẩn |

### 2.2 Từng đối thủ

**Stockmap — stockmap.vn**
- **Intent chính:** hiểu mô hình để áp vào đầu tư.
- **Mục họ có mà bài mình chưa có:** H3 "Khả năng hiện thực hóa tại Việt Nam" (nhưng ngắn ~71 từ), H3 "So sánh nhanh 4 cấu trúc thị trường".
- **Yếu tố đặc biệt:** sapo nhắc "tiêu chuẩn vàng" so sánh cấu trúc thị trường.
- **Content Gap:** họ không có phép tính, không bảng đối chiếu với thị trường cổ phiếu, không nguồn. Bài DSC có thể vượt ở dữ kiện.

**Luật Minh Khuê — luatminhkhue.vn**
- **Intent chính:** học bài (trắc nghiệm).
- **Mục họ có:** "Đặc điểm của doanh nghiệp khi tham gia thị trường cạnh tranh hoàn toàn" (233+186 từ) — người chấp nhận giá, đường cầu nằm ngang, đóng cửa khi lỗ.
- **Yếu tố đặc biệt:** câu hỏi trắc nghiệm + tự luận (~1.070 từ).
- **Content Gap:** bài DSC thiếu góc "doanh nghiệp quyết định gì" (P = MC, đóng cửa); không cần làm trắc nghiệm (lệch intent chính, kéo dài bài).

**Andrews — andrews.edu.vn**
- **Intent chính:** phân biệt cạnh tranh hoàn hảo và độc quyền.
- **Mục họ có:** bảng so sánh 2 loại, danh sách khác biệt chính.
- **Yếu tố đặc biệt:** bảng so sánh.
- **Content Gap:** DSC đã có bảng 5 loại thị trường (rộng hơn) → giữ.

**LAVN — lavn.com.vn**
- **Intent chính:** cạnh tranh không hoàn hảo (spin-off intent, khác).
- **Mục họ có:** 3 dạng không hoàn hảo, ảnh hưởng đến nền kinh tế.
- **Content Gap:** thuộc bài `canh-tranh-khong-hoan-hao-…` của DSC — chỉ link, không nhân bản (I118).

**Wikipedia — vi.wikipedia.org**
- **Intent chính:** định nghĩa chuẩn.
- **Mục họ có:** các giả thiết (999 từ, ít heading).
- **Content Gap:** thêm thuật ngữ "người chấp nhận giá", "hiệu quả phân bổ".

### 2.3 Intent Gap
- **Intent SERP:** định nghĩa + đặc điểm + ví dụ + phân biệt với loại thị trường khác.
- **Intent bài hiện tại:** khớp; thiếu (a) định nghĩa ngắn trích được ở đầu, (b) góc doanh nghiệp quyết định thế nào, (c) mối nối với thị trường đầu tư, (d) nguồn và số.
- **Gap cần xử lý:** thêm phép tính P = MC, bảng đối chiếu thị trường cổ phiếu, mốc pháp lý Việt Nam, FAQ 3 câu.

---

## 3. Kết quả Sweeps Audit

| Bước Quét | Điểm | Vấn đề chính | Ghi chú cải thiện |
| :--- | :--- | :--- | :--- |
| **Clarity** | 4/10 | 26 câu > 30 từ; đặc điểm 2, 4, 5 và Kết luận mỗi cái 1 khối dài | Tách thành list đánh số, mỗi ý ≤ 25 từ |
| **Voice** | 4/10 | "chúng tôi sẽ cung cấp cho bạn một số thông tin"; văn sách giáo khoa; không có giọng DSC | Sapo đoạn 2 theo I105; "Trong bài viết này, Chứng khoán DSC…" |
| **So What** | 3/10 | Không nối với người đọc/đầu tư | Bảng thị trường cổ phiếu; Kết luận có checklist hành động |
| **Prove It** | 2/10 | 0 số, 0 nguồn, 0 mốc | Ví dụ tính toán; nguồn Luật Cạnh tranh 2018; biên độ HOSE 7% |
| **Specificity** | 3/10 | "rất nhiều", "một số", ví dụ chợ không số | Thay bằng số giả định ghi rõ (10.000 đồng/kg...) |
| **Emotion** | 3/10 | Lý thuyết suông | Hỏi đáp thực tế: "thị trường có tồn tại không?" |
| **Zero Risk** | 4/10 | Không nêu giới hạn mô hình rõ | FAQ "tồn tại trong thực tế không?"; ghi rõ ví dụ số là giả định |
| **GEO/AEO** | 4/10 | 3/5 H2 không trả lời ở câu đầu; 0 FAQ; 0 temporal marker (chỉ cần với số biến động) | Câu đầu mỗi H2 ≤ 40 từ trả lời thẳng; thêm FAQ |

---

## 4. Phân tích Chi tiết (nhãn từng heading)

### GIỮ NGUYÊN

| Heading | Lý do giữ |
| :--- | :--- |
| H1: Cạnh tranh hoàn hảo là gì? Ví dụ về thị trường cạnh tranh hoàn hảo | Vị trí top 1–2; không đổi H1. |
| H2: So sánh các thị trường cạnh tranh | Bảng 5 loại thị trường đầy đủ, rộng hơn Andrews/Stockmap. Chỉ thêm 1 câu dẫn có link `canh-tranh-khong-hoan-hao-…` phía trên bảng (không sửa bảng) |
| H2: Tác động của cạnh tranh hoàn hảo đến thị trường | Heading cha; nội dung nằm ở H3 |

### XÓA BỎ
Không có (giới hạn thứ hạng). Đề xuất duy nhất ngoài heading: dòng `>> Xem thêm: Chỉ số PCE là gì?` (lạc đề với cạnh tranh hoàn hảo, bị `LINK-xemthem` bắt). Xin ý kiến user: (a) bỏ dòng và mất 1 inlink tới bài PCE, hoặc (b) giữ, viết thành câu có ngữ cảnh. Mặc định: bỏ (a) vì PCE là chỉ số lạm phát, không liên quan intent.

### CẬP NHẬT

🔄 **Sapo (2 đoạn dưới H1)**
- **Vấn đề:** đoạn 1 mở bằng câu chung, không trả lời thẳng, không dùng biến thể GSC; đoạn 2 liệt kê câu hỏi, "chúng tôi sẽ cung cấp".
- **Hướng xử lý:** (I105) Đoạn 1: "Cạnh tranh hoàn hảo là gì? Đó là thị trường có rất nhiều người mua và người bán, hàng hóa giống hệt nhau, nên không ai tự quyết định được giá" — thay "rất nhiều" bằng tiêu chí có số (5 điều kiện, mô hình do Cournot/Marshall... [chỉ nêu nếu xác minh]). Gọi tên biến thể: "thị trường cạnh tranh hoàn toàn", "thị trường hoàn hảo". Đoạn 2: "Trong bài viết này, Chứng khoán DSC giải thích 5 đặc điểm, điều kiện, ví dụ số, bảng so sánh với độc quyền kèm đối chiếu với thị trường cổ phiếu HOSE." Giữ link `kinh tế học vi mô` ở đoạn 1.
- **Entities cần có:** `thị trường cạnh tranh hoàn toàn`, `thị trường hoàn hảo`, `hàng hóa đồng nhất`, `người chấp nhận giá`
- **Word count target:** ~90 từ (hiện ~95)

🔄 **H2: Cạnh tranh hoàn hảo là gì?**
- **Vấn đề:** câu đầu 51 từ, đoạn 2 viết dài, thiếu thuật ngữ "người chấp nhận giá", "thị trường cạnh tranh hoàn toàn"; dòng PCE.
- **Hướng xử lý:** câu đầu ≤ 40 từ, định nghĩa trọn ý (đoạn Paragraph snippet, kèm "còn gọi là thị trường cạnh tranh hoàn toàn / perfect competition"). Giải thích "người chấp nhận giá (price taker)" 1 câu. Giữ link `cạnh tranh độc quyền`. Xử lý dòng PCE theo mục XÓA BỎ.
- **Entities:** `perfect competition`, `người chấp nhận giá`, `cung - cầu`
- **Word count target:** ~120 từ

🔄 **H2: Đặc điểm cơ bản của cạnh tranh hoàn hảo**
- **Vấn đề:** 5 đoạn "Thứ nhất…Thứ năm" dài (câu 41–76 từ), 3 đoạn liên tiếp không có visual, câu đầu 41 từ.
- **Hướng xử lý:** câu đầu "Thị trường cạnh tranh hoàn hảo có 5 đặc điểm: …" (≤ 40 từ, kể tên 5). Chuyển 5 đoạn thành list đánh số, mỗi mục nhãn đậm + 1–2 câu ≤ 25 từ; giữ nguyên toàn bộ ý và định nghĩa trong ngoặc (doanh thu cận biên, chi phí cận biên). Đặc điểm 4 tách rõ: lợi nhuận kinh tế bằng 0 tại cân bằng dài hạn (không đổi nghĩa). Đặc điểm 5: tách phần "rút lui" và "gia nhập" thành 2 gạch đầu dòng.
- **Entities:** `hàng hóa đồng nhất`, `doanh thu cận biên`, `chi phí cận biên`, `lợi nhuận kinh tế`, `rào cản gia nhập`, `gia nhập và rút lui`
- **Word count target:** ~330 từ (hiện 356, bớt lặp)

🔄 **H2: Sự vận động của thị trường cạnh tranh hoàn hảo trong ngắn và dài hạn**
- **Vấn đề:** đoạn 1 khối 81 từ, không số; câu đầu 48 từ.
- **Hướng xử lý:** câu đầu ≤ 40 từ tóm tắt: ngắn hạn có thể lãi kinh tế, dài hạn lãi về 0. Thêm **ví dụ số giả định** (xem [IG1]): doanh nghiệp rau sạch, giá thị trường 20.000 đồng/kg; chi phí cận biên 12.000 → 20.000 → 28.000 đồng/kg ở các mức sản lượng; doanh nghiệp tăng sản lượng đến khi `P = MC` (20.000 đồng); chi phí trung bình 16.000 đồng → lãi kinh tế 4.000 đồng/kg ở ngắn hạn; doanh nghiệp mới gia nhập đẩy giá về 16.000 → lãi kinh tế = 0. Thêm quy tắc đóng cửa 1 câu (giá thấp hơn chi phí biến đổi trung bình thì dừng sản xuất). Bảng 3 dòng: Ngắn hạn / Dài hạn / Điểm đóng cửa. Ghi rõ "số giả định, minh họa". Số lấy phép tính nội bộ, không phải thống kê thị trường.
- **Entities:** `chi phí cận biên`, `doanh thu cận biên`, `lợi nhuận kinh tế`, `điểm đóng cửa`, `gia nhập và rút lui`
- **Word count target:** ~190 từ (hiện 81; +110)

🔄 **H3: Ưu điểm** (dưới "Tác động…")
- **Vấn đề:** 4 đoạn không mở đầu bằng nhãn, câu 69 từ, không đề cập hiệu quả phân bổ.
- **Hướng xử lý:** chuyển 4 đoạn thành list nhãn đậm ("Giá minh bạch", "Chất lượng đồng đều", "Chi phí marketing thấp", "Dễ đổi nhà cung cấp"), thêm 1 ý hiệu quả phân bổ (giá bằng chi phí cận biên: P = MC nghĩa là tài nguyên được dùng vào hàng người mua đánh giá cao hơn chi phí tạo ra). Giữ nguyên ý cũ.
- **Entities:** `hiệu quả phân bổ`, `chi phí cận biên`
- **Word count target:** ~170

🔄 **H3: Nhược điểm**
- **Vấn đề:** 2 đoạn dài, ý lặp; không nêu nhược điểm về đổi mới (R&D) rõ.
- **Hướng xử lý:** list 2–3 ý ngắn: không có động lực đổi mới/đầu tư sản phẩm; doanh nghiệp không có chiến lược giá. Giữ link `lý thuyết trò chơi` (đặt trong câu về độc quyền nhóm, như hiện tại).
- **Word count target:** ~100

🔄 **H2: Ví dụ về thị trường cạnh tranh hoàn hảo**
- **Vấn đề:** đoạn 6 câu (câu 33, 43 từ) kể chuyện chợ rau, không đối chiếu với 5 đặc điểm.
- **Hướng xử lý:** giữ ví dụ chợ rau; chuyển thành 5 gạch đầu dòng đối chiếu từng đặc điểm với chợ rau (nhiều người bán, rau cải cùng loại, giá niêm yết ở các sạp, tự do mở sạp/nghỉ, người mua đổi sạp). Thêm 1 câu giới hạn thực tế: chợ truyền thống chỉ gần đúng (khác nhau độ tươi, vị trí). Không số thống kê.
- **Entities:** `hàng hóa đồng nhất`, `người chấp nhận giá`
- **Word count target:** ~170

🔄 **H2: Thực trạng thị trường cạnh tranh hoàn hảo tại Việt Nam**
- **Vấn đề:** 2 đoạn 278 từ, câu 40–55 từ, không có số, không có nguồn, "xu hướng tất yếu" mơ hồ.
- **Hướng xử lý:** câu đầu ≤ 40 từ: Việt Nam chưa có thị trường nào đạt đủ 5 điều kiện, ngành gần nhất là nông sản tươi bán lẻ [không số]. Thêm mốc pháp lý (IG3): Luật Cạnh tranh 2018 (Luật số 23/2018/QH14) coi doanh nghiệp có thị phần từ 30% trở lên là có dấu hiệu vị thế thống lĩnh, có link nguồn trong whitelist nếu có (kiểm `knowledge/1-brand/source-whitelist.md`; không có thì ghi tên văn bản, không link ngoài). **Bắt buộc tra văn bản gốc (Điều 24) trước khi viết; chưa xác nhận thì bỏ mức %, chỉ nêu tên luật.** Giữ link `cạnh tranh` (canh-tranh-la-gi). Cắt đoạn khởi nghiệp lan man còn 2 câu. Thêm link pillar `phân tích vĩ mô trong đầu tư chứng khoán` (qa_lint `LINK-pillar`).
- **Entities:** `Luật Cạnh tranh 2018`, `vị thế thống lĩnh thị trường`, `thị phần`
- **Word count target:** ~200 (hiện 278; cắt khoảng 80, thêm mốc luật)

🔄 **H2: Kết luận**
- **Vấn đề:** mở bằng "Tóm lại", câu 98 từ, không CTA, không bước tiếp theo (I113).
- **Hướng xử lý:** 1 nhận định ≤ 30 từ + checklist 3 mục hành động (nhận diện 5 điều kiện khi gặp thị trường mới; so sánh giá với chi phí; kiểm tra thông tin trước khi mua/bán cổ phiếu) + CTA link `https://www.dsc.com.vn/mo-tai-khoan` theo P2: "Mở tài khoản — 3 phút" (eKYC 3 phút, I111). Không dùng "Tóm lại". Không hứa lợi nhuận.
- **Word count target:** ~110 (hiện 160)

---

## 5. Đề xuất Thêm mới (Content Gaps)

✨ **[THÊM MỚI] H2: Thị trường cổ phiếu có phải là cạnh tranh hoàn hảo không?**
- **Học từ đối thủ:** Competitor 1 — stockmap.vn (có H3 nối với đầu tư nhưng chỉ lý thuyết, 71 từ) và Competitor 2 — luatminhkhue.vn (khía cạnh người chấp nhận giá). Bảng đối chiếu là phần DSC tự thêm.
- **Vị trí chèn:** ngay dưới H2 "Ví dụ về thị trường cạnh tranh hoàn hảo", trên H2 "Thực trạng…".
- **Nội dung chính:** câu đầu trả lời thẳng (≤ 40 từ): gần đúng ở 3/5 điều kiện, lệch ở thông tin và rào cản. Bảng 5 dòng đối chiếu 5 điều kiện với cổ phiếu niêm yết HOSE: (1) số người mua bán — hàng triệu tài khoản [CẦN XÁC NHẬN số tài khoản nếu dùng, nguồn VSDC/SSC, ghi tháng; nếu không có thì viết "rất đông" không số]; (2) hàng hóa đồng nhất — cổ phiếu cùng mã giống hệt nhau; (3) thông tin — giá công khai tức thời nhưng thông tin nội bộ không công bằng; (4) rào cản — mở tài khoản eKYC 3 phút, nhưng biên độ giá ±7% mỗi phiên (HOSE) và lô giao dịch 100 cổ phiếu, T+2 hạn chế; (5) người chấp nhận giá — nhà đầu tư cá nhân khớp lệnh theo giá thị trường. Dùng fact cấu trúc không hết hạn (biên độ HOSE 7% / HNX 10% / UPCoM 15%, lô 100, T+2 — anti-ai-rules §8.7e); tra `market_facts.py` trước khi viết, nếu exit 3 chỉ dùng fact cấu trúc.
- **Product Bridge:** 1–2 câu cuối: nhà đầu tư cá nhân là người chấp nhận giá nên khác biệt nằm ở thông tin và người đồng hành, nhắc Môi giới 1:1 + mở tài khoản eKYC 3 phút; banner CTA giữa bài đặt dưới H2 này (đoạn dẫn ≥ 10 từ phía trên; P2 cho phép banner).
- **Entities:** `người chấp nhận giá`, `hàng hóa đồng nhất`, `rào cản gia nhập`, `biên độ giá`, `HOSE`
- **Bằng chứng / Số liệu cần có:** biên độ ±7% HOSE, lô 100 cổ phiếu, T+2 (fact cấu trúc); số tài khoản [CẦN XÁC NHẬN, tùy chọn].
- **Định dạng:** câu trả lời đầu + bảng so sánh 5 dòng + 1–2 câu bridge
- **Word count ước tính:** ~170 từ (kể cả bảng)
- **Lưu ý:** không đề cập phái sinh/quỹ mở (I111); không tự ra khuyến nghị đầu tư.

✨ **[THÊM MỚI] H2: Câu hỏi thường gặp về cạnh tranh hoàn hảo**
- **Học từ đối thủ:** Related Searches Google + query GSC (không có PAA trong SERP); chưa đối thủ nào có FAQ.
- **Vị trí chèn:** ngay trên H2 "Kết luận" (Kết luận vẫn là H2 cuối, I113).
- **Nội dung chính:** 3 câu hỏi dạng PAA, câu đầu mỗi đáp ≤ 60 từ, có số/mốc khi có: (1) "Thị trường hoàn hảo là gì?" — đồng nghĩa cạnh tranh hoàn hảo, 5 điều kiện (GSC 224 impr, CTR 1,34%); (2) "Cạnh tranh hoàn hảo có tồn tại trong thực tế không?" — chỉ gần đúng, ví dụ chợ rau và cổ phiếu niêm yết; (3) "Cạnh tranh hoàn hảo khác cạnh tranh không hoàn hảo như thế nào?" — 1–2 câu + link `canh-tranh-khong-hoan-hao-phan-tich-chi-tiet-cac-mo-hinh`.
- **Entities:** `cạnh tranh không hoàn hảo`, `thị trường hoàn hảo`, `perfect competition`
- **Bằng chứng / Số liệu cần có:** số điều kiện (5), tham chiếu bảng so sánh có sẵn.
- **Định dạng:** H3 là câu hỏi + đoạn trả lời (không JSON-LD, I-memory: CMS không hỗ trợ)
- **Word count ước tính:** ~170 từ

**Mục đã loại:** bài tập trắc nghiệm (Luật Minh Khuê) — lệch intent, kéo dài bài; "Cạnh tranh độc quyền / không hoàn hảo" — đã có bài riêng, chỉ link (I118).

---

## 6. Chiến lược Internal Links
Link hiện có giữ nguyên (5): kinh tế học vi mô (hub) · cạnh tranh độc quyền · lý thuyết trò chơi · cạnh tranh (canh-tranh-la-gi) · chỉ số PCE (xem mục XÓA BỎ).

| Anchor đề xuất | Bài đích (slug) | Vị trí chèn |
| :--- | :--- | :--- |
| phân tích vĩ mô trong đầu tư chứng khoán | phan-tich-vi-mo-trong-dau-tu-chung-khoan-la-gi | H2: Thực trạng… (pillar, qa_lint `LINK-pillar`) |
| cạnh tranh không hoàn hảo | canh-tranh-khong-hoan-hao-phan-tich-chi-tiet-cac-mo-hinh | Câu dẫn trên bảng "So sánh các thị trường cạnh tranh" + FAQ câu 3 |
| mở tài khoản chứng khoán | mo-tai-khoan (https://www.dsc.com.vn/mo-tai-khoan) | H2 Kết luận (CTA) + banner dưới H2 thị trường cổ phiếu |

### 📎 Backfill Link Suggestions (cho bài khác, thực thi trên CMS sau, không thuộc phạm vi bài này)
| Bài nguồn | Đoạn | Anchor | Clicks |
| :--- | :--- | :--- | ---: |
| npv-va-irr-la-gi | IRR là gì? — hiện link qua dòng "Xem thêm" | chuyển vào câu | 139 |
| canh-tranh-khong-hoan-hao-phan-tich-chi-tiet-cac-mo-hinh | Cạnh tranh không hoàn hảo là gì? — đoạn nói điều kiện không đáp ứng | "điều kiện của cạnh tranh hoàn hảo" | 19 |
| ly-thuyet-tro-choi-ung-dung-… | Các thành phần cốt lõi — hiện link qua "Xem thêm" | chuyển vào câu | 6 |

---

## 7. Chiến lược Hình ảnh

### 7.1 Ảnh GỐC cần bảo toàn
| Cú pháp Markdown ảnh gốc | Vị trí hiện tại | Hướng xử lý |
| :--- | :--- | :--- |
| `![canh-tranh-hoan-hao.png](https://extgw.dsc.com.vn/eback/uploads/canh_tranh_hoan_hao_eec0fb77df.png)` | Dưới sapo, trên H2 "Cạnh tranh hoàn hảo là gì?" | Giữ URL và vị trí 100%; chỉ đổi alt thành `Thị trường cạnh tranh hoàn hảo: nhiều người mua, người bán và hàng hóa đồng nhất` |

### 7.2 Ảnh mới (tối đa 2)
| Vị trí đề xuất | Concept | Alt chứa keyword |
| :--- | :--- | :--- |
| Dưới H2 "Sự vận động… ngắn và dài hạn" | Đồ thị đường cầu nằm ngang P = MR với đường MC và ATC, điểm P = MC (vẽ bằng `dsc_design.py`, 800×500, số khớp ví dụ 20.000/16.000 đồng/kg, không đỏ, không chữ thừa) | `Đồ thị cạnh tranh hoàn hảo: giá bằng chi phí cận biên tại điểm cân bằng` |
| (tùy chọn) Dưới H2 thị trường cổ phiếu | Infographic 5 điều kiện: gần đúng / lệch | `Cạnh tranh hoàn hảo và thị trường cổ phiếu: 5 điều kiện đối chiếu` |

---

## 8. Cần user quyết trước khi sang Bước 4
1. Đồng ý thêm 2 H2 `[THÊM MỚI]` vào bài đang top 1–2 (rủi ro nhỏ, không đổi H2 cũ)?
2. Title: đổi sang bản 55 ký tự (giữ H1) hay giữ nguyên 66 ký tự?
3. Dòng "Xem thêm: Chỉ số PCE" — bỏ hay chuyển thành câu?
4. Meta hiện tại: cần user dán từ CMS.
5. Mức % thị phần 30% của Luật Cạnh tranh 2018 và số tài khoản (nếu dùng): chưa xác nhận; Bước 4 sẽ tra hoặc bỏ số.
6. Registry `key_chinh`/`anchor` đang thiếu dấu ("canh tranh hoan hao là gì"): đề xuất sửa thành `cạnh tranh hoàn hảo là gì` — `serp_research.py` từ chối keyword có dấu ("không có trong registry"), buộc phải `--force`; cần coordinator sửa pages.csv.
