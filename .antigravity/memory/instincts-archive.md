# Instincts Archive — nguồn của mọi rule viết bài

> **KHÔNG đọc cả file khi viết bài** (~110 KB). Agent viết bài đọc `instincts.md` (sinh tự động, ~8 KB) + đúng 1 file `instincts-by-scope/<topic>.md`.
> Cần xem 1 rule / lịch sử: `python scripts/optimize_instincts.py --show <ID|tag|slug>` — chỉ in block khớp.
> - `--show I105` → 1 rule · `--show sapo` → rule theo tag · `--show <slug>` → ghi chú ARTICLE của bài đó (dùng trước /optimize).
> Sửa rule: `/learn` (cổng nhận rule trong `.antigravity/skills/content-feedback-loop/SKILL.md`) → `python scripts/optimize_instincts.py --check`.

**Trạng thái:** `ACTIVE` = đang áp dụng (chỉ mục *Rule chuẩn*) · `DEPRECATED` = đã gộp, xem `Thay bởi` · `ARTICLE` = ghi chú riêng 1 bài, không load khi viết bài mới.
**Mỗi (Tag, Phạm vi) chỉ 1 rule ACTIVE.** Phản hồi mới cùng chủ đề → sửa rule đó tại chỗ (giữ ID, cập nhật `Cập nhật:`), không thêm rule mới.

## Format

```
### [Tên ngắn — 1 chủ đề]
- **ID:** I1xx
- **Trạng thái:** ACTIVE
- **Tag:** sapo
- **Nguồn:** slug | gộp từ I0xx, …
- **Phản hồi từ User:** "quote gốc"
- **Phạm vi:** Global | Chỉ topic: X
- **Checklist:** qa_lint:CL1-sapo, outline_lint:…   (nếu có)
- **Máy kiểm:** full | partial
- **Cập nhật:** YYYY-MM-DD
- **Bản năng:** tối đa 3 ý, ≤ 450 ký tự, viết thành hành động
```

---

## Rule chuẩn (ACTIVE)

### Sapo: keyword + trả lời thẳng, đoạn 2 có DSC và câu dẫn vào bài
- **ID:** I105
- **Trạng thái:** ACTIVE
- **Tag:** sapo
- **Nguồn:** gộp từ I004, I024, I030, I034, I075, I093, I096, I098
- **Phạm vi:** Global
- **Checklist:** qa_lint:CL1-sapo, qa_lint:CL2-blacklist, outline_lint:META-sapo-dsc
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Sapo 2 đoạn ngay dưới H1. Đoạn 1: chứa nguyên keyword dạng truy vấn, trả lời thẳng (how-to: tóm tắt số bước) kèm 1 mốc có ngày. Đoạn 2: có DSC + 1 câu nêu phạm vi bài + 1 câu mời đọc tiếp gắn lợi ích (“Trong bài viết này, DSC phân tích …”). Không mở bằng bối cảnh vĩ mô hay “Bạn chỉ cần…”.

### Văn phong định chế tài chính, từ cấm nằm trong blacklist
- **ID:** I106
- **Trạng thái:** ACTIVE
- **Tag:** van-phong
- **Nguồn:** gộp từ I004, I025, I031, I032, I037, I043, I073, I094
- **Phạm vi:** Global
- **Checklist:** qa_lint:CL2-softban, qa_lint:CL2-quotes
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Giọng định chế tài chính: mộc mạc, chính xác, đi thẳng vào số liệu. Không từ cường điệu, văn nói, từ lóng, ngoặc kép bọc từ thường, tiếng Anh thô khi có từ Việt chuẩn (trader → nhà đầu tư chủ động). Từ cấm cụ thể: anti-ai-rules-blacklist.md.

### Tiêu đề Sentence case, giọng báo cáo, có H2 chứa keyword
- **ID:** I107
- **Trạng thái:** ACTIVE
- **Tag:** heading
- **Nguồn:** gộp từ I010, I053, I075, I094, I102
- **Phạm vi:** Global
- **Checklist:** qa_lint:CL1-title, outline_lint:H2-keyword
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Mọi tiêu đề (Title ≤ 59 ký tự, H1–H4) viết Sentence case, chỉ viết hoa tên riêng/mã (DSC, HOSE, VN-Index). H2/H3 là cụm danh từ mô tả, giọng báo cáo (“Các loại phí khi đầu tư chứng chỉ quỹ và mức ảnh hưởng đến lợi nhuận”); không văn nói (“ăn bao nhiêu”), không nhãn mở đầu kiểu “Số liệu 2026:”. Ít nhất 1 H2 chứa keyword hoặc câu hỏi keyword. H2/H3 lấy từ PAA giữ nguyên dạng câu hỏi.

### Câu ngắn phải mang dữ kiện, không nhân vật có tên
- **ID:** I108
- **Trạng thái:** ACTIVE
- **Tag:** cau-ngan
- **Nguồn:** gộp từ I075, I102
- **Phạm vi:** Global
- **Checklist:** slop_check:SLOP-filler
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Câu ≤ 7 từ dùng để ngắt nhịp phải mang dữ kiện (“MAGEF dẫn đầu với 64,31%.”); cấm câu nhận xét rỗng hoặc câu hỏi tu từ chuyển ý (“Kết quả này đáng chú ý.”, “Vậy nhà đầu tư nhận được gì?”) — xử lý hết SLOP-filler. Không dùng nhân vật có tên, tuổi, nghề (chị Lan, Minh 27 tuổi) ở mọi loại bài; viết “Ví dụ, với 500 triệu …”.

### Mốc thời gian chỉ đi với số liệu biến động
- **ID:** I109
- **Trạng thái:** ACTIVE
- **Tag:** moc-thoi-gian
- **Nguồn:** gộp từ I023, I064
- **Phạm vi:** Global
- **Checklist:** qa_lint:GEO-vague-time
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Chỉ gắn mốc thời gian (thời điểm thật) vào câu có số liệu biến động: phí, lãi suất, chỉ số. Không lặp “Tính đến tháng M/Y,” đầu câu hay đầu H2; phần lý thuyết, quy định chung không cần mốc.

### Số liệu: 12 tháng gần nhất, kiểm bài gốc, có nguồn
- **ID:** I110
- **Trạng thái:** ACTIVE
- **Tag:** so-lieu
- **Nguồn:** gộp từ I009, I048, I086, I089, I103
- **Phạm vi:** Global
- **Checklist:** market_facts:FACT-index-wrong, market_facts:FACT-stale, outline_lint:DATA-stale, outline_lint:DATA-unverified
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Ưu tiên số trong 12 tháng gần nhất (cuối 2026 thì số 2025 là cũ), mỗi số có nguồn + ngày. Số lấy qua WebSearch/AI Overview phải mở bài gốc kiểm năm, mốc, nguồn. Chỉ số/mã chạy lại market_facts.py, kể cả bài optimize đã có số. Quy định có số tiền tra văn bản hiện hành. Không lập bảng so sánh đối thủ khi không có nguồn công khai.

### Chỉ nhắc sản phẩm DSC thật có (không phái sinh, không quỹ mở)
- **ID:** I111
- **Trạng thái:** ACTIVE
- **Tag:** dsc-san-pham
- **Nguồn:** gộp từ I010, I036, I037, I099, I104
- **Phạm vi:** Global
- **Checklist:** qa_lint:CL5-fact
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Chỉ nhắc tính năng DSC có trong profile.md / service-operations.md, không tự suy (đặt lệnh 24/7…). DSC KHÔNG có phái sinh và KHÔNG phân phối quỹ mở (chỉ ETF niêm yết): bài về các sản phẩm này không kêu gọi mở tài khoản cho chúng, hướng về cổ phiếu cơ sở/ETF + Môi giới 1:1. eKYC luôn ghi “3 phút”.

### Product Bridge nối từ kết luận bài, nói lợi ích bằng tiền
- **ID:** I112
- **Trạng thái:** ACTIVE
- **Tag:** product-bridge
- **Nguồn:** gộp từ I026, I034, I044, I049, I101, cach-dau-tu-chung-chi-quy
- **Phản hồi từ User:** "phần Đầu tư chứng chỉ quỹ ETF trên App DSC Trading dẫn chưa hợp lý" · "chưa thể hiện được vì sao nên mở ở DSC, có ưu điểm gì, so với các cty chứng khoán khác và công ty quản lý quỹ, phân phối" (2026-11-09)
- **Phạm vi:** Global
- **Checklist:** cta_audit
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** 1) Câu mở H2 DSC nêu lý do cụ thể người đọc cần sản phẩm (vd ETF niêm yết → cần tài khoản CK), không tham chiếu ngược “ví dụ ở bước X”, nói rõ điều DSC KHÔNG làm. 2) Trả lời vì sao chọn DSC: bảng so DSC với kênh thay thế (CTCK khác, công ty quản lý quỹ/đại lý) bằng tiền trên ví dụ của bài; DSC không rẻ nhất thì nói thẳng, nhấn Môi giới 1:1 hỗ trợ tư vấn đầu tư. 3) Không list tính năng rời.

### H2 Kết luận + CTA mở tài khoản, miễn trừ cho bài khuyến nghị
- **ID:** I113
- **Trạng thái:** ACTIVE
- **Tag:** ket-luan
- **Nguồn:** gộp từ I030, I034, I052, I101
- **Phạm vi:** Global
- **Checklist:** outline_lint:H2-conclusion, qa_lint:LINK-cta
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Bài kết thúc bằng H2 “Kết luận”: 1 nhận định + checklist hành động 3 mục + CTA có link https://www.dsc.com.vn/mo-tai-khoan; không mở bằng “Tóm lại”. Bài khuyến nghị/đánh giá mã thêm câu miễn trừ trách nhiệm.

### Banner CTA: headline hành động, 3 dữ kiện thật, đoạn dẫn phía trên
- **ID:** I114
- **Trạng thái:** ACTIVE
- **Tag:** banner
- **Nguồn:** gộp từ I002, I076, I082, I085
- **Phạm vi:** Global
- **Checklist:** cta_audit, qa_lint:CTA
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Headline banner nêu hành động/lợi ích gắn chủ đề, không câu hỏi mồi; dòng phụ 3 dữ kiện thật (eKYC 3 phút, miễn phí mở/duy trì, phí từ 0,1%, 963369). Banner giữa ở ~35–40% thân bài sau phần sản phẩm DSC; banner cuối khác ý banner giữa. Ngay trên banner là 1 đoạn văn dẫn (≥ 10 từ), không phải list. Màu Dark Navy #0D1B2A + nút #2BE841.

### Trình bày: bảng/list cho so sánh và quy trình, ngắt đoạn theo ý
- **ID:** I115
- **Trạng thái:** ACTIVE
- **Tag:** trinh-bay
- **Nguồn:** gộp từ I029, I038, I039, I040, I049, I050, I060
- **Phạm vi:** Global
- **Checklist:** qa_lint:CL6-paragraph, qa_lint:CL6-lists, qa_lint:FMT-codeblock, slop_check:SLOP-table-thin
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Số liệu so sánh, phí, quy trình → bảng hoặc list; khái niệm dễ nhầm → bảng đối sánh. Phần ngắn 2–3 câu gộp thành bullet có nhãn đậm, không tách H3. Ngắt đoạn theo ý (≤ 3 câu), không bẻ câu máy móc; 2 list liền nhau phải có câu nối. Lưu đồ, code → bảng hoặc list đánh số. Bài glossary chia nhóm H2 theo chủ đề.

### Định dạng Markdown để lint và CMS đọc đúng
- **ID:** I116
- **Trạng thái:** ACTIVE
- **Tag:** dinh-dang
- **Nguồn:** gộp từ I028, I033, I035, I041, I042, I043, I046, I047, I057, I058, I060, I063, I066, I067
- **Phạm vi:** Global
- **Checklist:** qa_lint:FMT-latex, qa_lint:FMT-callout, qa_lint:FMT-hr, qa_lint:FM-quotes, qa_lint:FMT-bold-label, qa_lint:CL3-decimal, qa_lint:CL6-sentence, qa_lint:CL6-list-item
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** Heading `##`/`###` (không giữ `### H2:` của outline). 1 dòng trống trước/sau list, bảng và giữa câu hỏi–đáp FAQ. Dấu ?/. đặt ngoài `**…**`; câu dẫn vào list liền kề kết thúc bằng “.”; nhãn đậm đầu bullet dùng “:”. Số thập phân dấu phẩy. Không LaTeX (công thức in đậm), callout `> [!NOTE]`, `---`, ký tự `|` trong ô bảng, ngoặc kép trong YAML.

### Internal link tuyệt đối, khớp sitemap, đặt trong câu
- **ID:** I117
- **Trạng thái:** ACTIVE
- **Tag:** link
- **Nguồn:** gộp từ I051, I052, I054, I055, I056, I068
- **Phạm vi:** Global
- **Checklist:** qa_lint:LINK-sitemap, qa_lint:LINK-relative, qa_lint:LINK-local, qa_lint:LINK-anchor, qa_lint:LINK-xemthem, qa_lint:LINK-cta
- **Máy kiểm:** full
- **Cập nhật:** 2026-11-09
- **Bản năng:** URL tuyệt đối khớp từng ký tự với sitemap (find_links.py), gắn trong câu có ngữ cảnh, không dòng “Xem thêm”; mỗi bài có link https://www.dsc.com.vn/mo-tai-khoan ở Bridge hoặc Kết luận.

### Một URL một intent, chủ đề đã có bài riêng thì chỉ link
- **ID:** I118
- **Trạng thái:** ACTIVE
- **Tag:** intent
- **Nguồn:** gộp từ I074, I085, I096
- **Phạm vi:** Global
- **Cập nhật:** 2026-11-09
- **Bản năng:** Trước khi viết, find_links.py xem bài DSC cùng cụm. Bài lựa chọn chỉ nhắc quy trình 2–3 câu + link sang bài hướng dẫn (và ngược lại); bài how-to mua mã không chứa phân tích BCTC. Chủ đề đã có bài riêng (rủi ro, phí…) → 1 câu + link, không dựng H2 riêng. Anchor dạng hướng dẫn chỉ trỏ bài hướng dẫn, dạng lựa chọn chỉ trỏ bài lựa chọn.

### Bài how-to: cùng cỡ đối thủ, H3 là bước, web/app theo ảnh
- **ID:** I119
- **Trạng thái:** ACTIVE
- **Tag:** how-to
- **Nguồn:** gộp từ I075, I095, I096
- **Phạm vi:** Global
- **Cập nhật:** 2026-11-09
- **Bản năng:** Giữ số từ, số H2 cùng cỡ 2 đối thủ top; cắt phần lệch intent. H3 dưới H2 hướng dẫn là bước đánh số. Bước đã minh họa bằng sản phẩm DSC thì không thêm H2 “tại DSC”; H1 có DSC. Web hay app xác định từ chính ảnh chụp; khác quy trình thì tách H2 cho app.

### Toplist: N mục là nội dung chính, mỗi mục cùng khung
- **ID:** I120
- **Trạng thái:** ACTIVE
- **Tag:** toplist
- **Nguồn:** gộp từ I014, I072, I097, I099
- **Phạm vi:** Global
- **Checklist:** outline_lint:FMT-mismatch, outline_lint:LIST-count
- **Máy kiểm:** partial
- **Cập nhật:** 2026-11-09
- **Bản năng:** N mục là nội dung chính, tối đa 3 H2 hỗ trợ (bảng tóm tắt, cách chọn, FAQ) + H2 Kết luận như mọi bài (I113, chốt 09/11). Mỗi H3 ~200 từ: Giới thiệu → Ưu → Nhược → Hợp với ai, mỗi ý 1 dữ kiện đã xác minh; mục DSC cũng có nhược điểm thật. Bài khuyến nghị mã: chọn theo đồng thuận báo cáo CTCK có ngày, ghi nguồn cạnh giá mục tiêu; DSC không tự đặt giá mục tiêu.

### Khi /optimize: giữ xương bài gốc, dùng query GSC
- **ID:** I121
- **Trạng thái:** ACTIVE
- **Tag:** optimize
- **Nguồn:** gộp từ I086, I089, I090, I093, I097
- **Phạm vi:** Global
- **Cập nhật:** 2026-11-09
- **Bản năng:** Giữ thứ tự H2 và mẫu block bản gốc, chỉ thay nội dung; thêm H2 mới phải hỏi. Query GSC của URL: biến thể nhiều click vào sapo/H2, câu hỏi nhiều impression thành H2. CTR thấp dù hiển thị cao → Title có con số/giải pháp, 50 ký tự đầu Meta trả lời thẳng.

### Phản hồi “ko có X” nghĩa là đang thiếu X
- **ID:** I122
- **Trạng thái:** ACTIVE
- **Tag:** phan-hoi
- **Nguồn:** gộp từ I098, I100
- **Phạm vi:** Global
- **Cập nhật:** 2026-11-09
- **Bản năng:** Phản hồi ngắn “ko có X”, “chưa có X” = bài đang THIẾU X, cần thêm. Chỉ hiểu là bỏ khi user viết rõ “bỏ”, “xóa”, “đừng”. Cách hiểu đi ngược rule hiện có hoặc làm mất nội dung đang có → hỏi lại 1 câu trước khi sửa.

### Bài BCTC/chỉ báo/công cụ có phần nền và phần thực hành
- **ID:** I123
- **Trạng thái:** ACTIVE
- **Tag:** nen-tang
- **Nguồn:** gộp từ I027, I063
- **Phạm vi:** Global
- **Cập nhật:** 2026-11-09
- **Bản năng:** Ngoài phần chiến lược, có phần nền (cách lập, cấu tạo, công thức) để khớp truy vấn học thuật. Bài cho nhà đầu tư chủ động (P3) thêm hướng dẫn thực hành từng bước và sai lầm thường gặp.

