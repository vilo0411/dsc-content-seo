# Anti-AI Writing Rules — DSC Content System

> **Mục đích:** File này là bộ luật viết bài thực chiến. Mỗi rule đều có ví dụ ❌ BAD → ✅ GOOD để agent tự audit trước khi submit.
> **Bắt buộc:** Mọi agent đọc toàn bộ file này trước khi viết bất kỳ dòng nào.

---

## NGUYÊN TẮC GỐC: AI viết khác người ở chỗ nào?

AI có xu hướng:
1. **Tổng quát hóa** khi có thể cụ thể hóa
2. **Trung lập** khi đáng lẽ phải có lập trường
3. **Liệt kê** khi đáng lẽ phải kể chuyện
4. **Cẩn thận quá mức** → dùng hedge words liên tục ("có thể", "tương đối", "nhìn chung")
5. **Đối xứng giả tạo** → luôn liệt kê "ưu điểm và nhược điểm" đều nhau dù thực tế không đối xứng

---

## PHẦN 1: CẤM — Những pattern phải loại 100%

### 1.1 Trigger Phrases bị cấm (Blacklist)

Bất kỳ đoạn nào chứa các cụm sau → **rewrite ngay, không thương lượng:**

**Mở bài AI điển hình:**
- "Trong kỷ nguyên số ngày nay..."
- "Trong bối cảnh thị trường tài chính ngày càng..."
- "Chứng khoán là một lĩnh vực đầy tiềm năng..."
- "Bạn có bao giờ tự hỏi..."
- "[Keyword] là gì? [Keyword] là..."
- "Thị trường chứng khoán Việt Nam đang trải qua..."
- "Để hiểu rõ hơn về [topic], trước tiên chúng ta cần..."

**Kết bài AI điển hình:**
- "Tóm lại, bài viết đã cung cấp..."
- "Nhìn chung, [topic] là..."
- "Hy vọng bài viết này mang lại kiến thức bổ ích..."
- "Trên đây là toàn bộ thông tin về..."
- "Như vậy có thể thấy rằng..."
- "Qua bài viết này, bạn đã nắm được..."

**Transition AI điển hình:**
- "Hơn nữa, ..." → thay bằng: bắt đầu câu mới trực tiếp
- "Bên cạnh đó, ..." → xóa, viết thẳng
- "Đáng chú ý là ..." → xóa, để thực tế tự nói
- "Không chỉ vậy, ..." → xóa
- "Về cơ bản, ..." → xóa
- "Cốt lõi là ..." → xóa

**Hedge words AI điển hình (dùng quá nhiều):**
- "Tương đối", "khá", "khá là" → thay bằng con số cụ thể
- "Có thể nói rằng" → bỏ, nói thẳng
- "Nhìn một cách tổng quan" → bỏ

---

### 1.2 Emphatic Quotes — Cấm tuyệt đối

Không dùng dấu ngoặc kép cho từ thông thường, tiếng lóng, hay ẩn dụ:

❌ **BAD:** Nhiều nhà đầu tư đã bị "ôm hàng" mà không biết thoát ra.
✅ **GOOD:** Nhiều nhà đầu tư ôm hàng mà không có kế hoạch thoát.

❌ **BAD:** Đây là "điểm vào" lý tưởng cho nhà đầu tư trung hạn.
✅ **GOOD:** Đây là điểm vào lý tưởng cho nhà đầu tư trung hạn.

---

### 1.3 Cấu trúc "Ưu điểm & Nhược điểm" cân bằng giả tạo

AI thường liệt kê 3 ưu - 3 nhược để có vẻ cân bằng. Người viết thật có lập trường.

❌ **BAD:**
> Gửi tiết kiệm ACB có những ưu điểm: lãi suất ổn định, an toàn, dễ tất toán. Tuy nhiên cũng có nhược điểm: lãi suất thấp hơn kênh khác, bị phạt khi rút sớm, không sinh lời vượt trội.

✅ **GOOD:**
> Gửi tiết kiệm ACB phù hợp với người cần chắc chắn — lãi 5.8%/năm kỳ hạn 12 tháng, rủi ro gần như bằng 0. Nếu bạn đang kỳ vọng tăng trưởng 15%+/năm thì đây không phải kênh phù hợp.

