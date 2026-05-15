# Skill: SEO Drafting (Phase 3 & 4)

This skill focuses on converting an approved Outline into a high-quality, human-centric draft and learning from feedback.

## 🛠️ Execution Strategy: Execute & Finalize

### Step 1: Execute (Drafting & Quality)
1. **Context Loading**: Read the approved Outline from `knowledge/4-content/1-outlines/`.
2. **Anti-AI Drafting**: Write the draft by **demonstrating** the rules in `anti-ai-rules.md`. 
    *   Avoid all "AI-vibe" phrases and structures.
    *   Use the **3S Rule** (Specific, Story, Statistics) throughout.
    *   Maintain the **Persona** (Senior Expert) and **POV**.
3. **Internal QA**: Self-audit based on `anti-ai-rules.md`. If AI patterns are found, rewrite before presenting.
4. **Present Draft**: Deliver the draft to the user with a Feedback Table.

### Step 2: Finalize & Learn
1. **Iterative Revision**: Revise the draft based on user feedback rounds.
2. **Final Approval**: User issues `/approve` to finalize the article.
3. **File Management (MANDATORY)**: 
    *   Move the approved file from `knowledge/4-content/2-drafts/` to `knowledge/4-content/3-finalized/`.
    *   Rename the file to `Final-[slug].md`.
    *   Update `knowledge/4-content/topic-clusters.md` status to `Finalized`.
4. **Learning**: Trigger **`content-feedback-loop`** skill to analyze revisions and update project rules in `.antigravity/memory/instincts.md`.
5. **Delivery**: Confirm finalized paths to the user.
