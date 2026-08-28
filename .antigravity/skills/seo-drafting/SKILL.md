# Skill: SEO Drafting (Phase 3 & 4)

This skill focuses on converting an approved Outline into a high-quality, human-centric draft and learning from feedback.

## 🛠️ Execution Strategy: Execute & Finalize

### Step 1: Execute (Drafting & Quality)
1. **Context Loading**: Read the approved Outline from `knowledge/4-content/1-outlines/`.
2. **Anti-AI Drafting**: Write the draft by **demonstrating** the rules in `anti-ai-rules.md`. 
    *   Avoid all "AI-vibe" phrases and structures.
    *   Use the **3S Rule** (Specific, Story, Statistics) throughout.
    *   Maintain the **Persona** (Senior Expert) and **POV**.
    *   **Ngắt đoạn theo ngữ nghĩa (Semantic Grouping)**: Tránh ngắt đoạn cơ học (chia mỗi câu thành 1 đoạn). Hãy gộp các câu liên quan mật thiết thành các đoạn văn ngắn từ 2-3 câu để bài viết trôi chảy tự nhiên, đồng thời vẫn đáp ứng chuẩn Mobile-First (độ dài đoạn ≤ 3 câu, độ dài câu ≤ 30 từ).
    *   **Định dạng Danh sách**: Khi viết danh sách liệt kê, trước mỗi danh sách phải có câu dẫn dắt có dấu hai chấm `:`. Đối với các nhãn in đậm ở đầu mục danh sách, bắt buộc sử dụng dấu hai chấm `:` thay vì dấu chấm `.` làm ký tự phân tách nhãn và nội dung (Ví dụ: `* **Nhãn**: Nội dung`).
    *   Embed internal links theo `Internal_Links:` đã plan trong outline — đặt tự nhiên trong câu, không thêm riêng cuối bài. Toàn bộ link BẮT BUỘC phải dùng URL tuyệt đối (`https://www.dsc.com.vn/...`) đối soát chính xác từ sitemap live `https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml`, tuyệt đối không dùng đường dẫn file cục bộ (`file:///...`) hay relative path.
3. **4-Sweep Quality Check (BẮT BUỘC trước khi present)**: Sau khi viết xong, tự kiểm tra 4 sweeps sau trên toàn bài. Nếu fail bất kỳ điểm nào → sửa trước khi trình bày:
    - **So What?** — Mỗi H2 phải có ít nhất 1 câu trả lời rõ ràng "tại sao reader phải quan tâm đến section này?" Không chỉ mô tả — phải có lợi ích cụ thể.
    - **Prove It** — Mỗi claim/nhận định phải có số liệu, ví dụ cụ thể, hoặc case thực tế đi kèm. Sử dụng cơ sở dữ liệu chứng khoán tham chiếu 2026 tại `knowledge/3-pipeline/anti-ai-rules.md` để lấy dẫn chứng nhanh. Scan toàn bài: mọi câu dạng "[X] là quan trọng/tốt/hiệu quả" mà không có bằng chứng → rewrite.
    - **Specificity** — Grep các từ: "tốt", "nhanh", "hiệu quả", "đáng kể", "nhiều", "một số". Mỗi từ tìm được → thay bằng con số hoặc ví dụ cụ thể, hoặc xóa.
    - **GEO Check** — Scan từng H2: (1) Có ít nhất 1 câu thoả mãn Load-Bearing Claim (Extract-friendly + Verifiable + Specific) theo Phần 8.2 của `anti-ai-rules.md` không? (2) Mọi data point có prefix "Tính đến tháng M/Y" hoặc "Tháng M/Y:" không? (3) Chủ thể câu có phải brand/entity cụ thể không, hay đang bị động che khuất? Nếu fail bất kỳ H2 nào → thêm/sửa claim trước khi present.
4. **Internal QA**: Self-audit based on `anti-ai-rules.md`. If AI patterns are found, rewrite before presenting.
5. **Present Draft**: Deliver the draft to the user with a Feedback Table.

### Step 2: Finalize & Learn
1. **Iterative Revision**: Revise the draft based on user feedback rounds.
2. **Final Approval**: User issues `/approve` to finalize the article.
3. **File Management (MANDATORY)**: 
    *   Move the approved file from `knowledge/4-content/2-drafts/` to `knowledge/4-content/3-finalized/`.
    *   Rename the file to `Final-[slug].md`.
    *   Delete the original outline file `[slug].md` in `knowledge/4-content/1-outlines/` (if it exists) to clean up the repository.
    *   Update `knowledge/4-content/topic-clusters.md` status to `Finalized`.
4. **Learning**: Trigger **`content-feedback-loop`** skill to analyze revisions and update project rules in `.antigravity/memory/instincts.md`.
5. **Delivery**: Confirm finalized paths to the user.
