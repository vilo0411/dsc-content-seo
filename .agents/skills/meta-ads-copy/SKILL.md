---
name: meta-ads-copy
description: Viết biến thể ad copy Meta (primary text / headline / description) + creative brief từ ads brief đã duyệt; QA bằng mkt_lint + Compliance Reviewer. Không đẩy lên Meta.
---

# /meta-ads-copy <job|brief> [--variants N] [--frameworks PAS,Proof,…]

## Bước 0 — Context
Như `/ads-brief`. Đọc `<job>/ads/brief.md` (phải ở trạng thái đã duyệt; chưa có → chạy `/ads-brief`).

## Bước 1 — Viết
- Mặc định 5 biến thể, trải ít nhất 2 khung (playbook §2). Mỗi biến thể:
```
## V<n> · <khung> · <persona>
Primary text: …
Headline: …
Description: …
CTA button: Learn more | Sign up | …
Creative: <tỷ lệ> · <style S0x> · chữ trên ảnh: "…" (≤ 8 từ)
Landing: <url>
```
- Câu đầu primary đứng một mình được khi bị cắt ở ~125 ký tự. Điều kiện ưu đãi nằm ở primary hoặc landing.
- Ưu tiên angle đã thắng trong `learnings.md`; ghi lý do nếu đi ngược.

## Bước 2 — QA (tối đa 2 vòng)
```bash
python scripts/mkt_lint.py <job>/ads/copy-v1.md --channel meta-ad
```
Sau đó **luôn** chạy Compliance Reviewer (sub-agent read-only, `.agents/core/agents/compliance-reviewer.md`). BLOCK → sửa, không trình bày bản BLOCK.

## Bước 3 — Ảnh (sau khi copy qua lint + compliance)
Chạy `/creative <job>/ads/copy-v<n>.md` (init → render → QA máy + creative-qa). Chữ trên ảnh lấy nguyên từ dòng `chữ trên ảnh: "…"` và bị khoá — muốn đổi thì sửa copy trước.

## Bước 4 — Gate
Bảng: biến thể · khung · độ dài primary/headline · lint · verdict compliance · QA ảnh; link `ads/creatives/v<N>/preview.html`. Dừng chờ duyệt.
Duyệt → copy sang `<job>/approved/ads-copy-v<n>.md` + `python scripts/creative.py approve <job>/ads/creatives/design.json --ids … --xac-nhan "…"`.

## Đẩy lên Meta (chỉ khi user yêu cầu rõ)
Xác nhận lại tài khoản, page, campaign/ad set đích và từng biến thể; chỉ dùng ảnh trong `<job>/approved/`; đặt tên ad `<JOB> | <id> | v<N>` (để `/ads-learn` ghép số theo mẫu ảnh); tạo creative + ad ở trạng thái **PAUSED** qua Facebook Ads MCP; không đổi budget/bid. Báo lại ID đã tạo và ghi vào `<job>/ads/meta-ids.md`. User tự bật.

## Ghi activity log (bước cuối)
Sau khi lưu output (và sau mỗi lần user duyệt → `--action approve`): `python scripts/activity_log.py add --domain ads-meta --skill meta-ads-copy --action create --target <CMP-id> --path <job>/ads/copy-v<n>.md`. Hiện ở tab **Hoạt động** của `knowledge/0-dashboard/index.html`.
