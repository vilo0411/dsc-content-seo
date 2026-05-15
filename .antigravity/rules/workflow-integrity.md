# Rule: Workflow Integrity

1.  **Phase-Gate Protocol**: Never skip phases. Every task must follow: `Research -> Outline -> User Approve -> Draft -> QA -> User Approve -> Finalize -> Learn`.
    *   **Research Requirement**: Must use `.antigravity/skills/web-serp/SKILL.md` (Jina AI) for SERP lookup and competitor extraction. Do not use browser directly. Do not rely on snippets.

2.  **Mandatory Context Loading**: Before starting ANY phase or agent, load the full context set:
    *   `knowledge/1-brand/profile.md`
    *   `knowledge/3-pipeline/anti-ai-rules.md`
    *   `knowledge/3-pipeline/glossary.md`
    *   `.antigravity/memory/instincts.md`
    *   **Agent-specific files** as listed in each agent's "Context Loading" block.
    *   **Failure to load context = Invalid execution.** Stop and load before proceeding.

3.  **No Hallucinations**: All interest rates, market data, and facts must be grounded in SERP or Knowledge Base. If data is missing, STOP and ask the user.

4.  **Mandatory Approval Gates**: 
    *   Do not proceed to Drafting without a clear `/approve` on the Outline.
    *   Do not Finalize without a clear `/approve` on the Draft.
    *   After each gate, confirm the state update in `topic-clusters.md` before moving on.

5.  **Inline Revision Logging**: Bất cứ khi nào user yêu cầu sửa nội dung trong chat (VD: "sửa đoạn này", "đổi câu kia"), agent phải **log ngay** vào `knowledge/3-pipeline/revision-log.md` trước khi thực hiện sửa. Không chờ đến `/approve` mới ghi.

6.  **Quality Guardian is Non-Negotiable**: Every draft must pass QA before being presented to the user. A draft with unresolved QA FAILs must NOT be surfaced for approval.
