---
name: SEO Optimization
description: >
  Use this skill to diagnose, audit, and rewrite existing published content 
  (Decay Content) to improve search rankings, update brand features, and 
  fix anti-AI violations using the Seven Sweeps Framework.
---

# Skill: SEO Optimization (Tối ưu bài cũ)

## 🔄 Context Loading (Đọc trước khi bắt đầu)
- [ ] `knowledge/4-content/3-finalized/Final-[slug].md` — Bài gốc đang được tối ưu
- [ ] `knowledge/4-content/2-drafts/Optimize-[slug].md` — Working copy (đã được tạo bởi workflow)
- [ ] `knowledge/3-pipeline/anti-ai-rules.md` — Quy tắc Anti-AI đầy đủ
- [ ] `knowledge/1-brand/profile.md` — Brand USPs hiện tại để fact-check
- [ ] `.antigravity/skills/seo-optimization/assets/proposal-template.md` — Template bắt buộc cho Proposal

---

Kỹ năng này chuyên dùng để chẩn đoán và nâng cấp các bài viết đã xuất bản nhằm khôi phục và tăng trưởng traffic mà không làm mất đi các giá trị cốt lõi của bài gốc. Kỹ năng này tích hợp Framework Seven Sweeps (7 Bước Quét) để đảm bảo chất lượng nội dung đạt chuẩn cao nhất.

## 🛠️ Procedures

### Phase 1: Content Audit & Proposal (Khám bệnh & Đề xuất)
1. **Health Check & Analysis:**
   - Phân tích On-page SEO (H1, Meta, Mật độ từ khóa).
   - Kiểm tra vi phạm văn phong AI dựa theo `knowledge/3-pipeline/anti-ai-rules.md`.
   - **7 Sweeps Audit**: Đánh giá sơ bộ nội dung dựa trên 7 tiêu chí: Clarity (Rõ ràng), Voice (Giọng văn), So What (Giá trị), Prove It (Bằng chứng), Specificity (Cụ thể), Emotion (Cảm xúc), Zero Risk (Tin cậy).
2. **Output Proposal:**
   - Hệ thống **BẮT BUỘC** phải xuất ra Báo cáo Đề xuất (Optimize Outline) tuân thủ CHÍNH XÁC cấu trúc tại file `.antigravity/skills/seo-optimization/assets/proposal-template.md` trước khi sửa văn bản.
   - **⚠️ Anti-AI trong Proposal:** Mọi văn bản trong Proposal (mô tả Section 4, 5 — bao gồm cả hướng xử lý và nội dung THÊM MỚI) phải tuân thủ quy tắc anti-AI: **không dùng dấu ngoặc kép nhấn mạnh** quanh từ thông thường, tiếng lóng hoặc ẩn dụ. Proposal là văn bản chuyên nghiệp, không phải ngoại lệ.
3. **Proposal Anti-AI Self-Check (BẮT BUỘC trước khi print Proposal):**
   Trước khi trình bày Proposal cho người dùng, grep toàn bộ nội dung Proposal cho các pattern sau và sửa ngay tại chỗ nếu có vi phạm:
   - **Emphatic quotes:** từ thông thường bị bao trong `"..."` → xóa dấu ngoặc kép
   - **Tiêu đề/heading dùng ngoặc kép nhấn mạnh** → xóa
   - **Trigger phrases AI** trong phần mô tả hướng xử lý: "Hơn nữa,", "Bên cạnh đó,", "Đáng chú ý là", "Nhìn chung," → viết lại tự nhiên
   - **Opener/closer vĩ mô** kiểu "Trong bối cảnh hiện nay...", "Hy vọng bài này giúp..." → xóa
   Chỉ sau khi sạch các pattern trên → mới được in Proposal ra.
4. **Pause for Approval**: In báo cáo Proposal ra và DỪNG LẠI chờ người dùng gõ `/approve` (Trừ khi đang chạy ở chế độ `--auto`).

### Phase 2: Execution (Thực thi nâng cấp với 7 Sweeps)
Khi thực hiện viết lại (Rewrite), áp dụng tuần tự theo thứ tự sau:

