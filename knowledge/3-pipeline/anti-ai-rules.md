# Anti-AI Writing Rules — DSC (v3.0, 2026-11-09)

> **Phần phán đoán máy không bắt được.** Đọc 1 lần/session trước khi viết.
> Máy đã bắt (không cần nhớ, sửa theo báo lỗi): cụm từ cấm, hedge, từ cường điệu → `anti-ai-rules-blacklist.md` (qa_lint `CL2-*`) · định dạng, độ dài câu/đoạn, link → qa_lint `CL6-*` / `FMT-*` / `LINK-*` · nhịp câu, mật độ bằng chứng → `slop_check.py` · số liệu chỉ số/mã → `market_facts.py --verify`. Chạy cả 3 bằng `python scripts/qa_gate.py <draft>`.
> Rule học từ phản hồi user nằm ở `instincts.md` (sapo I105, heading I107, Kết luận I113…). File này không lặp lại chúng.
> Bản cũ đầy đủ ví dụ: `knowledge/3-pipeline/archive/anti-ai-rules-v2.2-2026-10-16.md`.

## 0. AI viết khác người ở đâu

1. **Tổng quát** khi có thể cụ thể → mọi tính từ cần con số hoặc ví dụ (§2 S1).
2. **Trung lập** khi phải có lập trường → nói rõ ai nên, ai không nên (§3.1).
3. **Liệt kê** khi cần lập luận → nối nguyên nhân – hệ quả bằng văn xuôi.
4. **Rào đón** ("có thể", "tương đối") → thay bằng số (lint `CL2-hedge`).
5. **Đối xứng giả** → ưu/nhược theo thực tế, không ép đều (§1.3).

## 1. Cấm

### 1.1 Cụm từ cấm
Danh sách ở `anti-ai-rules-blacklist.md`; qa_lint báo `CL2-blacklist` / `CL2-softban` / `CL2-hedge`. Gặp cụm sáo mới mà lint chưa bắt → thêm vào blacklist (qua `/learn`), không ghi vào đây.

### 1.2 Ngoặc kép nhấn mạnh
Không bọc từ thường, tiếng lóng, ẩn dụ trong ngoặc kép (lint `CL2-quotes`).
❌ Nhiều nhà đầu tư bị "ôm hàng". ✅ Nhiều nhà đầu tư ôm hàng mà không có kế hoạch thoát.

### 1.3 Ưu điểm & nhược điểm cân bằng giả tạo
AI liệt kê 3 ưu – 3 nhược cho có vẻ khách quan. Người viết thật có lập trường.
❌ Gửi tiết kiệm có ưu điểm: ổn định, an toàn, dễ tất toán. Tuy nhiên có nhược điểm: lãi thấp, bị phạt khi rút sớm, không sinh lời vượt trội.
✅ Gửi tiết kiệm hợp với người cần chắc chắn: lãi 5,8%/năm kỳ hạn 12 tháng, rủi ro gần như bằng 0. Kỳ vọng 15%/năm trở lên thì đây không phải kênh phù hợp.
*Ngoại lệ — bài Toplist (I120):* mỗi mục có Ưu / Nhược là khung của thể loại, không tính là đối xứng giả, miễn mỗi ý là 1 dữ kiện đã xác minh và số ưu – nhược không ép bằng nhau.

## 2. Quy tắc 3S

### S1 — Specific: tính từ nào cũng phải có số hoặc ví dụ
| ❌ Mơ hồ | ✅ Cụ thể |
|---|---|
| Lãi suất margin thấp | Lãi suất margin từ 10%/năm, thấp hơn mức 13–15% phổ biến ở các CTCK lớn |
| Mở tài khoản nhanh | Mở tài khoản eKYC trên App DSC Trading trong 3 phút, không cần ra văn phòng |
| F0 thường gặp khó khăn | Nhà đầu tư mới thường thua lỗ 3–6 tháng đầu trước khi có phương pháp riêng |