### Bài phân tích mã: số quý mới nhất, tách khoản bất thường
- **ID:** I124
- **Trạng thái:** ACTIVE
- **Tag:** phan-tich-ma
- **Nguồn:** gộp từ I003, I008, I009, I012, I084, I091, I092
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu
- **Cập nhật:** 2026-11-09
- **Bản năng:** Số liệu quý mới nhất (doanh thu, LNST, backlog, P/B, giá), Title ghi quý/năm; soát mã bị copy sai ở heading; giữ biểu đồ gốc. Tách khoản bất thường một lần khỏi KQKD cốt lõi; niên độ lệch năm dương lịch nói rõ đầu phần KQKD. Phủ biến thể tên gọi (MB Bank/MBB) trong H2, FAQ. Mã đang biến cố: không gợi ý margin cho F0.

### Bài chỉ báo/mô hình: bảng phân biệt mẫu dễ nhầm, tín hiệu có xác nhận
- **ID:** I125
- **Trạng thái:** ACTIVE
- **Tag:** chi-bao-mo-hinh
- **Nguồn:** gộp từ I005, I016, I021, I022, I079, I082, I087
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật
- **Cập nhật:** 2026-11-09
- **Bản năng:** Mở bằng phân biệt với mẫu dễ nhầm (bảng đối sánh: Stochastic vs StochRSI, Hammer vs Hanging Man…); mục công thức chỉ nói biến số và cách tính. Tín hiệu luôn kèm điều kiện xác nhận (volume ≥ 1,5× MA20 hoặc nến xác nhận), điểm cắt lỗ, R:R ≥ 1:2, nhắc T+2. Code (AFL, Pine) trình bày bằng bảng 2 cột, không code block.

### Vĩ mô: số Việt Nam gần nhất, biến số quốc tế gắn tác động trong nước
- **ID:** I126
- **Trạng thái:** ACTIVE
- **Tag:** vi-mo
- **Nguồn:** gộp từ I001, I007, I019, I044, I048, I069, I088, I089
- **Phạm vi:** Chỉ topic: Vĩ mô
- **Cập nhật:** 2026-11-09
- **Bản năng:** Dùng số liệu vĩ mô Việt Nam đã công bố gần nhất, không số giả định. Biến số quốc tế (DXY, Fed, KOSPI, giờ sàn Mỹ) gắn với tác động tại Việt Nam (tỷ giá, dòng vốn ngoại, VN-Index) ngay ở H1/Meta; giờ quốc tế quy đổi UTC+7 có DST. Bridge từ vàng/tiết kiệm sang cổ phiếu lập luận bằng logic tài chính; nhắc cá nhân VN chưa được tự mua cổ phiếu nước ngoài.

### F0: thông số giao dịch chuẩn và khái niệm dễ nhầm
- **ID:** I127
- **Trạng thái:** ACTIVE
- **Tag:** f0-thong-so
- **Nguồn:** gộp từ I002, I006, I010, I013, I015, I064, I080, I081
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)
- **Cập nhật:** 2026-11-09
- **Bản năng:** Biên độ HOSE ±7%, HNX ±10%, UPCoM ±15%, lô chẵn 100 cp, T+2 (cổ phiếu về 13h ngày T+2 mới bán được; VN chưa có T0 — “lướt T0” là bán hàng có sẵn). Tài khoản 024Cxxxxxx: tiểu khoản 1 thường, 6 ký quỹ; nạp qua mã định danh 963369. Cặp dễ nhầm (Sở GDCK vs CTCK, thuế 0,1% vs 5% cổ tức) phân biệt ngay đầu; margin luôn có kịch bản 2 chiều trừ lãi vay.

### Chỉ số tài chính: ví dụ từ BCTC thật, ngưỡng theo ngành
- **ID:** I128
- **Trạng thái:** ACTIVE
- **Tag:** chi-so-tai-chinh
- **Nguồn:** gộp từ I020, I059, I061, I065, I070
- **Phạm vi:** Chỉ topic: Chỉ số tài chính & BCTC
- **Cập nhật:** 2026-11-09
- **Bản năng:** Ví dụ tính bằng số liệu BCTC thật của doanh nghiệp niêm yết (không số giả định), kèm bảng ngưỡng theo ngành (ngân hàng, BĐS, công nghệ…). Chỉ số dễ nhầm có bảng đối sánh (mệnh giá vs giá sổ sách vs thị giá; QoQ vs YoY); nối chỉ số với các chỉ số liên quan (LLR–NPL–CASA).

### Phái sinh: bài kiến thức, Bridge về cổ phiếu cơ sở
- **ID:** I129
- **Trạng thái:** ACTIVE
- **Tag:** phai-sinh
- **Nguồn:** gộp từ I017, I018, I083
- **Phạm vi:** Chỉ topic: Phái sinh
- **Cập nhật:** 2026-11-09
- **Bản năng:** DSC không cung cấp phái sinh: Bridge hướng về cổ phiếu cơ sở, không kêu gọi mở tài khoản phái sinh. Phân biệt giá trị danh nghĩa vs ký quỹ vs vốn đệm; lịch đáo hạn lấy năm hiện tại; HĐTL VN30 có ATO/ATC, HĐTL TPCP không.

### Tài chính cá nhân: CCQ dùng NAV, ví dụ dòng tiền theo tháng
- **ID:** I130
- **Trạng thái:** ACTIVE
- **Tag:** tai-chinh-ca-nhan
- **Nguồn:** gộp từ I062, I071, I072, I078, I103
- **Phạm vi:** Chỉ topic: Tài chính cá nhân
- **Cập nhật:** 2026-11-09
- **Bản năng:** Chứng chỉ quỹ không gọi “lãi suất” — dùng hiệu suất/tăng trưởng NAV; so sánh với tiết kiệm bằng bảng và ví dụ tích lũy định kỳ. Bảo hiểm tiền gửi: 350 triệu VNĐ từ 13/7/2026 (Thông tư 05/2026/TT-NHNN), không còn 125 triệu. So sánh kênh tiết kiệm/đầu tư dùng mô phỏng dòng tiền theo tháng bằng tiền thật; tiền gửi lớn nhắc phần lãi thỏa thuận tại quầy.

---

## Lịch sử (DEPRECATED / ARTICLE — giữ nguyên văn)


### Chỉ số kinh tế địa phương GRDP: Bảng xếp hạng 2025–2026, Giá so sánh loại trừ lạm phát & Ứng dụng lọc cổ phiếu
- **ID:** I001
- **Trạng thái:** ARTICLE
- **Thay bởi:** I126
- **Nguồn:** grdp-la-gi-chi-so-quan-trong-danh-gia-su-phat-trien-kinh-te-dia-phuong
- **Phản hồi từ User:** "Click giảm 54% → thêm bảng GRDP các tỉnh năm 2025–2026 mới nhất", "/approve"
- **Bản năng:** 1. Khi tối ưu bài viết về chỉ số kinh tế địa phương (GRDP) cho F0 (P2) bị suy giảm click nghiêm trọng do thông tin lỗi thời, bắt buộc phải cập nhật Bảng xếp hạng GRDP các tỉnh thành mới nhất (Top 10 tốc độ tăng trưởng và Top 5 quy mô giá trị tuyệt đối) theo dữ liệu chính thức từ Tổng cục Thống kê, kèm định hướng mục tiêu giai đoạn 2026–2030. 2. Làm rõ công thức tính tốc độ tăng trưởng GRDP liên năm dựa trên giá so sánh (không dùng giá hiện hành để loại trừ tác động lạm phát) và bổ sung khái niệm GRDP bình quân đầu người phản ánh năng suất lao động thực chất. 3. Xây dựng Bảng đối chuẩn đa chiều 5 tiêu chí giữa GRDP và GDP quốc gia, giải thích rõ cơ chế tính trùng chi phí trung gian liên tỉnh trước năm 2017. 4. Chuyển hóa dữ liệu vĩ mô địa phương thành cơ hội đầu tư thực chiến bằng việc liên kết các tỉnh tăng trưởng cao với cổ phiếu Bất động sản KCN (BCM, IDC, KBC), Cảng biển & Logistics (GMD, HAH) và xây lắp hạ tầng.
- **Phạm vi:** Chỉ topic: Vĩ mô

### Hướng dẫn mua cổ phiếu online cho F0: Nạp tiền định danh 963369, Bảng tính vốn 1 lô chẵn 100 cp & Chu kỳ T+2
- **ID:** I002
- **Trạng thái:** ARTICLE
- **Thay bởi:** I114
- **Nguồn:** cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau
- **Phản hồi từ User:** "Click giảm 55%, sát chuyển đổi → làm mới các bước, thêm CTA mở tài khoản DSC", "/approve"
- **Bản năng:** 1. Khi tối ưu bài viết hướng dẫn thao tác mua cổ phiếu online cho F0 (P2) bị suy giảm CTR và yếu chuyển đổi, bắt buộc phải cập nhật quy trình mở tài khoản eKYC 100% online 3 phút trên App DSC Trading (tài khoản dạng 024Cxxxxxx, phân định rõ tiểu khoản thường đuôi 1 và ký quỹ đuôi 6). 2. Quy trình nạp tiền bắt buộc phải hướng dẫn công thức nạp tự động qua Mã định danh 963369 (kết nối BIDV) và chuyển khoản Napas 24/7 tiền vào ngay tức thì, loại bỏ hoàn toàn các hướng dẫn chuyển khoản thủ công lỗi thời. 3. Thỏa mãn bài toán "Cần bao nhiêu tiền để bắt đầu?" bằng Bảng tính số vốn tối thiểu thực tế mua 1 lô chẵn 100 cổ phiếu (HPG, MBB, TCB, VNM, FPT) để người mới hình dung rõ ngân sách từ 2–3 triệu đồng. 4. Bổ sung Bảng thông số kỹ thuật 3 sàn (HOSE biên độ ±7%, HNX ±10%, UPCoM ±15%, khung giờ ATO/ATC), phân biệt rõ lệnh LO vs MP, làm rõ quy định chu kỳ thanh toán T+2 (cổ phiếu về lúc 13h00 ngày T+2 mới được bán) và kỷ luật cắt lỗ (-7% đến -8%). 5. Chèn 2 Banner CTA Dark Navy (#0D1B2A) + Nút Neon Green (#2BE841) chuẩn WCAG AA đạt 100/100 CRO audit.
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)

### Phân tích cổ phiếu Bất động sản dân cư: Hai mũi nhọn BCTC môi giới vs Điểm rơi bàn giao dự án
- **ID:** I003
- **Trạng thái:** ARTICLE
- **Thay bởi:** I124
- **Nguồn:** co-phieu-dxg-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat
- **Phản hồi từ User:** "Cập nhật KQKD quý 3/2026, ghi năm và quý vào title"
- **Bản năng:** 1. Khi tối ưu hoặc viết bài phân tích cổ phiếu ngành bất động sản dân cư (như DXG), tiêu đề bắt buộc tuân thủ chuẩn Sentence case và nêu rõ mốc năm, quý tài chính cập nhật (quý 3/2026). 2. Về mặt nội dung phân tích cơ bản, bắt buộc bóc tách đồng thời 2 trụ cột tạo dòng tiền: (a) Kết quả kinh doanh định kỳ theo quý của mảng dịch vụ môi giới/phân phối bất động sản (DXS) phản ánh sức mua thị trường sớm nhất; (b) Tiến độ tháo gỡ vướng mắc pháp lý và cấp phép/nghiệm thu hạ tầng các dự án đô thị trọng điểm (Gem Sky World, Opal Luxury) kết hợp chỉ báo "Người mua trả tiền trước" để định vị chính xác điểm rơi lợi nhuận chu kỳ 2026–2027.
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu

### Loại bỏ từ ngữ giật gân slop & Sapo mọi loại bài có DSC + 1 câu dẫn đọc bài
- **ID:** I004
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I105
- **Nguồn:** yoy-la-gi-cach-tinh-va-y-nghia-cua-chi-so-yoy
- **Phản hồi từ User:** "mấy từ như sống còn các thứ nghe slop quá. loại bỏ. Sau đó viết bài sửa theo proposal", "Sapo ko CTA đọc bài và ko có phần nhắc đến brand."
- **Bản năng:** 1. Tuyệt đối loại bỏ các từ ngữ cường điệu, đao to búa lớn hoặc marketing sáo rỗng gây cảm giác AI slop (như "sống còn", "bí quyết vàng", "siêu bảng", "bản năng độc quyền", "ma trận 2D 4 góc phần tư") trong bài viết tài chính cho người mới (P2); sử dụng ngôn phong mộc mạc, chuẩn xác và đi thẳng vào bản chất số liệu. 2. Sapo mọi loại bài (định nghĩa, phân tích, how-to): đoạn 1 chứa keyword, trả lời thẳng kèm mốc có ngày; đoạn 2 có DSC + 1 câu nêu phạm vi bài và 1 câu mời đọc tiếp gắn lợi ích cụ thể (mẫu: "Trong bài viết này, DSC phân tích … Đọc tiếp để biết …"). Không dùng cụm sáo "Hãy cùng khám phá", "Bài viết dưới đây" (blacklist). 3. Đính chính 2026-11-09 (bài rui-ro-chung-chi-quy): phản hồi gốc "Sapo ko CTA đọc bài và ko có phần nhắc đến brand" nghĩa là sapo đang THIẾU CTA và brand, không phải cấm. User xác nhận: "Sapo phải nhắc DSC và kêu gọi người đọc xem tiếp bài viết chứ".
- **Phạm vi:** Global

### Chỉ báo dao động kỹ thuật Stochastic: Phân định bản chất toán học vs StochRSI & Hóa giải bẫy nằm lì siêu sóng
- **ID:** I005
- **Trạng thái:** ARTICLE
- **Thay bởi:** I125
- **Nguồn:** chi-bao-stochastic-la-gi
- **Phản hồi từ User:** "Phần công thức sao lại có nội dung h3 so sánh."
- **Bản năng:** 1. Khi xây dựng outline và bài viết về các chỉ báo dao động (Oscillators), các mục đề mục công thức phải tập trung thuần túy vào biến số toán học và cơ chế làm mượt tín hiệu, không lồng ghép các H3 so sánh đối chiếu làm loãng intent tìm kiếm. 2. Đối với chỉ báo Stochastic cho nhà đầu tư chủ động (P3), bắt buộc phân định rạch ròi ngay từ đầu giữa Stochastic Oscillator (George Lane) tính trực tiếp trên giá đóng cửa và Stochastic RSI (Chande & Kroll) tính trên chỉ số RSI để dập tắt nhầm lẫn trên SERP, khuyến nghị Slow Stochastic (14, 3, 3) trên D1. 3. Không khuyên bán non khi Stochastic chạm ngưỡng 80 trong xu hướng tăng mạnh mà hướng dẫn dùng đường trung bình động (EMA10/EMA20) làm mốc chặn lãi (Trailing Stop) bám theo thân sóng.
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật

### Thuế chuyển nhượng & Chi phí giao dịch chứng khoán: Phân định thuế khoán vs Thuế cổ tức hai tầng
- **ID:** I006
- **Trạng thái:** ARTICLE
- **Thay bởi:** I127
- **Nguồn:** thue-khi-ban-co-phieu
- **Phản hồi từ User:** "/approve" (duyệt draft không chỉnh sửa)
- **Bản năng:** Khi viết bài về thuế khi bán cổ phiếu và chi phí giao dịch cho F0 (P2), luôn phân định rạch ròi ngay từ đầu giữa thuế khoán chuyển nhượng 0,1% (tính trên doanh thu bán, không bù trừ lỗ, áp dụng từ Luật 71/2014/QH13) và thuế thu nhập từ đầu tư vốn 5% khi bán cổ tức bằng cổ phiếu theo Nghị định 126/2020/NĐ-CP (thuế 5% tính theo mệnh giá 10.000đ + thuế 0,1% tính theo giá bán thực tế). Kết hợp Bảng đối sánh 5 loại thuế phí trọn gói (thuế TNCN, phí giao dịch CTCK, phí trả Sở 0,027%, phí lưu ký VSDC 0,27đ/cp/tháng, phí ứng trước tiền bán) và Bảng tính toán định lượng mức độ hao mòn vốn khi lướt sóng quá mức (Overtrading 5, 10, 20, 40 vòng) để cảnh báo rủi ro bào mòn tài khoản và dẫn dắt giải pháp đồng hành cùng Môi giới 1:1 của DSC.
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)

### Thuật ngữ kinh tế vi mô: Trực quan hóa công thức & Liên kết sức mạnh định giá cổ phiếu
- **ID:** I007
- **Trạng thái:** ARTICLE
- **Thay bởi:** I126
- **Nguồn:** do-co-gian-cua-cau-theo-gia-la-gi
- **Phản hồi từ User:** "ko" (duyệt draft)
- **Bản năng:** Khi tối ưu bài viết thuật ngữ kinh tế vi mô (như độ co giãn của cầu, quy luật cung cầu) cho F0 (P2), luôn chuyển hóa các công thức học thuật thành định dạng văn bản in đậm trực quan (tránh dùng mã LaTeX $...), kết hợp ví dụ tính toán đời sống dễ hiểu và liên hệ trực tiếp với phân tích cổ phiếu thực chiến (nhận diện con hào kinh tế, năng lực định giá và phân bổ nhóm cổ phiếu phòng thủ vs chu kỳ). Tuyệt đối không dùng ký tự gạch đứng `|` (như `|Ed|`) bên trong các ô bảng Markdown vì sẽ làm hỏng cấu trúc cột (pipe delimiter); thay bằng cách viết chữ rõ nghĩa như `Trị tuyệt đối Ed`, `hệ số > 1`. Luôn áp dụng định dạng Sentence case cho Title H1, Meta Title và toàn bộ Headings.
- **Phạm vi:** Chỉ topic: Vĩ mô