**⚠️ Sweep 0 — Anti-AI Pre-check (BẮT BUỘC trước mọi sweep):**
Grep toàn bộ bản draft cho từng pattern sau. Đánh dấu (highlight hoặc ghi line number) mọi vi phạm tìm được — sửa ngay tại chỗ trước khi tiếp tục:
- **Emphatic quotes:** bất kỳ từ thông thường, tiếng lóng, hoặc ẩn dụ nào bị bao bởi `"..."` → xóa dấu ngoặc kép, giữ nguyên từ
- **Trigger phrases blacklist** (Phần 1.1 của `anti-ai-rules.md`): opener vĩ mô, closer tóm tắt, transition AI ("Hơn nữa,", "Bên cạnh đó,", "Đáng chú ý là", v.v.)
- **Hedge words:** "tương đối", "khá", "có thể nói rằng", "nhìn một cách tổng quan"

Chỉ sau khi Sweep 0 sạch → mới được chạy Sweep 1–7.

1.  **Clarity (Rõ ràng)**: Xóa bỏ câu cú phức tạp, thuật ngữ khó hiểu. Một câu = Một ý chính.
2.  **Voice & Tone (Giọng văn)**: Đảm bảo đúng POV của chuyên gia DSC, thân thiện nhưng chuyên nghiệp.
3.  **So What (Thì sao?)**: Biến tính năng thành lợi ích. Luôn trả lời câu hỏi "Tại sao khách hàng phải quan tâm?"
4.  **Prove It (Chứng minh)**: Thêm số liệu, trích dẫn chuyên gia, bằng chứng thực tế (Statistics & Evidence).
5.  **Specificity (Cụ thể)**: Thay thế các từ chung chung (tốt, nhanh, rẻ) bằng con số hoặc ví dụ cụ thể.
6.  **Heightened Emotion (Cảm xúc)**: Đánh vào nỗi đau (pain points) hoặc khát khao của nhà đầu tư.
7.  **Zero Risk (Xóa bỏ rào cản)**: Address các lo ngại, thêm các cam kết/hướng dẫn bước tiếp theo rõ ràng.

**⚠️ Self-Audit Gate (BẮT BUỘC sau Sweep 7 — trước khi chuyển sang QA):**
Chạy toàn bộ Self-Audit Checklist tại Phần 6 của `knowledge/3-pipeline/anti-ai-rules.md`. Mọi điểm trong Checklist Bắt buộc phải đạt. Nếu có điểm fail → sửa ngay, không chuyển sang QA khi còn lỗi tự phát hiện được.

---

## 📋 Quality Checklists

### Word-Level Checks
- **Cắt bỏ**: "Rất", "Thực sự", "Cực kỳ", "Để mà" (dùng "Để").
- **Thay thế**:
  | Từ yếu | Từ mạnh/Cụ thể |
  | :--- | :--- |
  | Sử dụng | Áp dụng/Triển khai |
  | Tốt hơn | Tăng X% / Vượt trội |
  | Nhanh chóng | Ngay lập tức / Trong 5 phút |

### Sentence & Paragraph Checks
- **Độ dài câu**: Tối đa 25 từ.
- **Đoạn văn**: 2-3 câu (Mobile-first).
- **Cấu trúc**: Thông tin quan trọng nhất đặt ở đầu câu/đoạn.

---

## 🚦 Success Assertions
- [ ] Báo cáo Proposal xuất ra đúng template và được duyệt TRƯỚC KHI sửa bài.
- [ ] Giữ nguyên tuyệt đối nội dung của các Heading được gắn nhãn `[GIỮ NGUYÊN]`.
- [ ] Nội dung sau khi sửa phải vượt qua bài kiểm tra "So What?" và "Specificity".
- [ ] Không còn các từ ngữ sáo rỗng vi phạm `anti-ai-rules.md`.

---

---

## 📚 References
- [Content Refresh Checklist](references/content-refresh.md): Quy trình chi tiết để làm mới nội dung cũ.
- [Plain Vietnamese Alternatives](references/plain-vietnamese-alternatives.md): Bảng tra cứu thay thế ngôn ngữ rườm rà.
- [Anti-AI Rules](../../../knowledge/3-pipeline/anti-ai-rules.md): Các quy tắc viết chuẩn Anti-AI của dự án.

## ⚠️ Gotchas
- **Blind Rewriting**: Tuyệt đối không xóa trắng viết lại. Phải giữ "SEO Juice" của bài cũ.
- **Losing SEO Juice**: Không tự ý đổi URL Slug hoặc H1 nếu không có trong Proposal.
- **AI-Vibe**: Tránh các kết bài "Tóm lại", "Hy vọng...".
