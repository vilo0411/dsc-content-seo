---
name: mkt-status
description: Bảng trạng thái mọi việc marketing — job chiến dịch (Brief → Đóng), việc chờ duyệt, và tình trạng pipeline SEO/link hiện có.
---

# /mkt-status

1. Chiến dịch: `python scripts/campaign.py status` (hoặc `--json`).
2. SEO: `python scripts/topic_status.py --summary`.
3. Việc vận hành (link plan, syndication): đọc `knowledge/raw/operations/status.json` (trường `tasks[].name/state/next_step`).

Trình bày 1 bảng ≤ 25 dòng, nhóm theo: **Chờ user duyệt** → Đang làm → Live cần đo (+7/+14/+28 ngày) → còn lại. Mỗi dòng có lệnh tiếp theo (`/social-post …`, `/ads-review …`, `/campaign-report …`). Không sửa file.
