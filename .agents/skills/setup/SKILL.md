---
name: setup
description: "Dựng Knowledge Base lần đầu (profile, ICP, persona, glossary, rules) qua Research Agent. Chỉ dùng khi khởi tạo project mới hoặc user yêu cầu xây lại knowledge/1-brand."
---

# Setup Knowledge Base

`/setup [company | audience | rules | all]` — chạy 1 lần khi khởi tạo project, hoặc khi user yêu cầu dựng lại. Vai trò thực hiện: `.agents/skills/setup/references/research-agent.md`.

| Tham số | Việc | Ghi vào |
|---|---|---|
| `company` | Hồ sơ công ty, sản phẩm, USP, tone | `knowledge/1-brand/profile.md` · fact có số → `knowledge/1-brand/brand-facts.json` |
| `audience` | ICP + persona P1–P4 | `knowledge/1-brand/icp.md` · `knowledge/1-brand/personas.md` |
| `rules` | Rule văn + glossary (từ template) | `knowledge/1-brand/anti-ai-rules.md` · `knowledge/1-brand/glossary.md` (mẫu: `.agents/templates/1-brand/`) |
| `all` | Cả 3, rồi cập nhật `.agents/context.md` cho khớp | |

Ghi `Status: Assumed ⚠️` cho thông tin chưa được user xác nhận; câu hỏi cần lãnh đạo chốt → `knowledge/1-brand/confirm-with-leadership.md`. Không ghi đè file đã có `Status: Verified` khi chưa hỏi user.