### Phân tích cổ phiếu Cảng biển & Logistics: M&A hạ tầng, liên minh đội tàu và chu kỳ tài sản
- **ID:** I008
- **Trạng thái:** ARTICLE
- **Thay bởi:** I124
- **Nguồn:** co-phieu-vsc-tong-quan-danh-gia-va-ket-qua-kinh-doanh-moi-nhat
- **Phản hồi từ User:** "oke. nhớ cập nhật thêm data mới nhất", "ko" (duyệt draft)
- **Bản năng:** Khi viết hoặc tối ưu bài phân tích cổ phiếu ngành cảng biển và logistics (như VSC), bắt buộc phải cập nhật tác động từ các thương vụ M&A hạ tầng cầu bến trọng điểm (Nam Hải Đình Vũ), liên minh đội tàu feeder (HAH), sản lượng TEU thực tế, thời điểm hết khấu hao tài sản cố định làm tăng biên lợi nhuận gộp, và định giá tài sản ròng qua P/B kết hợp P/E dự phóng. Tuân thủ định dạng Sentence case cho toàn bộ tiêu đề và headings.
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu

### Cập nhật data BCTC mới nhất & Soát lỗi mã chứng khoán cho bài phân tích cổ phiếu
- **ID:** I009
- **Trạng thái:** ARTICLE
- **Thay bởi:** I110
- **Nguồn:** co-phieu-vhm-tong-quan-danh-gia-va-cap-nhan-ket-qua-kinh-doanh-moi-nhat
- **Phản hồi từ User:** "oke. nhớ cập nhật thêm data mới nhất"
- **Bản năng:** Khi tối ưu bài phân tích cổ phiếu cụ thể (ticker), luôn chủ động tra cứu BCTC và số liệu quý mới nhất của năm (doanh thu, LNST, backlog, P/B, thị giá hiện tại), rà soát kỹ các lỗi copy-paste sai mã chứng khoán ở heading phân tích kỹ thuật, và bảo toàn 100% các biểu đồ tài chính gốc đã có trên web.
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu

### Tiêu đề Sentence Case & Phân định pháp lý T0 / Tuyệt đối không gán phái sinh cho DSC
- **ID:** I010
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I107
- **Nguồn:** day-trading-la-gi
- **Phản hồi từ User:** "sao lại có T0. Tưởng Việt Nam ko có T0", "oke. Ngoài ra tối muốn tất cả tiêu đề bài viết phải viết dạng sentences case", "DSC ko có giao dịch phái sinh"
- **Bản năng:** 
  1. Tất cả tiêu đề bài viết (Title H1, Meta Title) và các tiêu đề mục phụ (H2, H3, H4) bắt buộc phải viết ở dạng **Sentence case** (chỉ viết hoa chữ cái đầu tiên và danh từ riêng/viết tắt/mã cổ phiếu như DSC, HOSE, HNX, VN-Index, HPG). Tuyệt đối không dùng Title Case.
  2. Tuyệt đối không đề cập hoặc giới thiệu giao dịch phái sinh/Hợp đồng tương lai gắn liền với sản phẩm, dịch vụ hay thương hiệu DSC (DSC không cung cấp giao dịch phái sinh).
  3. Khi đề cập đến Day trading/Lướt sóng trong ngày tại thị trường Việt Nam, bắt buộc phải khẳng định rõ ranh giới pháp lý: thị trường cơ sở là chu kỳ T+2.5 (chưa có T0 chính thức). Bản chất thực tế của "lướt T0" tại Việt Nam là kỹ thuật giao dịch trên kho hàng cổ phiếu có sẵn (available inventory) để hạ giá vốn và ăn chênh lệch biên độ, đi kèm cảnh báo rủi ro kẹp hàng nếu giá không hồi.
- **Phạm vi:** Global

### Bảng so sánh 4 nhóm CTCK & Gom mạng lưới Hub-and-Spoke cho bài Pillar F0
- **ID:** I011
- **Trạng thái:** SUPERSEDED (2026-10-16 — thay bằng "Re-optimize pillar: kiểm lại số liệu bản trước, bảng so sánh CTCK chỉ khi có nguồn")
- **Nguồn:** cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau
- **Phản hồi từ User:** "Làm mới nội dung 2026, thêm phần so sánh công ty chứng khoán, gom internal link từ cả cụm “người mới” về bài này"
- **Bản năng:** Khi tối ưu bài viết trụ cột (Pillar) nhập môn chứng khoán cho F0 (P2), luôn cập nhật bối cảnh số liệu mới nhất của năm (số tài khoản VSDC, thanh khoản HOSE, VN-Index), tích hợp Bảng đối sánh 5 tiêu chí của 4 nhóm công ty chứng khoán (Thị phần lớn, Trực thuộc ngân hàng, Fintech phí 0 đồng, và Ngân hàng Đầu tư DSC Môi giới 1:1) để định hướng mở tài khoản an toàn, và xây dựng mạng lưới internal links 2 chiều gom trọn cụm chủ đề vệ tinh (mở tài khoản, mua cổ phiếu, bán cổ phiếu, phí giao dịch).
- **Phạm vi:** Global

### Phủ sâu biến thể từ khóa phụ H2/FAQ & Bảng thông số giao dịch cổ phiếu ngân hàng
- **ID:** I012
- **Trạng thái:** ARTICLE
- **Thay bởi:** I124
- **Nguồn:** lam-the-nao-de-mua-co-phieu-mbb-ngan-hang-quan-doi
- **Phản hồi từ User:** "Mất hiển thị nhiều hơn mất thứ hạng, nghĩa là đang rơi khỏi các từ khóa phụ. Bổ sung các biến thể như “MB Bank”, “MBB”, “mua cổ phiếu MB” vào H2 và FAQ"
- **Bản năng:** Khi tối ưu bài hướng dẫn mua cổ phiếu ngân hàng cụ thể (như MBB) bị mất hiển thị do rơi rụng từ khóa phụ, bắt buộc phải phủ đều các biến thể tên gọi phổ biến của ngân hàng (“MB Bank”, “MBB”, “mua cổ phiếu MB”) vào tiêu đề H2 và cụm câu hỏi FAQ, kết hợp Bảng thông số kỹ thuật sàn HOSE (biên độ ±7%, lô chẵn 100 cp, bước giá, chu kỳ T+2), Bảng tính chi phí vốn thực tế 1 lô chẵn 100 cp, phân định rõ giao dịch qua CTCK vs App ngân hàng số, và xây dựng liên kết chéo chống cannibalization với bài phân tích cơ bản.
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu

### Bảng 6 màu bảng điện tử 3 sàn & Bóc tách bẫy tâm lý Xanh vỏ đỏ lòng cho F0
- **ID:** I013
- **Trạng thái:** ARTICLE
- **Thay bởi:** I127
- **Nguồn:** cac-mau-trong-chung-khoan-y-nghia-va-tac-dong-den-nha-dau-tu
- **Phản hồi từ User:** "/approve bài viết tối ưu các màu trong chứng khoán"
- **Bản năng:** Khi viết hoặc tối ưu các bài giải thích về màu sắc trên bảng giá chứng khoán cho F0 (P2), luôn tích hợp Bảng tra cứu 6 màu sắc chuẩn và biên độ giá 3 sàn (HOSE ±7%, HNX ±10%, UPCoM ±15%), bóc tách cơ chế đổi màu khớp lệnh theo thời gian thực (giá khớp lệnh vs giá tham chiếu/trần/sàn), phân tích hiện tượng thị trường lệch pha "Xanh vỏ đỏ lòng" (khi nhóm VN30/trụ kéo điểm ảo) vs "Đỏ vỏ xanh lòng", kết hợp 3 bẫy tâm lý F0 (FOMO đu tím, bán tháo xanh lơ, tê liệt khi sideway) và khuyến nghị kỷ luật cắt lỗ 7%–8% cùng chuyên gia Môi giới 1:1 DSC.
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)

### Bảng Chỉ Số Định Giá Ngân Hàng 2026 & 5 chỉ số định giá cổ phiếu ngân hàng
- **ID:** I014
- **Trạng thái:** ARTICLE
- **Thay bởi:** I120
- **Nguồn:** top-5-co-phieu-ngan-hang-dinh-gia-hop-ly-tiem-nang-but-pha-manh
- **Phản hồi từ User:** "/approve bài viết tối ưu top 5 cổ phiếu ngành ngân hàng tiềm năng 2026"
- **Bản năng:** Khi viết hoặc tối ưu bài toplist cổ phiếu ngân hàng cho F0 (P2), luôn tích hợp Bảng Chỉ Số Định Giá đa chiều (P/E, P/B, ROE, CASA, NPL, Giá mục tiêu, Upside), bóc tách phương pháp định giá qua 5 chỉ số (NIM, CASA, NPL/LLR, CAR, P/B), ưu tiên các mã ngân hàng có CASA cao và room tín dụng ưu đãi như MBB, TCB, ACB, đồng thời lồng ghép phân tích tác động vĩ mô từ chu kỳ tín dụng và làn sóng nâng hạng FTSE Russell 2026.
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu

### Bảng đối sánh Sở giao dịch vs CTCK & Bảng 3 sàn HOSE HNX UPCoM
- **ID:** I015
- **Trạng thái:** ARTICLE
- **Thay bởi:** I127
- **Nguồn:** san-giao-dich-chung-khoan-la-gi
- **Phản hồi từ User:** "/approve bài viết tối ưu sàn chứng khoán là gì"
- **Bản năng:** Khi viết/tối ưu các bài giải thích sàn chứng khoán cho F0 (P2), luôn phân định rạch ròi ngay từ đầu giữa Sở giao dịch chứng khoán (nơi tổ chức thị trường tập trung) và Công ty chứng khoán (định chế trung gian nơi F0 mở tài khoản eKYC), kết hợp Bảng đối sánh 3 sàn (HOSE vs HNX vs UPCoM về vốn điều lệ, biên độ dao động ±7%, ±10%, ±15% và lô chẵn 100 cp), Bảng khung giờ các phiên giao dịch (ATO, liên tục, ATC, thỏa thuận, PLO) và Checklist nhận diện bẫy sàn quốc tế/Forex lừa đảo.
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)

### Bảng đối sánh RSI Phân kỳ Thường vs Ẩn & Quy trình 4 bước tiếp diễn xu hướng
- **ID:** I016
- **Trạng thái:** ARTICLE
- **Thay bởi:** I125
- **Nguồn:** phan-ky-an-rsi-la-gi
- **Phản hồi từ User:** "/approve bài viết tối ưu phân kỳ ẩn RSI là gì"
- **Bản năng:** Khi viết/tối ưu các bài về phân kỳ ẩn RSI cho nhà đầu tư chủ động (P3), luôn phân định rõ cơ chế xung lực tiếp diễn xu hướng của nhịp Pullback so với phân kỳ thường (đảo chiều), kết hợp Bảng đối sánh, Quy trình 4 bước xác nhận thanh khoản (Vol 1,5x MA20) & tỷ lệ R:R kỷ luật (Stop Loss 0,5%–1%, Take Profit R:R ≥ 1:2), đồng thời liên kết giải pháp tư vấn Môi giới 1:1 và Margin DSC 10–13,5%/năm.
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật

### Phân định Cấu trúc phiên HĐTL VN30 vs TPCP và Giá trị dẫn dắt của 15 phút mở cửa sớm
- **ID:** I017
- **Trạng thái:** ARTICLE
- **Thay bởi:** I129
- **Nguồn:** gio-giao-dich-phai-sinh
- **Phản hồi từ User:** "/approve bài viết giờ giao dịch phái sinh"
- **Bản năng:** Khi viết bài về thời gian và các phiên giao dịch phái sinh cho F0 (P2) và Active Trader (P3), luôn phân định rõ cấu trúc phiên của HĐTL VN30 (có phiên ATO/ATC) vs HĐTL TPCP (khớp liên tục toàn phiên không có ATO/ATC), giải thích giá trị dự báo sớm của 15 phút mở cửa sớm (08:45) đối với thị trường cơ sở (HOSE 09:00), công thức tính giá FSP ngày đáo hạn chống thao túng, và giữ vững định vị thương hiệu DSC hướng nhà đầu tư về cổ phiếu cơ sở an toàn.
- **Phạm vi:** Chỉ topic: Phái sinh

### Phân định Giá trị danh nghĩa vs Tiền ký quỹ và Vốn đệm an toàn phái sinh
- **ID:** I018
- **Trạng thái:** ARTICLE
- **Thay bởi:** I129
- **Nguồn:** 1-hop-dong-phai-sinh-bao-nhieu-tien
- **Phản hồi từ User:** "/approve bài viết 1 hợp đồng phái sinh bao nhiêu tiền"
- **Bản năng:** Khi viết các bài giải thích số vốn và ký quỹ phái sinh cho F0 (P2), luôn phân định rạch ròi giữa Giá trị danh nghĩa của hợp đồng (120–140 triệu VNĐ) và Số tiền ký quỹ thực tế (22–27 triệu VNĐ nhờ đòn bẩy 5:1 - 6:1), bổ sung khái niệm Vốn đệm an toàn dự phòng biến động (30–35 triệu VNĐ/hợp đồng) để tránh bẫy Call Margin, đồng thời giữ vững lập trường thương hiệu DSC không cung cấp phái sinh mà ưu tiên cổ phiếu cơ sở bền vững.
- **Phạm vi:** Chỉ topic: Phái sinh

### Phân định rạch ròi Chỉ số vs ETF và Bóc tách rổ cổ phiếu kín room ngoại
- **ID:** I019
- **Trạng thái:** ARTICLE
- **Thay bởi:** I126
- **Nguồn:** vn-diamond-la-gi
- **Phản hồi từ User:** "/approve bài viết vn diamond là gì"
- **Bản năng:** Khi viết bài về các chỉ số chứng khoán đặc thù và quỹ ETF mô phỏng (như VN Diamond - FUEVFVND) cho F0 (P2), luôn phân định rạch ròi ngay từ đầu giữa Chỉ số tham chiếu (Index) và Sản phẩm chứng chỉ quỹ niêm yết (ETF), kết hợp Bảng đối sánh trực quan với chỉ số đại chúng (VN30), bóc tách cơ chế giới hạn tỷ lệ sở hữu nước ngoài (FOL ≥ 95%) và hướng dẫn chiến lược tích sản trung bình giá (DCA) qua App DSC Trading.
- **Phạm vi:** Chỉ topic: Vĩ mô

### Bảng tiêu chuẩn phân ngành & Bảng đối sánh 3 chiều chỉ số lợi nhuận
- **ID:** I020
- **Trạng thái:** ARTICLE
- **Thay bởi:** I128
- **Nguồn:** bien-loi-nhuan-gop-la-gi-y-nghia-cua-bien-loi-nhuan-gop-khi-lua-chon-co-phieu
- **Phản hồi từ User:** "Optimize bài biên lợi nhuận gộp là gì"
- **Bản năng:** Khi viết/tối ưu các bài giải thích chỉ số tài chính cơ bản (như Gross Profit Margin) cho F0 (P2), luôn thay thế các ví dụ minh họa giả định nhỏ lẻ bằng bài toán tính toán số liệu thực tế từ BCTC doanh nghiệp niêm yết (như HPG) kết hợp Bảng phân ngành tiêu chuẩn và Bảng đối sánh 3 chiều giữa Lợi nhuận gộp, Lợi nhuận ròng và Lợi nhuận cận biên.
- **Phạm vi:** Chỉ topic: Chỉ số tài chính & BCTC

### Bảng ma trận hậu quả gồng lỗ & Quy tắc cắt lỗ 7-8% vs. Chốt lời 20-25% CANSLIM
- **ID:** I021
- **Trạng thái:** ARTICLE
- **Thay bởi:** I125
- **Nguồn:** khi-nao-nen-ban-co-phieu-5-truong-hop-nha-dau-tu-can-luu-y
- **Phản hồi từ User:** "Optimize bài khi nào nên bán cổ phiếu"
- **Bản năng:** Luôn lồng ghép Bảng ma trận hậu quả gồng lỗ (-5% hòa vốn +5,3% vs -50% hòa vốn +100%) kết hợp Quy tắc cắt lỗ 7-8% & chốt lời 20-25% CANSLIM và Hướng dẫn thời điểm bán trước vs. sau ngày chốt quyền cổ tức khi viết/tối ưu các bài tư vấn thời điểm chốt lời/cắt lỗ cho nhà đầu tư mới (P2).
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật

### Bảng đối sánh Cờ đuôi nheo vs Lá cờ vs Tam giác & Volume Profile 3 giai đoạn
- **ID:** I022
- **Trạng thái:** ARTICLE
- **Thay bởi:** I125
- **Nguồn:** mo-hinh-co-duoi-nheo-la-gi
- **Phản hồi từ User:** "Optimize bài mô hình cờ đuôi nheo"
- **Bản năng:** Luôn lồng ghép Bảng đối sánh Cờ đuôi nheo (Pennant) vs Mô hình lá cờ (Flag) vs Mô hình tam giác (Triangle) kết hợp quy luật biến động thanh khoản Volume Profile 3 giai đoạn (Cột cờ - Thân cờ cạn vol - Breakout bùng nổ 1,5–2 lần MA20) và phương pháp xử lý bẫy breakout giả khi viết/tối ưu các mô hình giá tiếp diễn cho Active Trader (P3).
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật

### Loại bỏ mốc thời gian máy móc và gượng ép
- **ID:** I023
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I109
- **Nguồn:** chi-phi-bien-la-gi
- **Phản hồi từ User:** "phần Tính đến tháng 8/2026 bị gượng ép, bỏ rule đi hoặc cải tiến. Thứ 1 là bây giờ đã tháng 9, thứ 2 là khi đọc cả câu thì thấy phần đó thêm vào ko phù hợp"
- **Bản năng:** Tuyệt đối không chèn máy móc hoặc lặp đi lặp lại cụm từ "Tính đến tháng M/Y," ở đầu câu khi giải thích lý thuyết. Chỉ chèn mốc thời gian (như "năm 2026", "tháng 9/2026") một cách tự nhiên và đúng thời điểm thực tế (hiện tại là tháng 9/2026) khi thực sự dẫn chứng số liệu thống kê biến động thực tế.
- **Phạm vi:** Global

