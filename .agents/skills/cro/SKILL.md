---
name: cro
description: Tối ưu chuyển đổi — audit CTA, dựng Product Bridge, chèn banner đúng persona, sinh biến thể A/B.
---

# Tối Ưu Chuyển Đổi (CRO)

## Options Hỗ Trợ
- `--audit-all`: Quét toàn bộ `knowledge/4-content/3-finalized/`, ra bảng xếp hạng bài cần vá trước. **Chỉ báo cáo, không ghi file.**
- `--variants N`: Sinh N biến thể banner/copy cho bài để A/B test.
- `--apply`: Ghi thay đổi vào file. Mặc định chỉ trình bày và dừng ở approval gate.
- `--utm`: Gắn UTM vào link CTA. Mặc định **tắt**.
- `--ga4 <csv>`: Dùng với `--audit-all` — xếp hạng theo traffic thực từ export GA4 landing page.

## Nhiệm vụ
Chèn tầng chuyển đổi vào bài viết: đoạn Product Bridge dẫn từ kiến thức sang sản phẩm, rồi banner CTA đặt đúng vị trí với cường độ khớp persona.

---

## Quy trình thực thi chi tiết

### 🔄 Bước 0: System Context Load (BẮT BUỘC — trước mọi bước)
1. `knowledge/1-brand/profile.md`
2. `knowledge/3-pipeline/anti-ai-rules.md` — bước dựng Product Bridge là viết văn xuôi, không có exception
3. `.antigravity/rules/cta-conversion.md` — rule cứng về CTA
4. `.antigravity/memory/instincts.md` — bản rút gọn
5. `knowledge/1-brand/personas.md` — **chỉ section persona của bài** (xác định ở Bước 2), gồm `### DSC Product Bridge`

> Đây là lần load context **duy nhất** trong session. Các bước sau không đọc lại.
> **Không đọc `glossary.md`** — skill này không viết nội dung chuyên môn mới.

---

### ⚙️ Bước 1: Audit hiện trạng

`/cro` nhận **file path, slug, hoặc URL** — script tự phân giải, bạn không cần tra trước:

```bash
python scripts/cta_audit.py knowledge/4-content/3-finalized/Final-[slug].md   # file local
python scripts/cta_audit.py [slug]                                            # slug
python scripts/cta_audit.py https://www.dsc.com.vn/kien-thuc/[slug]           # URL
```

**🚫 TUYỆT ĐỐI KHÔNG dùng `web-serp` / `scrape.py` / Firecrawl / Jina cho URL dsc.com.vn.**
Những công cụ đó tồn tại để vượt bot protection của **trang đối thủ** và **tốn phí mỗi lần gọi**. Site của mình trả HTML trực tiếp: `cta_audit.py` fetch bằng `urllib` stdlib mất **~0.6 giây**, cache vào `knowledge/raw/pages/`. Gọi Firecrawl ở đây là vừa chậm vừa mất tiền vô ích.

Thứ tự phân giải (script tự làm):
1. Có `Final-[slug].md` ở local → dùng file local. Đây là bản nguồn sửa được, luôn ưu tiên.
2. Không có → fetch trang live, tách `<main>`, chuyển sang markdown để audit. Dùng `--refresh` nếu cần bỏ cache.

**Bài chỉ có trên web (732/824 URL hiện chưa có bản local):** chỉ audit và đề xuất được, **không ghi file**. Output là banner HTML + chỉ dẫn vị trí để bạn dán vào CMS. Không tự tạo file trong `3-finalized/` từ HTML đã render — đó là bản render, không phải bản nguồn.

Với `--audit-all`:
```bash
python scripts/cta_audit.py --all
python scripts/cta_audit.py --all --ga4 knowledge/raw/ga4/landing-pages.csv   # nếu có data
```

Chế độ `--audit-all` **kết thúc ở đây** — trình bày bảng kèm danh sách ưu tiên, không sửa gì. Dựng Product Bridge là sinh văn xuôi, không được chạy hàng loạt không giám sát.

---

### ⚙️ Bước 2: Xác định persona & cường độ CTA

