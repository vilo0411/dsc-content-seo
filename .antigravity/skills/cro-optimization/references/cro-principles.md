# CRO Principles — tra cứu khi viết copy CTA

> Rule cứng ở `.antigravity/rules/cta-conversion.md`. File này là phần diễn giải + công thức, đọc khi cần viết copy.

---

## 1. Công thức headline

```
[Kết quả người đọc nhận được] + [rào cản được gỡ bỏ]
```

Kiểm tra bằng một câu hỏi: **thay "DSC" bằng tên đối thủ, câu này còn đúng không?** Nếu còn đúng → headline rỗng, viết lại.

| ✗ | Vì sao hỏng |
| :--- | :--- |
| "Đầu tư chứng khoán cùng DSC" | Brand-centric. Không nói người đọc nhận được gì |
| "Giải pháp đầu tư toàn diện" | Sáo rỗng, đúng với mọi công ty |
| "Bạn đã sẵn sàng đầu tư chưa?" | Câu hỏi tu từ — `anti-ai-rules.md` cấm |

| ✓ | Vì sao được |
| :--- | :--- |
| "Mở tài khoản trong 30 giây, bắt đầu với số vốn bạn có" | Có kết quả + gỡ rào cản "cần nhiều tiền" |
| "Đặt lệnh thật để hiểu, không cần đọc thêm bài nào nữa" | Gắn thẳng vào ngữ cảnh bài kiến thức |

Headline nên nhắc lại chủ đề bài. Banner trong bài "lệnh ATO là gì" khác banner trong bài "chọn quỹ mở".

## 2. Dòng phụ — ba yếu tố giảm ma sát

Chọn tối đa 3, cách nhau bằng `•`. Mỗi cái phải trả lời một nỗi lo có thật:

| Nỗi lo | Yếu tố |
| :--- | :--- |
| "Tốn tiền không?" | Mở tài khoản miễn phí |
| "Mất thời gian không?" | Online 100%, không cần ra quầy |
| "Sai thì sao?" | Hỗ trợ 24/7 · môi giới 1:1 |
| "Phức tạp không?" | eKYC bằng CCCD |

Chỉ nêu điều đúng. Không chắc một con số → bỏ, đừng làm tròn cho đẹp.

## 3. Nút

`[Động từ] + [tính tức thì hoặc chi phí thấp]`

- ✓ "Mở tài khoản — 3 phút", "Bắt đầu miễn phí"
- ✗ "Xem thêm", "Tại đây", "Tìm hiểu", "Chi tiết", "Click vào đây" (lint bắt qua `GENERIC_ANCHORS`)

Nút phải hứa **đúng thứ URL giao**. Xem phần giới hạn một-offer trong `assets/product-bridge-patterns.md`.

## 4. Vị trí

Người đọc chỉ nhận lời mời sau khi đã nhận ra vấn đề. Thứ tự bắt buộc: **hiểu vấn đề → thấy giải pháp → được mời**.

- Banner trong 25% đầu bài informational: người đọc chưa nhận ra vấn đề → bị coi là quảng cáo chen ngang.
- Điểm tốt nhất giữa bài: ngay sau section giải quyết xong nỗi đau chính, khi người đọc vừa thấy "à, hoá ra là vậy".
- Kết bài: `anti-ai-rules.md:174` — kết bài phải là CTA hoặc bước tiếp theo, không phải tóm tắt.
- Hai banner cách nhau < 300 từ → cảm giác bị ép.

## 5. Sinh biến thể A/B

Mỗi biến thể chỉ đổi **một** biến, nếu không sẽ không biết cái gì tạo ra khác biệt:

| Biến | Ví dụ hai đầu |
| :--- | :--- |
| Trục headline | Lợi ích đạt được ↔ Rủi ro tránh được |
| Cường độ nút | "Mở tài khoản — 3 phút" ↔ "Tìm hiểu cách mở" |
| Yếu tố giảm ma sát | Nhấn chi phí ↔ nhấn tốc độ |
| Vị trí | Giữa bài ↔ chỉ kết bài |

Không UTM thì không tách được biến thể trong cùng một bài — chỉ so được sequential (trước/sau). Cần tách số → bật `--utm`.

## 6. Checklist trước khi chèn

- [ ] Headline không chứa tên brand ở vị trí chủ ngữ; thay tên đối thủ vào thì sai
- [ ] Headline gắn với chủ đề bài, không dùng chung cho mọi bài
- [ ] Dòng phụ ≤ 3 yếu tố, mọi con số kiểm chứng được
- [ ] Text nút không nằm trong danh sách chung chung
- [ ] Nút hứa đúng thứ URL giao
- [ ] Cường độ khớp persona (`personas.md` — ma trận CTA)
- [ ] Không nhắc sản phẩm trong cột "Tránh" của persona
- [ ] Banner đứng sau đoạn Product Bridge, không mồ côi
- [ ] Không nằm trong 25% đầu bài informational
- [ ] Palette đúng, tương phản ≥ 4.5:1, không màu đỏ
- [ ] Không còn placeholder `{{...}}`
- [ ] `python scripts/qa_lint.py <file> --cta` sạch
