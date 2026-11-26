---
name: social-post
description: Viết post Facebook Fanpage / Zalo OA / LinkedIn từ 1 bài đã live hoặc 1 chủ đề — tối đa 3 biến thể/kênh, QA compliance, brief hình. Không tự đăng.
---

# /social-post <slug|chủ đề> [--channel facebook,zalo,linkedin] [--job CMP-…] [--variants N]

## Bước 0 — Context (1 lần/session)
`.agents/core/README.md` §1 (profile, brand.json, compliance-finance, blacklist) + `.agents/domains/social/README.md` và các file nó liệt kê.

## Bước 1 — Chất liệu
- Có slug: xác nhận bài đã live (`grep <slug> knowledge/3-seo/logs/publish-ledger.csv`; cần nội dung live: `python scripts/sync_live.py --show <slug>`). Lấy 1 ý mạnh nhất + số liệu có nguồn trong bài. Finalized nhưng chưa live → dừng, báo user.
- Chủ đề tự do: `python scripts/news_feed.py --topic "<chủ đề>" --days 14`, số liệu `python scripts/market_facts.py --brief`.
- Persona: chọn theo kênh (channel-specs.md) → `python scripts/persona.py P<n> --part tone`.

## Bước 2 — Viết
- Mặc định kênh: facebook. Mỗi kênh ≤ 3 biến thể (mặc định 2), mỗi biến thể 1 mục `## <kênh> · V<n> · <format>`.
- Mỗi biến thể: câu mở theo giới hạn hook, thân, CTA (link bài web hoặc CTA persona), hashtag, dòng `Hình:` (style S01–S04 + chữ trên ảnh ≤ 8 từ, hoặc "dùng ảnh bài gốc: <url>").
- Claim không có trong `profile.md` → gắn `[CẦN PHÁP CHẾ DUYỆT]`.

## Bước 3 — QA (tối đa 2 vòng)
```bash
python scripts/mkt_lint.py <file> --channel <kênh>
```
Có số liệu / phí / lãi suất / mã cổ phiếu → chạy Compliance Reviewer (`.agents/core/agents/compliance-reviewer.md`, sub-agent read-only).

## Bước 3b — Ảnh
Biến thể cần ảnh mới (dòng `Hình:` có kích thước + style, không phải "dùng ảnh bài gốc") → `/creative <file post>`: init → điền slide carousel → render → QA máy + creative-qa.

## Bước 4 — Lưu & gate
- File: `knowledge/6-campaigns/<job>/social/<kênh>-<slug>-v1.md`. Không có `--job` → `python scripts/campaign.py path social-<YYYY-MM>` hoặc tạo `python scripts/campaign.py new social-<YYYY-MM> --title "Social <tháng>" --channels social`.
- Trình bày ≤ 25 dòng: biến thể đề xuất, kết quả lint, QA ảnh + link `social/creatives/v<N>/preview.html`, việc cần user (pháp chế, ảnh minh hoạ). Dừng chờ duyệt.
- User duyệt → copy bản chọn vào `<job>/approved/`. Muốn đưa lên kênh syndication cộng đồng → `/syndicate <slug>`.

## Ghi activity log (bước cuối)
Sau khi lưu output (và sau mỗi lần user duyệt → `--action approve`): `python scripts/activity_log.py add --domain social --skill social-post --action create --target <CMP-id> --path <file post>`. Hiện ở tab **Hoạt động** của `knowledge/0-dashboard/index.html`.
