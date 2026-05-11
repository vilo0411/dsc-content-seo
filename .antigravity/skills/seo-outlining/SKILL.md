# Skill: SEO Outlining (Phase 1 & 2)

This skill focuses on SERP intelligence and creating high-detail Content Briefs that outperform competitors.

## 🛠️ Execution Strategy: Plan & Validate

### Step 1: Plan (SERP & Context Collection)
1. **SERP Research (MANDATORY)**: Use `search_web` to analyze Top 3-5 competitors for the target keyword. Extract:
    *   Actual data (interest rates, figures, specific facts).
    *   Heading structures (H2/H3).
    *   Content gaps and unique angles.
2. **Consult Knowledge**: Read brand profile and anti-ai rules.
3. **Verify Product Match**: Identify which brand product fits this specific intent.

### Step 2: Validate (Expert Outline)
1. **Generate Outline**: Use the template at `references/brief-template.md`. 
2. **Dynamic Rules**: Extract prohibited phrases from `knowledge/3-pipeline/anti-ai-rules.md` and insert them into the `Anti_AI_Flags` YAML field.
3. **SERP Proofing**: Ensure the `SERP Data Points` section contains actual figures found in Step 1. **DO NOT hallucinate data.**
4. **User Approval**: Present to user with a summary of SERP findings. **DO NOT proceed without `/approve`**.

## 📦 Reference Materials
- [Brief Template](references/brief-template.md)