### S2 — Story: đặt người đọc vào tình huống, không mô tả tính năng
❌ Tính năng cảnh báo giá cho phép thiết lập ngưỡng cảnh báo tự động.
✅ 14h45, VN-Index giảm mạnh trong lúc bạn đang họp. App gửi cảnh báo: HPG chạm vùng hỗ trợ 24.500 đồng. Bạn đặt lệnh từ điện thoại, không cần mở máy tính.
Tình huống dùng con số và thời điểm, **không dùng nhân vật có tên/tuổi/nghề** (instinct I108): viết "Ví dụ, với 500 triệu …".

### S3 — Statistics: số liệu có nguồn và thời điểm
- Số thị trường lấy từ `python scripts/market_facts.py --brief`, sự kiện có ngày từ `news_feed.py` — **không viết số theo trí nhớ**, không dùng bộ số "tham chiếu" cố định (bản cũ có VN-Index 7/2026, 13,66 triệu tài khoản: đã bị chèn vào 14 bài không liên quan, lint `DATA-boilerplate`).
- Số lấy qua WebSearch/AI Overview: mở bài gốc kiểm năm, mốc, nguồn (I110).
- Không có số xác thực cho một claim → bỏ claim, hoặc ghi `[CẦN XÁC NHẬN: …]` và báo user. Không tự điền.

## 3. Giọng văn

### 3.1 Có lập trường
Bài DSC là ý kiến chuyên gia dựa trên dữ liệu.
❌ Mỗi kênh đầu tư đều có ưu và nhược điểm riêng, nhà đầu tư cần cân nhắc kỹ.
✅ Vốn dưới 500 triệu và chưa có kinh nghiệm: gửi tiết kiệm 12 tháng là lựa chọn đúng lúc này. Chứng khoán không phải nơi thử với khoản tiền bạn chưa biết quản lý.

### 3.2 Xưng hô
DSC nói với nhà đầu tư: "chúng tôi" (DSC) + "bạn". Không gọi DSC là "họ". Trong văn xuôi dùng "nhà đầu tư", "bạn", không dùng "người dùng", "khách hàng".

### 3.3 Mở bài
Câu đầu trả lời thẳng câu hỏi của người đọc hoặc đặt họ vào bối cảnh cụ thể; không dạo đầu vĩ mô. Cấu trúc sapo: instinct I105.
| Kiểu | Ví dụ |
|---|---|
| Số liệu ngay | ACB trả 5,8%/năm kỳ hạn 12 tháng gửi online, cao nhất nhóm ngân hàng tư nhân lớn tháng 11/2026. |
| Câu hỏi thực tế | Gửi 500 triệu vào ACB 12 tháng thì nhận bao nhiêu tiền lãi? |

### 3.4 Kết bài
H2 "Kết luận": 1 nhận định + checklist hành động 3 mục + CTA có link mở tài khoản (I113). Kết luận tóm **insight**, không kể lại bài ("Qua bài viết này, bạn đã nắm được…" là cụm cấm).
✅ Nếu bạn đang cân nhắc chuyển một phần tiết kiệm sang đầu tư, hãy bắt đầu với 10–20% số tiền và hỏi chuyên gia Môi giới 1:1 của DSC trước lệnh đầu tiên.

## 4. Định dạng
Giới hạn cứng (câu ≤ 30 từ, đoạn 2–3 câu, ≤ 3 đoạn văn liền nhau không có bảng/list, nhãn đậm đầu bullet dùng ":", không `---`) do qa_lint kiểm. Phần phán đoán:
- **Bảng:** so sánh 2+ lựa chọn cùng tiêu chí (lãi suất, phí). **Bullet:** danh sách không thứ tự, ≤ 5 ý (trừ danh sách các bước / list nhắm Featured Snippet: 6–8 mục). **Văn xuôi:** lập luận nguyên nhân – kết quả, nhận định, tình huống.
- Ngắt đoạn theo ý: các câu cùng một ý ở chung đoạn, không tách mỗi câu một đoạn.

## 5. DSC Product Bridge

