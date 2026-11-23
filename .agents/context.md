# Marketing Context — Chứng khoán DSC

> File nền chung. **Skill nào ngoài SEO cũng đọc file này trước** (giống `ak-init` / `product-marketing-context`).
> File này chỉ tóm tắt và trỏ link. Số liệu sản phẩm (phí, margin, mã nạp tiền…) **không chép vào đây**: lấy từ `knowledge/1-brand/brand-facts.json` (có trạng thái verified / needs_confirmation).
> Cập nhật: 2026-11-19.

## 1. Doanh nghiệp & sản phẩm
- **Thương hiệu:** Chứng khoán DSC — dsc.com.vn. Chi tiết: `knowledge/1-brand/profile.md`.
- **Sản phẩm bán qua marketing số:**
  - Mở tài khoản online (eKYC) — offer chính, URL `https://www.dsc.com.vn/mo-tai-khoan`.
  - Môi giới 1:1 + Margin — khách giao dịch chủ động.
  - DSC Invest (ủy thác, vốn lớn) — tư vấn 1:1, không chốt online.
- **Nghiệp vụ / quy trình thật** (nạp tiền, tiểu khoản, eKYC): `knowledge/1-brand/service-operations.md`.

## 2. Khách hàng
- **ICP:** F0 trẻ, dùng smartphone, vốn 10 triệu – 1 tỷ — `knowledge/1-brand/icp.md`.
- **4 persona:** P1 Tiết kiệm · P2 F0 · P3 Active Trader · P4 Vốn lớn. Tra nhanh: `python scripts/persona.py --matrix`; chi tiết 1 persona: `python scripts/persona.py P2 [--part bridge|tone]`.
- **CTA theo persona:** P1 "Tìm hiểu thêm" · P2 "Mở tài khoản — 3 phút" · P3 "Trao đổi với chuyên gia" · P4 "Đặt lịch tư vấn".

## 3. Kênh
| Kênh | Vai trò | Skill | Output |
|---|---|---|---|
| SEO (dsc.com.vn/kien-thuc) | Kênh chính, tạo traffic + lead | `/write`, `/optimize`, `/weekly`… | `knowledge/3-seo/content/` |
| Google Ads | Lead trả phí cho keyword mua ngay | `/ads-audit`, `/ads-copy` | `knowledge/4-channels/ads/` |
| Social / syndication (Facebook, LinkedIn, Zalo, Pinterest…) | Phân phối lại bài SEO | `/syndicate` | `knowledge/4-channels/social/` |
| Email | Nuôi dưỡng sau khi mở tài khoản | `/email-sequence` | `knowledge/4-channels/email/` |
| Landing page | Chuyển đổi | `/copy-landing`, `/cro` | `knowledge/4-channels/landing/` |
| Đo lường | KPI, báo cáo | `/analytics-report` | `knowledge/5-analytics/` |
| Thị trường & đối thủ | Ai rank keyword của DSC, đối thủ đăng gì, xu hướng | `/competitor-watch`, `/competitor-profile`, `/market-research` | `knowledge/2-market/` |

## 4. KPI
Định nghĩa đầy đủ: `knowledge/5-analytics/kpi-definitions.md`. Tóm tắt: **Lead = GA4 key event chính** (mở tài khoản). Chỉ số chính: Sessions, Lead, CVR, CPL SEO (chi phí SEO / lead SEO), CPA Ads.

## 5. Ràng buộc (áp dụng cho mọi kênh)
- **Giọng thương hiệu:** chuyên nghiệp, gần gũi, không hàn lâm. Rule văn: `knowledge/1-brand/anti-ai-rules.md` + blacklist `anti-ai-rules-blacklist.md`; tên sản phẩm / từ cấm: `knowledge/1-brand/glossary.md`.
- **Tài chính (YMYL):** không hứa lợi nhuận, không cam kết mức sinh lời, không nói "chắc chắn / không rủi ro". Nhận định mua/bán mã cụ thể phải có câu miễn trừ (instinct I113). Copy quảng cáo có số liệu sản phẩm phải khớp `brand-facts.json`; fact nào `needs_confirmation` thì không dùng trong ads/email.
- **Pháp lý quảng cáo chứng khoán và chính sách Google Ads về dịch vụ tài chính:** câu nào nghi vấn → đánh dấu `[CẦN PHÁP CHẾ DUYỆT]`, không tự quyết. Việc đang chờ lãnh đạo xác nhận: `knowledge/1-brand/confirm-with-leadership.md`.
- **Link ngoài:** chỉ tới nguồn trong `knowledge/1-brand/source-whitelist.md`.
- **Không UTM** trừ khi user yêu cầu (đã chọn tắt UTM cho syndication).
- **Không đăng / chạy / gửi thật.** Skill chỉ soạn bản nháp + đề xuất; user tự publish, tự bật campaign, tự gửi email.

## 6. Dữ liệu
- **SEO Dashboard MCP** (read-only): GSC, GA4, Google Ads, cost/CPL. Property: `sc-domain:dsc.com.vn`. Cách dùng + cache cho agent không có MCP: `.agents/skills/seo-dashboard/SKILL.md`.
- **Dashboard Excel tháng** (ngoài repo): `E:\project\dashboard\dashboard_SEO_Ads_v1.xlsx` — cùng định nghĩa KPI.