---

## PHẦN 2: QUY TẮC 3S — Specific · Story · Statistics

### Rule S1: SPECIFIC — Không có "thông tin chung chung"

Mọi tính từ mô tả phải đi kèm con số hoặc ví dụ cụ thể.

| ❌ Viết vague | ✅ Viết specific |
|---|---|
| "Lãi suất Margin thấp" | "Lãi suất Margin chỉ từ 10% — thấp hơn mức 13–15% phổ biến ở các CTCK lớn" |
| "Quy trình mở tài khoản nhanh" | "Mở tài khoản online qua App DSC Trading trong 3 phút — không cần ra văn phòng" |
| "DSC Trading có nhiều tính năng" | "DSC Trading tích hợp bảng giá real-time, cảnh báo giá qua Zalo và lịch sử giao dịch 2 năm" |
| "Lãi suất tiết kiệm ACB cạnh tranh" | "ACB trả 5.8%/năm cho kỳ hạn 12 tháng gửi online — cao hơn Vietcombank (5.0%) và BIDV (5.1%) cùng kỳ" |
| "Nhà đầu tư F0 thường gặp khó khăn" | "Nhà đầu tư F0 thường mất 3–6 tháng đầu thua lỗ trước khi tìm được phương pháp giao dịch phù hợp" |

---

### Rule S2: STORY — Không miêu tả, hãy đặt người đọc vào tình huống

Thay vì giải thích tính năng, hãy mô tả khoảnh khắc người dùng cần nó.

❌ **BAD (miêu tả tính năng):**
> Tính năng cảnh báo giá của DSC Trading cho phép nhà đầu tư thiết lập ngưỡng cảnh báo tự động.

✅ **GOOD (đặt vào tình huống):**
> 14h45 phiên thứ 3 — VN-Index đang giảm mạnh. Bạn đang họp không thể xem bảng giá. DSC Trading đã gửi cảnh báo vào Zalo lúc 14h47: cổ phiếu HPG chạm vùng hỗ trợ 24.500. Bạn đặt lệnh mua ngay từ điện thoại, không cần mở laptop.

❌ **BAD (giải thích lý thuyết):**
> Nhà đầu tư F0 thường không có kinh nghiệm và cần sự hỗ trợ từ chuyên gia.

✅ **GOOD (ngữ cảnh thực):**
> Tuần đầu tiên mua cổ phiếu, Minh (28 tuổi, kế toán) mua HPG ở đỉnh vì "nghe thấy nhiều người nói". Sau 2 tháng nắm giữ, anh bán lỗ 18%. Đây là lý do DSC thiết kế dịch vụ Môi giới 1:1 — có người hỏi được ngay trước khi đặt lệnh.

---

### Rule S3: STATISTICS — Số liệu phải có nguồn và thời điểm

Không dùng số liệu mơ hồ hoặc không có mốc thời gian.

| ❌ Sai | ✅ Đúng |
|---|---|
| "Nhiều nhà đầu tư đã..." | "Theo UBCKNN, số tài khoản F0 mở mới Q1/2026 đạt 180.000 tài khoản" |
| "Lãi suất đang ở mức cao" | "Lãi suất tiết kiệm kỳ hạn 12 tháng trung bình toàn hệ thống tháng 5/2026: 5.4%/năm" |
| "Cổ phiếu ngành ngân hàng tăng mạnh" | "Cổ phiếu VCB tăng 12% trong 3 tháng đầu 2026, dẫn đầu nhóm ngân hàng" |

**Quan trọng:** Nếu không có số liệu xác thực → DỪNG, không tự điền số. Ghi `[CẦN XÁC NHẬN: nguồn số liệu]` và báo user.

