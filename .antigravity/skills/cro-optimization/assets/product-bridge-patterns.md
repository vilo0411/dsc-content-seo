# Product Bridge Patterns

> Đoạn **2–3 câu, mỗi câu ≤ 30 từ** chuyển từ kiến thức bài đang nói sang lý do DSC giải quyết được việc đó. Đứng ngay trước banner CTA.
> **Luận điểm không tự nghĩ** — lấy từ `knowledge/1-brand/personas.md` → `### DSC Product Bridge` của persona bài đó.
> Đây là văn xuôi → chịu toàn bộ `knowledge/3-pipeline/anti-ai-rules.md`.

---

## Bảng tra nhanh theo persona

| Persona | Góc dẫn dắt (nguyên văn từ `personas.md`) | Sản phẩm được nhắc | Tránh |
| :--- | :--- | :--- | :--- |
| **P1 Tiết kiệm** | "Dành một phần nhỏ tiết kiệm để thử — có chuyên gia DSC đồng hành" | eKYC + Môi giới 1:1 | DSC Invest (ngưỡng 3 tỷ) |
| **P2 F0** | "Không cần biết hết mới bắt đầu — có chuyên gia DSC ở đó khi bạn cần hỏi" | eKYC (3 phút) + Môi giới 1:1 | DSC Invest |
| **P3 Active Trader** | "Phí margin thấp hơn + chuyên gia phân tích IB level — không phải chatbot, không phải call center" | Môi giới 1:1 + Margin 10–13.5% | DSC Invest (họ muốn tự giao dịch); **CTA aggressive kiểu "mở tài khoản ngay"** |
| **P4 Vốn lớn** | "Năng lực IB của DSC — đối tác quản lý tài sản, không phải môi giới bán lẻ" | DSC Invest (1.5%/năm + 20% profit share trên 8%) | Push DSC Invest ngay trong bài informational; nội dung kiểu hướng dẫn F0 |

---

## ⚠️ Giới hạn hiện tại: chỉ có một offer

Hệ thống mới chỉ có một đích đến: `https://www.dsc.com.vn/mo-tai-khoan`. Điều này khớp tốt với P1/P2 nhưng **lệch với P3 và P4**:

- `personas.md` quy định CTA của P3 là *"Trao đổi với chuyên gia"*, P4 là *"Đặt lịch tư vấn"*.
- Nút ghi "Đặt lịch tư vấn" mà dẫn tới trang mở tài khoản là **lời hứa lệch đích** — người đọc bấm vào thấy form đăng ký, thoát ngay. Hại chuyển đổi hơn là không có nút.

**Quy tắc xử lý cho tới khi có thêm landing page:**

| Persona | Banner |
| :--- | :--- |
| P1 | `slim-inline`, copy mềm, nói đúng là mở tài khoản |
| P2 | `primary-midarticle` + `closing` — đầy đủ |
| P3 | Tối đa 1 banner `slim-inline`. Không dùng "ngay". Nói thẳng về phí margin / môi giới, không hứa "trao đổi chuyên gia" |
| P4 | **Không banner.** Chỉ link text trong Product Bridge. Chờ có landing page đặt lịch tư vấn |

Khi có thêm URL (đặt lịch tư vấn, trang DSC Invest, trang margin) → cập nhật `.antigravity/rules/cta-conversion.md` mục 1 và bảng trên.

---

## Khuôn đoạn (cấu trúc, không phải văn mẫu)

Không copy nguyên văn — đây là bộ khung. Nội dung cụ thể phải bám vào chủ đề bài.

### A. Từ khái niệm → hành động (bài "X là gì")
1. Câu nối: điều vừa giải thích chỉ có giá trị khi đem ra dùng thật.
2. Câu ma sát: nêu đúng rào cản của persona (P2: sợ chưa biết đủ; P1: sợ mất gốc).
3. Câu cầu: góc dẫn dắt của persona, gắn với sản phẩm được phép nhắc.

### B. Từ quy trình → công cụ (bài "cách…", "hướng dẫn…")
1. Câu nối: các bước trên cần một tài khoản/công cụ để thực hiện.
2. Câu khác biệt: một điểm cụ thể của DSC liên quan tới đúng việc bài đang hướng dẫn.
3. Câu hạ ma sát: con số thật (3 phút, online, miễn phí mở tài khoản).

### C. Từ so sánh → lựa chọn (bài "A vs B", "nên chọn…")
1. Câu chốt: bài đã cho tiêu chí, quyết định vẫn thuộc về người đọc.
2. Câu định vị: DSC đứng ở đâu theo chính tiêu chí vừa nêu — **không** tự tuyên bố là tốt nhất.
3. Câu mời: bước tiếp theo nhỏ, không cam kết lớn.

### D. Từ rủi ro → an toàn (bài về lỗi, thua lỗ, cảnh báo)
1. Câu thừa nhận: rủi ro là thật, không nói giảm.
2. Câu giảm thiểu: cái gì giúp giảm rủi ro đó (môi giới 1:1, công cụ).
3. Câu mời: thận trọng, không hứa hẹn kết quả.

---

## Cấm

- Bịa số liệu sản phẩm. Chỉ dùng con số đã có trong `personas.md` / `profile.md`. Không chắc → không nêu.
- Cam kết lợi nhuận dưới mọi hình thức (vi phạm pháp lý — `personas.md:250`).
- Tuyên bố so sánh hơn kém không dẫn nguồn ("phí thấp nhất thị trường").
- Mở đoạn bằng câu chuyển vô nghĩa kiểu "Nếu bạn đang tìm kiếm...", "Hiểu được điều đó,...".
- Nhắc sản phẩm nằm trong cột "Tránh" của persona.
- Quá **3 câu** trong một đoạn — `qa_lint` bắt `CL6-paragraph`, và đoạn dài thành quảng cáo, mất tin cậy.
- Câu quá **30 từ** — `qa_lint` bắt `CL6-sentence`. Tách câu thay vì nối bằng dấu phẩy.
