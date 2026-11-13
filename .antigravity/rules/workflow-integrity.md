# Rule: Workflow Integrity

1.  **Phase-Gate Protocol**: Never skip phases. Every task must follow: `Research -> Outline -> User Approve -> Draft -> QA -> User Approve -> Finalize -> Learn`.
    *   **Research Requirement**: Must use `.antigravity/skills/web-serp/SKILL.md` (`serp_research.py`: DataForSEO + local parser, Jina fallback, cached — do not bypass cache) for SERP lookup and competitor extraction. Do not use browser directly. Do not rely on snippets.

2.  **Mandatory Context Loading**: the context set and the "load once per session" rule live in `CLAUDE.md` §Mandatory Context Protocol (single source). Agent-specific files are listed in each agent's "Context Loading" block. **Failure to load context = Invalid execution.**

3.  **No Hallucinations**: All interest rates, market data, and facts must be grounded in SERP, the Knowledge Base, or `scripts/market_facts.py` (live OHLCV + listed-symbol list). Never write a price, index level, or ticker from memory. If the data source is unreachable (exit 3), fall back to structural facts that do not expire (biên độ HOSE 7% / HNX 10% / UPCoM 15%, T+2, lô 100 cp) — see `anti-ai-rules.md` §8.7e. If data is still missing, STOP and ask the user.

3a. **Three-Layer QA (bắt buộc, không bỏ tầng nào)**: mọi file trong `knowledge/4-content/` trước khi trình bày hoặc finalize phải qua:
    *   **Một lệnh cho A + B + dữ liệu:** `python scripts/qa_gate.py <file>`.
    *   **Tầng A — `scripts/qa_lint.py`**: hình thức (từ vựng, format, SEO, link, word count) **và thực chất** (`coverage`: thuật ngữ đối thủ, Information_Gain, PAA, trùng lặp · `trust`: nguồn gốc, miễn trừ, bằng chứng thực tế). Exit 1 = FAIL.
    *   **Tầng B — `scripts/slop_check.py` (BLOCKING)**: nhịp câu, mật độ bằng chứng, câu sáo rỗng, trùng khung H2. Score < 80 = FAIL. Tầng A **không** thấy được các lỗi này — bài 100/100 ở tầng A vẫn có thể là slop.
    *   **Tầng dữ liệu — `scripts/market_facts.py --verify` (advisory)**: `FACT-index-wrong` / `FACT-ticker` phải sửa; `FACT-stale` cần thêm 1 mốc trong 18 tháng. Exit 3 không chặn pipeline.
    *   **Tầng C — Quality Guardian**: chỉ gọi khi tầng A + B đã PASS.
    *   Vòng lặp sửa–check **tối đa 2 vòng**; vẫn FAIL → dừng, trình bày `⚠️ Remaining issues`.

4.  **Mandatory Approval Gates**: 
    *   Do not proceed to Drafting without a clear `/approve` on the Outline.
    *   Do not Finalize without a clear `/approve` on the Draft.
    *   After each gate, set and confirm the state with `python scripts/topic_status.py <slug> [--set …]` (never open `topic-clusters.md`).
    *   Gate output shown to the user = a summary (≤ 25 lines) + the file path. Never paste the whole outline / draft into chat.

5.  **Inline Revision Logging**: Bất cứ khi nào user yêu cầu sửa nội dung trong chat (VD: "sửa đoạn này", "đổi câu kia"), agent phải **log ngay** bằng `python scripts/revision_log.py add <slug> --fix … --pattern … --rule …` trước khi thực hiện sửa (không mở `revision-log.md`). Không chờ đến `/approve` mới ghi.

6.  **Quality Guardian is Non-Negotiable**: Every draft must pass QA before being presented to the user. A draft with unresolved QA FAILs must NOT be surfaced for approval.
