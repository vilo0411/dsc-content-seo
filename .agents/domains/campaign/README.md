# Domain: Campaign / Landing

Một chiến dịch = 1 job folder gom mọi kênh, để brief, bản nháp, bản duyệt và kết quả ở cùng chỗ.

```
knowledge/6-campaigns/CMP-YYMMDD-<slug>/
├── brief.md        # Status: … (đọc/ghi bằng scripts/campaign.py)
├── seo/            # outline/draft vẫn ở knowledge/3-seo/content/… — ở đây chỉ ghi slug + link
├── social/         # post, calendar
├── ads/            # brief, copy-v<n>, review-<date>
├── landing/        # copy-v<n>.md, landing-v<n>.html
├── approved/       # bản đã duyệt — không sửa, sửa = v mới
└── report.md       # /campaign-report
```

## Skill
| Lệnh | Làm |
|---|---|
| `/campaign-brief <tên>` | Tạo job + brief đa kênh + danh sách việc con |
| `/landing <job\|sản phẩm>` | Copy + HTML 1 trang theo `brand.json` |
| `/campaign-report <job>` | Gộp GSC + Meta + syndication → report |
| `/mkt-status` | Bảng job theo trạng thái |

## Context riêng
- `references/brief-template.md` (dùng bởi `campaign.py new`)
- `references/landing-structure.md`
- `.agents/rules/cta-conversion.md` (CTA, persona → sản phẩm)
