# Anti-AI Blacklist (QA Fast-Check)

> **Dùng cho:** Quality Guardian, Brand Guardian — thay thế đọc toàn bộ `anti-ai-rules.md`.
> Drafting Agent đọc thêm `anti-ai-rules.md` (v3.0, ~10 KB — phần phán đoán; danh sách cụm cấm chỉ nằm ở file này).

---

## 1. Trigger Phrases bị cấm — Rewrite ngay, không thương lượng

**Mở bài:**
- "Trong kỷ nguyên số ngày nay..."
- "Trong bối cảnh thị trường tài chính ngày càng..."
- "Chứng khoán là một lĩnh vực đầy tiềm năng..."
- "Bạn có bao giờ tự hỏi..."
- "[Keyword] là gì? [Keyword] là..."
- "Thị trường chứng khoán Việt Nam đang trải qua..."
- "Để hiểu rõ hơn về [topic], trước tiên chúng ta cần..."
- "Bài viết này sẽ..." / "Bài viết này giúp..." / "Bài viết dưới đây..." — sapo tự giới thiệu bài; nói thẳng điều người đọc nhận được

**Kết bài:**
- "Tóm lại, bài viết đã cung cấp..."
- "Nhìn chung, [topic] là..."
- "Hy vọng bài viết này mang lại kiến thức bổ ích..."
- "Trên đây là toàn bộ thông tin về..."
- "Như vậy có thể thấy rằng..."
- "Qua bài viết này, bạn đã nắm được..."

**Transition:**
- "Hơn nữa, ..." / "Bên cạnh đó, ..." / "Đáng chú ý là ..."
- "Không chỉ vậy, ..." / "Về cơ bản, ..." / "Cốt lõi là ..."

**Hedge words (dùng quá nhiều):**
- "Tương đối", "khá", "khá là", "Có thể nói rằng", "Nhìn một cách tổng quan"

---

## 2. Emphatic Quotes — Cấm tuyệt đối

Không dùng dấu ngoặc kép `"..."` bao từ thông thường, tiếng lóng, hay ẩn dụ.
- ❌ "ôm hàng", "điểm vào", "vùng kiếm tiền", "đu đỉnh"
- ✅ Viết thẳng không có ngoặc kép

---

## 3. Các từ bị cấm khác (từ instincts)

- "cơ chế truyền dẫn" → dùng "tác động"
- "thủ thuật" / "chiêu trò" → dùng "chiến lược" / "phương pháp"
- "rõ ràng" (dạng vô nghĩa: "phân biệt rõ ràng") → bỏ
- "xương máu" → dùng "quý báu", "cốt lõi"
- "sống còn" / "siêu bảng" / "bí quyết vàng" / "chỉ số vàng" / "cổ phiếu vua" → bỏ từ cường điệu, gọi đúng tên ("bảng so sánh", "5 chỉ số định giá", "yếu tố quyết định")
- "Active Trader" / "trader" (trong văn xuôi tiếng Việt) → dùng "nhà đầu tư chủ động", "nhà đầu tư lướt sóng", "nhà giao dịch ngắn hạn"

---

## 4. Lỗi Format bị cấm

- LaTeX `$$` hoặc `$` cho công thức → dùng **in đậm** thông thường
- ASCII Art lưu đồ trong code block → dùng bảng Markdown
- Callout `> [!NOTE]`, `> [!TIP]` → dùng `> **Lưu ý:**`
- Relative URL `/kien-thuc/...` → phải dùng `https://www.dsc.com.vn/kien-thuc/...`
