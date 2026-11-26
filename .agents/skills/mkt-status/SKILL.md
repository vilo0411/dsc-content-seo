---
name: mkt-status
description: Bảng trạng thái mọi việc marketing — job chiến dịch (Brief → Đóng), việc chờ duyệt, và tình trạng pipeline SEO/link hiện có.
---

# /mkt-status

1. Chiến dịch: `python scripts/campaign.py status` (hoặc `--json`).
2. SEO: `python scripts/topic_status.py --summary`.
3. Việc vận hành (link plan, syndication): đọc `knowledge/0-dashboard/status.json` (trường `tasks[].name/state/next_step`).
4. Mọi kênh: cùng file đó — `channels[]` (số liệu từng kênh), `channel_pending[]` (nháp ngoài SEO chờ duyệt), `activity_recent[]` (50 việc gần nhất). Cần dài hơn: `python scripts/activity_log.py tail --days 7 [--domain social]` · `stats`.

Trình bày 1 bảng ≤ 25 dòng, nhóm theo: **Chờ user duyệt** → Đang làm → Live cần đo (+7/+14/+28 ngày) → còn lại. Mỗi dòng có lệnh tiếp theo (`/social-post …`, `/ads-review …`, `/campaign-report …`). Không sửa file.
