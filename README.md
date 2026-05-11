# SEO Writer Agent Boilerplate

A modular, cross-platform template for professional SEO content production. Works seamlessly with **Claude Code**, **Gemini CLI**, and **Antigravity**.

## 🚀 Quick Start

1. **Initialize Project:**
   Copy the contents of this boilerplate into your new project directory.
   ```bash
   cp -r . /path/to/your-new-seo-project/
   ```

2. **Interactive Setup:**
   Run the following command to start the interactive onboarding and build your knowledge base:
   ```text
   /setup
   ```
   *The system will initialize your project structure and ask for your Brand Name, Website, and Competitors to build the `knowledge/1-brand` and `knowledge/2-market` contexts.*

3. **Plan Keywords:**
   Run the clustering command to generate a Topic Cluster Map from your keyword CSV or raw files:
   ```text
   /cluster
   ```
   Then choose which articles to write next:
   ```text
   /keyword-plan
   ```

4. **Start Writing:**
   Activate the standardized SEO writing framework:
   ```text
   /write "your target keyword"
   ```

5. **Review & Approve:**
   Approve the current stage (Outline → Draft → Final) to progress the pipeline:
   ```text
   /approve
   ```

## 🏗️ Architecture

Following the **Zen Structure 2.0** methodology, the repository is logically divided into two main domains:

### 1. The Engine (`.agents/` & `.antigravity/`)
Contains the core logic, autonomous workflows, and isolated skills (Plan-Validate-Execute framework).

- **`.agents/workflows/`**: Command routing for tasks like `/setup`, `/write`, `/optimize`, etc.
- **`.antigravity/skills/`**: Specialized capabilities (e.g., `seo-optimization`, `seo-writing`) enforcing hard assertions and progressive disclosure.
- **`.antigravity/agents/`**: Task-specific, persona-based sub-agents (e.g., SEO Collector, Brand Guardian).

### 2. The Brain & Factory (`knowledge/`)
A centralized, standardized data structure ensuring multi-platform portability and token efficiency.

- **`knowledge/1-brand/`**: Brand Identity, Personas, ICP, and Voice guidelines.
- **`knowledge/2-market/`**: Market Landscape, Competitors, and Topic Cluster Maps.
- **`knowledge/3-pipeline/`**: Content strategy, backlog, keyword lists, and Sprint Planners.
- **`knowledge/4-content/`**: The production line spanning granular stages (`0-raw` -> `1-outline` -> `2-draft` -> `3-finalized`).
- **`knowledge/raw/`**: Raw, unprocessed uploads (e.g., client briefs, data dumps).

## ⚡ Key Features

- **Zen Structure 2.0:** Standardized modular design for seamless scaling and multi-project portability without context degradation.
- **Token Efficiency:** Context-selective agents and progressive disclosure ensure you don't burn tokens on unnecessary context.
- **Hard Assertions & Quality Assurance:** Mandatory audit templates and independent QA/QC checkpoints maintain human-like, authoritative content.
- **Granular Pipeline Control:** Distinct stages for content (Planned, Optimizing, Finalized) aligned perfectly with brand and strategy rules.

## 🛠️ Requirements
- AI Assistant supporting Slash Commands (Claude Code, Gemini CLI, or Antigravity).
- Internet access (for SERP research and Web Fetching).
