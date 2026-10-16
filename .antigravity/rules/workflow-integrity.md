# Rule: Workflow Integrity

1.  **Phase-Gate Protocol**: Never skip phases. Every task must follow: `Research -> Outline -> User Approve -> Draft -> QA -> User Approve -> Finalize -> Learn`.
    *   **Research Requirement**: Must use `.antigravity/skills/web-serp/SKILL.md` (`serp_research.py`: DataForSEO + Jina, cached — do not bypass cache) for SERP lookup and competitor extraction. Do not use browser directly. Do not rely on snippets.

2.  **Mandatory Context Loading**: Before starting ANY phase or agent, load the full context set:
    *   `knowledge/1-brand/profile.md`
    *   `knowledge/3-pipeline/anti-ai-rules.md`
    *   `knowledge/3-pipeline/glossary.md`
    *   `.antigravity/memory/instincts.md`
    *   **Agent-specific files** as listed in each agent's "Context Loading" block.
    *   **Failure to load context = Invalid execution.** Stop and load before proceeding.

3.  **No Hallucinations**: All interest rates, market data, and facts must be grounded in SERP, the Knowledge Base, or `scripts/market_facts.py` (live OHLCV + listed-symbol list). Never write a price, index level, or ticker from memory. If the data source is unreachable (exit 3), fall back to structural facts that do not expire (biên độ HOSE 7% / HNX 10% / UPCoM 15%, T+2, lô 100 cp) — see `anti-ai-rules.md` §8.7e. If data is still missing, STOP and ask the user.

3a. **Three-Layer QA (bắt buộc, không bỏ tầng nào)**: mọi file trong `knowledge/4-content/` trước khi trình bày hoặc finalize phải qua:
    *   **Tầng A — `scripts/qa_lint.py`**: từ vựng, format, SEO, link, word count. Exit 1 = FAIL.
    *   **Tầng B — `scripts/slop_check.py` (BLOCKING)**: nhịp câu, mật độ bằng chứng, câu sáo rỗng, trùng khung H2. Score < 80 = FAIL. Tầng A **không** thấy được các lỗi này — bài 100/100 ở tầng A vẫn có thể là slop.
    *   **Tầng dữ liệu — `scripts/market_facts.py --verify` (advisory)**: `FACT-index-wrong` / `FACT-ticker` phải sửa; `FACT-stale` cần thêm 1 mốc trong 18 tháng. Exit 3 không chặn pipeline.
    *   **Tầng C — Quality Guardian**: chỉ gọi khi tầng A + B đã PASS.
    *   Vòng lặp sửa–check **tối đa 2 vòng**; vẫn FAIL → dừng, trình bày `⚠️ Remaining issues`.

4.  **Mandatory Approval Gates**: 
    *   Do not proceed to Drafting without a clear `/approve` on the Outline.
    *   Do not Finalize without a clear `/approve` on the Draft.
    *   After each gate, confirm the state update in `topic-clusters.md` before moving on.

5.  **Inline Revision Logging**: Bất cứ khi nào user yêu cầu sửa nội dung trong chat (VD: "sửa đoạn này", "đổi câu kia"), agent phải **log ngay** vào `knowledge/3-pipeline/revision-log.md` trước khi thực hiện sửa. Không chờ đến `/approve` mới ghi.

6.  **Quality Guardian is Non-Negotiable**: Every draft must pass QA before being presented to the user. A draft with unresolved QA FAILs must NOT be surfaced for approval.
