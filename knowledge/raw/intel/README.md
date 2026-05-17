# Intel — Kho Ý tưởng Content

Folder này lưu **topic ideas** và **data insights** thu thập được trong quá trình research.  
Khác với `0-sources/` (bài cũ cần repurpose) — đây là ideas chưa có nội dung, cần develop thành outline.

## Phân biệt 3 loại raw data

| Folder | Bản chất | Ví dụ |
|---|---|---|
| `knowledge/raw/intel/` | IDEA (chưa có nội dung) | Trend thị trường, insight từ SERP |
| `knowledge/4-content/0-sources/` | CONTENT (bài cũ, cần repurpose) | Bài DSC đã đăng cần refresh |
| `knowledge/2-market/` | KNOWLEDGE BASE (tra cứu lâu dài) | Số liệu market, framework phân tích |

## 30-second Rule

> Nếu gặp data/insight hay trong lúc research mà không chắc dùng ngay:  
> **Save vào `dump.md` trong vòng 30 giây. Categorize sau.**

## Quy trình capture

1. **Quick:** Thêm 1-2 dòng vào `dump.md` → ngày, nguồn, mô tả ngắn
2. **Full:** Tạo file riêng theo template `intel-capture-template.md` trong `.antigravity/internal-templates/`
3. **File naming:** `YYYY-MM_[nguon]-[chu-de].md` — ví dụ: `2026-05_cafef-lai-suat-q2.md`

## Status tracking

Trong mỗi file intel, field `status` nhận 3 giá trị:
- `new` — chưa dùng
- `used` — đã dùng trong project nào đó
- `archived` — không còn relevant
