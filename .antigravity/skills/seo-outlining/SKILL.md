# Skill: SEO Outlining (Phase 1 & 2)

This skill focuses on SERP intelligence and creating high-detail Content Briefs that outperform competitors.

## 🛠️ Execution Strategy: Plan & Validate

### Step 1: Plan (SERP & Context Collection)
1. **SERP Research (MANDATORY)**:
    *   **Dùng `.antigravity/skills/web-serp/SKILL.md`** — không dùng browser trực tiếp.
    *   **Chạy 1 lệnh**: `python .antigravity/skills/web-serp/scripts/serp_research.py "<keyword>" --top 10 --extract 5` — DataForSEO (Google VN, vi) + Jina song song, cache 30 ngày. Query = Target Keyword, không dùng tiêu đề bài hay tên file. **Không dùng `--no-cache`** trừ khi user yêu cầu (API có phí).
    *   Script đã lọc nav/footer, giữ 2.000 từ đầu mỗi trang, in sẵn Headings / Data points / Special elements / PAA / Related Searches / Featured Snippet.
    *   Từ output script, bổ sung:
        *   Actual data (interest rates, figures, specific facts).
        *   Detailed heading structures (H1/H2/H3/H4) theo đúng thứ tự.
        *   Intent từng section — trả lời câu hỏi gì của reader?
        *   Content gaps, unique angles, and UX elements (tables, calculators, FAQ schema).
    *   **Chạy Competitor Gap Synthesis** theo format trong `web-serp/SKILL.md` — bắt buộc trước khi sang Step 2.
    *   **Điền `### PAA plan`** (cuối output script): mỗi câu PAA → `body` hoặc `faq`; Related Searches → `same_intent` / `spin_off`. Ghi kết quả vào YAML `PAA_Questions` + `Related_Searches` của outline (xem `brief-template.md`). Câu PAA không đối thủ nào có heading khớp = gap ưu tiên.
2. **Consult Knowledge**: Read brand profile and anti-ai rules.
3. **Verify Product Match**: Identify which brand product fits this specific intent.
4. **Internal Link Planning**: **KHÔNG đọc `anchor-index.md`.** Chạy `python scripts/find_links.py "[keyword]" --top 6` (thêm 1 lần với từ khoá phụ nếu cần) — script đã đối soát sitemap. Chọn 2–3 URL có Sitemap ✓. Ghi vào field `Internal_Links:` của outline YAML theo format:
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