#### Cơ sở dữ liệu chứng khoán tham chiếu chính thức (Cập nhật tháng 8/2026)
Để đảm bảo tính nhất quán và E-E-A-T vượt trội, hãy sử dụng các mốc số liệu thực tế đã được kiểm chứng dưới đây trong các bài viết:
*   **Quy mô tài khoản:** Tính đến tháng 8/2026, tổng số tài khoản chứng khoán toàn thị trường đạt gần **13,66 triệu tài khoản**, trong đó nhà đầu tư cá nhân trong nước chiếm hơn **13,58 triệu tài khoản** (theo số liệu chính thức từ Tổng công ty Lưu ký và Bù trừ chứng khoán Việt Nam - VSDC).
*   **Thanh khoản thị trường:** Giá trị giao dịch khớp lệnh bình quân trên sàn HOSE trong tháng 6–7/2026 dao động quanh mức **15.000 tỷ đồng/phiên**.
*   **Chỉ số thị trường:** Chỉ số VN-Index đóng cửa tháng 7/2026 tại mốc **1.735,78 điểm** và tích lũy/dao động quanh vùng hỗ trợ **1.700 điểm** trong tháng 8/2026.
*   **Kỳ vọng nâng hạng:** Việt Nam đang thực hiện các cải tiến vận hành hệ thống hạ tầng đồng bộ nhằm chuẩn bị đáp ứng tiêu chuẩn nâng hạng lên thị trường mới nổi thứ cấp (Secondary Emerging) của **FTSE Russell** (kỳ vọng thu hút dòng vốn ngoại khoảng **1,5 tỷ USD**).

---

## PHẦN 3: GIỌNG VĂN — POV và Tone

### 3.1 Có lập trường, không trung lập vô vị

Bài viết DSC là bài của chuyên gia tư vấn — phải có ý kiến dựa trên dữ liệu.

❌ **BAD (trung lập AI):**
> Mỗi kênh đầu tư đều có ưu và nhược điểm riêng. Nhà đầu tư cần cân nhắc kỹ trước khi quyết định.

✅ **GOOD (có lập trường):**
> Nếu bạn có vốn dưới 500 triệu và chưa có kinh nghiệm: gửi tiết kiệm 12 tháng là quyết định đúng. Chứng khoán không phải "cờ bạc may rủi", nhưng cũng không phải nơi để thử với tiền chưa có kinh nghiệm quản lý.

---

### 3.2 Xưng hô nhất quán

- **DSC nói với nhà đầu tư:** "Chúng tôi" (DSC) + "Bạn" (nhà đầu tư)
- **Không dùng "họ"** khi nói về DSC trong bài viết của DSC
- **Không dùng "người dùng", "khách hàng"** trong văn xuôi — dùng "nhà đầu tư", "bạn"

---

### 3.3 Mở bài — Đi thẳng vào vấn đề của người đọc

Câu đầu tiên phải trả lời câu hỏi của người đọc hoặc đặt họ vào bối cảnh cụ thể. Không dạo đầu vĩ mô.

**Công thức mở bài hiệu quả:**

| Loại | Ví dụ |
|---|---|
| **Số liệu ngay** | "ACB đang trả 5.8%/năm cho kỳ hạn 12 tháng gửi online — mức cao nhất trong nhóm ngân hàng tư nhân lớn tháng 5/2026." |
| **Câu hỏi thực tế** | "Gửi 500 triệu vào ACB 12 tháng thì nhận được bao nhiêu tiền lãi?" |
| **Tình huống ngay** | "Bạn đang so sánh lãi suất giữa ACB, VPBank và MB — đây là bảng so sánh đầy đủ nhất tháng 5/2026." |

---

### 3.4 Kết bài — Hành động cụ thể, không tổng kết

Kết bài không bao giờ là tóm tắt lại bài viết. Kết bài là CTA hoặc bước tiếp theo.

❌ **BAD:** "Qua bài viết này, bạn đã nắm được lãi suất tiết kiệm ACB mới nhất. Hy vọng thông tin hữu ích."
✅ **GOOD:** "Nếu bạn đang so sánh để chuyển một phần tiết kiệm sang đầu tư, đặt lịch tư vấn với chuyên gia DSC — hoàn toàn miễn phí, không ràng buộc."

---

## PHẦN 4: ĐỊNH DẠNG — Mobile-First

### 4.1 Giới hạn cứng