### 5.1 Sản phẩm theo persona
| Persona | Ưu tiên | Tránh |
|---|---|---|
| F0 — nhà đầu tư mới | eKYC + Môi giới 1:1 | DSC Invest (ngưỡng 3 tỷ) |
| Nhà đầu tư chủ động | Môi giới 1:1 + margin 10–13,5%/năm | DSC Invest |
| Vốn lớn (3 tỷ trở lên) | DSC Invest (ủy thác) | — |
| Người đọc bài tiết kiệm | eKYC → so sánh lãi suất | DSC Invest |

### 5.2 Dẫn dắt bằng giá trị, không quảng cáo
❌ Mở tài khoản DSC ngay hôm nay để nhận ưu đãi đặc biệt!
✅ Lãi tiết kiệm 5,8% là mức an toàn tốt. Khi đã có quỹ dự phòng và muốn tối ưu phần vốn chấp nhận rủi ro cao hơn, đây là lúc cân nhắc thêm kênh chứng khoán, với sự hỗ trợ của chuyên gia Môi giới 1:1 tại DSC.
Cấu trúc đoạn Bridge: instinct I112. Sản phẩm DSC thật có: I111.

### 5.3 So sánh với đối thủ
Chỉ so sánh khi có số liệu nguồn công khai. Không viết "DSC tốt hơn X" nếu không có bằng chứng.

## 6. Self-audit ngữ nghĩa (sau khi `qa_gate.py` PASS)
- [ ] Mỗi H2 có ≥ 1 Load-Bearing Claim (§8.2) và mỏ neo đúng ý định H2 (§8.7a), không nhồi số cho đủ (§8.7b)
- [ ] Có lập trường (§3.1), không ưu/nhược đối xứng giả (§1.3)
- [ ] Câu đầu trả lời thẳng (§3.3); Kết luận là insight + hành động (§3.4)
- [ ] Sản phẩm DSC đúng persona (§5.1); Bridge nối từ vấn đề bài vừa phân tích (I112)
- [ ] Chủ thể câu là brand/entity, không bị động che chủ thể (§8.4)
- [ ] Mốc thời gian chỉ gắn với số liệu (§8.3); có ≥ 1 mốc trong 18 tháng (§8.7d)

## 8. GEO/AEO — câu AI search trích được

### 8.1 Mật độ thông tin
Đoạn văn không có ít nhất 1 claim có entity, con số hoặc danh từ riêng là đoạn đệm → viết lại hoặc xoá.
❌ Lựa chọn công ty chứng khoán phù hợp là rất quan trọng để tối ưu lợi nhuận.
✅ Phí giao dịch 0,1% so với 0,25% chênh 750.000 đồng mỗi tháng với danh mục 500 triệu giao dịch mỗi tuần một lần.

### 8.2 Load-Bearing Claim
Mỗi H2 có ≥ 1 câu đồng thời: **(a)** đứng một mình vẫn đủ nghĩa · **(b)** kiểm chứng được (có tên nguồn/tổ chức) · **(c)** có entity, con số hoặc danh từ riêng.
❌ Mở tài khoản tại DSC rất đơn giản và nhanh chóng.
✅ DSC cho phép mở tài khoản eKYC qua App DSC Trading trong 3 phút bằng CCCD gắn chip.

### 8.3 Mốc thời gian
- Gắn mốc ("tháng 11/2026", "năm 2026", "ngày 18/5/2026") **chỉ** vào câu có số liệu biến động hoặc quy định có ngày hiệu lực. Viết thành câu tự nhiên, không bắt buộc mẫu "Tính đến tháng …".
- Không gắn mốc vào định nghĩa, lý thuyết, quy định chung; không lặp mốc đầu mỗi câu/H2 (lint `GEO-overuse`).
- Thay mốc mơ hồ ("gần đây", "hiện nay", "trong những năm qua") bằng mốc thật (lint `GEO-vague-time`).

