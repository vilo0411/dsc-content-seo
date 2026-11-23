---
name: competitor-watch
description: "Theo dõi content đối thủ hằng tuần: tuần này đối thủ đăng bài gì, nhịp đăng (bài/tuần, 12 tuần), chủ đề nào, DSC đã có bài chưa; tìm đối thủ đang rank tốt cho keyword của DSC. Dùng khi hỏi 'đối thủ tuần này lên content gì', 'mật độ đăng bài', 'ai đang rank top keyword X', competitor monitoring."
---

# Competitor Watch

`/competitor-watch [--week 2026-W47] [--keyword "<kw>"]` — chạy hằng tuần (thứ Hai) trong `/weekly`, hoặc khi user hỏi.
Script làm hết phần thu thập (0 token LLM); agent chỉ đọc báo cáo và rút ra việc nên làm.

## Bước 1 — Ai là đối thủ (khi chưa có config, hoặc mỗi quý)
`python scripts/competitor_watch.py discover [--keyword "<kw>"] --top 15` → domain có mặt trong top 10 các SERP đã cache (0 phí), kèm thư mục bài (hub).
- Chọn CTCK / site cùng ngành rank nhiều keyword; báo, wiki, tài liệu (cafef, vnexpress, studocu) chỉ ghi chú, không theo dõi.
- Ghi vào `knowledge/2-market/competitors/competitors.json` bằng `--add N` hoặc sửa tay (`hub`, `listing` khi site không có sitemap đầy đủ).
- User hỏi theo 1 keyword chưa có SERP cache → `serp_research.py "<kw>"` trước (có phí, hỏi user).

## Bước 2 — Thu thập + báo cáo
```bash
python scripts/competitor_watch.py run            # sitemap / trang danh sách → URL mới → đọc tiêu đề, ngày đăng, nhóm chủ đề
python scripts/competitor_watch.py report         # → knowledge/2-market/competitors/watch/<YYYY-Www>.md + velocity.csv
```
- Lần chạy đầu của 1 domain = **baseline** (chưa có "bài mới"); những lần sau script đọc dần các URL cũ để dựng lịch sử nhịp đăng.
- Sitemap `lastmod` không đáng tin (VPBankS gắn cùng 1 ngày cho mọi URL). "Mới" = URL chưa thấy trước đó, ngày lấy theo ngày đăng trên trang.
- Site chặn (403) / không sitemap → script crawl trang danh sách theo `listing`; vẫn 0 URL → ghi rõ trong báo cáo, không đoán.

## Bước 3 — Đọc và trình user (≤ 20 dòng)
Mở file báo cáo tuần (nhỏ). Trình:
1. Bảng tóm tắt: đối thủ · bài mới tuần này · TB 4 tuần · nhóm chủ đề chính.
2. 3–5 thay đổi đáng chú ý (đối thủ dồn bài vào 1 nhóm, refresh pillar, đăng loạt bài cùng keyword DSC đang rank).
3. Mục "DSC chưa có bài": lọc theo intent (bỏ tin tức/PR) → đề xuất keyword cho `/keyword-plan`; keyword DSC đã có bài nhưng đối thủ vừa làm tốt hơn → đề xuất `/optimize`.
Chỉ dựa trên số trong báo cáo; suy luận ghi rõ là suy luận.

## Related Skills
`/competitor-profile` (phân tích sâu 1 đối thủ) · `/market-research` · `/keyword-plan` · `/optimize` · `/weekly`
