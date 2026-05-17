# Strategic Decisions & Lessons Learned (DECISIONS.md)

This file tracks key decisions made during the project lifecycle to ensure long-term consistency.

---

## 🏛️ Architectural Decisions
- **2026-05-17:** Adopted the **Multi-Agent (Sub-agent) Framework** for modularity.
- **2026-05-17:** All production files must follow the `0-sources` -> `1-outlines` -> `2-drafts` -> `3-finalized` pipeline.
- **2026-05-17:** Slash commands are the primary interface for triggering workflows.
- **2026-05-17:** Writer profiles added (`knowledge/1-brand/writers/`) — phân loại theo loại bài: educational / analytical / comparison.
- **2026-05-17:** Intel capture system added (`knowledge/raw/intel/`) — 30-second rule áp dụng khi SERP research.

## ✍️ Content & Style Decisions
- **2026-05-17:** Anti-AI rules established in `knowledge/3-pipeline/anti-ai-rules.md`. Chuẩn câu: tối đa 25 từ/câu, 2-3 câu/đoạn.
- **2026-05-17:** Target Persona selection is mandatory for every outline.
- **2026-05-17:** Mandatory linking strategy based on `anchor-index.md`.
- **2026-05-17:** Brand guidelines + anti-ai-rules luôn có độ ưu tiên cao hơn writer profiles khi xung đột.

## 💡 Lessons Learned (Retrospective)
- **2026-05-17:** Product Bridge cho bài kỹ thuật (P3) → ưu tiên Môi giới 1:1, không phải công cụ tư vấn số.
- **2026-05-17:** Bài về báo cáo tài chính cần thêm phần nền tảng ("cách tạo ra", "cấu trúc chi tiết") để satisfy academic search intent.
- **2026-05-17:** Không dùng ngoặc kép nhấn mạnh cho từ thông thường — trông AI rõ ràng.