| Yếu tố | Giới hạn |
|---|---|
| Độ dài câu | Tối đa 30 từ |
| Số câu mỗi đoạn | 2–3 câu |
| Đoạn văn liên tục không có visual | Tối đa 3 đoạn liên tiếp |

**Quy tắc ngắt đoạn theo ngữ nghĩa (Semantic Grouping):**
- Tuyệt đối tránh chia đoạn cơ học (như tách tất cả các câu đơn lẻ thành từng đoạn riêng biệt làm bài viết rời rạc).
- Hãy chủ động gộp các câu có cùng nhóm nội dung, bổ trợ logic cho nhau thành một đoạn văn từ 2-3 câu để bài viết trôi chảy tự nhiên, đồng thời vẫn đáp ứng đúng giới hạn cứng trên.

### 4.2 Định dạng Punctuation cho Bullet Points

- Đối với các nhãn in đậm (bold labels) ở đầu các mục của danh sách (bulleted/numbered lists), bắt buộc sử dụng dấu hai chấm `:` thay vì dấu chấm `.` làm ký tự phân tách nhãn và nội dung câu tiếp theo (Ví dụ: `* **Nhãn**: Nội dung`). Điều này đảm bảo sự đồng bộ trong cấu trúc định dạng.

### 4.3 Khi nào dùng bảng vs. bullet vs. văn xuôi

- **Bảng:** So sánh 2+ lựa chọn có cùng tiêu chí (lãi suất các ngân hàng, phí giao dịch)
- **Bullet:** Danh sách không có thứ tự ưu tiên, không quá 5 điểm
- **Văn xuôi:** Khi kể chuyện, giải thích nguyên nhân-kết quả, hoặc đưa ra nhận định

### 4.4 Không sử dụng đường kẻ ngang (---) giữa các phần/heading

- Tuyệt đối không dùng ký tự `---` (đường phân cách ngang) giữa các tiêu đề (heading) hoặc giữa các phần trong nội dung bài viết (trừ phần YAML front matter ở đầu trang nếu có). Giữa các heading và đoạn văn chỉ sử dụng đúng một dòng trống để phân cách.

---

## PHẦN 5: DSC PRODUCT BRIDGE — Quy tắc dẫn dắt về sản phẩm

### 5.1 Thứ tự ưu tiên sản phẩm theo persona

| Persona | Sản phẩm ưu tiên | Sản phẩm tránh đề xuất |
|---|---|---|
| F0 — nhà đầu tư mới | Mở tài khoản eKYC + Môi giới 1:1 | DSC Invest (ngưỡng 3 tỷ quá cao) |
| Active Trader có kinh nghiệm | Môi giới 1:1 + Margin 10-13.5% | DSC Invest (họ muốn tự giao dịch) |
| Nhà đầu tư vốn lớn (3 tỷ+) | DSC Invest (ủy thác chuyên nghiệp) | — |
| Người đọc bài tiết kiệm ngân hàng | Mở tài khoản eKYC → so sánh lãi suất | DSC Invest (chưa sẵn sàng) |

### 5.2 Cách dẫn dắt tự nhiên, không bán hàng lộ liễu

❌ **BAD (quảng cáo lộ):**
> Nếu bạn muốn sinh lời cao hơn, hãy mở tài khoản DSC ngay hôm nay để nhận ưu đãi đặc biệt!

✅ **GOOD (dẫn dắt bằng giá trị):**
> Lãi suất tiết kiệm ACB 5.8% là mức an toàn tốt. Nếu bạn đã có khoản tiết kiệm ổn định và muốn tối ưu thêm phần vốn "chấp nhận rủi ro hơn", đây là lúc cân nhắc thêm kênh chứng khoán — với sự hỗ trợ của chuyên gia môi giới 1:1 của DSC.

### 5.3 Không so sánh trực tiếp bất lợi cho DSC nếu không có dữ liệu xác thực

Chỉ đưa ra so sánh khi có số liệu cụ thể. Không nói "DSC tốt hơn X" nếu không có bằng chứng.

---

## PHẦN 6: SELF-AUDIT CHECKLIST (Chạy trước khi submit)

