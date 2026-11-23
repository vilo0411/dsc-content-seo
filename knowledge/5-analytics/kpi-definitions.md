# KPI Definitions — DSC Digital Marketing

> Dùng chung cho `/analytics-report`, `/ads-audit`, `/weekly`, `/optimize`. Định nghĩa khớp với dashboard Excel `dashboard_SEO_Ads_v1.xlsx` (sheet CALC).
> Nguồn số: SEO Dashboard MCP (`sc-domain:dsc.com.vn`). GSC trễ 2–4 ngày → báo cáo tháng chạy từ ngày 5 tháng sau.

## Lead
**Lead = GA4 key event chính** (hoàn tất đăng ký mở tài khoản). Không cộng các event phụ (click CTA, xem trang mở tài khoản) vào Lead. Event phụ báo cáo riêng: "micro-conversion".

## Kênh
| Kênh | Định nghĩa GA4 |
|---|---|
| SEO | Default channel group = Organic Search |
| Ads | Default channel group = Paid Search (Google Ads) |
| AI | Referral từ ChatGPT / Perplexity / Gemini / Copilot… (MCP `get_ai_traffic`) |

## Chỉ số
| Chỉ số | Công thức | Nguồn MCP |
|---|---|---|
| Clicks, Impressions, CTR, Avg position | GSC | `get_overview`, `query_search_analytics` |
| Sessions (theo kênh) | GA4 | `get_ga4_acquisition` |
| Engagement rate | GA4 engaged sessions / sessions | `get_ga4_engagement` |
| Lead (theo kênh) | GA4 key event chính | `get_conversion_breakdown` |
| CVR | Lead / Sessions | tính |
| Chi phí SEO | Nhập tay hằng tháng (nhân sự + tool + content) | `get_cost_cpl` / dashboard Excel `RAW_Spend_SEO` |
| CPL SEO | Chi phí SEO / Lead SEO | `get_cost_cpl` |
| Ads cost, Ads conversions | Google Ads | `get_ads_overview` |
| CPA Ads | Ads cost / Ads conversions | `get_ads_overview` |
| MoM % | (kỳ này − kỳ trước) / kỳ trước | tham số `compare_mode=prev_period` |
| YoY % | so cùng kỳ năm trước | `compare_mode=same_period_ly` |

## Quy ước trình bày
- Tiền: VND, phân cách hàng nghìn bằng dấu chấm (5.500.000).
- %: 1 chữ số thập phân. Position: số nhỏ hơn = tốt hơn; delta âm = tăng hạng.
- Không làm tròn trước khi tính tỷ lệ. Tổng lấy từ `meta.totals` của MCP, không tự cộng các dòng.
