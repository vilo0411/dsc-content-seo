---
name: image
description: Tạo chiến lược hình ảnh và Gemini prompts/ảnh trực tiếp chuẩn Brand Guidelines DSC.
---

# Chiến lược hình ảnh & Gemini Prompts (DSC Brand Standard)

Kích hoạt Visual Architect + SEO Image Skill để tạo hệ thống hình ảnh cho bài viết.
Output: Gemini prompts + Hình ảnh trực tiếp chuẩn Brand DNA DSC.

---

## 🎨 Quy tắc bắt buộc (DSC Brand Rules)

1. **Brand Palette bắt buộc**: 
   - Primary Accent: `#00AD14` (Xanh lá DSC)
   - Gradient Start/End: `#2BE841` ➔ `#10E7B3` (Teal)
   - Background Tối/Sáng: `#0D1B2A` (Dark Navy) / `#FFFFFF` (White) hoặc nền Pastel nhẹ (Light Pastel Mint `#E8F8F2`)
2. **Ngăn chặn chữ rác (Strict No-Text Rule)**: 
   - AI Image Generator **tuyệt đối không sinh chữ tiếng Anh rác, chữ ngẫu nhiên, hoặc font tiếng Việt bị méo**.
   - Thêm câu chốt bắt buộc ở cuối mọi prompt: `Absolutely NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO ENGLISH LABELS.`
3. **Cấm màu đỏ (No Red Rule)**: 
   - Không dùng màu đỏ trong bất kỳ hình ảnh nào (tránh ám chỉ lỗ/giảm giá trong giao dịch chứng khoán tại Việt Nam).
4. **Phân định Kích thước & Tỷ lệ Khung hình (Aspect Ratio Standards)**:
   - **Ảnh bìa (Featured Image):** Tỷ lệ `16:9` (Dạng Banner ngang rộng, dùng cho Thumbnail blog card, đầu bài viết, Og:Image social share).
   - **Ảnh trong bài (Inline Image / H2 Infographics):** Tỷ lệ `4:3` (Khuôn hình trung tính, gọn gàng, vừa vặn luồng đọc trên cả Mobile & Desktop mà không chiếm quá nhiều chiều cao gây ngắt đoạn chữ).
5. **Nguyên tắc Chống rối mắt (Zero Clutter & Focal Point Rule)**:
   - **Ảnh bìa (Featured Image):** Duy nhất 1 vật thể chính (Single Central Hero Object) ở giữa, 70% khoảng trống âm.
   - **Ảnh trong bài (Inline Image / H2 Infographics):** Linh hoạt trình bày sơ đồ/diagram minh họa 2–3 phần tử liên quan (ví dụ: đối sánh 2 trường phái, hoặc sơ đồ 3–4 bước) nhưng phải giữ bố cục tối giản, không rối mắt.
   - **Khoảng trống âm (Negative Space):** Dành ít nhất 50–60% diện tích làm khoảng trống đơn sắc pastel.
   - **Lệnh cấm rối (Clutter Ban):** Bắt buộc thêm cụm từ `clean minimalist composition, 50-60% negative space, zero clutter, no crowded network lines, no extra icons` vào prompt.
6. **Ghép Logo tự động chuẩn Brand Assets (Auto-Watermark Rule)**:
   - **Vị trí cố định:** Trên cùng bên trái (`Top-Left` corner, lề `4%`).
   - **Tự động chọn file Logo theo nền:**
     * Nền sáng (Light/Pastel Mint/White): Dùng `knowledge/1-brand/assets/logos/logo-for-light-bg.png`
     * Nền tối (Dark Navy): Dùng `knowledge/1-brand/assets/logos/logo-for-dark-bg.png`

---

## 🛠️ Quy trình thực thi & Tối ưu

### 🔄 Bước 0: Context Load
1. `knowledge/1-brand/profile.md` & `visual-brand-guidelines.md` — Brand DNA và màu sắc chính thức.
2. `knowledge/4-content/3-finalized/Final-[slug].md` — Ưu tiên file final.
3. Nếu chưa final: `knowledge/4-content/2-drafts/Draft-[slug].md` hoặc `Optimize-[slug].md`.

### ⚡ Bước 1: Phân tích bài viết & Áp dụng Prompt Template (Tối ưu 1)
Xác định số lượng và vị trí ảnh cần tạo:
- **1 Featured Image (Đầu bài):** Tỷ lệ `16:9`
  * **Prompt Template chuẩn:**
    ```text
    Minimalist 3D vector isometric illustration of a SINGLE isolated [Featured Concept Metaphor], generous light pastel mint green background, 70% negative space, sleek modern finance tech aesthetic, DSC Brand accents (#00AD14 Emerald Green, #2BE841 to #10E7B3 Teal gradient), zero clutter, no extra icons, no circuit lines, clean composition. Absolutely NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO ENGLISH LABELS.
    ```
- **1–2 Inline Images (Dưới các section H2 chính):** Tỷ lệ `4:3`
  * **Prompt Template chuẩn:**
    ```text
    Minimalist 3D vector isometric diagram of a SINGLE focused [H2 Section Metaphor], generous soft pastel neutral background, 70% negative space, DSC Brand Palette (#00AD14 green accents), clean zero-clutter layout. Absolutely NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO ENGLISH LABELS.
    ```

### 📁 Bước 2: Sinh ảnh, Ghép Logo Top-Left & Lưu trữ (Tối ưu 2)
1. Gọi tool `generate_image` với prompt từ Template tương ứng (`AspectRatio: "16:9"` cho ảnh bìa, `AspectRatio: "4:3"` cho ảnh trong bài).
2. **Chạy Script ghép Logo tự động:**
   - Tự động kiểm tra màu nền và chèn logo tương ứng (`logo-for-light-bg.png` hoặc `logo-for-dark-bg.png`) tại **góc trên bên trái (Top-Left)**.
3. **Quy chuẩn đặt tên & quản lý lưu trữ:**
   - Ảnh bìa: `knowledge/4-content/images/[slug-bai-viet]-featured.jpg`
   - Ảnh trong bài: `knowledge/4-content/images/[slug-bai-viet]-[h2-slug].jpg`
4. Lưu ảnh đã ghép logo vào `knowledge/4-content/images/` và chèn link Markdown vào bài viết:
   ```markdown
   ![[Alt Text mô tả từ khóa SEO]](knowledge/4-content/images/[slug-bai-viet]-featured.jpg)
   ```

---

## ✅ Bước 3: QA Checklist
- [ ] **Vị trí Logo:** Nằm ở góc **trên bên trái** (`Top-Left`), sử dụng đúng biến thể logo cho nền sáng/nền tối.
- [ ] **Kích thước & Aspect Ratio:** Ảnh bìa tỉ lệ `16:9`, ảnh trong bài tỉ lệ `4:3`.
- [ ] **Màu sắc Brand:** Tuân thủ 100% mã màu DSC (`#00AD14`, `#2BE841`, `#10E7B3`), không dùng màu đỏ.
- [ ] **Độ thoáng & Tối giản:** Chỉ có 1 vật thể chính ở giữa, $\ge 60\%$ khoảng trống âm, 0% chi tiết thừa rối mắt.
- [ ] **Chất lượng hình ảnh:** 0% chữ rác / typography lỗi.
- [ ] **SEO Asset Management:** Ảnh nằm trong `knowledge/4-content/images/` với tên file theo chuẩn SEO slug.