### Tránh mở bài vĩ mô
- **ID:** I024
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I105
- **Nguồn:** Feedback chung
- **Phản hồi từ User:** "Đừng bao giờ mở bài bằng cụm 'Trong kỷ nguyên số ngày nay...'"
- **Bản năng:** Mở bài đi thẳng vào vấn đề cụ thể của người dùng. Không dạo đầu bằng bối cảnh vĩ mô (kỷ nguyên số, thế giới công nghệ, thị trường biến động...).
- **Phạm vi:** Global

### Loại bỏ ngoặc kép nhấn mạnh (Emphatic Quotes)
- **ID:** I025
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I106
- **Nguồn:** adx-la-gi
- **Phản hồi từ User:** "sao tôi thấy đang sử dụng các ngoặc kép. Loại bỏ kiểu trình bày nài, AI quá"
- **Bản năng:** Tuyệt đối không sử dụng dấu ngoặc kép cho các cụm từ ẩn dụ, ví von hoặc thuật ngữ thông thường (ví dụ: đu đỉnh, vùng kiếm tiền). Viết thẳng và trực diện để tránh cảm giác máy móc.
- **Phạm vi:** Global

### Ưu tiên Môi giới 1:1 trong Product Bridge
- **ID:** I026
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I112
- **Nguồn:** adx-la-gi
- **Phản hồi từ User:** "dẫn về dịch vụ môi giới chứng khoán hoặc mở tài khoản chứng khoán DSC thay vì tư vấn số nhé"
- **Bản năng:** Khi viết bài về phân tích kỹ thuật chuyên sâu cho Active Traders, hãy ưu tiên dẫn dắt về dịch vụ Môi giới 1:1 và Mở tài khoản eKYC thay vì các công cụ Tư vấn số tự động, để tạo sự tin cậy và cá nhân hóa.
- **Phạm vi:** Global

### Thỏa mãn Search Intent kỹ thuật trong bài phân tích
- **ID:** I027
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I123
- **Nguồn:** bao-cao-luu-chuyen-tien-te
- **Phản hồi từ User:** (Tham khảo AI Overview)
- **Bản năng:** Đối với các bài viết về báo cáo tài chính hoặc công cụ kỹ thuật, ngoài việc phân tích chiến lược cho nhà đầu tư, cần bổ sung các kiến thức nền tảng như 'Phương pháp lập' hoặc 'Cấu tạo chi tiết'. Điều này giúp thỏa mãn các truy vấn tìm kiếm mang tính học thuật mà không làm loãng ảnh hưởng chiến lược của DSC.
- **Phạm vi:** Global

### Tuân thủ độ dài đoạn và cấu trúc Heading chuẩn
- **ID:** I028
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** phi-giao-dich-chung-khoan
- **Phản hồi từ User:** QA script `count_words.py` báo sai lệch khi dùng sai thẻ Heading.
- **Bản năng:** Khi chuyển từ Outline sang Draft, luôn sử dụng Markdown Headings tiêu chuẩn (`#`, `##`, `###`) thay vì giữ nguyên các chuỗi định dạng của Outline (`### H2:`). Điều này đảm bảo Script QA hoạt động chính xác khi cắt block nội dung.
- **Phạm vi:** Global

### Trình bày trực quan bằng List/Table
- **ID:** I029
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I115
- **Nguồn:** phi-luu-ky-chung-khoan
- **Phản hồi từ User:** "trình bày bài viết linh hoạt giữa list, table thay vì chỉ có text thôi"
- **Bản năng:** Khi trình bày các số liệu so sánh, mức phí, hoặc quy trình từng bước, ưu tiên sử dụng Bảng (Table) hoặc Danh sách (Bullet list) để bài viết trực quan, dễ đọc, tránh các đoạn văn bản (text) quá dài.
- **Phạm vi:** Global

### Bắt buộc có Sapo và Link CTA
- **ID:** I030
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I105
- **Nguồn:** phi-luu-ky-chung-khoan
- **Phản hồi từ User:** "chưa thấy dẫn về mở tài khoản", "chưa thấy có phần sapo bài viết"
- **Bản năng:** Mọi bài viết phải có đoạn Sapo (Mở bài) ngay dưới tiêu đề H1. Trong phần Kết bài (CTA), phải luôn chèn link trực tiếp đến trang mở tài khoản chứng khoán hoặc bài hướng dẫn tương ứng, không được để lời kêu gọi suông.
- **Phạm vi:** Global

### Sử dụng từ Chiến lược thay cho Thủ thuật hoặc Chiêu trò
- **ID:** I031
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I106
- **Nguồn:** bollinger-bands-la-gi
- **Phản hồi từ User:** "dùng từ chiến lược hơn từ thủ thuật", "từ chiêu trò nghe không chuyên nghiệp", "kinh điển giống văn nói"
- **Bản năng:** Khi phân tích các phương pháp giao dịch, chỉ báo kỹ thuật hoặc các thủ pháp tài chính chuyên sâu cho Active Trader (P3), luôn sử dụng từ "chiến lược" hoặc "phương pháp" thay cho "thủ thuật" hay "chiêu trò". Điều này đảm bảo giọng văn mang tính chuyên nghiệp cao cấp, chuẩn mực ngôn từ của một định chế tài chính (Investment Bank tone) đồng hành cùng nhà đầu tư.
- **Phạm vi:** Global

### Tránh sử dụng thuật ngữ "cơ chế truyền dẫn"
- **ID:** I032
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I106
- **Nguồn:** cac-chi-so-phan-tich-bao-cao-tai-chinh
- **Phản hồi từ User:** "'cơ chế truyền dẫn' không phải từ ngữ phù hợp trong văn viết, đặc biệt là lĩnh vực tài chính. Viết là Tác động là được rồi. Không cần cơ chế đâu"
- **Bản năng:** Không sử dụng cụm từ "cơ chế truyền dẫn" trong các bài viết tài chính hay kinh tế vĩ mô. Hãy thay thế hoàn toàn bằng từ "tác động" để đảm bảo câu văn ngắn gọn, dễ hiểu, phù hợp với văn phong chuyên nghiệp và tự nhiên của nhà đầu tư.
- **Phạm vi:** Global

### Loại bỏ công thức LaTeX và tối ưu đếm câu list-item
- **ID:** I033
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** chia-tach-co-phieu
- **Phản hồi từ User:** "phần công thức lên docs sẽ bị lỗi. Sửa lại" + "word count / sentence length check"
- **Bản năng:** Tuyệt đối không sử dụng định dạng LaTeX `$$` hay `$` cho các công thức tính toán tài chính vì dễ gây lỗi hiển thị trên CMS. Thay thế bằng công thức in đậm chuẩn trực quan (ví dụ: `**P' = P / (1 + a)**`). Đối với các danh sách (list-item) hoặc câu định nghĩa bắt đầu bằng cụm in đậm có dấu hai chấm `: `, hãy thay thế `:` bằng dấu chấm `. ` để ngăn script QA đếm gộp thành câu dài quá 25 từ, đồng thời giúp câu văn gãy gọn hơn.
- **Phạm vi:** Global

### Ràng buộc từ khóa Sapo, Bridge hỗ trợ tư vấn và Miễn trừ trách nhiệm
- **ID:** I034
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I105
- **Nguồn:** co-nen-mua-co-phieu-las
- **Phản hồi từ User:** "sapo chưa chứa từ khóa 'có nên mua cổ phiếu LAS không'. Phần dẫn về DSC ko có nói về hỗ trợ tư vấn đầu tư. Chưa có phần miễn trừ trách nhiệm. viết vào thành 1 điểm liệt kê thay vì tách riêng ra thành tip"
- **Bản năng:**
  1. Luôn bảo đảm đoạn Sapo đầu bài viết chứa từ khóa chính xác dạng truy vấn (như "có nên mua cổ phiếu LAS không") một cách tự nhiên.
  2. Phần dẫn dắt dịch vụ DSC (Product Bridge) bắt buộc phải tích hợp rõ ràng thông tin "hỗ trợ tư vấn đầu tư" từ chuyên gia Môi giới 1:1. Đồng thời, nên gộp thông tin này thành một điểm liệt kê (bullet point) đồng nhất thay vì tách riêng thành hộp Tip để liền mạch với hệ sinh thái.
  3. Bắt buộc chèn hộp cảnh báo "Tuyên bố miễn trừ trách nhiệm" rõ ràng ở phần đánh giá hoặc cuối bài viết để đảm bảo tính khách quan pháp lý.
- **Phạm vi:** Global

### Tách biệt hoàn toàn visual elements để pass check đoạn văn liên tiếp
- **ID:** I035
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** co-nen-mua-co-phieu-novaland
- **Phản hồi từ User:** "consecutive paragraphs check"
- **Bản năng:** Trong bài viết, các danh sách liệt kê (bullet points, numbered lists) hoặc bảng biểu khi đứng ngay sau một đoạn giới thiệu ngắn (ví dụ: "Các mốc tiến độ bao gồm:") phải được ngăn cách bằng 2 dòng trống (`\n\n`) thay vi viết liền kề. Việc này ngăn chặn script QA tự động đếm gộp đoạn văn và danh sách thành một khối không trực quan dài dòng, đồng thời tạo nhịp đọc thông thoáng cho người dùng.
- **Phạm vi:** Global

### Ràng buộc về năng lực sản phẩm thực tế của thương hiệu
- **ID:** I036
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I111
- **Nguồn:** chung-khoan-phai-sinh-la-gi
- **Phản hồi từ User:** "DSC k có trading phái sinh nên k dẫn về mở tk giao dịch phái sinh được"
- **Bản năng:** Trước khi viết bất kỳ Product Bridge hay ví dụ thực tiễn nào liên quan đến sản phẩm tài chính, luôn kiểm tra chéo năng lực sản phẩm và dịch vụ thực tế của định chế. Nếu định chế không cung cấp sản phẩm đó (ví dụ: DSC không hỗ trợ giao dịch phái sinh), tuyệt đối không kêu gọi mở tài khoản phái sinh hay đề cập tỷ lệ ký quỹ tại đây. Hãy định hướng người dùng rèn luyện kiến thức và xây dựng nền tảng vững chắc thông qua sản phẩm cơ sở (như cổ phiếu cơ sở), đồng thời sử dụng các dịch vụ hỗ trợ của định chế (như Môi giới 1:1, mở tài khoản eKYC cổ phiếu) để tích lũy kinh nghiệm.
- **Phạm vi:** Global

### Thống nhất thời gian đăng ký eKYC DSC và loại bỏ từ dạng xương máu
- **ID:** I037
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I106
- **Nguồn:** cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau
- **Phản hồi từ User:** "bỏ từ dạng xương máu đi. ekyc chỗ thì 3 phút, 5 phút giờ lại 30 giây. thống nhất lại"
- **Bản năng:**
  1. Tuyệt đối không sử dụng từ ngữ giật gân, thiếu chuyên nghiệp như "xương máu" khi viết bài tư vấn đầu tư. Thay thế bằng các cụm từ trung tính, sang trọng và chuẩn mực như "quý báu", "sống còn", "cốt lõi".
  2. Thống nhất thời gian mở tài khoản định danh điện tử eKYC tại DSC là "3 phút" trên toàn hệ thống bài viết để đảm bảo tính đồng bộ dữ liệu thương hiệu và độ tin cậy.
- **Phạm vi:** Global

### Tải cấu trúc đoạn văn theo ngữ nghĩa thay vì chia câu cơ học
- **ID:** I038
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I115
- **Nguồn:** quy-dong-la-gi
- **Phản hồi từ User:** "việc ngắt của bạn đang ko theo nội dung. sau cái đầu tiên ko ngắt mà cái thứ 2 lại ngắt"
- **Bản năng:** Khi tối ưu cấu trúc đoạn văn để đáp ứng chuẩn Mobile-First (tối đa 3 câu/đoạn, câu dưới 25 từ), phải gộp và ngắt đoạn dựa trên sự liên kết ngữ nghĩa (semantic grouping) của nội dung thay vì bẻ câu hay gộp câu một cách máy móc. Các câu thuộc cùng một khía cạnh giải thích phải nằm chung trong một đoạn (tối đa 3 câu) để đảm bảo mạch văn trôi chảy và tự nhiên.
- **Phạm vi:** Global

### Trực quan hóa danh sách để tối ưu độ cô đọng
- **ID:** I039
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I115
- **Nguồn:** quy-tuong-ho-la-gi
- **Phản hồi từ User:** "bài viết đang toàn text, dài. cô đọng hơn"
- **Bản năng:** Đối với các bài viết tài chính cho F0, tránh lạm dụng các khối văn bản lớn (text-heavy). Hãy cấu trúc lại thông tin thành các danh sách gạch đầu dòng có tiêu đề in đậm làm mốc phân cấp để tăng tính cô đọng và scannable. Các câu chuyện minh họa thực tế nên được trình bày thành các điểm dữ liệu ngắn gọn thay vì viết thành đoạn văn miêu tả dài dòng.
- **Phạm vi:** Global

### Hợp nhất các danh sách liên tiếp để tránh đứt đoạn mạch đọc
- **ID:** I040
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I115
- **Nguồn:** quy-trai-phieu-la-gi
- **Phản hồi từ User:** "Tham khảo nội dung AI overview trên để tối ưu" (Đặc điểm nổi bật + Ai nên đầu tư)
- **Bản năng:** Khi gặp các nội dung phân loại liệt kê liên tiếp (như Đặc điểm nổi bật và Đối tượng phù hợp), tránh thiết lập các khối danh sách (bullet list) đứng kề nhau. Hãy hợp nhất chúng thành một danh sách kết hợp hoặc viết thêm một đoạn văn xuôi ngắn ở giữa làm cầu nối dẫn dắt để mạch đọc tự nhiên và pass QA.
- **Phạm vi:** Global

---

### Tránh sử dụng callout box không tương thích
- **ID:** I041
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** dcf-la-gi
- **Phản hồi từ User:** "các phần quote kiểu > [!NOTE] ko hoạt động trên website tôi nên bỏ đi"
- **Bản năng:** Không sử dụng cú pháp callout mở rộng của Markdown (như `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`) vì chúng không tương thích hiển thị trên một số CMS. Hãy thay thế bằng cú pháp trích dẫn chuẩn của Markdown kết hợp tiêu đề in đậm (ví dụ: `> **Lưu ý:**` hoặc `> **Mẹo:**`).
- **Phạm vi:** Global

### Cách đặt dấu câu trong list-item/FAQ để tối ưu tách câu
- **ID:** I042
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** chi-so-gia-tieu-dung-cpi-la-gi-va-moi-quan-he-voi-thi-truong-chung-khoan
- **Phản hồi từ User:** Lỗi "Sentence too long" do script QA gộp câu trong danh sách hoặc FAQ.
- **Bản năng:** Khi viết câu hỏi FAQ hoặc list-item bắt đầu bằng thẻ in đậm `**`, hãy đặt dấu chấm `. ` hoặc dấu chấm hỏi `? ` ngay bên ngoài thẻ in đậm (ví dụ: `* **Nhóm hàng hóa tỷ trọng lớn nhất**. Hàng ăn...` thay vì `* **Nhóm hàng hóa tỷ trọng lớn nhất?** Hàng ăn...`). Điều này giúp regex phân tách câu của script QA nhận diện dấu câu chính xác và ngăn chặn hiện tượng gộp đầu dòng thành câu dài quá 25 từ.
- **Phạm vi:** Global

---

### Tách biệt list-item chứa nhiều câu và loại bỏ từ trigger "rõ ràng"
- **ID:** I043
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I106
- **Nguồn:** loi-nhuan-rong-va-loi-nhuan-sau-thue
- **Phản hồi từ User:** Lỗi "Paragraph too many sentences" do script QA gộp các list item và cảnh báo từ trigger "rõ ràng".
- **Bản năng:**
  1. Với các danh sách gạch đầu dòng (list-item) mà mỗi dòng chứa từ 2 câu trở lên, luôn chèn một dòng trống ngăn cách giữa các dòng. Điều này giúp ngăn script QA tự động gộp các câu thành một đoạn văn quá dài (> 3 câu), đồng thời làm thoáng bố cục trên giao diện di động.
  2. Tuyệt đối không sử dụng từ trigger rỗng nghĩa như "rõ ràng" (ví dụ: "phân biệt rõ ràng") để đảm bảo văn phong chuyên nghiệp và khách quan.
- **Phạm vi:** Global

---

### Tối ưu hóa cầu nối sản phẩm chuyển dịch dòng vốn và trực quan hóa các yếu tố vĩ mô
- **ID:** I044
- **Trạng thái:** ARTICLE
- **Thay bởi:** I112
- **Nguồn:** cach-dau-tu-vang
- **Phản hồi từ User:** "Những yếu tố ảnh hưởng đến sự biến động của giá vàng viết theo dạng list để dễ skim ý chính. Phần chuyển từ đầu tư vàng sang đầu tư chứng khoán DSC chưa được tối ưu"
- **Bản năng:**
  1. Khi viết các yếu tố tác động vĩ mô (ví dụ: yếu tố tác động đến giá vàng, giá dầu), luôn trình bày dưới dạng danh sách gạch đầu dòng có in đậm tiêu đề để tăng tính trực quan và dễ skim ý chính cho người đọc.
  2. Phần dẫn dắt chuyển dịch dòng tiền (Product Bridge) từ các kênh phòng thủ (như vàng, gửi tiết kiệm) sang kênh cổ phiếu tăng trưởng/chứng chỉ quỹ của DSC phải được lập luận bằng logic tài chính (rủi ro mua đuổi vùng đỉnh, chênh lệch spread rộng của vàng vật chất, tính chất không sinh dòng tiền thụ động của vàng so với lợi thế cổ tức tiền mặt của cổ phiếu) để tạo động lực chuyển dịch tài sản một cách tự nhiên và thuyết phục.
- **Phạm vi:** Chỉ topic: Vĩ mô
---

