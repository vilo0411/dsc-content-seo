---
name: ads-brief
description: Brief quảng cáo Meta — mục tiêu, objective, persona, offer, KPI, audience, tham khảo Ad Library đối thủ. Chỉ đọc, không tạo gì trên Meta.
---

# /ads-brief <mục tiêu> [--job CMP-…] [--product eKYC|brokerage|invest|margin]

## Bước 0 — Context
`.agents/core/README.md` §1 + `.agents/domains/ads/README.md`, `references/meta-ads-playbook.md`, `learnings.md` + `knowledge/2-market/research/voc-objections.md` (nỗi lo & ngôn ngữ khách hàng thật) + `knowledge/2-market/account-opening-comparison.md` (vị thế cạnh tranh).

## Bước 1 — Hỏi những gì không suy ra được (1 lần, gộp)
Ngân sách, thời gian chạy, sự kiện chuyển đổi đã cài (pixel/dataset), offer hiện hành. Không tự đặt ngân sách.

## Bước 2 — Dữ liệu (read-only)
- Tài khoản: `ads_get_ad_accounts` → `ads_get_ad_entities` (campaign gần nhất cùng mục tiêu) để lấy baseline CPL/CTR. Chạy các `next_actions` read-only theo hướng dẫn MCP.
- Đối thủ: `ads_library_search` với VPS, TCBS, SSI, VNDirect… — ghi angle, offer, format; **không** chép copy.
- Persona & trigger: `python scripts/persona.py --matrix`.
- Lưu số kéo về: `knowledge/raw/ads/<YYYY-MM-DD>-brief-<slug>.json`.

## Bước 3 — Brief
Theo khung playbook §1: objective, KPI chính + mục tiêu (dựa baseline, ghi rõ nguồn), persona, 2–3 angle (khung PAS/Proof/Question/Expert), audience đề xuất (tuân compliance-finance §3), landing đích (có sẵn hay cần `/landing`), creative cần.
File: `knowledge/6-campaigns/<job>/ads/brief.md` (chưa có job → `python scripts/campaign.py new <slug> --title "…" --channels ads[,landing,social]`).

## Bước 4 — Gate
Tóm tắt ≤ 20 dòng, dừng chờ duyệt. Tiếp theo: `/meta-ads-copy <job>`.

## Ghi activity log (bước cuối)
Sau khi lưu output (và sau mỗi lần user duyệt → `--action approve`): `python scripts/activity_log.py add --domain ads-meta --skill ads-brief --action create --target <CMP-id> --path <job>/ads/brief.md`. Hiện ở tab **Hoạt động** của `knowledge/0-dashboard/index.html`.
