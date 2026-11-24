# Domain: Social / Fanpage

Kênh chủ: **Facebook Fanpage, Zalo OA, LinkedIn** (post gốc, lịch nội dung). Kênh syndication cộng đồng (X, Mastodon, BAND, Pinterest, Medium…) vẫn do `/syndicate` + `knowledge/raw/operations/syndication/` lo — không trùng việc.

## Skill
| Lệnh | Làm |
|---|---|
| `/social-plan [YYYY-MM]` | Lịch nội dung tháng cho fanpage/Zalo/LinkedIn |
| `/social-post <slug\|chủ đề> [--channel …]` | Viết post (tối đa 3 biến thể / kênh) + brief hình |

## Context riêng
1. `.antigravity/domains/social/references/channel-specs.md` — format, độ dài, giờ đăng gợi ý
2. `.antigravity/domains/social/references/content-pillars.md` — 4 trụ nội dung + tỷ lệ
3. `.antigravity/domains/social/learnings.md`
4. Hình: `knowledge/raw/operations/syndication/visual-styles.md` (S01–S04) + `knowledge/1-brand/brand.json`

## QA
`python scripts/mkt_lint.py <file> --channel facebook|zalo|linkedin` → Compliance Reviewer (`.antigravity/core/agents/compliance-reviewer.md`) nếu post có số liệu, lãi suất, phí, mã cổ phiếu.

## Lưu file
- Post lẻ: `knowledge/5-campaigns/<job>/social/<kênh>-<slug>-v1.md`. Post không thuộc chiến dịch: tạo job `CMP-<YYMMDD>-social-<YYYY-MM>` cho cả tháng.
- Lịch tháng: `<job>/social/calendar-<YYYY-MM>.csv` với cột `date,channel,pillar,persona,topic,source_slug,format,status,post_file`.