### Bỏ qua tạo ảnh fallback khối vuông khi gặp lỗi Quota
- **ID:** I045
- **Trạng thái:** ACTIVE
- **Nguồn:** chi-so-roa-la-gi-y-nghia-va-cach-su-dung
- **Phản hồi từ User:** "khi bị quota thì tôi muốn ko tạo ảnh nữa"
- **Bản năng:** Khi công cụ sinh ảnh AI (`generate_image`) bị báo lỗi Quota (429 RESOURCE_EXHAUSTED), tuyệt đối không sinh các hình ảnh fallback khối vuông 3D bằng script Python PIL. Hãy bỏ qua việc tạo ảnh mới, bảo toàn 100% hình ảnh gốc của bài viết và trình bày bài viết chuẩn văn bản/bảng biểu trực quan.
- **Phạm vi:** Global

---

### Tránh sử dụng dấu ngoặc kép trong YAML front matter
- **ID:** I046
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** co-tien-nen-dau-tu-bac
- **Phản hồi từ User:** Lỗi Emphatic Quotes từ script QA do phát hiện dấu ngoặc kép bao quanh chuỗi ký tự trong YAML front matter.
- **Bản năng:** Khi định nghĩa các trường văn bản trong YAML front matter (như Featured_Snippet, Anti_AI_Flags), không bao quanh chuỗi bằng dấu ngoặc kép kép (`""`). Hãy viết trực tiếp chuỗi không có dấu ngoặc kép hoặc dùng dấu ngoặc đơn (`''`) để tránh trigger nhầm bộ quét Emphatic Quotes của Quality Guardian.
- **Phạm vi:** Global

---

### Đặt dấu câu FAQ ngoài thẻ bold
- **ID:** I047
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** dau-tu-vang-nen-mua-loai-na
- **Phản hồi từ User:** QA script báo câu quá dài ở FAQ vì script đọc text bên trong bold tag cộng với dấu hỏi cuối là một câu liên tục.
- **Bản năng:** Với câu hỏi FAQ dạng `**Câu hỏi?**`, phải di chuyển dấu `?` ra ngoài thẻ bold: `**Câu hỏi**?`. Điều này giúp QA script tách câu đúng vị trí và không tính phần bold label vào độ dài câu trả lời.
- **Phạm vi:** Global

---

### Sử dụng số liệu vĩ mô thực tế tại Việt Nam
- **ID:** I048
- **Trạng thái:** ARTICLE
- **Thay bởi:** I110
- **Nguồn:** he-so-icor-la-gi
- **Phản hồi từ User:** Phê duyệt đề xuất đưa số liệu thực tế Việt Nam thay cho số liệu giả định chung chung.
- **Bản năng:** Đối với các bài viết phân tích vĩ mô, bắt buộc phải sử dụng các số liệu thực tế đã được công bố của Việt Nam trong các giai đoạn gần nhất (ví dụ: giai đoạn phục hồi 2021-2025, mục tiêu 2026) thay vì sử dụng các số liệu giả định chung chung. Điều này nhằm tối đa hóa độ tin cậy và chiều sâu phân tích của DSC.
- **Phạm vi:** Chỉ topic: Vĩ mô

---

### Bảng so sánh định nghĩa & Chi tiết hóa Product Bridge
- **ID:** I049
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I112
- **Nguồn:** von-hoa-thi-truong-la-gi
- **Phản hồi từ User:** "phần content về DSC ngắn quá, phần Sự khác biệt giữa vốn hóa thị trường và vốn chủ sở hữu có thể tạo dạng bảng", "nhiều phần ngắn thì ko cần phải tách ra thành H3 đâu, viết thành list luôn"
- **Bản năng:**
  1. Khi viết các mục phân biệt hoặc đối chiếu giữa hai hay nhiều khái niệm tài chính quan trọng (ví dụ: Vốn chủ sở hữu vs Vốn hóa thị trường), hãy chuyển đổi cấu trúc dạng văn xuôi thành bảng so sánh đối chuẩn trực quan (Table) để tối ưu khả năng đọc lướt (scannability) cho người đọc di động.
  2. Phần giới thiệu giải pháp/sản phẩm của DSC (Product Bridge) cần được chi tiết hóa đầy đủ, tránh viết chung chung. Hãy giới thiệu cụ thể các dịch vụ thực tế như: tính năng phân loại vốn hóa/cảnh báo giá trên App DSC Trading, quy trình mở tài khoản eKYC 3 phút, dịch vụ Môi giới 1:1 hỗ trợ cá nhân hóa danh mục, và chính sách phí giao dịch ưu đãi chỉ từ 0.1% cùng báo cáo phân tích miễn phí.
  3. Đối với các phần giới thiệu dịch vụ ngắn hoặc phần thông tin phụ có độ dài ít câu (2-3 câu mỗi phần), không cần chia nhỏ bằng tiêu đề H3 mà hãy gộp chung thành một danh sách gạch đầu dòng (bulleted list) có in đậm tiêu đề ở đầu mỗi bullet để tăng tính liền mạch và gọn gàng.
- **Phạm vi:** Global

---

### Tuyệt đối không dùng lưu đồ Code Block (ASCII Art) cho CMS
- **ID:** I050
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I115
- **Nguồn:** quan-tri-rui-ro-la-gi
- **Phản hồi từ User:** "phần lưu đồ trong CMS ko hiển thị được. Cập nhật lại skill liên quan đến internal link"
- **Bản năng:** CMS website không hỗ trợ tốt hiển thị các khối code block lưu đồ/sơ đồ ASCII (`+---+`, `[Bước 1] -> [Bước 2]`, cây phân nhánh), gây vỡ layout và không tối ưu trên di động. Bắt buộc chuyển đổi toàn bộ lưu đồ, quy trình và phân loại thành Bảng Markdown (Table), Danh sách đánh số từng bước (Ordered List), hoặc khối trích dẫn (Blockquote). Công thức toán học biểu diễn bằng chữ in đậm thông thường thay vì khối LaTeX.
- **Phạm vi:** Global

---

### Xác thực Internal Link bằng Sitemap Live của DSC
- **ID:** I051
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I117
- **Nguồn:** quan-tri-rui-ro-la-gi
- **Phản hồi từ User:** "phần gợi ý internal link tôi muốn cào dữ liệu sitemap (https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml) để gợi ý chính xác hơn"
- **Bản năng:** Khi gợi ý hoặc gắn internal link, bắt buộc phải cào dữ liệu trực tiếp từ sitemap knowledge của DSC (`https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml`) để lấy danh sách URL live thực tế. Tuyệt đối không tự suy đoán slug hoặc dùng đường dẫn tương đối không kiểm chứng. Chọn anchor text chứa từ khóa ngữ cảnh tự nhiên nhất để tối ưu sức mạnh liên kết nội bộ.
- **Phạm vi:** Global

---

### Bắt buộc có Internal Link dẫn về trang Mở tài khoản chứng khoán DSC
- **ID:** I052
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I113
- **Nguồn:** quan-tri-rui-ro-la-gi
- **Phản hồi từ User:** "trang này cơ mà: https://www.dsc.com.vn/mo-tai-khoan trang bạn đề xuất target key 'cách mở tài khoản chứng khoán' cơ"
- **Bản năng:** 100% mọi bài viết trong toàn bộ pipeline (Drafting, Optimize, Write, Link) bắt buộc phải gắn ít nhất 01 link chuyển đổi dẫn trực tiếp về Landing Page Mở tài khoản chứng khoán chính thức của DSC: `https://www.dsc.com.vn/mo-tai-khoan` (không nhầm với bài blog chia sẻ kiến thức có target key "cách mở tài khoản chứng khoán" tại `/kien-thuc/cach-mo-tai-khoan-chung-khoan`). Vị trí đặt: Phần Product Bridge hoặc đoạn Kết luận (Call to Action). Anchor text tự nhiên: `mở tài khoản chứng khoán`, `mở tài khoản chứng khoán online`, `mở tài khoản trực tuyến eKYC tại DSC`, `mở tài khoản eKYC tại DSC`.
- **Phạm vi:** Global

---

### Tiêu đề SEO (Title) Bắt buộc Tối đa 59 Ký tự
- **ID:** I053
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I107
- **Nguồn:** thao-tung-thi-truong-chung-khoan-la-gi
- **Phản hồi từ User:** "title đề xuất quá 60 ký tự. check lại và cập nhật skill liên quan"
- **Bản năng:** Mọi Tiêu đề SEO (SEO Title / Title đề xuất trong Proposal / Outline Title) BẮT BUỘC có độ dài tối đa 59 ký tự (bao gồm cả khoảng trắng và dấu câu) và chứa từ khóa chính (Target Keyword) ngay đầu hoặc giữa tiêu đề. Điều này đảm bảo tiêu đề không bị Google cắt bớt (truncate) trên trang kết quả tìm kiếm (SERP), tối ưu tỷ lệ click (CTR). Luôn đếm ký tự chính xác trước khi xuất báo cáo Proposal hoặc bài viết.
- **Phạm vi:** Global

---

### Bắt buộc dùng Đường dẫn Tuyệt đối (Absolute URLs & Absolute Paths)
- **ID:** I054
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I117
- **Nguồn:** thao-tung-thi-truong-chung-khoan-la-gi
- **Phản hồi từ User:** "dùng absolute path nhé"
- **Bản năng:**
  1. **Internal Links trong bài viết:** 100% internal links và conversion links trong bài viết SEO bắt buộc dùng URL tuyệt đối đầy đủ (`https://www.dsc.com.vn/kien-thuc/[slug]` hoặc `https://www.dsc.com.vn/mo-tai-khoan`), tuyệt đối không dùng relative path dạng `/kien-thuc/...` hay `/mo-tai-khoan`.
  2. **File Paths khi tương tác:** Luôn dẫn link và tham chiếu file bằng absolute path đầy đủ trong workspace/hệ thống.
- **Phạm vi:** Global

---

### Xác thực Internal Link bằng Sitemap Live của DSC (Bắt buộc)
- **ID:** I055
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I117
- **Nguồn:** Global feedback (duong-trendline-la-gi)
- **Phản hồi từ User:** "có 1 vấn đề là internal link đang ko quét sitemap mà chỉ lấy các bài viết ở folder 4-content"
- **Bản năng:** Khi tạo hoặc tối ưu bài viết, tuyệt đối không dùng link file cục bộ (`file:///...` hoặc `.md`) làm internal link. Phải đọc trực tiếp sitemap live `https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml` để lấy URL tuyệt đối của bài viết đích. Đồng thời, đối chiếu kỹ slug của file cục bộ với sitemap để tránh sai lệch cấu trúc URL (ví dụ: file `Final-rsi-la-gi.md` trên sitemap live có URL là `https://www.dsc.com.vn/kien-thuc/chi-so-rsi-la-gi`, file `Final-chi-bao-ky-thuat-la-gi.md` có URL là `https://www.dsc.com.vn/kien-thuc/chi-bao-ky-thuat`).
- **Phạm vi:** Global

---

### Viết đoạn văn ngữ cảnh tự nhiên cho Internal Link (Không dùng "Xem thêm")
- **ID:** I056
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I117
- **Nguồn:** bien-do-giao-dong-gia-co-phieu-la-gi
- **Phản hồi từ User:** "phần >> xem thêm có thể viết đoạn ngữ nghĩa để internal link"
- **Bản năng:** Thay vì sử dụng các khối liên kết thô cứng ngắt mạch đọc của người dùng dạng `*>> Xem thêm:* [***Tên bài viết***](URL)`, hãy chuyển đổi và tích hợp liên kết nội bộ (internal link) một cách tự nhiên vào một câu hoặc đoạn văn có đầy đủ ngữ cảnh ngữ nghĩa liên quan. Điều này vừa giúp tối ưu trải nghiệm đọc (UX) vừa nâng cao hiệu quả truyền tải dòng chảy tin cậy (Link Juice) cho SEO.
- **Phạm vi:** Global

---

### Định dạng nhãn in đậm trong danh sách (Sử dụng dấu hai chấm)
- **ID:** I057
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** bien-do-giao-dong-gia-co-phieu-la-gi
- **Phản hồi từ User:** "phần list thì dùng : thay vì . nhé. Ví dụ Biên độ đối với Chứng quyền (CW). phải là Biên độ đối với Chứng quyền (CW):"
- **Bản năng:** Khi trình bày các nhãn in đậm ở đầu các mục danh sách (bullet points/ordered lists), bắt buộc sử dụng dấu hai chấm `:` thay vì dấu chấm `.` làm ký tự phân tách giữa nhãn in đậm và nội dung câu tiếp theo (Ví dụ: `* **Nhãn**: Nội dung`).
- **Phạm vi:** Global

---

### Sử dụng dấu chấm ở cuối câu dẫn dắt danh sách liền kề
- **ID:** I058
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** phan-tich-nganh-la-gi
- **Phản hồi từ User:** QA script cảnh báo lỗi câu dài do gộp câu dẫn dắt danh sách với mục list-item đầu tiên khi dùng dấu hai chấm.
- **Bản năng:** Khi viết câu dẫn dắt vào danh sách (bullet points/ordered lists) nằm liền kề (không có dòng trống phân cách), hãy kết thúc câu dẫn dắt bằng dấu chấm `.` thay vì dấu hai chấm `:` để script QA nhận diện và phân tách câu giới thiệu với mục đầu tiên của danh sách, tránh lỗi đếm gộp câu dài quá giới hạn.
- **Phạm vi:** Global

---

### Bảng so sánh đa chiều các loại giá trị cổ phiếu
- **ID:** I059
- **Trạng thái:** ARTICLE
- **Thay bởi:** I128
- **Nguồn:** thi-gia-co-phieu-la-gi
- **Phản hồi từ User:** "không" (Người dùng duyệt bản nháp tối ưu có bảng so sánh chi tiết và phân biệt rõ ràng các khái niệm)
- **Bản năng:** Đối với các bài viết giải thích khái niệm dễ gây nhầm lẫn (như Thị giá cổ phiếu - P2/F0), bắt buộc phải tích hợp một Bảng đối sánh đa chiều (Mệnh giá vs Giá trị sổ sách vs Thị giá) để triệt tiêu hoàn toàn sự mơ hồ. Hãy luôn duy trì 100% liên kết tuyệt đối khớp với sitemap live của DSC và đặt dấu hai chấm `:` ở cuối nhãn in đậm trong danh sách để tuân thủ định dạng.
- **Phạm vi:** Chỉ topic: Chỉ số tài chính & BCTC

---

### Phân nhóm H2 cho bài viết từ điển/glossary và Đặt dấu câu ngoài thẻ bold
- **ID:** I060
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I115
- **Nguồn:** cac-thuat-ngu-trong-chung-khoan
- **Phản hồi từ User:** "ko" (Người dùng duyệt bản nháp tối ưu đã phân nhóm chuyên đề H2 và chỉnh sửa dấu câu FAQ ngoài bold tag để pass QA)
- **Bản năng:** Đối với các bài viết glossary dạng tổng hợp thuật ngữ, bắt buộc phải chia nhỏ danh sách phẳng thành 5 nhóm chuyên đề H2 rõ ràng để tăng scannability. Các câu hỏi FAQ hoặc list-item in đậm kết thúc bằng dấu chấm hỏi `?` hoặc dấu chấm `.` phải đặt dấu câu đó ra ngoài thẻ bold `**` (ví dụ: `**Câu hỏi**?`) để script QA tách câu chính xác và không đếm gộp nhãn in đậm vào câu trả lời gây lỗi câu quá dài (>30 từ).
- **Phạm vi:** Global

---

### Bảng phân nhóm LLR và Loại bỏ LaTeX
- **ID:** I061
- **Trạng thái:** ARTICLE
- **Thay bởi:** I128
- **Nguồn:** ty-le-bao-phu-no-xau
- **Phản hồi từ User:** "ko" (Người dùng duyệt bản nháp đã tối ưu hóa bảng phân nhóm LLR, loại bỏ LaTeX, cập nhật số liệu 2026 và tích hợp product bridge)
- **Bản năng:** Đối với các bài viết về chỉ số tài chính chuyên sâu (như Tỷ lệ bao phủ nợ xấu - LLR), bắt buộc phải có Bảng phân nhóm trực quan các ngưỡng an toàn của chỉ số và ý nghĩa đầu tư thực tế cho từng nhóm. Không sử dụng ký tự LaTeX (như $ hoặc $$) cho công thức tính toán mà hãy sử dụng định dạng chữ in đậm thông thường để tránh lỗi hiển thị trên CMS. Tích hợp phân tích liên kết chỉ số LLR với các chỉ số chất lượng tài sản khác như NPL, CASA, ROA để tăng độ sâu phân tích.
- **Phạm vi:** Chỉ topic: Chỉ số tài chính & BCTC

---

### Bản chất NAV và Đính chính Thuật ngữ Lãi suất CCQ
- **ID:** I062
- **Trạng thái:** ARTICLE
- **Thay bởi:** I130
- **Nguồn:** lai-suat-chung-chi-quy
- **Phản hồi từ User:** "ko"
- **Bản năng:** Đối với các bài viết về chứng chỉ quỹ nhắm đến tệp Người tiết kiệm thận trọng (P1), phải chủ động đính chính thuật ngữ "lãi suất" (vốn là cách gọi quen thuộc nhưng không đúng bản chất của chứng chỉ quỹ) và chuyển đổi sang hiệu suất sinh lời hoặc sự tăng trưởng giá trị tài sản ròng (NAV) để đảm bảo tính chính xác và uy tín chuyên môn. Luôn cung cấp bảng so sánh trực quan giữa CCQ và gửi tiết kiệm ngân hàng, kết hợp bảng mô phỏng lãi kép định kỳ (ví dụ: tích lũy định kỳ 2 triệu đồng/tháng sau 1, 3, 5, 10 năm) để thuyết phục người đọc phân bổ dòng tiền gửi tiết kiệm sang chứng chỉ quỹ hoặc tài khoản chứng khoán DSC.
- **Phạm vi:** Chỉ topic: Tài chính cá nhân

---

