---
name: image
description: "Ảnh cho bài SEO: chọn ảnh cần có, vẽ infographic/ảnh bìa bằng code theo image-design-system, hoặc viết Gemini prompt theo brand DSC. Dùng khi hỏi ảnh bìa, infographic, ảnh minh hoạ, alt text cho 1 bài."
---

# Chiến lược hình ảnh & Gemini Prompts (DSC Brand Standard)

Kích hoạt Visual Architect + SEO Image Skill để tạo hệ thống hình ảnh cho bài viết.
Output: Gemini prompts + Hình ảnh trực tiếp chuẩn Brand DNA DSC.

---

## 🎨 Quy tắc bắt buộc (DSC Brand Rules)

1. **Brand Palette bắt buộc** (nguồn: `knowledge/1-brand/DESIGN.md` v1.0 — brand guideline chính thức; không dùng hex nào khác):
   - Điểm nhấn: Lime Green `#2AD03D` (chính) · Emerald `#1BBE72` (phụ) · Frosted Mint `#8CFFCC` (glow trên nền tối)
   - Gradient: Primary `#61CC6C` ➔ `#14A46E` · Ambient `#156A1F → #31AE40 → #156A1F` / `#354D38 → #2C7B50 → #7D9E9F → #B6C7AF`
   - Nền Tối/Sáng: Gunmetal `#272D2B` hoặc Pine Teal `#1D4130` / White `#FFFFFF` hoặc mint nhạt `#F2FBF6`
   - Phong cách mặc định cho ảnh AI: **trừu tượng 3D xanh** (dải lụa/kính, khối mềm, vệt sáng) — mẫu `knowledge/1-brand/guideline/20-abstract.png`, style `assets/styles/abstract-brand.md`.
2. **Ngăn chặn chữ rác (Strict No-Text Rule)**: 
   - AI Image Generator **tuyệt đối không sinh chữ tiếng Anh rác, chữ ngẫu nhiên, hoặc font tiếng Việt bị méo**.
   - Thêm câu chốt bắt buộc ở cuối mọi prompt: `Absolutely NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO ENGLISH LABELS.`
3. **Cấm màu đỏ (No Red Rule)**: 
   - Không dùng màu đỏ trong bất kỳ hình ảnh nào (tránh ám chỉ lỗ/giảm giá trong giao dịch chứng khoán tại Việt Nam).
4. **Phân định Kích thước & Tỷ lệ Khung hình (Aspect Ratio Standards)**:
   - **Ảnh bìa (Featured Image):** `1000×600` (5:3) — chuẩn CMS DSC, dùng cho đầu bài, thumbnail, OG image.
   - **Ảnh trong bài (Inline Image / H2 Infographics):** `800×500` (16:10) — cùng chuẩn; thẻ `<img style="aspect-ratio:800/500;" … width="800" height="500">`.
5. **Nguyên tắc Chống rối mắt (Zero Clutter & Focal Point Rule)**:
   - **Ảnh bìa (Featured Image):** Duy nhất 1 vật thể chính (Single Central Hero Object) ở giữa, 70% khoảng trống âm.
   - **Ảnh trong bài (Inline Image / H2 Infographics):** Linh hoạt trình bày sơ đồ/diagram minh họa 2–3 phần tử liên quan (ví dụ: đối sánh 2 trường phái, hoặc sơ đồ 3–4 bước) nhưng phải giữ bố cục tối giản, không rối mắt.
   - **Khoảng trống âm (Negative Space):** Dành ít nhất 50–60% diện tích làm khoảng trống đơn sắc pastel.
   - **Lệnh cấm rối (Clutter Ban):** Bắt buộc thêm cụm từ `clean minimalist composition, 50-60% negative space, zero clutter, no crowded network lines, no extra icons` vào prompt.
6. **Ghép Logo tự động chuẩn Brand Assets (Auto-Watermark Rule)**:
   - **Vị trí cố định:** Trên cùng bên trái (`Top-Left` corner, lề `4%`).
   - **Tự động chọn file Logo theo nền:**
     * Nền sáng (Light/Pastel Mint/White): Dùng `knowledge/1-brand/assets/logos/logo-for-light-bg.png`
     * Nền tối (Gunmetal / Pine Teal): Dùng `knowledge/1-brand/assets/logos/logo-for-dark-bg.png`

---

## 🛠️ Quy trình thực thi & Tối ưu

