---
name: SEO Optimization
description: >
  Use this skill to diagnose, audit, and rewrite existing published content 
  (Decay Content) to improve search rankings, update brand features, and 
  fix anti-AI violations without breaking the core structure.
---

# Skill: SEO Optimization (Tối ưu bài cũ)

Kỹ năng này chuyên dùng để "chẩn đoán" và "nâng cấp" các bài viết đã xuất bản nhằm khôi phục và tăng trưởng traffic mà không làm mất đi các giá trị cốt lõi của bài gốc.

## 🛠️ Procedures

### Phase 1: Content Audit & Proposal (Khám bệnh & Đề xuất)
1. **Health Check & Analysis:**
   - Phân tích On-page SEO (H1, Meta, Mật độ từ khóa).
   - Kiểm tra vi phạm văn phong AI dựa theo `knowledge/3-pipeline/anti-ai-rules.md`.
   - Phân tích gap nội dung so với SERP.
2. **Output Proposal:**
   - Hệ thống **BẮT BUỘC** phải xuất ra Báo cáo Đề xuất (Optimize Outline) tuân thủ CHÍNH XÁC cấu trúc tại file `.antigravity/skills/seo-optimization/assets/proposal-template.md` trước khi sửa văn bản.
3. **Pause for Approval**: In báo cáo Proposal ra và DỪNG LẠI chờ người dùng gõ `/approve` (Trừ khi đang chạy ở chế độ `--auto`).

### Phase 2: Execution (Thực thi nâng cấp)
1. **Targeted Rewrite**: Bắt đầu sửa đổi trực tiếp trên file làm việc (Optimize copy). CHỈ thao tác trên các phần `[CẬP NHẬT]` và `[THÊM MỚI]`.
2. **Strict Preservation**: Bảo tồn 100% nội dung chữ và link của các phần `[GIỮ NGUYÊN]`.
3. **Smooth Transitions**: Sử dụng các câu chuyển ngữ mượt mà để nối đoạn văn cũ với đoạn mới viết thêm.

---

## 🚦 Success Assertions
- [ ] Báo cáo Đề xuất (Audit Report) phải được xuất ra màn hình và được người dùng duyệt TRƯỚC KHI tiến hành sửa code/text.
- [ ] Giữ nguyên tuyệt đối nội dung của các Heading được gắn nhãn `[GIỮ NGUYÊN]`.
- [ ] Tất cả các bảng biểu hoặc tính năng mới từ `knowledge/1-brand/profile.md` phải được lồng ghép tự nhiên.

---

## ⚠️ Gotchas
- **Blind Rewriting (Viết lại mù quáng)**: Xóa trắng và tự viết lại toàn bộ bài từ đầu làm mất đi đoạn văn đang kéo traffic. *Hãy tuân thủ nghiêm ngặt Proposal.*
- **Abrupt Transitions (Chuyển ý gượng ép)**: Lắp ghép đoạn mới và cũ không liền mạch. *Luôn kiểm tra ngữ pháp câu nối.*
- **Losing SEO Juice (Mất sức mạnh SEO)**: Tự ý sửa đổi thẻ H1 gốc, thay đổi URL slug, hoặc làm đứt gãy internal link cũ.
