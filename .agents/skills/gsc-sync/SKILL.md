---
name: gsc-sync
description: Fetch GSC data và generate opportunity report.
---

# Fetch GSC Data & Opportunity Report

## Nhiệm vụ
Sync data từ Google Search Console API, phân tích cơ hội, và xuất báo cáo ưu tiên nội dung.

## Options
- `--days=30`: Số ngày fetch data (mặc định: 30, tối đa nên dùng: 90)
- `--force`: Bỏ qua cache TTL (7 ngày), fetch ngay kể cả khi cache còn mới

## Điều kiện tiên quyết
File credentials phải tồn tại tại `.antigravity/config/gsc-credentials.json`.
Nếu chưa có: làm theo hướng dẫn tại `.antigravity/config/gsc-config.md`.

---

## Quy trình thực thi

### Bước 1: Fetch GSC Data
Chạy script sync:
```bash
python scripts/sync_gsc.py [--days=30] [--force]
```

Output nếu thành công:
- `knowledge/raw/gsc/queries.csv` — query-level data (page, query, clicks, impressions, ctr, position)
- `knowledge/raw/gsc/pages.csv` — page-level data
- `knowledge/raw/gsc/cache-meta.json` — metadata (timestamp, days range, site)

Nếu cache còn mới (< 7 ngày) và không có `--force`: báo `[SKIP]` và dùng cache hiện tại.

### Bước 2: Generate Opportunity Report
```bash
python scripts/process_gsc.py
```

Output: `knowledge/3-pipeline/gsc-opportunities.md`

### Bước 3: Đọc và tóm tắt report
Đọc `knowledge/3-pipeline/gsc-opportunities.md` và trình bày tóm tắt cho người dùng:

```
📊 GSC Opportunities Report — [ngày tạo]
Kỳ dữ liệu: [period]

🔴 CTR Gap (optimize title ngay):   [N] bài
   Top 1: [slug] — [impr] impr, [ctr] CTR, pos [pos]

🟡 Position Gap (cần internal links): [N] bài
   Top 1: [slug] — pos [pos], [clicks] clicks

💤 Keyword ngủ quên:                [N] queries
   Top 1: "[query]" ranking cho [slug] (pos [pos], [clicks] clicks)

🔗 Backfill candidates (traffic cao): [N] trang
   Top 1: [slug] — [clicks] clicks/kỳ
```

### Bước 4: Gợi ý hành động
Đề xuất top 3 action items cụ thể dựa trên report, ví dụ:
- `/optimize [slug-ctr-gap]` — rewrite title để tăng CTR
- `/optimize [slug-position-gap]` — strengthen E-E-A-T, thêm internal links
- `/link` sau khi draft mới → ưu tiên backfill candidates

---

## Lưu ý
- Data GSC có lag ~3 ngày — numbers trong report là của ~3 ngày trước
- Cache TTL 7 ngày: phù hợp với workflow optimize theo tuần
- File CSV trong `knowledge/raw/gsc/` là gitignored (chứa traffic data nhạy cảm)
- File `gsc-opportunities.md` có thể commit để team đọc chung