### Định dạng số thập phân bằng dấu phẩy và Hướng dẫn thực hành cho Active Trader (P3)
- **ID:** I063
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** backtest-la-gi
- **Phản hồi từ User:** "không"
- **Bản năng:**
  1. **Định dạng số thập phân tiếng Việt:** Bắt buộc sử dụng dấu phẩy `,` thay vì dấu chấm `.` cho số thập phân khi viết bài tiếng Việt (ví dụ: `T+1,5` thay vì `T+1.5`, phí `0,1%` thay vì `0.1%`, margin `13,5%` thay vì `13.5%`). Điều này vừa giúp tuân thủ chính xác quy tắc chính tả tiếng Việt của brand, vừa tránh lỗi QA script nhận diện nhầm dấu chấm thập phân là dấu chấm hết câu gây tách câu sai lệch.
  2. **Tăng tính thực chiến P3:** Đối với các bài phân tích kỹ thuật và chiến lược trading nhắm đến Active Trader (P3), luôn cung cấp hướng dẫn thực hành từng bước chi tiết (ví dụ: các bước sử dụng Bar Replay trên TradingView, code mẫu Pine Script v5) và phân tích sâu các sai lầm/bẫy tâm lý giao dịch (Overfitting, Survivorship Bias) để tối ưu E-E-A-T.
- **Phạm vi:** Global

---

### Tiết giảm mốc thời gian động và bổ sung quy định NFC/CCCD
- **ID:** I064
- **Trạng thái:** ARTICLE
- **Thay bởi:** I109
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "ko phải phần nào cũng viết "Tính đến tháng 8/2026,", ngoài ra có thêm fact, thông tin báo chí gì mới liên quan có thể cho vào bài viết ko?"
- **Bản năng:**
  1. Tránh lạm dụng mốc thời gian động (ví dụ: "Tính đến tháng 8/2026,") ở đầu mọi tiêu đề H2 hoặc phần quy định pháp luật chung. Chỉ dùng mốc thời gian động ở những câu thực sự chứa số liệu/thống kê biến động (như biểu phí, số lượng tài khoản, lãi suất). Đa dạng hóa cách viết tự nhiên (ví dụ: "Theo quy chế hiện hành...", "Thống kê nội bộ tháng 8/2026 cho thấy...", "Theo thông tin dịch vụ cập nhật tháng 8/2026...").
  2. Cập nhật các dữ liệu thực tế và quy chế mới nhất của cơ quan quản lý (như quy định bắt buộc của UBCKNN về quét NFC trên thẻ CCCD gắn chip để đồng bộ thông tin với Cơ sở dữ liệu quốc gia về dân cư) làm luận cứ tăng tính E-E-A-T và thời sự cho bài viết hướng dẫn mở tài khoản.
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)

### Phân tích chỉ số tài chính theo ngành và xử lý lỗi ngoặc kép "Số cuối kỳ"
- **ID:** I065
- **Trạng thái:** ARTICLE
- **Thay bởi:** I128
- **Nguồn:** dar-la-gi
- **Phản hồi từ User:** "không"
- **Bản năng:** Khi phân tích các chỉ số cơ cấu tài chính (như DAR), luôn đính kèm so sánh định lượng đặc thù từng nhóm ngành cụ thể (như Ngân hàng 88%-92%, Bất động sản 55%-75%, Công nghệ 20%-35%). Tránh dùng dấu ngoặc kép bọc quanh tên các chỉ mục báo cáo tài chính (ví dụ: dùng "cột Số cuối kỳ" thay vì "cột 'Số cuối kỳ'") để tránh trigger lỗi emphatic quotes của QA script.
- **Phạm vi:** Chỉ topic: Chỉ số tài chính & BCTC

### Không sử dụng đường kẻ ngang giữa các phần/heading
- **ID:** I066
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** take-profit-la-gi
- **Phản hồi từ User:** "bỏ "---" giữa các heading"
- **Bản năng:** Tuyệt đối không sử dụng ký tự đường kẻ ngang (`---`) ở giữa các heading hoặc giữa các phần trong nội dung bài viết (trừ phần YAML front matter ở đầu trang nếu có). Giữa các phần chỉ dùng đúng một dòng trống để phân cách.
- **Phạm vi:** Global

---

### Phân tách câu hỏi và câu trả lời trong mục FAQs
- **ID:** I067
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I116
- **Nguồn:** ty-le-ky-quy
- **Phản hồi từ User:** Lỗi gộp câu tại mục FAQs do script QA đếm gộp câu hỏi và câu trả lời thành câu dài.
- **Bản năng:** Phân tách câu hỏi và câu trả lời trong mục FAQs bằng dòng trống để script QA không đếm gộp thành câu dài.
- **Phạm vi:** Global

---

### Đối soát Internal Link với Sitemap Live từ nguồn chính thức
- **ID:** I068
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I117
- **Nguồn:** chi-so-ps
- **Phản hồi từ User:** "các internal link đang bị sai. Bạn có đúng là lấy tư sitemap DSC ko?"
- **Bản năng:** 100% URL internal link và conversion link phải dùng Absolute URL đầy đủ khớp chính xác từng ký tự với sitemap_knowledge.xml (hoặc sitemap-cache.json). Tuyệt đối không tự suy đoán slug ngắn hơn và không tự ý chèn dấu / ở cuối URL khi sitemap không có.
- **Phạm vi:** Global

---

### Phân tích liên thị trường và tác động chuỗi cung ứng cho chỉ số chứng khoán quốc tế
- **ID:** I069
- **Trạng thái:** ARTICLE
- **Thay bởi:** I126
- **Nguồn:** chi-so-kospi
- **Phản hồi từ User:** Phê duyệt bài viết Chỉ số Kospi thành công.
- **Bản năng:** Khi phân tích các chỉ số chứng khoán quốc tế (như KOSPI, Nikkei 225, Dow Jones), luôn tích hợp góc nhìn Phân tích liên thị trường (Intermarket Analysis) kết nối với thị trường Việt Nam (tác động chuỗi cung ứng, dòng vốn FDI, độ lệch múi giờ giao dịch) và các cơ chế quản trị rủi ro hạ nhiệt thị trường (Circuit Breaker) để cung cấp giá trị thực chiến vượt trội cho Active Trader (P3).
- **Phạm vi:** Chỉ topic: Vĩ mô

---

### Bảng kết hợp QoQ x YoY và Bóc tách bẫy mùa vụ cho chỉ số kết quả kinh doanh quý
- **ID:** I070
- **Trạng thái:** ARTICLE
- **Thay bởi:** I128
- **Nguồn:** chi-so-qoq
- **Phản hồi từ User:** Phê duyệt bài viết Chỉ số QoQ thành công.
- **Bản năng:** Đối với các bài viết về chỉ số tài chính kết quả kinh doanh quý (như QoQ), luôn tích hợp Bảng kết hợp giữa QoQ và YoY (4 kịch bản: Tăng tốc, Phục hồi, Cảnh báo, Suy thoái) và phân tích chiều sâu về bẫy mùa vụ (Seasonality) trong các ngành đặc thù (bán lẻ Q4, bất động sản) để nâng cao tính định lượng thực chiến cho nhà đầu tư (P3 & P2).
- **Phạm vi:** Chỉ topic: Chỉ số tài chính & BCTC

---

### Mô phỏng lộ trình thặng dư và chuyển dịch dòng tiền cho bài viết quản lý nợ cá nhân
- **ID:** I071
- **Trạng thái:** ARTICLE
- **Thay bởi:** I130
- **Nguồn:** phuong-phap-qua-cau-tuyet
- **Phản hồi từ User:** Phê duyệt bài viết Phương pháp quả cầu tuyết thành công.
- **Bản năng:** Đối với các chủ đề về phương pháp tài chính cá nhân/trả nợ (như Quả cầu tuyết), luôn kết hợp cơ sở tâm lý học hành vi (Small Wins) với bảng mô phỏng lộ trình dòng tiền thực tế từng tháng và lộ trình chuyển dịch thặng dư sang kênh đầu tư tích lũy DSC.
- **Phạm vi:** Chỉ topic: Tài chính cá nhân

---

### Phân rã Target word count cho dạng Toplist và Đối sánh rủi ro pháp lý tài sản số
- **ID:** I072
- **Trạng thái:** ARTICLE
- **Thay bởi:** I120
- **Nguồn:** san-giao-dich-tien-dien-tu
- **Phản hồi từ User:** Phê duyệt bài viết Top 7 sàn giao dịch tiền điện tử dạng Toplist thành công.
- **Bản năng:** Khi viết các bài thuộc dạng Toplist đánh giá sản phẩm/dịch vụ tài chính hoặc tiền điện tử, luôn phân rã target word count chi tiết cho từng mục H3 trong outline để script QA đếm chính xác, đồng thời tích hợp Bằng chứng dự trữ (Proof of Reserves) và bảng đối sánh rủi ro ngắt kết nối pháp lý giữa thị trường tiền điện tử và kênh đầu tư chứng khoán chính thống được UBCKNN bảo hộ.
- **Phạm vi:** Chỉ topic: Tài chính cá nhân











### Ràng buộc thông tin sản phẩm và Tiêu đề Product Bridge
- **ID:** I104
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I111
- **Phạm vi:** Global
- **Bản năng:** Luôn đối soát 100% tính năng và thông tin sản phẩm với Brand KB (profile.md & service-operations.md), tuyệt đối không tự tạo hoặc giả định các tính năng sản phẩm chưa được xác thực (như đặt lệnh 24/7). Tiêu đề H2 cho phần Product Bridge phải được đặt tự nhiên (như Tối ưu hiệu quả giao dịch theo từng phiên cùng App DSC Trading và Môi giới 1:1), tập trung vào giải pháp cho bài toán thực tế của độc giả F0 thay vì dùng các từ gượng ép (như giao dịch đúng khung giờ).

---

### Hạn chế dùng thuật ngữ tiếng Anh "Active Trader" hoặc "trader" trong văn xuôi tiếng Việt
- **ID:** I073
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I106
- **Nguồn:** duong-ma-la-gi
- **Phản hồi từ User:** "bỏ từ active trader đi. Sử dụng từ tiếng Việt phù hợp với văn phong tài chính Việt Nam."
- **Bản năng:** Đối với đối tượng Active Trader (P3) hoặc các bài phân tích kỹ thuật, tuyệt đối không chèn trực tiếp các từ tiếng Anh mượn thô như "Active Trader" hay "trader" vào văn xuôi bài viết tiếng Việt. Thay vào đó, hãy sử dụng các thuật ngữ tiếng Việt chuẩn mực tài chính Việt Nam như "nhà đầu tư chủ động", "nhà đầu tư lướt sóng", "nhà giao dịch ngắn hạn" hoặc "nhà đầu tư".
- **Phạm vi:** Global


### Một URL một intent — chống cannibalization giữa bài hướng dẫn và bài lựa chọn
- **ID:** I074
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I118
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "hiện tại khi tìm cách mở tài khoản chứng khoán thì ra bài nen-mo-tai-khoan-chung-khoan-o-dau ở trang 2. Bạn có biết nguyên nhân ko? Dù tôi đã thực hiện link chéo giữa 2 bài"
- **Bản năng:** Khi viết/tối ưu một bài, kiểm tra các bài DSC cùng cụm (`find_links.py`) xem có bài nào đang trả lời cùng intent không. Bài so sánh/lựa chọn (ví dụ "mở tài khoản ở đâu") chỉ được nhắc quy trình bằng 2–3 câu + link anchor đúng từ khóa sang bài hướng dẫn, không đặt H2/H3 hướng dẫn chi tiết. Anchor dạng hướng dẫn ("mở tài khoản eKYC", "cách mở...") chỉ trỏ về bài hướng dẫn; anchor dạng lựa chọn ("nên mở ở đâu") chỉ trỏ về bài lựa chọn.
- **Phạm vi:** Global

### Giọng văn bài hướng dẫn (How-to) của DSC
- **ID:** I075
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I105
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "sapo chưa ổn cho 1 bài viết SEO của DSC về hướng dẫn... ko cần phải ghi hẳn Minh, 27 tuổi... phần Có tài khoản rồi, bạn cần làm thêm 3 việc... hơi giống văn nói hơn 1 bài viết SEO hướng dẫn"
- **Bản năng:** 1. Sapo bài hướng dẫn: câu đầu chứa keyword và tóm tắt các bước (ví dụ "Cách mở tài khoản chứng khoán online gồm 5 bước: ..."), câu sau nêu điều kiện cần; đoạn 2 nêu phạm vi bài và phần hướng dẫn riêng tại DSC. Không mở bằng "Bạn chỉ cần...". 2. Không đưa nhân vật persona có tên, tuổi, nghề (Minh, 27 tuổi...) vào bài hướng dẫn; nêu thẳng tình huống/lỗi bằng câu khách quan. 3. Đoạn dẫn H2/H3 dùng giọng trang trọng ("Sau khi tài khoản được kích hoạt, nhà đầu tư cần..."), tránh văn nói như "Có tài khoản rồi", "nhanh hơn hẳn", "thử hết mà vẫn chưa xong", "khi đã quen". 4. Mọi H3 nằm dưới H2 hướng dẫn phải là bước làm (danh sách đánh số), không phải đoạn so sánh; bảng so sánh chỉ dùng khi H2 có mục đích so sánh.
- **Phạm vi:** Global

### Copy và vị trí banner CTA trong bài hướng dẫn
- **ID:** I076
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I114
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "Nội dung của banner chưa tốt, phù hợp... banner đầu ở vị trí hơi thấp"
- **Bản năng:** Headline banner nêu thẳng hành động/lợi ích gắn chủ đề bài (ví dụ "Mở tài khoản chứng khoán DSC chỉ với CCCD gắn chip"), không dùng câu hỏi mồi hay lối nói đùa ("Đã có CCCD...? Bạn chỉ còn cách..."). Dòng phụ là 3 dữ kiện sản phẩm thật (eKYC 3 phút, miễn phí mở và duy trì, Môi giới 1:1, phí từ 0,1%, Mã định danh 963369). Banner cuối bài phải khác ý banner giữa bài. Banner giữa bài đặt ngay sau H3 hướng dẫn sản phẩm DSC chính (khoảng 35–40% thân bài), không đợi hết toàn bộ H2.
- **Phạm vi:** Global

### Target word count H2 trong outline chỉ tính thân riêng
- **ID:** I077
- **Trạng thái:** DEPRECATED
- **Ghi chú:** chuyển vào brief-template.md (quy ước **Target:**)
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "(Phát hiện khi chạy qa_lint --outline: H2 có H3 con bị báo WC-under sai)"
- **Bản năng:** Khi viết outline, `**Target:**` của H2 có H3 con chỉ ghi số từ phần thân riêng của H2 (trước H3 đầu tiên), vì `count_words.py` không cộng H3 vào H2. Câu FAQ trong outline không dùng nhãn `**Target:**` (sẽ bị gán nhầm vào H2 FAQ); phần kết bài nếu có heading thì ghi `### H2: ...` kèm target riêng.
- **Phạm vi:** Global

---

### Đối chiếu dữ liệu thực tế từ Google AI Overview cho bài toán quy mô vốn lớn
- **ID:** I078
- **Trạng thái:** ARTICLE
- **Thay bởi:** I130
- **Nguồn:** co-1-ty-nen-gui-ngan-hang-nao
- **Phản hồi từ User:** "tôi thử search google thì data trả về khác" (Kèm ảnh chụp màn hình kết quả Google AI Overview cho query 1 tỷ gửi ngân hàng nào)
- **Bản năng:** Khi viết các bài viết so sánh lãi suất tiền gửi quy mô vốn lớn (từ 1 tỷ VNĐ trở lên), luôn bổ sung góc nhìn thương lượng lãi suất thỏa thuận riêng tại quầy (+0,5%–1,5%/năm so với niêm yết) và các gói ưu đãi trực tuyến ngân hàng số (7,4%–9,6%/năm) bên cạnh biểu lãi suất niêm yết chuẩn, giúp bài viết chuẩn xác với kết quả Google AI Overview và thấu hiểu nhu cầu thực tế của người gửi tiền.
- **Phạm vi:** Chỉ topic: Tài chính cá nhân


---

### Bảng tỷ lệ Fibonacci và 3 Nguyên tắc đếm sóng cho bài viết Sóng Elliott
- **ID:** I079
- **Trạng thái:** ARTICLE
- **Thay bởi:** I125
- **Nguồn:** song-elliott-va-fibonacci-la-gi
- **Phản hồi từ User:** Phê duyệt bài viết Sóng Elliott và Fibonacci thành công.
- **Bản năng:** Luôn lồng ghép Bảng Ma trận Tỷ lệ Fibonacci cho các bước sóng 1-5 & A-B-C kết hợp 3 nguyên tắc bất biến đếm sóng (Sóng 2 không quá đáy 1, Sóng 3 không bao giờ ngắn nhất, Sóng 4 không phạm vùng giá 1), kỹ thuật xác định Vùng hội tụ Fibonacci Cluster và bảng Quản trị Rủi ro Stop Loss/Take Profit khi tối ưu bài viết về Sóng Elliott và Fibonacci cho nhà đầu tư chủ động (P3).
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật

---

### Bảng đối sánh đòn bẩy hai chiều kèm chi phí lãi vay và Bảng phân biệt Tiểu khoản 1 vs 6
- **ID:** I080
- **Trạng thái:** ARTICLE
- **Thay bởi:** I127
- **Nguồn:** margin-la-gi
- **Phản hồi từ User:** Phê duyệt bài viết Margin là gì thành công (QA Score 100/100).
- **Bản năng:** Khi viết hoặc tối ưu các bài viết về giao dịch ký quỹ (Margin) cho nhà đầu tư mới (P2), luôn lồng ghép Bảng đối sánh kết quả đầu tư 2 chiều (kịch bản tăng giá vs kịch bản giảm giá) kèm trừ chi phí lãi vay thực tế và tính toán tỷ lệ an toàn sau biến động, đồng thời lập Bảng phân biệt rõ ràng giữa Tài khoản thường (Tiểu khoản 1) và Tài khoản ký quỹ (Tiểu khoản 6) để đảm bảo góc nhìn khách quan và cảnh báo rủi ro đòn bẩy toàn diện.
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)


---