### 8.4 Chủ thể rõ ràng
Brand, sản phẩm, tổ chức là chủ ngữ trực tiếp. Tránh "được [động từ] tại/bởi/qua" khi brand là tác nhân.
❌ Mức phí được áp dụng tại DSC là 0,1%. ✅ DSC thu phí giao dịch từ 0,1% giá trị lệnh.

### 8.7 Mỏ neo dữ liệu, nhịp câu, độ tươi (cách sửa lỗi `SLOP-*` / `FACT-*`)
**(a) Mỏ neo theo ý định H2** — mỗi H2 nội dung ≥ 1 mỏ neo thuộc về chính claim của câu:
| Ý định H2 | Mỏ neo |
|---|---|
| Định nghĩa | Pháp lý/cấu trúc: Luật Chứng khoán, biên độ, T+2, lô 100 cp |
| Phân loại | Ngưỡng hoặc kỳ hạn phân biệt các nhóm |
| So sánh, "có nên" | **Bắt buộc** số so sánh có nguồn |
| Hướng dẫn | Mốc quy trình: giờ phiên, số bước, thời hạn |
| Rủi ro | Biên độ thiệt hại, ngưỡng call margin, ví dụ lịch sử có ngày |
| Bối cảnh thị trường | Dữ liệu sống kèm ngày (`market_facts.py --brief`) |
| Product Bridge | Thông số sản phẩm: phí từ 0,1%, margin 10–13,5%/năm, eKYC 3 phút |

**(b)** Không nhồi số không liên quan claim để qua lint ("Trên sàn HOSE biên độ 7%, cổ phiếu là chứng chỉ sở hữu…"). H2 định nghĩa thuần chỉ cần 1 mỏ neo cấu trúc.
**(c) Nhất quán thước đo:** đỉnh/đáy chỉ số ghi rõ giá đóng cửa (mặc định) hay intraday — VN-Index 2022: 1.529 đóng cửa, 1.536 intraday.
**(d) Độ tươi:** bài có số thị trường cần ≥ 1 mốc trong 18 tháng; mốc cũ ghi bối cảnh ("đỉnh chu kỳ 2022"), không gọi "đỉnh lịch sử" (`FACT-stale`).
**(e) Mất nguồn (exit 3):** dùng dữ kiện cấu trúc: biên độ HOSE 7% / HNX 10% / UPCoM 15%, T+2, lô 100 cp, ATO 9h00–9h15, ATC 14h30–14h45. Không bịa giá.
**(f) Nhịp câu:** cứ 3–4 câu dài có ≥ 1 câu ≤ 7 từ, và câu ngắn phải mang dữ kiện (I108). Đặt sau chuỗi giải thích hoặc trước kết luận.
**(g) Không lặp khung H2** của bài đã có (> 55% trùng = template cũ đổi chủ đề, `SLOP-template`); trừ series có chủ ý (`cach-mua-co-phieu-<mã>`).

| Lỗi máy báo | Sửa |
|---|---|
| `SLOP-rhythm` / `SLOP-burstiness` / `SLOP-uniform-run` | Chèn câu 3–7 từ có dữ kiện mỗi 3–4 câu dài; gộp/cắt câu để đổi nhịp (§8.7f) |
| `SLOP-evidence` / `SLOP-anchor` | Thêm mã CP, mốc tháng/năm, % thật vào đúng claim đang thiếu (§8.7a) |
| `SLOP-filler` / `SLOP-vague` | Xoá câu nhận xét rỗng hoặc thay bằng câu có dữ kiện |
| `SLOP-template` | Đổi khung H2 theo intent thật của keyword (§8.7g) |
| `FACT-index-wrong` / `FACT-ticker` | Sửa bắt buộc theo số `market_facts.py` |
| `FACT-stale` | Thêm 1 mốc trong 18 tháng gần nhất (§8.7d) |

*v3.0 (2026-11-09): bỏ phần lint đã kiểm, bỏ bộ số tham chiếu cũ, thống nhất với instincts (Kết luận, không nhân vật có tên, mốc thời gian tự nhiên). Bản v2.2: `archive/anti-ai-rules-v2.2-2026-10-16.md`.*
