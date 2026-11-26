---
name: social-plan
description: Lập lịch nội dung tháng cho Fanpage / Zalo OA / LinkedIn theo 4 pillar, lấy chất liệu từ bài SEO đã live + tin thị trường. Ra file CSV, không viết post.
---

# /social-plan [YYYY-MM] [--channels facebook,zalo,linkedin]

## Bước 0 — Context
`.agents/core/README.md` §1 + `.agents/domains/social/README.md`, `references/content-pillars.md`, `references/channel-specs.md`, `learnings.md`.

## Bước 1 — Nguồn
1. Bài live gần đây và bài có traffic: `knowledge/3-seo/logs/publish-ledger.csv`; số GSC nếu có MCP SEO Dashboard (`query_search_analytics`, dimension page) — ưu tiên bài clicks cao / bài mới 2–6 tuần.
2. Sự kiện tháng: `python scripts/news_feed.py --topic "chứng khoán" --days 30`; lịch cố định (họp FOMC, đáo hạn phái sinh, công bố BCTC quý) — ghi "cần xác minh ngày" nếu không chắc.
3. Ma trận persona: `python scripts/persona.py --matrix`.

## Bước 2 — Lịch
- Tần suất & tỷ lệ pillar theo `content-pillars.md`; không 2 post Sản phẩm liền ngày.
- Mỗi dòng: `date,channel,pillar,persona,topic,source_slug,format,status,post_file` — status = `Planned`, post_file trống.
- Tạo/tìm job: `python scripts/campaign.py new social-<YYYY-MM> --title "Social <MM/YYYY>" --channels social` (đã có thì `campaign.py path`).
- Ghi `<job>/social/calendar-<YYYY-MM>.csv`.

## Bước 3 — Gate
Trình bày: số post theo kênh × pillar, 5 post đầu tiên, khoảng trống cần user (ảnh con người DSC, ưu đãi tháng). Dừng chờ duyệt. Sau duyệt: `python scripts/campaign.py set social-<YYYY-MM> --status "Đang làm"`; từng dòng viết bằng `/social-post`.

## Ghi activity log (bước cuối)
Sau khi lưu output (và sau mỗi lần user duyệt → `--action approve`): `python scripts/activity_log.py add --domain social --skill social-plan --action create --target <CMP-id> --path <calendar-YYYY-MM.csv>`. Hiện ở tab **Hoạt động** của `knowledge/0-dashboard/index.html`.
