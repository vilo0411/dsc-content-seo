---
name: email-sequence
description: Soạn chuỗi email cho DSC (chào mừng sau mở tài khoản, kích hoạt nạp tiền / giao dịch đầu tiên, nuôi dưỡng lead, win-back) theo persona, kèm subject, preheader, lịch gửi và điều kiện dừng. Dùng khi cần email marketing, email automation, drip, onboarding email, nurture.
---

# Email Sequence

`/email-sequence [welcome | activate | nurture | winback] [P1-P4]` — chỉ soạn nội dung + kịch bản; không gửi, không cấu hình công cụ email.

## Bước 0: Context
1. `.agents/context.md`
2. `knowledge/1-brand/service-operations.md` — bước thật sau khi mở tài khoản (nạp tiền, tiểu khoản, app); email hướng dẫn phải khớp file này
3. `knowledge/1-brand/brand-facts.json` · `knowledge/1-brand/anti-ai-rules.md` · `glossary.md`
4. Persona: `python scripts/persona.py P<n>` (tone, trigger sợ / kỳ vọng, CTA)

## Bước 1: Thiết kế chuỗi (trình user duyệt trước khi viết)
Bảng: # · ngày gửi (D0, D1, D3…) · trigger / điều kiện · mục tiêu 1 hành động · chủ đề · CTA · điều kiện thoát (vd đã nạp tiền → thoát chuỗi activate).
Gợi ý khung:
- **welcome** (sau mở tài khoản, 4–5 email / 10 ngày): xác nhận + việc cần làm tiếp → nạp tiền qua mã định danh → giới thiệu môi giới 1:1 → lệnh đầu tiên → nội dung học (link bài SEO).
- **activate** (đã mở, chưa nạp / chưa giao dịch): gỡ từng lo ngại của persona, mỗi email 1 lo ngại.
- **nurture** (lead chưa mở tài khoản): dùng bài SEO đang tốt nhất theo chủ đề — `python scripts/find_links.py "<chủ đề>" --top 5`.
- **winback** (lâu không giao dịch): nhận định thị trường (có miễn trừ) + mời trao đổi với môi giới.

## Bước 2: Viết từng email
- Subject ≤ 50 ký tự, preheader ≤ 90, không viết hoa toàn bộ, không dùng từ dễ vào spam ("miễn phí 100%", "!!!").
- Thân 80–150 từ, 1 CTA chính (nút) + tối đa 1 link phụ. Câu ≤ 25 từ, đoạn ≤ 3 câu.
- Mở bằng việc của người đọc, không mở bằng "DSC xin trân trọng…". Ký tên người thật (môi giới / đội CSKH) nếu user cung cấp.
- Số liệu sản phẩm chỉ từ brand-facts `verified`. Không hứa lợi nhuận. Nhận định thị trường → câu miễn trừ.
- Link nội bộ tuyệt đối `https://www.dsc.com.vn/...`. Không gắn UTM trừ khi user yêu cầu.

## Bước 3: Tự kiểm
Soát blacklist (`knowledge/1-brand/anti-ai-rules-blacklist.md`), độ dài subject/preheader (đếm bằng script), mỗi email đúng 1 mục tiêu, bước hướng dẫn khớp `service-operations.md`.

## Output → `knowledge/4-channels/email/YYYY-MM-DD-<chuoi>-<persona>.md`
`Status: Draft` · bảng kịch bản · từng email (subject · preheader · body · CTA + URL) · chỉ số theo dõi đề xuất (open, click, tỷ lệ hoàn thành hành động mục tiêu).

## Ghi activity log (bước cuối)
Sau khi lưu output (và sau mỗi lần user duyệt → `--action approve`): `python scripts/activity_log.py add --domain email --skill email-sequence --action create --target <chuoi>-<persona> --path <file email>`. Hiện ở tab **Hoạt động** của `knowledge/0-dashboard/index.html`.

## Related Skills
`/copy-landing` (landing mà email dẫn tới) · `/write` (bài SEO dùng làm nội dung nuôi dưỡng) · `/analytics-report`
