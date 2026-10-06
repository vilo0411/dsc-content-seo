---
name: CRO Optimization
description: >
  Tối ưu tầng chuyển đổi của bài viết — chấm điểm CTA hiện trạng, dựng đoạn Product Bridge,
  chọn và chèn banner CTA đúng persona, sinh biến thể copy để A/B test.
  Kích hoạt từ workflow /cro, hoặc như một bước trong /write và /optimize.
---

# CRO Optimization

Bài viết SEO tốt mà không có đường dẫn tới hành động thì chỉ là chi phí. Skill này lo tầng chuyển đổi: người đọc đi hết mạch lập luận rồi được mời làm bước tiếp theo, đúng lúc và đúng cường độ.

**Output:** đoạn Product Bridge (nếu bài chưa có) + 1–2 banner CTA HTML inline, đã qua `qa_lint --cta`.

---

## 🔄 Context Loading (đọc trước khi bắt đầu)

- [ ] `.antigravity/rules/cta-conversion.md` — rule cứng, nguồn sự thật duy nhất về CTA
- [ ] `knowledge/1-brand/personas.md` — **chỉ section persona của bài**, gồm `### DSC Product Bridge`
- [ ] `assets/product-bridge-patterns.md` — bảng tra persona + khuôn đoạn
- [ ] `assets/banner-templates.md` — HTML template
- [ ] `references/cro-principles.md` — công thức copy (đọc khi viết, không cần đọc trước)

`profile.md`, `anti-ai-rules.md`, `instincts.md` đã có trong context từ Bước 0 của workflow gọi tới — **không đọc lại**.

---

## ⚙️ Bước 1: Chấm điểm hiện trạng

```bash
python scripts/cta_audit.py <file>
```

Script trả về: số banner, vị trí theo % thân bài, có đoạn dẫn hay không, số link mở tài khoản, danh sách vấn đề, CRO score.

**Không đoán bằng mắt.** Script đo vị trí bằng số từ người đọc đã đi qua, không phải số dòng.

---

## ⚙️ Bước 2: Xác định persona và cường độ CTA

1. Đọc `Persona` trong frontmatter. Không có → suy từ intent + độ sâu thuật ngữ của bài, rồi **ghi bổ sung vào frontmatter**.
2. Tra bảng trong `assets/product-bridge-patterns.md` → lấy Góc dẫn dắt, sản phẩm được nhắc, danh sách Tránh.
3. Tra cường độ nút theo ma trận CTA của `personas.md`.

**Chốt chặn theo persona** (mục "Giới hạn hiện tại: chỉ có một offer"):

| Persona | Được phép |
| :--- | :--- |
| P1 | 1 × `slim-inline`, copy mềm |
| P2 | `primary-midarticle` + `closing` |
| P3 | Tối đa 1 × `slim-inline`, không dùng từ "ngay" |
| P4 | **Không banner** — chỉ link text trong Product Bridge |

Lý do P4 không banner: CTA đúng của họ là "Đặt lịch tư vấn", ta chưa có landing page đó. Nút hứa một đằng, URL giao một nẻo thì hại hơn không có nút.

---

## ⚙️ Bước 3: Dựng Product Bridge (nếu thiếu)

Bỏ qua bước này nếu bài đã có đoạn cầu nối hợp lý — **giữ nguyên văn cũ**, chỉ chèn banner.

Cần dựng mới thì:

1. Chọn khuôn A/B/C/D trong `assets/product-bridge-patterns.md` theo dạng bài.
2. Viết **2–3 câu, mỗi câu ≤ 30 từ**, xương sống là Góc dẫn dắt của persona. Không tự nghĩ luận điểm mới.
   Quá ngưỡng sẽ dính `CL6-paragraph` / `CL6-sentence` — đây là giới hạn cứng của `qa_lint`, không phải gợi ý.
3. Đặt ngay sau section giải quyết xong nỗi đau chính của bài.

> ⚠️ Đây là viết văn xuôi → chịu toàn bộ **Content Edit Rule** trong `CLAUDE.md`: `anti-ai-rules.md` phải có trong context, viết xong phải qua `qa_lint.py` + Self-Audit ngữ nghĩa.

**Cấm:** bịa số liệu sản phẩm, cam kết lợi nhuận, so sánh hơn kém không nguồn, nhắc sản phẩm trong cột Tránh, đoạn dài quá 4 câu.

---

## ⚙️ Bước 4: Chọn template và viết copy

1. Chọn template theo bảng ở đầu `assets/banner-templates.md`.
2. Viết `{{HEADLINE}}` `{{SUB}}` `{{BUTTON}}` theo công thức trong `references/cro-principles.md`.
3. Kiểm tra headline bằng phép thử thay tên: thay "DSC" bằng tên đối thủ, câu còn đúng → headline rỗng, viết lại.
4. Headline phải gắn với **chủ đề bài này**, không dùng chung cho mọi bài.
5. `{{URL}}` = `https://www.dsc.com.vn/mo-tai-khoan`, không UTM trừ khi workflow bật `--utm`.

**Không sửa màu, không sửa style trong template.** Cần đổi → sửa file template, không sửa tại chỗ trong bài.

---

## ⚙️ Bước 5: Chèn

- Một dòng trống trước và sau khối HTML, để markdown không nuốt đoạn văn liền kề.
- Banner mid-article đặt **ngay sau** đoạn Product Bridge, không cách bởi heading.
- Banner `closing` đặt cuối bài, sau phần kết.
- Hai banner phải cách nhau ≥ 300 từ.
- Không thay thế hay xoá link text mở tài khoản đang có trong bài.
- Giữ nguyên 100% nội dung và hình ảnh còn lại.

---

## 🧪 Sinh biến thể A/B (khi được yêu cầu)

Mỗi biến thể đổi **đúng một** biến — nếu không sẽ không biết cái gì tạo ra khác biệt. Bảng biến trong `references/cro-principles.md` mục 5.

Không có UTM thì chỉ so được sequential (trước/sau) ở mức bài. Cần tách số theo biến thể → bật `--utm`, khi đó `utm_content=YYYYMMDD-<placement>-<variant>`.

---

## ✅ QA Checklist

```bash
python scripts/cta_audit.py <file>
python scripts/qa_lint.py <file> --cta
```

- [ ] Không còn placeholder `{{...}}`
- [ ] Headline gắn chủ đề bài, không brand-centric, qua được phép thử thay tên
- [ ] Nút hứa đúng thứ URL giao
- [ ] Cường độ CTA khớp persona; không nhắc sản phẩm trong cột Tránh
- [ ] Banner đứng sau đoạn dẫn, không mồ côi
- [ ] Không banner trong 25% đầu bài informational
- [ ] Số banner đúng giới hạn của persona
- [ ] Palette đúng brand, tương phản ≥ 4.5:1
- [ ] Đoạn Product Bridge mới qua được anti-AI (không còn CL2/CL3 mới phát sinh)
- [ ] Nội dung và ảnh còn lại giữ nguyên 100%