### Phân định năng lực hạ tầng vs Khung pháp lý và Minh họa kịch bản lệnh MTL
- **ID:** I081
- **Trạng thái:** ARTICLE
- **Thay bởi:** I127
- **Nguồn:** krx-la-gi
- **Phản hồi từ User:** Phê duyệt bài viết Hệ thống KRX là gì thành công (QA Score 100/100).
- **Bản năng:** Khi viết bài về các nâng cấp hạ tầng công nghệ chứng khoán (như KRX, CCP), luôn phân định rạch ròi giữa năng lực kỹ thuật đã tích hợp sẵn và điều kiện khung pháp lý/thể chế cần có để kích hoạt sản phẩm mới (T+0, bán khống), đồng thời minh họa cơ chế lệnh thị trường mới (như MTL) bằng kịch bản khớp lệnh đối ứng từng phần cụ thể để nhà đầu tư mới (P2) nắm rõ cơ chế kiểm soát rủi ro trượt giá.
- **Phạm vi:** Chỉ topic: Giao dịch cơ bản (F0)

---

### Bảng phân tích mã AFL thay cho code block thô và Đoạn dẫn chuẩn cho Banner CTA
- **ID:** I082
- **Trạng thái:** ARTICLE
- **Thay bởi:** I114
- **Nguồn:** amibroker-la-gi
- **Phản hồi từ User:** Phê duyệt bài viết Amibroker là gì thành công (QA Score 100/100).
- **Bản năng:** 1. Khi viết về các phần mềm phân tích kỹ thuật hoặc thuật toán (như Amibroker, AFL), tuyệt đối không dùng code block thô mà hãy chuyển đổi thành Bảng Markdown 2 cột (Dòng lệnh AFL | Ý nghĩa thực thi) để tương thích CMS và tối ưu trải nghiệm đọc lướt. 2. Đối với khối Banner CTA chuyển đổi, bắt buộc phải có một đoạn văn xuôi dẫn dắt trực tiếp (độ dài ≥ 10 từ) nằm ngay phía trên khối banner, không đặt danh sách gạch đầu dòng sát banner để đảm bảo cấu trúc Product Bridge liền mạch.
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật

---

### Bảng Lịch Đáo Hạn 12 tháng kèm Trạng thái & Cơ chế tính FSP loại trừ nhiễu ATC
- **ID:** I083
- **Trạng thái:** ARTICLE
- **Thay bởi:** I129
- **Nguồn:** dao-han-phai-sinh-la-gi
- **Phản hồi từ User:** Phê duyệt bài viết Ngày đáo hạn phái sinh là gì thành công (QA Score 100/100).
- **Bản năng:** Khi viết hoặc tối ưu các bài viết về ngày đáo hạn phái sinh cho nhà đầu tư mới (P2), luôn tích hợp Bảng Lịch Đáo Hạn cả 12 tháng của năm hiện tại kèm cột Trạng thái cập nhật thực tế, Bảng đối sánh Ngày đáo hạn vs Ngày thanh toán T+1, và công thức tính Giá thanh toán cuối cùng (FSP) loại trừ các giá trị cực đoan trong 30 phút cuối phiên ATC để giải tỏa nỗi sợ thao túng chỉ số cho nhà đầu tư mới, kết hợp lệnh Stop-loss/Take-profit tự động trên App DSC Trading làm Product Bridge phòng thủ an toàn.
- **Phạm vi:** Chỉ topic: Phái sinh

---

### Phân tích cổ phiếu biến cố tái cấu trúc & Bóc tách khoản dự phòng một lần
- **ID:** I084
- **Trạng thái:** ARTICLE
- **Thay bởi:** I124
- **Nguồn:** co-nen-mua-co-phieu-pnj-hay-khong
- **Phản hồi từ User:** Phê duyệt bài viết Có nên mua cổ phiếu PNJ thành công (QA Score 100/100).
- **Bản năng:** Khi viết hoặc tối ưu các bài viết phân tích cổ phiếu bluechip gặp biến cố lớn hoặc tái cấu trúc (như PNJ năm 2026), luôn cập nhật ngay số liệu tài chính mới nhất từ đại hội cổ đông bất thường, bóc tách khoản trích lập dự phòng một lần khỏi kết quả kinh doanh cốt lõi để đánh giá đúng năng lực sinh lời thực, xây dựng Bảng ma trận kịch bản đầu tư đối chuẩn giữa trường phái thận trọng đứng ngoài và trường phái bắt đáy dài hạn có kiểm soát tỷ trọng (10%–20%), đồng thời cảnh báo bẫy giá trị (Value Trap) và nghiêm cấm sử dụng đòn bẩy ký quỹ (Margin) đối với nhà đầu tư F0 (P2).
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu

---

### Tách Intent chống Cannibalization mã cổ phiếu, Chuẩn Banner Dark Navy & Công thức CMS-ready
- **ID:** I085
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I114
- **Nguồn:** cach-mua-co-phieu-vcb-ngan-hang-vietcombank
- **Phản hồi từ User:** "CTA khó nhìn, ko theo chuẩn. Công thức format này ko hiển thị đc trên CMS của tôi"
- **Bản năng:** 1. Khi tối ưu bài hướng dẫn thực hành mua cổ phiếu (How-to / Transactional), kiên quyết loại bỏ hoàn toàn các phần phân tích cơ bản/BCTC khỏi bài để chống xung đột intent (Cannibalization) với bài phân tích tổng quan cùng mã, đồng thời xây dựng liên kết chéo 2 chiều (Cross-linking) phân luồng rõ ràng. 2. Tuyệt đối không dùng cú pháp LaTeX `$$...$$` cho các công thức tính toán tài chính; luôn chuyển đổi thành Markdown Blockquote in đậm kết hợp Bảng tính chi phí Markdown trực quan tương thích 100% với CMS. 3. Mọi banner CTA phải sử dụng chuẩn Responsive Gradient Dark Navy `#0D1B2A` phối nút Neon Green `#2BE841` (độ tương phản 10.2:1 chuẩn WCAG AA), tuyệt đối không dùng khối viền màu xanh nhạt `#E8F8F2` thiếu chuyên nghiệp.
- **Phạm vi:** Global


---

### Re-optimize pillar: kiểm lại số liệu bản trước, bảng so sánh CTCK chỉ khi có nguồn
- **ID:** I086
- **Trạng thái:** ARTICLE
- **Thay bởi:** I110
- **Nguồn:** cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau
- **Phản hồi từ User:** Phê duyệt bản re-optimize 16/10/2026 (lint 100, slop 94 → 97) sau khi bản 14/10 còn sai số tài khoản VSDC, giá HPG, chu kỳ T+1,5 và bảng phí đối thủ không nguồn.
- **Bản năng:** 1. Khi optimize lại một bài đã optimize trước đó, không tin số liệu của bản trước: chạy lại `market_facts.py --brief` cho mọi mã/chỉ số trong bài và đối chiếu số tài khoản/thanh khoản với mốc chuẩn ở anti-ai-rules §S3; chu kỳ thanh toán luôn viết T+2 theo glossary. 2. Bài pillar how-to cho F0 không đặt bảng so sánh phí/chất lượng app của đối thủ (VPS, SSI, TCBS...) khi không có nguồn công khai — thay bằng bảng câu hỏi kiểm tra + cột thông số DSC, và chỉ 2–3 câu + link sang bài lựa chọn "nên mở tài khoản ở đâu". 3. Kéo query GSC của chính URL: biến thể mang nhiều click nhất (ví dụ "cách chơi cổ phiếu") phải có mặt trong sapo hoặc H2/H3; query dạng câu hỏi có impressions lớn (ví dụ "chơi chứng khoán như thế nào") nâng thành H2. 4. Phần rủi ro/sai lầm neo vào biến động thật của năm hiện tại (đỉnh–đáy VN-Index có ngày) và tin có ngày từ `news_feed.py`.
- **Phạm vi:** Global

---

### Bảng ma trận 4 nến đơn đối sánh & Bộ lọc thanh khoản T+2 cho nến Hammer
- **ID:** I087
- **Trạng thái:** ARTICLE
- **Thay bởi:** I125
- **Nguồn:** mo-hinh-nen-hammer-la-gi
- **Phản hồi từ User:** Phê duyệt bài viết Mô hình nến Hammer tối ưu đạt QA Lint 100/100 và Slop 100/100.
- **Bản năng:** 1. Khi viết hoặc tối ưu các bài về mô hình nến đơn đảo chiều (như nến Hammer/Búa), luôn tích hợp Bảng ma trận 4 chiều đối sánh rạch ròi các mẫu nến có hình dáng tương đồng (Hammer vs Hanging Man vs Inverted Hammer vs Shooting Star) theo vị trí xuất hiện (đáy vs đỉnh) và tín hiệu đảo chiều (tăng vs giảm) để dập tắt triệt để sự nhầm lẫn kỹ thuật (đặc biệt không gộp Inverted Hammer vào nến đảo chiều giảm). 2. Bắt buộc phải gắn liền tín hiệu nến rút chân với điều kiện xác nhận thanh khoản Volume (vượt 20% - 50% MA20), cây nến xác nhận tiếp theo đóng cửa vượt đỉnh, tỷ lệ R:R tối thiểu 1:2 và cảnh báo rủi ro chu kỳ thanh toán T+2 trên thị trường chứng khoán cơ sở Việt Nam.
- **Phạm vi:** Chỉ topic: Phân tích kỹ thuật


---

### Quy ước Daylight Saving Time chuẩn giờ Việt Nam & Rào cản pháp lý Nghị định 135/2015/NĐ-CP
- **ID:** I088
- **Trạng thái:** ARTICLE
- **Thay bởi:** I126
- **Nguồn:** gio-giao-dich-chung-khoan-quoc-te
- **Phản hồi từ User:** Phê duyệt bài viết Giờ giao dịch chứng khoán quốc tế đạt QA Lint 99/100, Slop 100/100, Fact Check 0 lỗi.
- **Bản năng:** 1. Khi viết bài về các sàn chứng khoán quốc tế (Mỹ, Châu Âu, Châu Á) cho nhà đầu tư Việt Nam, luôn phải quy đổi trực quan sang giờ Việt Nam (UTC+7) và phân tách rõ ràng sự dịch chuyển 60 phút giữa mùa hè và mùa đông do quy ước Daylight Saving Time (DST); đồng thời giải mã mối liên hệ thực chiến giữa biến động Phố Wall rạng sáng với tâm lý ATO (09:00 - 09:15) trên sàn HOSE để tránh FOMO bán tháo. 2. Bắt buộc tích hợp cảnh báo pháp lý theo Nghị định số 135/2015/NĐ-CP và Luật Đầu tư 2020: khẳng định rõ cá nhân tại Việt Nam chưa được phép tự ý chuyển ngoại tệ ra nước ngoài mua cổ phiếu quốc tế, vạch trần rủi ro mất vốn từ các sàn phái sinh CFD không phép, từ đó dẫn dắt chuyển đổi sang đầu tư cổ phiếu Việt Nam hợp pháp và minh bạch cùng App DSC Trading và Môi giới 1:1.
- **Phạm vi:** Chỉ topic: Vĩ mô

---

### Liên kết biến số vĩ mô DXY với tỷ giá trong nước & Cơ chế truyền dẫn VN-Index
- **ID:** I089
- **Trạng thái:** ARTICLE
- **Thay bởi:** I110
- **Nguồn:** chi-so-dxy-la-gi
- **Phản hồi từ User:** Phê duyệt bài viết tối ưu Chỉ số DXY đạt QA Lint 100/100, Slop score 100/100, Fact Check 0 lỗi.
- **Bản năng:** 1. Đối với các bài viết về chỉ số vĩ mô quốc tế (như DXY, Fed Funds Rate), tiêu đề H1 và Meta Description phải gắn trực tiếp với biến số tác động tại Việt Nam (tỷ giá USD/VND, thanh khoản OMO và chỉ số VN-Index) để giải quyết khoảng trống CTR Gap. 2. Bắt buộc phải cập nhật diễn biến vĩ mô mới nhất giai đoạn gần nhất (2025–2026) kèm số liệu tỷ giá tại các ngân hàng thương mại lớn và động thái điều hành tiền tệ của Ngân hàng Nhà nước để bảo đảm tính xác thực E-E-A-T. 3. Phân định rạch ròi 3 kênh truyền dẫn vĩ mô (dòng vốn ngoại FII, tỷ giá/thanh khoản tiền tệ, phân hóa ngành xuất khẩu vs nợ vay USD) để đưa ra khuyến nghị cơ cấu danh mục thực chiến cho F0 (P2).
- **Phạm vi:** Chỉ topic: Vĩ mô


---

### Hóa giải nghịch lý CTR: Định nghĩa trực diện 50 ký tự đầu & Khung hành động chốt lời Target kỷ luật
- **ID:** I090
- **Trạng thái:** ARTICLE
- **Thay bởi:** I121
- **Nguồn:** target-trong-chung-khoan-la-gi
- **Phản hồi từ User:** "Impression tăng 224% nhưng gần như không ai click → kiểm tra query chính, sửa title/meta cho khớp ý định tìm kiếm", "/approve"
- **Bản năng:** 1. Khi một bài viết tài chính nhận được lượng hiển thị (Impressions) tăng vọt (>200%) nhưng CTR gần như bằng 0 (< 0,5%), nguyên nhân hàng đầu là Title và Meta Description thiếu tính kích hoạt hành vi nhấp chuột (quá khô khan, hoặc lãng phí ký tự đầu để nhắc lại câu hỏi mà không đưa ra định nghĩa/con số giải pháp). Bắt buộc đưa câu trả lời định nghĩa trực diện ngay 50 ký tự đầu của Meta Description (tối ưu hiển thị Mobile và Featured Snippet) và bổ sung con số giải pháp định lượng vào Title (Sentence case, ≤ 59 ký tự). 2. Người mới (F0: P2) tìm kiếm về "target/giá mục tiêu" không chỉ cần lý thuyết mà cần "kim chỉ nam hành động" khi thị giá tiệm cận mức giá đó; luôn tích hợp quy tắc chốt lời từng phần 50/50, lệnh Trailing Stop bảo toàn lợi nhuận, Bảng so sánh 3 phương pháp định giá Target (P/E & P/B vs DCF vs TA) và Product Bridge kết nối tính năng Cảnh báo giá tự động trên App DSC Trading cùng Môi giới 1:1.
- **Phạm vi:** Global


---

### Phân tích cổ phiếu Năng lượng & Tiện ích: Mốc thương mại COD điện khí LNG và Chuyển biến P/E động
- **ID:** I091
- **Trạng thái:** ARTICLE
- **Thay bởi:** I124
- **Nguồn:** co-nen-mua-co-phieu-pow-hay-khong
- **Phản hồi từ User:** "Click giảm 34%, impression giảm 38% → làm mới số liệu và nhận định", "/approve"
- **Bản năng:** 1. Đối với cổ phiếu ngành năng lượng và điện lực (như POW), rào cản tăng trưởng lớn nhất ở các chu kỳ cũ thường là chi phí đầu tư dở dang và thiếu hụt nguồn khí tự nhiên; khi dự án hạ tầng trọng điểm (như Nhơn Trạch 3 & 4) chuyển từ giai đoạn xây dựng sang vận hành thương mại (COD), bắt buộc phải cập nhật ngay mốc COD chính xác kèm sản lượng phát điện thương phẩm thực tế (tỷ kWh) và doanh thu đóng góp thực tế thay vì dùng nhận định định tính lỗi thời. 2. Khi phân tích định giá P/E cho doanh nghiệp vừa có lợi nhuận đột biến (nhờ ghi nhận doanh thu mới và thu hồi tố tài chính), phải giải thích rõ sự chuyển biến của mẫu số EPS trượt (trailing EPS) kéo P/E dự phóng về vùng định giá rẻ, kết hợp định giá tài sản ròng qua P/B để cung cấp biên an toàn rõ ràng cho nhà đầu tư F0 (P2). 3. Bắt buộc phân định rạch ròi 2 trường phái giải ngân: Tích sản phòng thủ hưởng dòng tiền cổ tức tiền mặt đều đặn (P2) vs Lướt sóng kỹ thuật theo điểm bùng nổ thanh khoản và các mốc hỗ trợ/kháng cự (P3).
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu


---

### Phân tích cổ phiếu Bất động sản chu kỳ: Niên độ kế toán lệch chuẩn & Tín hiệu người mua trả tiền trước đột biến
- **ID:** I092
- **Trạng thái:** ARTICLE
- **Thay bởi:** I124
- **Nguồn:** co-phieu-tch-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat
- **Phản hồi từ User:** "CTR thấp → cập nhật số liệu, sửa title", "/approve"
- **Bản năng:** 1. Đối với doanh nghiệp có niên độ tài chính đặc thù lệch chuẩn năm dương lịch (như TCH từ 01/04 năm này đến 31/03 năm sau), bắt buộc phải giải thích rõ ràng niên độ kế toán ngay đầu phần kết quả kinh doanh để nhà đầu tư F0 (P2) không nhầm lẫn giữa năm dương lịch và năm tài chính. 2. Khi phân tích cổ phiếu bất động sản đang ở vùng trũng lợi nhuận quá khứ nhưng có chỉ số "Người mua trả tiền trước ngắn hạn" tăng đột biến (gấp hàng chục lần, như TCH đạt gần 6.500 tỷ đồng), đây là tín hiệu chuyển pha quyết định báo hiệu điểm rơi lợi nhuận tương lai khi bàn giao dự án; bắt buộc phải bóc tách sâu cấu trúc khoản tiền cọc này gắn liền với tiến độ xây thô/cất nóc của các đại dự án cụ thể (như Hoàng Huy New City II và Green River tại Thủy Nguyên - Hải Phòng) thay vì chỉ nhìn định giá tĩnh P/E quá khứ. 3. Để xử lý nghịch lý CTR thấp ở trang 1 Google (< 0,5%), bắt buộc loại bỏ triệt để các mốc thời gian cũ trong ngoặc vuông như `[T5/2026]` trên Title và thay bằng Title Sentence case (≤ 59 ký tự) phản ánh định giá và kết quả kinh doanh năm tài chính mới nhất.
- **Phạm vi:** Chỉ topic: Phân tích cổ phiếu


