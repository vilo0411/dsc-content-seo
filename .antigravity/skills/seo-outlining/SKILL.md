# Skill: SEO Outlining (Phase 1 & 2)

This skill focuses on SERP intelligence and creating high-detail Content Briefs that outperform competitors.

## 🛠️ Execution Strategy: Plan & Validate

### Step 1: Plan (SERP & Context Collection)
1. **SERP Research (MANDATORY)**:
    *   **Dùng `.antigravity/skills/web-serp/SKILL.md`** — không dùng browser trực tiếp.
    *   **Function 1 — SERP Lookup**: WebFetch `https://r.jina.ai/https://www.bing.com/search?q=<từ+khóa+url+encoded>` để lấy top 5–10 URLs. Query = Target Keyword, không dùng tiêu đề bài hay tên file.
    *   **Function 2 — Content Extraction**: Chọn **tối đa 3–4 URL** có nội dung phong phú nhất (ưu tiên `.com.vn`, `.gov.vn`, loại bỏ trang quảng cáo/forum không có số liệu). Gọi **song song** qua `https://r.jina.ai/{url}`. Bỏ qua URL trả về nội dung rỗng hoặc < 200 ký tự. **Chỉ giữ lại tối đa 2.000 từ đầu mỗi trang** — đủ để lấy H-tags và data points chính, không cần toàn văn.
    *   Extract từ markdown output:
        *   Actual data (interest rates, figures, specific facts).
        *   Detailed heading structures (H1/H2/H3/H4) theo đúng thứ tự.
        *   Intent từng section — trả lời câu hỏi gì của reader?
        *   Content gaps, unique angles, and UX elements (tables, calculators, FAQ schema).
    *   **Chạy Competitor Gap Synthesis** theo format trong `web-serp/SKILL.md` — bắt buộc trước khi sang Step 2.
2. **Consult Knowledge**: Read brand profile and anti-ai rules.
3. **Verify Product Match**: Identify which brand product fits this specific intent.
4. **Internal Link Planning**: **KHÔNG đọc toàn bộ `anchor-index.md`** (file lớn, tốn token). Thay thế: dùng Grep tìm trong `knowledge/3-pipeline/anchor-index.md` với 2–3 từ khóa liên quan đến topic hiện tại (ví dụ: `grep "lãi suất"` hoặc `grep "tiết kiệm"`). Chọn 2–3 kết quả phù hợp nhất để link. Ghi vào field `Internal_Links:` của outline YAML theo format:
    ```yaml
    Internal_Links:
      - anchor: "[anchor text]"
        url: "[url từ anchor-index]"
        suggested_placement: "[tên H2 nên chèn link]"
    ```

### Step 2: Validate (Expert Outline)
1. **Generate Outline**: Use the template at `references/brief-template.md`. 
2. **Anti-AI Mastery**: Do not just list rules. **Apply** them to the outline's headings and descriptions. Ensure the outline itself avoids "AI-vibe" (e.g., no "In this section, we will explore...").
3. **SERP Proofing**: Ensure the `SERP Data Points` section contains actual figures found via Jina extraction in Step 1. **DO NOT hallucinate data.** Ngoài ra, đối chiếu và áp dụng các thông số cập nhật mới nhất từ Cơ sở dữ liệu chứng khoán tham chiếu 2026 tại `knowledge/3-pipeline/anti-ai-rules.md`.
4. **User Approval**: Present to user with a summary of SERP findings. **DO NOT proceed without `/approve`**.

## 📦 Reference Materials
- [Brief Template](references/brief-template.md)
