# 5-campaigns — job marketing đa kênh

Mỗi chiến dịch (hoặc lịch social của 1 tháng) là 1 thư mục `CMP-YYMMDD-<slug>/`. Tạo và xem bằng script, không tạo tay:

```bash
python scripts/campaign.py new <slug> --title "…" --channels social,ads,landing
python scripts/campaign.py status
python scripts/campaign.py set <slug> --status "Chờ duyệt"
```

Quy ước: bản nháp `<kênh>/<tên>-v<n>.md`; bản đã duyệt copy sang `approved/` và không sửa nữa (sửa = v mới). Bài SEO của chiến dịch vẫn nằm ở `knowledge/4-content/`, thư mục `seo/` chỉ ghi slug + link.
Chi tiết: `.antigravity/domains/campaign/README.md`.
