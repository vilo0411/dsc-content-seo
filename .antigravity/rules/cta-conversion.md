# Rule: CTA & Conversion (CRO)

> **Phạm vi:** Mọi bài trong `knowledge/4-content/`. Áp dụng cho `/cro`, `/write`, `/optimize`, `/link`, `/drafting`.
> **Nguồn sự thật duy nhất** về CTA. Các skill khác chỉ được tham chiếu file này, không phát biểu lại rule.

---

## 1. Offer

Chỉ **một** offer: mở tài khoản chứng khoán DSC — `https://www.dsc.com.vn/mo-tai-khoan`.

Không tự bịa offer khác (ebook, khoá học, hotline) trừ khi người dùng cung cấp link cụ thể.

---

## 2. Số lượng & vị trí

| Thành phần | Bắt buộc | Vị trí |
| :--- | :--- | :--- |
| Link text mở tài khoản | ≥ 1 | Trong thân bài, đặt tự nhiên trong câu |
| Banner CTA | 1–2 | 1 mid-article (sau Product Bridge) + 1 kết bài |

**Cấm:**
- Banner nằm trong **25% đầu thân bài** với bài informational (dạng "X là gì", "cách…"). Người đọc chưa nhận ra vấn đề thì chưa bán được.
- **Banner mồ côi** — banner không có đoạn văn dẫn ngay trước nó. Banner phải là kết quả của một mạch lập luận, không rơi đột ngột giữa bài.
- Quá 2 banner trong một bài.
- Hai banner đặt liền nhau, hoặc cách nhau dưới 300 từ.

---

## 3. Product Bridge (đoạn dẫn trước banner)

Mỗi banner mid-article phải đứng sau một đoạn Product Bridge: **2–3 câu** chuyển từ kiến thức bài đang nói sang lý do DSC giải quyết được việc đó.

Giới hạn cứng do `qa_lint.py` áp: **tối đa 3 câu/đoạn** (`CL6-paragraph`) và **tối đa 30 từ/câu** (`CL6-sentence`). Viết 4 câu là chắc chắn dính MINOR.

Luận điểm **lấy từ** `knowledge/1-brand/personas.md` → section `### DSC Product Bridge` của persona bài đó:
- **Ưu tiên** — sản phẩm được phép nhắc
- **Góc dẫn dắt** — luận điểm chính, dùng làm xương sống đoạn văn
- **Tránh** — sản phẩm/cách nói bị cấm với persona này

Không tự nghĩ luận điểm mới. Đoạn Product Bridge là văn xuôi → chịu toàn bộ `anti-ai-rules.md`.

---

## 4. Copy

### Headline
Nói **lợi ích người đọc nhận được**, không phải tên thương hiệu.

- ✗ "Đầu tư chứng khoán cùng DSC" — brand-centric, không cho người đọc lý do nào
- ✓ "Mở tài khoản trong 30 giây, bắt đầu với số vốn bạn có"

### Dòng phụ
Tối đa 3 yếu tố giảm ma sát, cách nhau bằng `•`. Chỉ nêu điều đúng sự thật: miễn phí mở tài khoản, online hoàn toàn, hỗ trợ 24/7.

### Nút
Động từ + tính tức thì. Cấm text chung chung: "Xem thêm", "Tại đây", "Click vào đây", "Tìm hiểu", "Chi tiết".

### Cường độ theo persona
Tra ma trận `knowledge/1-brand/personas.md` (mục *Ma trận nhanh: Persona → Điều chỉnh khi viết*, hàng **CTA**):

| Persona | Cường độ nút |
| :--- | :--- |
| P1 Tiết kiệm | "Tìm hiểu thêm" — mềm |
| P2 F0 | "Mở tài khoản — 3 phút" — trực tiếp |
| P3 Active Trader | "Trao đổi với chuyên gia" — ngang hàng |
| P4 Vốn lớn | "Đặt lịch tư vấn" — trang trọng |

P3 đặc biệt: `personas.md` ghi rõ **tránh CTA aggressive kiểu "mở tài khoản ngay"**.

---

## 5. Kỹ thuật

- **Inline style bắt buộc.** WordPress strip thẻ `<style>`. Không dùng class CSS ngoài.
- **Palette chỉ được dùng** màu trong `knowledge/1-brand/visual-brand-guidelines.md`: `#00AD14`, `#2BE841`, `#10E7B3`, `#0D1B2A`, `#E8F8F2`, `#FFFFFF`. Cấm `#27ae60`, `#229954` và mọi màu ngoài danh sách. Cấm màu đỏ.
- **Tương phản ≥ 4.5:1** (WCAG AA, text thường). Đã đo:

  | Tổ hợp | Tỉ lệ | Kết luận |
  | :--- | ---: | :--- |
  | Trắng trên `#27ae60` | 2.9:1 | ✗ cấm |
  | Trắng trên `#00AD14` | 3.0:1 | ✗ cấm làm nền text |
  | Trắng trên `#0D1B2A` | 17.4:1 | ✓ nền chuẩn |
  | `#0D1B2A` trên `#2BE841` | 10.2:1 | ✓ nút chuẩn |

  → **Nền banner là Dark Navy, nút là xanh lá sáng chữ navy.** Không dùng nền xanh lá cho khối có text thường.
- **Mobile:** container phải có `flex-wrap: wrap`, nút không được để `white-space: nowrap` kèm padding lớn. Test ở 360px.
- **Accessibility:** phần tử trang trí thuần hình phải có `aria-hidden="true"`.
- Link cùng domain → **không** dùng `target="_blank"`.

---

## 6. UTM

**Mặc định KHÔNG gắn UTM.** Chỉ gắn khi chạy A/B test có chủ đích (cờ `--utm`).

Khi bật, theo convention đã có trong repo:
```
?utm_source=blog&utm_medium=banner&utm_campaign=mo_tai_khoan&utm_content=YYYYMMDD-<placement>-<variant>
```
`placement` ∈ `mid_article` | `closing` | `inline`.

Check `LINK-cta` trong `qa_lint.py` dùng `startswith` nên query string không làm hỏng lint.

---

## 7. Lint

`python scripts/qa_lint.py <file> --cta` — các check: `CTA-missing-banner`, `CTA-position`, `CTA-orphan`, `CTA-count`, `CTA-copy`, `CTA-palette`, `CTA-gap`, `CTA-placeholder`.

Audit không qua lint: `python scripts/cta_audit.py <file>` (hoặc `--all`).

Cờ `--cta` hiện **chưa bật mặc định** vì 157 bài trong `3-finalized/` chưa được backfill banner. Backfill xong mới chuyển thành mặc định.
