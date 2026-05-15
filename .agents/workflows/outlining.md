---
description: Nghiên cứu SERP và tạo Expert Outline (Phase 1 & 2 của write pipeline)
---

# Lệnh: /outlining [keyword]

Dùng khi bạn chỉ muốn thực hiện bước Research + Outline mà chưa cần viết bài ngay.
Tương đương với `Phase 1` và `Phase 2` của lệnh `/write`.

## Quy trình thực thi

### 🔄 Bước 0: Context Load (BẮT BUỘC)
1. `knowledge/1-brand/profile.md`
2. `knowledge/1-brand/personas.md`
3. `knowledge/3-pipeline/anti-ai-rules.md`
4. `knowledge/3-pipeline/glossary.md`
5. `knowledge/4-content/topic-clusters.md`
6. `.antigravity/memory/instincts.md`

### Bước 1: SEO Collector — SERP Research
- Kích hoạt agent `.antigravity/agents/seo-collector.md`.
- Kích hoạt skill `.antigravity/skills/seo-outlining/SKILL.md` → Step 1: Plan.
- Dùng skill `.antigravity/skills/web-serp/SKILL.md` — SERP Lookup + Content Extraction song song qua Jina AI. KHÔNG dùng browser.
- Thu thập: H-tag structure, số liệu cụ thể, content gaps, UX elements.

### Bước 2: Brand Guardian — Brand Context
- Kích hoạt agent `.antigravity/agents/brand-guardian.md`.
- Output: `Brand Context Snippet` gồm Persona, mandatory USPs, Anti-AI checklist cho bài này.

### Bước 3: Expert Outline Generation
- Tích hợp Brand Context Snippet vào output của SERP Research.
- Tạo Outline theo template `.antigravity/skills/seo-outlining/references/brief-template.md`.
- Lưu tại: `knowledge/4-content/1-outlines/[slug].md`.
- Cập nhật `topic-clusters.md` → trạng thái `Outlining`.

### 🚧 APPROVAL GATE:
> Trình bày Outline + SERP summary cho người dùng.
> **DỪNG LẠI. Chờ `/approve` trước khi tiếp tục sang drafting.**
> Khi approve: cập nhật `topic-clusters.md` → `Outline-Approved`.
