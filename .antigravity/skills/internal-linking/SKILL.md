---
name: Internal Linking & Audit
description: >
  Use this skill when the user needs to build a strong internal link architecture 
  or audit the health of existing links. It ensures that the content ecosystem 
  is interconnected, boosting SEO authority and user navigation.
---

# Skill: Internal Linking & Audit

## 🛠️ Procedures

### Mode: Contextual Insertion (During Drafting)
1. **Identify Targets**: Scan `knowledge/3-pipeline/anchor-index.md` for pages relevant to the current topic.
2. **Find Opportunities**: Look for natural mentions of target keywords in the draft.
3. **Insert Links**: Use relative paths (e.g., `../3-finalized/Final-slug.md`) and approved anchor text variations.

### Mode: Backfill (After Publishing)
1. **Source Search**: Scan `knowledge/4-content/3-finalized/` for old articles that could link TO the new article.
2. **Update**: Append links to old articles without breaking the flow.

### Mode: Audit (Health Check)
1. **Execute Script**: Run `python .antigravity/skills/internal-linking/scripts/link_audit.py`.
2. **Analyze Dashboard**: Review `knowledge/3-pipeline/internal-link-dashboard.md`.
3. **Fix Issues**: Address "Over-optimized" or "Under-linked" pages.

---

## 🚦 Success Assertions
- [ ] Every new post has at least 2 outgoing internal links.
- [ ] No broken links (404) or dead-end pages.
- [ ] Anchor texts are varied (Exact vs. Partial vs. Title).

---

## ⚠️ Gotchas
- **Generic Anchors**: Avoid "click here" or "read more". *Use descriptive keywords.*
- **Circular Links**: Page A linking to Page B, and Page B linking back to Page A in the same context.
- **Link Stuffing**: Too many links in a single paragraph. *Limit to 1 link per 100-150 words.*
