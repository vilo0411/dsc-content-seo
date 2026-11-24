# Core — dùng chung cho mọi domain marketing

> Lớp này áp cho **mọi** skill: SEO, Social, Ads, Campaign/Landing. Rule riêng của từng kênh nằm ở `.antigravity/domains/<domain>/`.
> Pipeline SEO hiện chưa move vào `domains/seo/` (xem DECISIONS 2026-11-24) — vẫn chạy ở `.antigravity/skills|agents|rules/` như cũ.

## 1. Context load (1 lần / session, trước mọi output)

| # | File | Ai đọc |
|---|---|---|
| 1 | `knowledge/1-brand/profile.md` | mọi domain |
| 2 | `knowledge/1-brand/brand.json` | domain có hình / landing / ads (màu, logo, font, tone máy đọc được) |
| 3 | `.antigravity/core/rules/compliance-finance.md` | mọi domain — bắt buộc |
| 4 | `knowledge/3-pipeline/anti-ai-rules-blacklist.md` | mọi output có chữ; SEO đọc thêm `anti-ai-rules.md` |
| 5 | Persona: `python scripts/persona.py P<n> [--part tone\|bridge]` | khi output nhắm 1 persona |
| 6 | `.antigravity/domains/<domain>/README.md` + `learnings.md` | domain đang làm |

Số liệu thị trường: `python scripts/market_facts.py --brief`, không tự nhớ. Tin mới: `python scripts/news_feed.py --topic "<kw>" --days 14`.

## 2. Vòng đời 1 job (giống nhau mọi domain)

```
brief → draft (v1, v2…) → QA máy → Self-Audit → GATE: user duyệt → approved/ → user tự đăng/chạy → đo → learnings
```

- Job đa kênh sống ở `knowledge/5-campaigns/CMP-YYMMDD-<slug>/` — tạo bằng `python scripts/campaign.py new <slug> --title "…"`, xem trạng thái `python scripts/campaign.py status`.
- Không ghi đè bản đã duyệt: sửa sau duyệt = tạo `v<n+1>`.
- **Không tự publish, không tự chạy quảng cáo, không đổi ngân sách.** Ghi lên Meta Ads (tạo campaign/ad set/ad/creative) chỉ sau khi user xác nhận rõ trong lượt đó, và luôn tạo ở trạng thái `PAUSED`.

## 3. QA máy

| Output | Lệnh |
|---|---|
| Bài SEO | `python scripts/qa_gate.py <file>` (như cũ) |
| Post social, ad copy, landing copy | `python scripts/mkt_lint.py <file> --channel <facebook\|zalo\|linkedin\|meta-ad\|landing>` |
| Ảnh quảng cáo / post / carousel | `python scripts/creative.py render <design.json>` (QA máy) + agent `creative-qa` (QA mắt) — xem `.antigravity/core/creative/README.md` |

Vòng lặp QA tối đa 2 vòng; vẫn FAIL → dừng, trình bày `⚠️ Remaining issues`.

## 4. Trình bày ở gate
Tóm tắt ≤ 25 dòng + đường dẫn file. Ghi rõ: QA máy PASS/FAIL, điều gì máy **không** kiểm được (hình, số liệu chưa có nguồn, claim cần pháp chế duyệt).

## 5. Học từ kết quả
- SEO: `/learn` như cũ (instincts.md, sinh bằng `optimize_instincts.py`).
- Social / Ads: ghi vào `.antigravity/domains/<domain>/learnings.md` theo mẫu trong file đó — chỉ ghi điều có số đo (CTR, CPL, reach…) hoặc user sửa lặp ≥ 2 lần.
