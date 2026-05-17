# Skill: SEO Outlining (Phase 1 & 2)

This skill focuses on SERP intelligence and creating high-detail Content Briefs that outperform competitors.

## 🛠️ Execution Strategy: Plan & Validate

### Step 1: Plan (SERP & Context Collection)
1. **SERP Research (MANDATORY)**:
    *   **Dùng `.antigravity/skills/web-serp/SKILL.md`** — không dùng browser trực tiếp.
    *   **Function 1 — SERP Lookup**: WebFetch `https://r.jina.ai/https://www.bing.com/search?q=<từ+khóa+url+encoded>` để lấy top 5–10 URLs. Query = Target Keyword, không dùng tiêu đề bài hay tên file.
    *   **Function 2 — Content Extraction**: Gọi **song song** tất cả URLs hợp lệ qua `https://r.jina.ai/{url}`. Bỏ qua URL trả về nội dung rỗng hoặc < 200 ký tự.
    *   Extract từ markdown output:
        *   Actual data (interest rates, figures, specific facts).
        *   Detailed heading structures (H1/H2/H3/H4) theo đúng thứ tự.
        *   Intent từng section — trả lời câu hỏi gì của reader?
        *   Content gaps, unique angles, and UX elements (tables, calculators, FAQ schema).
    *   **Chạy Competitor Gap Synthesis** theo format trong `web-serp/SKILL.md` — bắt buộc trước khi sang Step 2.
2. **Consult Knowledge**: Read brand profile and anti-ai rules.
3. **Verify Product Match**: Identify which brand product fits this specific intent.
4. **Internal Link Planning**: Đọc `knowledge/3-pipeline/anchor-index.md`. Identify 2–3 bài đã publish phù hợp nhất để link từ bài này. Ghi vào field `Internal_Links:` của outline YAML theo format:
    ```yaml
    Internal_Links:
      - anchor: "[anchor text]"
        url: "[url từ anchor-index]"
        suggested_placement: "[tên H2 nên chèn link]"
    ```

### Step 2: Validate (Expert Outline)
1. **Generate Outline**: Use the template at `references/brief-template.md`. 
2. **Anti-AI Mastery**: Do not just list rules. **Apply** them to the outline's headings and descriptions. Ensure the outline itself avoids "AI-vibe" (e.g., no "In this section, we will explore...").
3. **SERP Proofing**: Ensure the `SERP Data Points` section contains actual figures found via Jina extraction in Step 1. **DO NOT hallucinate data.**
4. **User Approval**: Present to user with a summary of SERP findings. **DO NOT proceed without `/approve`**.

## 📦 Reference Materials
- [Brief Template](references/brief-template.md)
