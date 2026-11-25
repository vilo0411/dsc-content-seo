# Domain: Paid Ads (Meta)

Công cụ: **Facebook Ads MCP** (`mcp__claude_ai_Facebook_Ads__*`, đã kết nối). Nếu tool đang deferred → load bằng ToolSearch trước khi gọi.

## Skill
| Lệnh | Làm | Ghi lên Meta? |
|---|---|---|
| `/ads-brief <mục tiêu>` | Brief: mục tiêu, persona, offer, KPI, audience, tham khảo Ad Library | Không |
| `/meta-ads-copy <brief\|job>` | N biến thể primary/headline/description + brief creative | Không |
| `/ads-review [campaign\|account] [--days 7\|14\|30]` | Đọc số, chẩn đoán, đề xuất | Không |
| `/ads-learn` | Rút hook/angle thắng-thua → `learnings.md` | Không |

Tạo campaign / ad set / ad / creative trên Meta **không phải skill mặc định**: chỉ làm khi user yêu cầu rõ trong lượt đó, xác nhận lại từng entity, luôn `PAUSED`, không đổi budget/bid khi chưa hỏi. Xem `.agents/core/README.md` §2.

## Context riêng
1. `.agents/domains/ads/references/meta-ads-playbook.md`
2. `.agents/domains/ads/learnings.md`
3. `.agents/core/rules/compliance-finance.md` §3 (quảng cáo tài chính)

## QA
`python scripts/mkt_lint.py <file> --channel meta-ad` → luôn chạy Compliance Reviewer trước gate (ads là kênh rủi ro compliance cao nhất).

## Lưu file
`knowledge/6-campaigns/<job>/ads/` — `brief.md`, `copy-v<n>.md`, `review-<YYYY-MM-DD>.md`. Số liệu kéo về: `knowledge/raw/ads/<YYYY-MM-DD>-<account|campaign>.json` (cache, để `/ads-learn` và `/campaign-report` đọc lại không gọi API).
