---
name: Independent Quality Assurance
description: >
  Use this skill to perform a rigorous, final audit of any content before publication. 
  It acts as the final gatekeeper for SEO integrity, Brand compliance, and Fact-checking.
---

# Skill: Independent Quality Assurance

## 🛠️ Audit Procedure

1. **Intake**: Load the draft from `content/blog/2-user-review/`.
2. **Context Matching**:
   - Compare with the original Outline in `1-outlines/`.
   - Check against Search Intent requirements.
3. **Rule Enforcement**:
   - Run the **Anti-AI Vibe** check using `knowledge/3-pipeline/anti-ai-rules.md`.
   - Verify brand terminology using `knowledge/3-pipeline/glossary.md`.
4. **Scoring & Reporting**:
   - Issue a PASS or FAIL status.
   - For FAIL: Provide a list of "Must-fix" vs. "Suggested" improvements.

---

## 🚦 Hard Assertions (PASS Criteria)
- [ ] **SEO**: Target keyword is in the H1 and Meta Description.
- [ ] **Tone**: No flowery or redundant AI introductions (e.g., "In the ever-changing landscape...").
- [ ] **Truth**: All claims match the `knowledge/1-brand/profile.md`.
- [ ] **Structure**: Proper hierarchy (H1 -> H2 -> H3).

---

## ⚠️ Gotchas
- **Blind Trust**: Assuming the Main Agent followed the Outline perfectly. *Always re-verify the draft against the intent.*
- **Outdated Data**: Fact-checking against general internet knowledge instead of the brand's Knowledge Base. *Prioritize internal KB.*