Trước khi submit bất kỳ outline hay draft nào, agent phải tự check từng điểm sau:

### Checklist Bắt buộc (FAIL nếu không đạt)

- [ ] **Không có trigger phrase nào trong Blacklist (Phần 1.1)** — grep toàn bộ nội dung
- [ ] **Không có emphatic quotes** cho từ thông thường (Phần 1.2)
- [ ] **H1 chứa target keyword** — khớp chính xác, không paraphrase
- [ ] **Meta description chứa target keyword** + có CTA hoặc benefit cụ thể
- [ ] **Câu đầu tiên không phải opener vĩ mô** (Phần 3.3)
- [ ] **Đoạn kết không phải summary** (Phần 3.4)
- [ ] **Mọi số liệu đều có thời điểm** (tháng/năm) hoặc ghi `[CẦN XÁC NHẬN]`
- [ ] **Sản phẩm DSC được đề xuất đúng persona** (Phần 5.1)

### Checklist Khuyến nghị (Flag nếu không đạt)

- [ ] Có ít nhất 1 đoạn áp dụng Rule S2 (Story/tình huống thực)
- [ ] Câu văn trung bình dưới 20 từ (đếm random 5 đoạn)
- [ ] Không có 2 bullet list liên tiếp mà không có đoạn văn xuôi ở giữa
- [ ] Product Bridge xuất hiện tự nhiên, không phải đoạn riêng biệt "quảng cáo"

---

## PHẦN 7: QUICK REFERENCE — Bảng tra cứu nhanh

| Tình huống | Cần làm |
|---|---|
| Muốn nói "lãi suất cạnh tranh" | Thêm con số: "5.8%/năm — cao hơn trung bình 0.4%" |
| Muốn dùng "Hơn nữa, ..." | Xóa, bắt đầu câu mới trực tiếp |
| Muốn mở bài bằng định nghĩa | Thay bằng số liệu nổi bật hoặc tình huống cụ thể |
| Muốn kết bài bằng "Hy vọng..." | Thay bằng CTA cụ thể: "Mở tài khoản ngay tại [link]" |
| Không có số liệu xác thực | Ghi `[CẦN XÁC NHẬN]`, không tự điền |
| Nhân vật trong story | Đặt tên + tuổi + nghề nghiệp cụ thể (Minh, 28 tuổi, kế toán) |
| So sánh với đối thủ | Chỉ so sánh khi có số liệu nguồn rõ ràng |
| Có nhiều phần giới thiệu ngắn liên tiếp | Gộp thành danh sách liệt kê (bulleted list) thay vì chia nhỏ bằng các tiêu đề H3 |

---

## PHẦN 8: TIÊU CHUẨN GEO/AEO — Tối ưu cho AI Search Engine

> **Mục đích:** Các công cụ AI (Perplexity, ChatGPT Search, Claude, Gemini, Google SGE) khi tổng hợp câu trả lời sẽ ưu tiên trích xuất các câu có thể xác minh, đặc hiệu, và rõ chủ thể. Phần này bổ sung cho — không thay thế — các phần 1–7 ở trên.

---

### 8.1 Mật độ thông tin (Information Density)

**Nguyên tắc:** AI tối ưu theo tỷ lệ:

> `Mật độ thông tin = Số claim có thể xác minh / Tổng số từ`

Câu viết chung chung không chỉ bị xếp hạng thấp — nó **bị loại hoàn toàn** khỏi câu trả lời AI tổng hợp.

**Chỉ thị thực thi:** Trước khi submit, scan từng đoạn văn. Nếu đoạn không chứa ít nhất 1 claim có entity, số liệu, hoặc danh từ riêng → đây là "filler paragraph", phải rewrite hoặc xóa.

❌ **Filler (bị AI bỏ qua):**
> "Thị trường chứng khoán mang lại nhiều cơ hội cho nhà đầu tư có tầm nhìn dài hạn. Việc lựa chọn công ty chứng khoán phù hợp là rất quan trọng để tối ưu lợi nhuận."

