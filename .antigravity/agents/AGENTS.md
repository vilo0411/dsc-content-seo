# SEO Agent Ecosystem

This directory contains the persona definitions for the SEO Content System. These agents are designed to be modular and task-specific to minimize token usage and maximize accuracy.

| Agent | File | Primary Responsibility |
| :--- | :--- | :--- |
| **SEO Collector** | `seo-collector.md` | SERP research, Content Brief & Outline generation. |
| **Research Agent** | `research-agent.md` | Building the foundational Knowledge Base (Layer 1). |
| **Brand Guardian** | `brand-guardian.md` | Ensuring brand compliance and Anti-AI style. |
| **Quality Guardian** | `quality-guardian.md` | QA/QC, fact-checking, and final editing. |
| **Visual Architect** | `visual-architect.md` | Image strategy and prompt generation. |

## Usage Principles
1. **Separation of Concerns**: Only the Main Agent (the AI you are talking to) writes the final content. Sub-agents provide the *context* and *rules*.
2. **Context-Only Load**: Load these agents only when performing their specific phase in the pipeline.
3. **Reference by Path**: Use the full path when calling a sub-agent's logic.
