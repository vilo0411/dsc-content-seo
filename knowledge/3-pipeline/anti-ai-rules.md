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
| Độ dài câu | Tối đa 25 từ |
| Số câu mỗi đoạn | 2–3 câu |
| Đoạn văn liên tục không có visual | Tối đa 3 đoạn liên tiếp |

### 4.2 Khi nào dùng bảng vs. bullet vs. văn xuôi

- **Bảng:** So sánh 2+ lựa chọn có cùng tiêu chí (lãi suất các ngân hàng, phí giao dịch)
- **Bullet:** Danh sách không có thứ tự ưu tiên, không quá 5 điểm
- **Văn xuôi:** Khi kể chuyện, giải thích nguyên nhân-kết quả, hoặc đưa ra nhận định

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

---

*Last updated: 2026-05-15 | Phiên bản 2.0 — Rewrite toàn bộ từ v1.0 (chỉ có rules cơ bản)*