### 🔄 Bước 0: Context Load
0. **Ảnh có chữ/số liệu (infographic, biểu đồ, ảnh bìa có tiêu đề):** không dùng AI sinh ảnh — vẽ bằng code theo `knowledge/1-brand/image-design-system.md` (`scripts/images/dsc_design.py`, mẫu: `generate_cach_choi_chung_khoan_images.py`). Template AI bên dưới chỉ cho ảnh minh họa không chữ.
1. `knowledge/1-brand/profile.md` & `DESIGN.md` (màu, font, phong cách ảnh chính thức) — `visual-brand-guidelines.md` cho logo/khổ ảnh blog.
2. `knowledge/3-seo/content/3-finalized/Final-[slug].md` — Ưu tiên file final.
3. Nếu chưa final: `knowledge/3-seo/content/2-drafts/Draft-[slug].md` hoặc `Optimize-[slug].md`.

### ⚡ Bước 1: Phân tích bài viết & Áp dụng Prompt Template (Tối ưu 1)
Xác định số lượng và vị trí ảnh cần tạo:
- **1 Featured Image (Đầu bài):** `1000×600`
  * **Prompt Template chuẩn:**
    ```text
    Minimalist 3D vector isometric illustration of a SINGLE isolated [Featured Concept Metaphor], generous pale mint background (#F2FBF6), 70% negative space, sleek modern finance tech aesthetic, DSC Brand accents (lime green #2AD03D, emerald #1BBE72, gradient #61CC6C to #14A46E, dark gunmetal #272D2B details), zero clutter, no extra icons, no circuit lines, clean composition. Absolutely NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO ENGLISH LABELS.
    ```
- **1–2 Inline Images (Dưới các section H2 chính):** `800×500`
  * **Prompt Template chuẩn:**
    ```text
    Minimalist 3D vector isometric diagram of a SINGLE focused [H2 Section Metaphor], generous pale mint background (#F2FBF6), 70% negative space, DSC Brand Palette (lime green #2AD03D and emerald #1BBE72 accents, gunmetal #272D2B outlines), clean zero-clutter layout. Absolutely NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO ENGLISH LABELS.
    ```

### 📁 Bước 2: Sinh ảnh, Ghép Logo Top-Left & Lưu trữ (Tối ưu 2)
1. Gọi tool `generate_image` với prompt từ Template (`AspectRatio: "16:9"` — gần 16:10 nhất), rồi crop/resize về đúng `1000×600` (bìa) / `800×500` (trong bài).
2. **Chạy Script ghép Logo tự động:**
   - Tự động kiểm tra màu nền và chèn logo tương ứng (`logo-for-light-bg.png` hoặc `logo-for-dark-bg.png`) tại **góc trên bên trái (Top-Left)**.
3. **Quy chuẩn đặt tên & quản lý lưu trữ:**
   - Ảnh bìa: `knowledge/3-seo/content/images/[slug-bai-viet]-featured.jpg`
   - Ảnh trong bài: `knowledge/3-seo/content/images/[slug-bai-viet]-[h2-slug].jpg`
4. Lưu ảnh đã ghép logo vào `knowledge/3-seo/content/images/` và chèn link Markdown vào bài viết:
   ```markdown
   ![[Alt Text mô tả từ khóa SEO]](knowledge/3-seo/content/images/[slug-bai-viet]-featured.jpg)
   ```

---

## ✅ Bước 3: QA Checklist
- [ ] **Vị trí Logo:** Nằm ở góc **trên bên trái** (`Top-Left`), sử dụng đúng biến thể logo cho nền sáng/nền tối.
- [ ] **Kích thước:** ảnh bìa `1000×600`, ảnh trong bài `800×500`.
- [ ] **Màu sắc Brand:** Chỉ màu trong `DESIGN.md` §2–§3 (Gunmetal, Pine Teal, Lime, Emerald, Frosted Mint, White + gradient), không màu cũ (`#00AD14`/`#2BE841`/`#10E7B3`/`#0D1B2A`), không đỏ.
- [ ] **Độ thoáng & Tối giản:** Chỉ có 1 vật thể chính ở giữa, $\ge 60\%$ khoảng trống âm, 0% chi tiết thừa rối mắt.
- [ ] **Chất lượng hình ảnh:** 0% chữ rác / typography lỗi.
- [ ] **SEO Asset Management:** Ảnh nằm trong `knowledge/3-seo/content/images/` với tên file theo chuẩn SEO slug.
