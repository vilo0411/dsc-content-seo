# Skill: Content Feedback Loop (Learning & Synthesis)

This skill is the "Brain" of the project. It ensures that the system never makes the same mistake twice by analyzing the history of user feedback and manual revisions.

## 🛠️ Execution Strategy: Analyze-Synthesize-Update

This skill is triggered after the FINAL `/approve` of an article.

### Step 1: Historical Audit (Multi-version Analysis)
1. **Gather Data**: Retrieve all versions of the draft (v1, v2, v3...) and the corresponding User Feedback for the current article.
2. **Diff Analysis**: Identify consistent manual changes made by the user or requested in feedback.
3. **Pattern Recognition**:
   - What words/phrases does the user consistently remove?
   - What structure/tone does the user consistently ask for?
   - What factual corrections were made?

### Step 2: Synthesis of Rules
1. **Rule Generation**: Convert identified patterns into actionable instructions.
   - Example: "User removed 'Trong kỷ nguyên số' 3 times" -> Rule: Add to `Anti_AI_Flags`.
   - Example: "User asked for more 'Specific Statistics' in every H2" -> Rule: Update `brief-template.md` requirements.
2. **Persona Update**: Adjust the writing persona if the feedback relates to Tone (e.g., "Too formal").

### Step 3: Knowledge Base Update
1. **Update Anti-AI Rules**: Append new banned phrases to `knowledge/3-pipeline/anti-ai-rules.md`.
2. **Update Revision Log**: Log the specific learnings in `knowledge/3-pipeline/revision-log.md` with the article reference.
3. **Report to User**: Present a summary of what the AI has learned: *"I have learned 3 new rules from your feedback on this article..."*

## 🚦 Triggers
- Triggered automatically after a final `/approve` command.
- Can be triggered manually with `/learn [article_path]` to analyze a specific history.

## ⚠️ Critical Rule
- **No Over-generalization**: A one-time correction might be topic-specific. Only synthesize into a "General Rule" if the pattern is repeated or explicitly stated as a global preference.
