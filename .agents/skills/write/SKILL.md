---
name: write
description: "Cả pipeline bài SEO mới từ keyword: outline → duyệt → draft → QA → duyệt → finalize (--step, --auto, --no-serp, --sprint). Dùng khi /write <keyword> hoặc 'viết bài về …'. Chỉ một phase thì /outlining hoặc /drafting."
---

# /write — cả pipeline bài SEO

Điều phối 3 skill; **chi tiết từng bước chỉ nằm trong skill con** (không lặp lại ở đây):

| Giai đoạn | Làm theo | Dừng ở |
|---|---|---|
| 1. Outline | `.agents/skills/outlining/SKILL.md` (cannibalization gate → SERP → Brand Context → outline → `outline_lint`) | Gate 1: chờ `/approve` |
| 2. Draft | `.agents/skills/drafting/SKILL.md` (viết → internal link → CTA/banner → `qa_gate --cta --fix` → Quality Guardian) | Gate 2: chờ `/approve` |
| 3. Finalize | `.agents/skills/approve/SKILL.md` mục B | — |

## Bước 0 (1 lần)
1. Context theo `AGENTS.md` §4. Outline / draft vừa viết trong session → không mở lại file.
2. `python scripts/topic_status.py --find "<keyword>"` — đã có bài cùng intent → dừng, đề xuất `/optimize`. Chưa có dòng → `topic_status.py <slug> --add --keyword "<kw>" --cluster "<cluster>" --set Outlining`.
3. Mở `outlining/SKILL.md` ngay; `drafting/SKILL.md` chỉ mở sau Gate 1.

## Options
- `--step` (mặc định): dừng ở cả 2 gate.
- `--auto`: không chờ `/approve`, nhưng gate máy vẫn chặn — `outline_lint` hoặc `qa_gate` còn FAIL sau 2 vòng → dừng, báo user. Vẫn chạy `article_snapshot.py --stage gate2` trước khi finalize.
- `--no-serp`: bỏ `serp_research.py` ở giai đoạn 1, dùng cache `knowledge/raw/serp/` / dữ liệu user đưa; ghi `SERP: offline` vào outline.
- `--sprint`: lặp cả pipeline cho từng keyword `Planned` trong `knowledge/3-seo/strategy/sprint-backlog.md`; context load 1 lần cho cả lô; mỗi bài vẫn qua đủ gate.

## Báo cáo cuối
Đường dẫn Final + HTML CMS, dòng điểm (score · coverage · trust · slop), bài học mới (nếu có) — theo mục "Báo cáo" của `approve`.