✅ **Density (AI trích xuất):**
> "Tính đến tháng 8/2026, phí giao dịch cổ phiếu tại DSC là 0,1% — thấp hơn mức bình quân 0,25% của 10 CTCK lớn nhất theo thống kê UBCKNN. Với danh mục 500 triệu, chênh lệch phí này tiết kiệm 750.000 VNĐ/tháng nếu giao dịch 1 lần/tuần."

---

### 8.2 Load-Bearing Claims — Luận điểm đủ sức nặng

**Quy tắc:** Mỗi H2 phải có ít nhất **1 câu** thoả mãn đồng thời cả 3 điều kiện:

| Điều kiện | Định nghĩa | Kiểm tra |
| :--- | :--- | :--- |
| **(a) Extract-friendly** | AI có thể lift nguyên câu vào câu trả lời mà không cần ngữ cảnh thêm | Câu đứng một mình có nghĩa không? |
| **(b) Verifiable** | Có thể cross-check với nguồn bên ngoài (trang chính thức, báo cáo, UBCKNN) | Có tên nguồn hoặc tổ chức phát hành không? |
| **(c) Specific** | Có entity, con số, hoặc danh từ riêng — không có từ định tính mơ hồ | Thay được bằng con số/tên cụ thể chưa? |

**Ví dụ thực tế (lĩnh vực tài chính DSC):**

| # | ❌ Không đạt — AI bỏ qua | ✅ Đạt chuẩn — AI trích xuất |
| :--- | :--- | :--- |
| 1 | "DSC cung cấp mức phí giao dịch cạnh tranh so với thị trường." | "DSC thu phí giao dịch cổ phiếu từ 0,1%/lệnh — thấp hơn mức phí tối thiểu 0,15% của SSI và VNDS (tháng 8/2026)." |
| 2 | "VN-Index đã tăng mạnh trong thời gian gần đây nhờ dòng tiền từ nhà đầu tư F0." | "VN-Index đóng cửa tháng 7/2026 tại 1.735,78 điểm, tăng 8,2% so với đầu năm — theo số liệu HOSE." |
| 3 | "Mở tài khoản chứng khoán tại DSC rất đơn giản và nhanh chóng." | "DSC cho phép mở tài khoản eKYC qua App DSC Trading trong 3 phút — không cần ra văn phòng, xác thực bằng CCCD có chip." |

> **Lưu ý:** Rule S3 (Phần 2) đã yêu cầu nguồn + thời gian. GEO bổ sung yêu cầu câu phải **extract-friendly** — có thể đứng độc lập, không cần ngữ cảnh.

---

### 8.3 Temporal Marker — Mốc thời gian bắt buộc

**Format chuẩn:** Mọi data point số liệu phải dùng một trong 2 format:
- `"Tính đến tháng [M/Y], ..."` — cho số liệu tích lũy hoặc trạng thái hiện tại
- `"Tháng [M/Y]: ..."` — cho dữ liệu snapshot của một mốc cụ thể

**CẢNH BÁO LẠM DỤNG & CẬP NHẬT THỜI GIAN (BẮT BUỘC TUÂN THỦ):**
- **Cập nhật thời gian thực tế:** Hiện tại là **tháng 9/2026** (hoặc quý/năm thực tế tại thời điểm viết bài). Tuyệt đối không dùng lại mốc cũ gượng ép (như tháng 8/2026).
- **Không tự chế hoặc chèn bừa bãi** các mốc thời gian giả tạo (như `"Tính đến tháng 9/2026,"`, `"Theo thông tin phân tích cập nhật..."`) trước các định nghĩa kinh điển, khái niệm lý thuyết, hoặc các câu giải thích chung không chứa số liệu.
- **Chỉ sử dụng mốc thời gian khi thực sự có số liệu/dữ liệu thực tế** cần xác thực tính cập nhật (ví dụ: lãi suất tiết kiệm, số lượng tài khoản, biểu phí giao dịch, hoặc quy định pháp lý có ngày có hiệu lực thực tế) và phải viết thành câu tự nhiên (ví dụ: `"Năm 2026, HPG mở rộng dự án Dung Quất 2..."`).
- Việc lặp đi lặp lại cụm từ `"Tính đến tháng..."` một cách máy móc ở đầu câu/đoạn văn sẽ làm bài viết bị gượng ép, giảm chất lượng trôi chảy và tạo văn phong AI.