---

### Tối ưu CTR Gap cho từ khóa định nghĩa Trading: Phân định rạch ròi Trading vs Investing & Sapo thực chiến
- **ID:** I093
- **Trạng thái:** ARTICLE
- **Thay bởi:** I105
- **Nguồn:** trading-trong-chung-khoan-la-gi
- **Phản hồi từ User:** "“trading” (11k) và “trading là gì” (5k) có CTR thấp → viết lại title/meta, phần mở bài", "/approve"
- **Bản năng:** 1. Khi tối ưu bài viết thuật ngữ có lượng tìm kiếm lớn nhưng CTR cực thấp (< 0,5% dù ở Top 5 Google), nguyên nhân cốt lõi là Title và Meta mang tính định nghĩa lý thuyết từ điển hoặc dạo đầu sáo rỗng. Bắt buộc viết lại Title sentence case (dưới 60 ký tự) gắn liền từ khóa chính với mâu thuẫn nhận thức lớn nhất của F0: phân biệt rạch ròi giữa Trading (giao dịch lướt sóng ngắn hạn) và Investing (đầu tư tích sản dài hạn). 2. Meta description phải nêu bật lợi ích và nguyên tắc quản trị rủi ro thực chiến thay vì giải nghĩa từ điển tiếng Anh. 3. Đoạn Sapo mở đầu phải trả lời trực diện định nghĩa trong câu đầu tiên (chuẩn Featured Snippet), đưa số liệu thực tế về rủi ro (hơn 80% trader thua lỗ năm đầu tiên do thiếu kỷ luật cắt lỗ và cảm xúc), tuyệt đối không dùng câu chào mời đọc tiếp ("Hãy cùng tìm hiểu...", "Cùng DSC khám phá từ A-Z...") và không chèn thương hiệu DSC gượng ép vào Sapo.
- **Phạm vi:** Global


---

### Tối ưu CTR Gap cho chỉ số thị trường: Thỏa mãn Search Intent số liệu & Loại bỏ tiếng Anh, Emphatic Quotes
- **ID:** I094
- **Trạng thái:** ARTICLE
- **Thay bởi:** I106
- **Nguồn:** chi-so-vn-index-va-y-nghia-quan-trong-trong-thi-truong-chung-khoan-viet-nam
- **Phản hồi từ User:** "Gần như 0 click từ “vnindex” (9k) → người tìm muốn xem số liệu, nên thêm mức điểm hoặc biểu đồ gần đây", "2 heading trên chứa từ tiếng anh và ngoặc kép. Ngoài ra tôi cũng k hiểu 2 heading này có ý nghĩa gì, b tham khảo đối thủ nào hay tự thêm", "A", "/approve"
- **Bản năng:** 1. Khi một bài viết về chỉ số thị trường có lượng tìm kiếm lớn (như VN-Index) nhưng CTR gần như bằng 0 (CTR Gap), nguyên nhân chủ yếu là bài viết chỉ mang tính định nghĩa từ điển giáo khoa lịch sử mà thiếu dữ liệu snapshot điểm số thực tế và biểu đồ gần đây; bắt buộc phải cập nhật ngay mức điểm hiện tại, thanh khoản toàn thị trường và Bảng thống kê các mốc điểm lịch sử đáng nhớ (từ ngày cơ sở đến nay) để thỏa mãn ngay lập tức nhu cầu tra cứu số liệu của người dùng. 2. Tuyệt đối không dùng từ tiếng Anh lai căng (như Snapshot) trong đề mục bài viết tài chính tiếng Việt; tuyệt đối không dùng dấu ngoặc kép bọc từ thông thường hay tiếng lóng (như "xanh vỏ đỏ lòng") theo quy tắc Rule 1.2 Anti-AI, thay vào đó phải diễn đạt bằng thuật ngữ phân tích chuẩn xác: hiện tượng lệch pha giữa chỉ số chung và danh mục cổ phiếu do tác động vốn hóa của nhóm cổ phiếu lớn. 3. Khi giải thích chỉ số tính theo trọng số vốn hóa, phải hướng dẫn nhà đầu tư mới (P2 - F0) phối hợp đọc giữa điểm số danh nghĩa, thanh khoản khớp lệnh (Volume) và độ rộng thị trường (tỷ lệ mã tăng/giảm) để tránh bẫy mua đuổi khi chỉ số bị kéo tăng bởi một vài mã vốn hóa khổng lồ.
- **Phạm vi:** Global


---

### Bài hướng dẫn thao tác: xác định kênh web/app từ chính ảnh chụp
- **ID:** I095
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I119
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "ảnh là chụp mở tài khoản trên web. Còn app sẽ khác", "ekyc đang chỉ hỗ trợ trên app thôi. Có thể viết thêm cách mở tài khoản chứng khoán trên app như bên vpbanks làm"
- **Bản năng:** 1. Trước khi viết các bước thao tác, mở từng ảnh chụp màn hình để xác định ảnh thuộc web hay app và màn hình đó còn dùng không; không suy ra từ alt, tên file hay bản cũ của bài. 2. Khi web và app có quy trình khác nhau (ví dụ DSC: web chỉ đăng ký/OTP/chọn số, eKYC NFC chỉ trên App DSC Trading), viết luồng chính theo ảnh có thật và tách một H2 riêng cho app dạng danh sách bước gọn như đối thủ; ghi rõ bước nào chuyển kênh. 3. Ảnh chụp giao diện đã bỏ thì gỡ và báo user, không để ảnh mâu thuẫn với chữ bên cạnh.
- **Phạm vi:** Global

---

### Bài how-to dài hơn đối thủ: đo trước, cắt phần phụ, không lặp H2 thương hiệu
- **ID:** I096
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I105
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "tham khảo outline đối thủ. Outline này hơi rối", "outline và nội dung ko ổn, dài dòng so với 2 đói thủ", "Các phần hướng dẫn trên là hướng dẫn chung hay là áp dụng DSC mà phải cần thêm heading Cách lập tài khoản chứng khoán tại DSC? H2 Sau khi mở: nạp tiền và bảo mật tài khoản phần heading này có cần thiết ko?", "H1 khác, sapo phải có brand DSC ở trong đó"
- **Bản năng:** 1. Khi optimize bài how-to, đếm số từ và số H2 của 2 đối thủ top trước khi đề xuất outline; giữ độ dài cùng cỡ, cắt ví dụ phụ, bảng kiểm tra, FAQ ngoài PAA và các H2 lệch intent (việc sau khi mở). 2. Nếu các bước đã minh họa bằng sản phẩm DSC thì không thêm H2 "tại DSC" lặp lại quy trình; thông tin riêng DSC (số tài khoản, tiểu khoản, nạp tiền) gắn vào đúng bước. 3. Với bài hướng dẫn chạy trên sản phẩm DSC, H1 khác Title SEO và có DSC; sapo được nhắc DSC (ngoại lệ của quy tắc sapo không nhắc brand).
- **Phạm vi:** Global

---

### Bài "top cổ phiếu" khi optimize: nguồn CTCK có ngày, giữ xương outline gốc
- **ID:** I097
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I120
- **Nguồn:** top-5-co-phieu-dang-dau-tu
- **Phản hồi từ User:** "Có thể crawl báo cáo khác trên mạng và tổng hợp lại", "gắn cả link tham khảo vào để tôi check lại có phải mới nhất ko nhé. Ngoài ra sapo đang chưa ổn", "phần outline chỉnh sửa quá nhiều so với bản gốc"
- **Bản năng:** 1. Bài khuyến nghị nhiều mã: chọn mã theo mức đồng thuận trong báo cáo chiến lược có ngày của các CTCK, ghi tên CTCK cạnh từng giá mục tiêu kèm link nguồn, thêm danh sách nguồn có ngày cuối bài để user kiểm độ mới; DSC không tự đặt giá mục tiêu. 2. Khi /optimize, giữ thứ tự H2 và mẫu block của từng mục như bản gốc; thay nội dung chứ không thêm H2 mới (bảng tổng hợp, bối cảnh, FAQ…) nếu user chưa đồng ý. Chỗ nào buộc phải lệch gốc vì rule QA thì liệt kê cho user. 3. Tên CTCK trùng mã niêm yết (BSC) phải ghi tên đầy đủ ở lần nhắc đầu.
- **Phạm vi:** Global

---

### Sapo bài hướng dẫn mua cổ phiếu theo mã: có DSC và câu nêu phạm vi bài
- **ID:** I098
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I105
- **Nguồn:** cach-mua-co-phieu-flc
- **Phản hồi từ User:** "Sapo chưa đạt, ko có tên brand DSC, kêu gọi người xem đọc bài viết", "tôi đọc file mới thấy Sapo đã có thay đổi gì đâu"
- **Bản năng:** 1. Với bài hướng dẫn (`cach-mua-co-phieu-<mã>`, mở tài khoản, how-to thao tác), sapo gồm 2 đoạn: đoạn 1 chứa keyword và trả lời thẳng câu hỏi kèm mốc có ngày; đoạn 2 nêu điều kiện/bối cảnh rồi 1 câu có DSC giới thiệu phạm vi bài theo mẫu "Trong bài viết này, DSC cập nhật/hướng dẫn …" (như sapo bản live). 2. (Đã thay) Quy tắc "sapo không nhắc brand" đã bị bỏ — sapo mọi loại bài đều có DSC + câu mời đọc tiếp. 3. Khi user phản hồi ngắn gọn dạng liệt kê ("ko có X, Y"), hiểu là bài đang THIẾU X, Y; nếu mâu thuẫn với instinct cũ thì hỏi lại 1 câu trước khi sửa, không tự suy theo instinct.
- **Phạm vi:** Global

### Bài toplist app/sản phẩm: mục liệt kê là nội dung chính, mỗi mục có giới thiệu + ưu nhược điểm
- **ID:** I099
- **Trạng thái:** ARTICLE
- **Thay bởi:** I111
- **Nguồn:** app-mua-chung-chi-quy
- **Phản hồi từ User:** "tập trung vào toplist", "1 số phần heading 2 cảm giác k cần. Bạn đã check outline đối thủ chưa", "toplist là nội dung chính nên viết chi tiết hơn", "thêm phần giới thiệu App, ưu nhược điểm"
- **Bản năng:** 1. Keyword dạng "app/nơi/sàn + [hành động]" (app mua chứng chỉ quỹ, app đầu tư…) có intent toplist: dựng outline dạng "Top N …" ngay từ đầu, không phân nhóm theo khái niệm. 2. Trước khi đề xuất H2 phụ, đối chiếu outline đối thủ toplist (đếm H2 phụ ngoài danh sách); chỉ giữ tối đa 3 H2 hỗ trợ (bảng tóm tắt, cách chọn/kiểm tra, FAQ), gộp phí/loại sản phẩm vào từng mục, kết bài không cần heading (đã bỏ 09/11 — toplist vẫn có H2 Kết luận, xem I120/I113). 3. Mỗi mục (H3) ~200 từ theo khung: Giới thiệu (đơn vị phát hành, giấy phép, điểm App Store) → Ưu điểm → Nhược điểm → Hợp với ai. Ưu/nhược theo thực tế, không ép đối xứng, mỗi ý gắn 1 dữ kiện đã xác minh (biểu phí, giờ chốt lệnh, rating); mục DSC cũng ghi nhược điểm thật. 4. Lấy dữ kiện app từ App Store listing (apps.apple.com/vn), trang chi tiết sản phẩm trên nền tảng phân phối và trang chính thức; site chặn fetch → mô tả định tính, không tự điền số. 5. DSC không phân phối quỹ mở — trong bài về chứng chỉ quỹ, DSC Trading chỉ xuất hiện ở phạm vi ETF và không xếp hạng 1.
- **Phạm vi:** Global

### Đọc phản hồi rút gọn "ko có X, Y" là bài đang THIẾU X, Y
- **ID:** I100
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I122
- **Nguồn:** rui-ro-chung-chi-quy
- **Phản hồi từ User:** "sapo ko CTA đọc bài viết, ko có brand name" → sau khi bị hiểu ngược: "Sapo phải nhắc DSC và kêu gọi người đọc xem tiếp bài viết chứ"
- **Bản năng:** Phản hồi ngắn dạng "ko có X", "chưa có X", "ko X" về một phần của bài mặc định hiểu là phần đó đang THIẾU X và cần thêm X. Chỉ hiểu thành "bỏ X" khi user viết rõ "bỏ", "xóa", "đừng". Nếu cách hiểu khiến bản sửa đi ngược instinct hiện có hoặc làm mất thứ bài đang có, hỏi lại 1 câu trước khi sửa.
- **Phạm vi:** Global

### Product Bridge bài rủi ro/kiến thức: nối từ rủi ro vừa phân tích, có bảng so sánh bằng tiền + lợi ích mở tài khoản; bắt buộc H2 Kết luận
- **ID:** I101
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I112
- **Nguồn:** rui-ro-chung-chi-quy
- **Phản hồi từ User:** "phần content DSC chưa hay, hơi máy móc và dẫn về mở tài khoản DSC chưa tốt. Chưa thấy các ưu điểm khi mở tài khoản để đầu tư. Kết luận cũng chưa có"
- **Bản năng:** 1. H2 sản phẩm DSC không mở bằng list thông số. Câu đầu nối thẳng từ vấn đề bài vừa phân tích (ví dụ 2 rủi ro quỹ mở mà ETF tránh được), nói rõ rủi ro nào sản phẩm KHÔNG giải quyết. 2. Có 1 bảng so sánh lựa chọn thay thế vs giải pháp qua tài khoản DSC, dùng ví dụ tiền cụ thể (100 triệu bán sau 6 tháng: phí 1,5–2,5 triệu vs 100.000 VNĐ). 3. Có H3 "Lợi ích khi mở tài khoản chứng khoán DSC để …": mỗi bullet là lợi ích người đọc nhận được (vốn tối thiểu tính bằng tiền, miễn phí mở/duy trì, một tài khoản cho nhiều sản phẩm, Môi giới 1:1 lúc thị trường giảm), không phải tên tính năng. 4. Thêm 1 đoạn tình huống có ngày cho Môi giới 1:1, rồi link mở tài khoản ngay trước banner. 5. Bài kiến thức/phân tích luôn có H2 "Kết luận": 1 nhận định + checklist hành động 3 mục + CTA mở tài khoản; không mở bằng "Tóm lại".
- **Phạm vi:** Global

### Câu ngắn phải mang dữ kiện, heading giọng trang trọng, không nhân vật có tên
- **ID:** I102
- **Trạng thái:** DEPRECATED
- **Thay bởi:** I107
- **Nguồn:** co-nen-dau-tu-chung-chi-quy
- **Phản hồi từ User:** "Sao có những câu ngắn như kiểu 'Kết quả này đáng chú ý.' vậy?", "'Chi phí khi đầu tư chứng chỉ quỹ ăn bao nhiêu lợi nhuận' nghe ko chuyên nghiệp, 'Đã quyết định đầu tư: chọn loại quỹ theo thời gian cầm tiền'", "Bỏ kiểu 'Người như chị Lan' đi nhé"
- **Bản năng:** 1. Câu ≤7 từ dùng để ngắt nhịp (§8.7f) phải chứa dữ kiện ("MAGEF dẫn đầu với 64,31%.", "Chứng chỉ quỹ không có bảo hiểm này."); cấm câu nhận xét rỗng hoặc câu hỏi tu từ chuyển ý ("Kết quả này đáng chú ý.", "Kết luận từ số liệu khá rõ.", "Vậy nhà đầu tư nhận được gì?", "X là ví dụ gần nhất."). Chạy `slop_check.py -v` và xử lý hết mục SLOP-filler dù chỉ là MINOR. 2. H2/H3 viết dạng danh từ mô tả, giọng báo cáo ("Các loại phí khi đầu tư chứng chỉ quỹ và mức ảnh hưởng đến lợi nhuận", "Cách chọn loại chứng chỉ quỹ theo thời gian đầu tư", "Lợi nhuận thực tế của quỹ cổ phiếu so với VN-Index giai đoạn 2023–2026"); không dùng văn nói ("ăn bao nhiêu lợi nhuận", "khác … ở đâu"), không mở bằng nhãn kiểu "Số liệu 2026:", "Đã quyết định đầu tư:". 3. Không dùng nhân vật persona có tên/tuổi (chị Lan, 38 tuổi…) ở mọi loại bài, kể cả bài so sánh/quyết định; thay bằng "Ví dụ, với 500 triệu …".
- **Phạm vi:** Global

### Số liệu từ tóm tắt tìm kiếm phải đối chiếu bài gốc trước khi vào outline
- **ID:** I103
- **Trạng thái:** ARTICLE
- **Thay bởi:** I110
- **Nguồn:** co-nen-dau-tu-chung-chi-quy
- **Phản hồi từ User:** "Số liệu cũ, sắp 2027 rồi mà vẫn số liệu 2025"
- **Bản năng:** 1. Số liệu quỹ/thị trường lấy qua WebSearch phải mở bài gốc kiểm năm + mốc + nguồn trước khi đưa vào outline: ở bài này tóm tắt tìm kiếm đã sai 3/5 số ("không quỹ nào vượt VN-Index 2025", "0,8% vs 8,6%", "vượt 3–9 điểm %" không có trong nguồn) và gán nhầm bài Fmarket tháng 10/2025 thành 2026. 2. Ưu tiên số trong 12 tháng gần nhất; bài hiệu suất quỹ dùng lợi nhuận 3 năm của Fmarket kèm VN-Index cùng mốc lấy từ `market_facts.py` (cache `hist/VNINDEX:1200`), ghi rõ NAV đã trừ phí còn VN-Index là chỉ số giá. 3. Quy định pháp lý có số tiền (hạn mức bảo hiểm tiền gửi…) phải tra văn bản hiện hành: từ 13/7/2026 hạn mức là 350 triệu VNĐ (Thông tư 05/2026/TT-NHNN), không còn 125 triệu.
- **Phạm vi:** Global
