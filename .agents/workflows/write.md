---
description: Kích hoạt quy trình viết bài SEO chuẩn Framework (Full Pipeline)
---

# Lệnh: /write [keyword] [options]

## Options Hỗ Trợ
- `--step`: Viết từng bước, dừng lại chờ `/approve` tại mỗi gate.
- `--auto`: Tự động chạy toàn bộ pipeline đến Final, không cần duyệt.
- `--no-serp`: Bỏ qua bước SERP research (dùng khi đã có data ngoại tuyến).
- `--sprint`: Chế độ viết hàng loạt (batch), lần lượt từng keyword trong backlog.

---

## Quy trình thực thi chi tiết (Agent Sequencing)

### 🔄 Bước 0: System Context Load (BẮT BUỘC — trước mọi bước)
Trước khi làm bất cứ việc gì, hệ thống phải đọc:
1. `knowledge/1-brand/profile.md`
2. `knowledge/1-brand/personas.md`
3. `knowledge/3-pipeline/anti-ai-rules.md`
4. `knowledge/3-pipeline/glossary.md`
5. `knowledge/4-content/topic-clusters.md` — xác nhận keyword chưa có bài, cập nhật trạng thái thành `In Progress`
6. `.antigravity/memory/instincts.md` — nạp bài học từ các vòng viết trước

---

### ⚙️ Giai đoạn 1: Outlining (SEO Research + Expert Outline)
**Agent phụ trách:** SEO Collector + Brand Guardian (song song)

**Bước 1.1 — SEO Collector (SERP Research):**
- Kích hoạt skill `.antigravity/skills/seo-outlining/SKILL.md` → Step 1: Plan.
- Dùng skill `.antigravity/skills/web-serp/SKILL.md` — SERP Lookup + Content Extraction song song qua Jina AI. KHÔNG dùng browser.
- Thu thập: cấu trúc H-tag, số liệu thực tế, content gaps, UX elements.

**Bước 1.2 — Brand Guardian (Brand Context):**
- Chạy song song với 1.1 hoặc ngay sau khi 1.1 hoàn thành.
- Output: `Brand Context Snippet` — Persona, USPs bắt buộc, Anti-AI checklist riêng cho bài này.

**Bước 1.3 — SEO Collector (Expert Outline):**
- Kích hoạt skill `.antigravity/skills/seo-outlining/SKILL.md` → Step 2: Validate.
- Tích hợp Brand Context Snippet từ Brand Guardian vào Outline.
- Lưu Outline tại: `knowledge/4-content/1-outlines/[slug].md`.

**🚧 APPROVAL GATE 1:**
> Trình bày Outline kèm summary SERP findings cho người dùng.
> **DỪNG LẠI. Chờ người dùng gõ `/approve`.**
> Khi được approve: cập nhật `topic-clusters.md` → `Outline-Approved`.

---

### ⚙️ Giai đoạn 2: Drafting (Human-centric Draft)
**Agent phụ trách:** Main Agent (drafting) + Quality Guardian (QA)

**Bước 2.1 — Drafting:**
- Kích hoạt skill `.antigravity/skills/seo-drafting/SKILL.md` → Step 1: Execute.
- Đọc Outline đã approve từ `knowledge/4-content/1-outlines/[slug].md`.
- Viết bài theo 3S Rule (Specific, Story, Statistics). Internalize anti-ai-rules — không chỉ liệt kê.
- Lưu draft tại: `knowledge/4-content/2-drafts/Draft-[slug].md`.

**Bước 2.2 — Internal Linking:**
- Kích hoạt skill `.antigravity/skills/internal-linking/SKILL.md` → Mode: Contextual Insertion.
- Scan `knowledge/3-pipeline/anchor-index.md` để tìm link nội bộ phù hợp.
- Chèn tối thiểu 2 internal links vào draft.

**Bước 2.3 — Quality Guardian (QA):**
- Kích hoạt agent `.antigravity/agents/quality-guardian.md`.
- QA phải load: Outline gốc + anti-ai-rules + glossary + instincts.md.
- Kết quả: `PASS` hoặc `FAIL` với danh sách lỗi có số dòng.
- Nếu `FAIL`: sửa và chạy lại QA cho đến khi `PASS`.

**🚧 APPROVAL GATE 2:**
> Trình bày Draft + QA PASS report cho người dùng.
> **DỪNG LẠI. Chờ người dùng review và gõ `/approve`.**

---

### ⚙️ Giai đoạn 3: Finalize & Learn
**Agent phụ trách:** Main Agent + Content Feedback Loop

**Bước 3.1 — File Management (BẮT BUỘC):**
- Di chuyển `knowledge/4-content/2-drafts/Draft-[slug].md` → `knowledge/4-content/3-finalized/Final-[slug].md`.
- Cập nhật `knowledge/4-content/topic-clusters.md` → trạng thái `Finalized`.

**Bước 3.2 — Content Feedback Loop (Auto-trigger):**
- Kích hoạt skill `.antigravity/skills/content-feedback-loop/SKILL.md`.
- Phân tích sự khác biệt giữa Draft gốc và bản Final người dùng approve.
- Ghi bài học vào:
  - `knowledge/3-pipeline/revision-log.md` — log cụ thể theo bài
  - `knowledge/3-pipeline/anti-ai-rules.md` — nếu phát hiện pattern mới
  - `.antigravity/memory/instincts.md` — bản năng tổng hợp

**Bước 3.3 — Delivery:**
- Xác nhận đường dẫn file Final cho người dùng.
- Hiển thị tóm tắt: "Đã học X bài học mới từ vòng viết này."

---

## Luồng Quyết định theo Options

```
/write [keyword]
  └── --step  → Dừng tại mỗi GATE, chờ /approve
  └── --auto  → Bỏ qua GATE, chạy thẳng đến Final
  └── --no-serp → Bỏ qua Bước 1.1, dùng data có sẵn trong KB
  └── --sprint  → Lặp lại toàn bộ pipeline cho từng keyword trong backlog
```