**Blacklist bổ sung** (thêm vào Phần 1.1):

| ❌ Cấm dùng | ✅ Thay bằng |
| :--- | :--- |
| "Gần đây, lãi suất tiết kiệm..." | "Tháng 9/2026, lãi suất tiết kiệm kỳ hạn 12 tháng..." |
| "Trong những năm qua, thị trường..." | "Từ 2021 đến 2026, VN-Index đã..." |
| "Hiện nay, DSC đang cung cấp..." | "DSC đang áp dụng phí giao dịch..." (hoặc "Năm 2026, DSC áp dụng...") |
| "Thời gian gần đây có nhiều F0..." | "Trong Q1–Q2/2026, số tài khoản F0 mở mới đạt..." |

> **Ghi chú:** S3 đã yêu cầu tháng/năm — GEO chuẩn hóa format để AI parse được mốc thời gian, nhưng phải đảm bảo tính tự nhiên và chính xác theo mốc thời gian hiện tại.

---

### 8.4 Subject-Verb Clarity — Chủ thể rõ ràng

**Quy tắc:** Brand, sản phẩm, hoặc tổ chức phải là **chủ từ trực tiếp** của câu. Tránh cấu trúc bị động che khuất thực thể, vì AI khó xác định chủ thể của claim.

❌ **BAD — Chủ thể mờ:**
> "Mức phí giao dịch được áp dụng tại DSC là 0,1%."
> "Tài khoản có thể được mở trong vòng 3 phút thông qua ứng dụng di động."
> "Dịch vụ môi giới 1:1 đang được nhiều nhà đầu tư lựa chọn."

✅ **GOOD — Chủ thể rõ:**
> "DSC thu phí giao dịch 0,1%/lệnh — thấp hơn mức trung bình 0,25% của 5 CTCK lớn (tháng 8/2026)."
> "DSC cho phép mở tài khoản eKYC trong 3 phút qua App DSC Trading."
> "Nhà đầu tư P2–P3 chọn Môi giới 1:1 của DSC vì được tư vấn trước mỗi lệnh."

**Pattern cần tránh:** "được [động từ] bởi/tại/qua" khi brand/entity là tác nhân thực sự.

---

### 8.5 Bổ sung vào Self-Audit Checklist (Phần 6)

> Các items dưới đây được thêm vào **Checklist Bắt buộc** của Phần 6. Agent phải check trước mọi lần submit.

- [ ] **Mỗi H2 có ít nhất 1 Load-Bearing Claim** thoả mãn 3 điều kiện: Extract-friendly + Verifiable + Specific (Phần 8.2)
- [ ] **Mọi data point có prefix mốc thời gian chuẩn** "Tính đến tháng M/Y" hoặc "Tháng M/Y:" — không dùng "Gần đây", "Trong những năm qua", "Hiện nay" không có ngày (Phần 8.3). **Chỉ dùng khi có số liệu/dữ liệu thực tế, tuyệt đối không tự chế mốc thời gian cho câu định nghĩa, giải thích lý thuyết chung.**
- [ ] **Chủ thể câu là brand/entity cụ thể**, không dùng cấu trúc bị động che khuất thực thể (Phần 8.4)

---

### 8.6 Bổ sung vào Quick Reference (Phần 7)

| Tình huống | Cần làm |
| :--- | :--- |
| Muốn viết "Hiện nay lãi suất..." | Thêm mốc: "Tháng 8/2026, lãi suất..." |
| H2 không có claim cứng (chỉ có mô tả chung) | Bắt buộc thêm 1 Load-Bearing Claim trước khi submit (Phần 8.2) |
| Câu bị động che thực thể ("được áp dụng tại") | Đổi thành: "[Brand] + động từ chủ động + số liệu" (Phần 8.4) |

---

*Last updated: 2026-08-21 | Phiên bản 2.1 — Thêm Phần 8: GEO/AEO Optimization*