- Kích hoạt skill `.antigravity/skills/cro-optimization/SKILL.md` → Bước 2.
- Đọc `Persona` từ frontmatter. Thiếu → suy từ intent bài rồi ghi bổ sung vào frontmatter.
- Tra cường độ nút + giới hạn số banner theo persona.

**P4 (vốn lớn): không chèn banner**, chỉ link text. CTA đúng của họ là "Đặt lịch tư vấn" mà hệ thống chưa có landing page đó.

---

### ⚙️ Bước 3: Dựng Product Bridge (nếu bài chưa có)

- Kích hoạt `.antigravity/skills/cro-optimization/SKILL.md` → Bước 3.
- Luận điểm lấy từ "Góc dẫn dắt" của persona. **Không tự nghĩ.**
- Bài đã có đoạn cầu nối hợp lý → giữ nguyên văn cũ, bỏ qua bước này.

---

### ⚙️ Bước 4: Chọn template, viết copy, chèn

- Kích hoạt `.antigravity/skills/cro-optimization/SKILL.md` → Bước 4 & 5.
- Template ở `.antigravity/skills/cro-optimization/assets/banner-templates.md`.
- Có `--variants N` → sinh N biến thể, mỗi biến thể đổi đúng một biến.

**⚠️ Chỉ sửa đúng hai thứ:** đoạn Product Bridge mới và khối banner. Giữ nguyên 100% nội dung, ảnh, và link đang có.

**Nguồn là trang live** → không ghi file. Thay vào đó trình bày:
1. Khối banner HTML hoàn chỉnh, sẵn sàng copy
2. Vị trí dán: *"ngay sau đoạn kết của H2 «...», trước H2 «...»"*
3. Đoạn Product Bridge (nếu bài thiếu) để dán cùng, đặt trước banner

---

### ⚙️ Bước 5: QA (BẮT BUỘC trước khi trình bày)

```bash
python scripts/cta_audit.py [file]
python scripts/qa_lint.py [file] --cta --no-sitemap
```

Sau đó Self-Audit ngữ nghĩa theo checklist trong `.antigravity/skills/cro-optimization/SKILL.md`.

**Giới hạn vòng lặp:** FAIL → sửa → QA lại **tối đa 2 vòng**. Vẫn FAIL → dừng, trình bày kèm `⚠️ Remaining issues`. Không tự lặp vòng 3.

---

### 🚧 APPROVAL GATE

> Trình bày cho người dùng:
> - Đoạn Product Bridge mới (nguyên văn) + persona và Góc dẫn dắt đã dùng
> - Banner: template nào, headline / sub / nút, đặt ở đâu (% thân bài)
> - Kết quả `cta_audit` trước → sau
> - Nếu có `--variants`: bảng các biến thể kèm biến được đổi
>
> **DỪNG LẠI. Chờ người dùng gõ `/approve`.**
>
> Không có `--apply` → chỉ trình bày, chưa ghi file. Có `--apply` → đã ghi, trình bày diff để người dùng đối chiếu.

---

### 📁 Bước 6: Ghi nhận

- `python scripts/qa_lint.py [file] --log` — ghi score vào `revision-log.md`.
- Có chạy A/B → ghi biến thể đang dùng của từng bài vào `knowledge/3-pipeline/cta-variants.md` (tạo file nếu chưa có) để lần đo sau biết bài nào chạy gì.
- Phát hiện pattern copy lặp lỗi → `/learn`, ghi vào `instincts-archive.md` rồi chạy `python scripts/optimize_instincts.py`. Lỗi nào bắt được bằng regex thì thêm vào `qa_lint.py` thay vì thêm instinct.

---

## ✅ Checklist trước khi báo hoàn thành
- [ ] `cta_audit.py` không còn CRITICAL/MAJOR
- [ ] `qa_lint.py --cta` PASS
- [ ] Không còn placeholder `{{...}}` trong bài
- [ ] Headline qua được phép thử thay tên đối thủ
- [ ] Nút hứa đúng thứ URL giao
- [ ] Nội dung, ảnh, link cũ giữ nguyên 100%
