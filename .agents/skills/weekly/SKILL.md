---
name: weekly
description: Việc sau publish gom 1 lần/tuần — sync live, backfill link theo lô, đo GSC bài 4–8 tuần, dọn log.
---

# /weekly — Rà soát sau publish (chạy mỗi tuần, ~15 phút)

Thay cho các lời nhắc rời rạc ("nhớ sync_live", "đo lại GSC sau 4–6 tuần"). Nguồn: `knowledge/3-pipeline/publish-ledger.csv` (do `article_snapshot.py` ghi ở outline / gate2 / final) + snapshot live.

**Context:** không load `profile.md` / `anti-ai-rules.md` / instincts — đây là việc vận hành, không viết bài.

## Bước 1 — Báo cáo
```bash
python scripts/weekly_review.py
```
In 4 nhóm: (1) Final chưa thấy trên live, (2) bài live chưa backfill link, (3) bài live 28–56 ngày chưa đo GSC, (4) dọn dẹp.

## Bước 2 — Publish & sync (nhóm 1)
User dán `knowledge/4-content/4-cms/<slug>.html` vào CMS → chạy đúng lệnh `sync_live.py --only …` script in ra → chạy lại `weekly_review.py` (bài đã live tự chuyển sang nhóm 2).

## Bước 3 — Backfill link theo lô (nhóm 2)
- Mỗi bài: `python scripts/find_links.py --backfill <slug>` (chỉ đọc output gợi ý, không mở bài nguồn trừ block cần sửa).
- Gộp tất cả vào **1 spec** `knowledge/3-pipeline/internal-links/plans/<ngày>-weekly-backfill.json` theo `internal-linking/references/link-rules.md` (khớp câu trước/sau, ưu tiên `wrap`, không mặc định đoạn Kết luận, không hợp thì bỏ).
- `python scripts/link_plan.py build <spec>` → user sửa CMS một lượt → `sync_live.py --only <các bài nguồn>` → `link_plan.py verify <spec>`.
- `python scripts/weekly_review.py --done backfill <slug…>`

## Bước 4 — Đo GSC (nhóm 3)
Với từng bài (agent có SEO Dashboard MCP):
- `query_search_analytics` · `property_url: "sc-domain:dsc.com.vn"` · `dimensions: ["query"]` · lọc page = URL script in ra · `days: 28` → `python scripts/dashboard_cache.py save page-queries <slug>`.
- Quyết định (ghi 1 dòng mỗi bài vào báo cáo cho user):
  | Tín hiệu | Việc |
  |---|---|
  | Có impressions, vị trí 1–10, CTR < 1% | `/optimize` Title/Meta |
  | Vị trí 11–30 | `/optimize` nội dung — query thiếu trong H2/FAQ |
  | < 50 impressions sau 8 tuần | kiểm index + `get_cannibalization` |
  | Còn lại | OK, không làm gì |
- **Ghi kết quả vào sổ, từng bài:** `python scripts/weekly_review.py --done gsc <slug> --result "pos 8.2 · clicks 120 · imp 3400"` — sổ lưu kết quả cạnh điểm QA lúc final (score · coverage · trust · slop).
- **AI visibility** (agent có MCP, 1 lần cho cả site mỗi tuần): `get_ai_visibility` + `get_ai_traffic` → `python scripts/dashboard_cache.py save …`; bài nào trong danh sách đo tuần này được AI trích / có traffic từ trợ lý AI → thêm `· AI cited` vào `--result`.
- **Trước khi đề xuất sửa rule QA** (ở `/learn` hoặc khi user hỏi rule có hiệu quả không): `python scripts/weekly_review.py --outcomes` — bài điểm cao mà không rank, hay ngược lại, là bằng chứng để chỉnh trọng số / ngưỡng; phản hồi của người duyệt chỉ là một nửa tín hiệu.
- Bài cũ (trước khi có sổ): MCP `get_content_decay` 1 lần cho cả site, lấy top 5 bài giảm mạnh nhất.

## Bước 5 — Dọn dẹp
- `python scripts/rotate_revision_log.py`
- `python scripts/optimize_instincts.py --stats` — rule nào còn tái diễn ở các bài tuần này → đưa vào `/learn`.
- File cũ trong `2-drafts/`: **hỏi user** trước khi xoá hay chuyển vào `knowledge/4-content/archive/`.

## Báo cáo cho user
Bảng ngắn: bài nào cần dán CMS · spec backfill (số mục) · bài nào cần `/optimize` và vì sao · rule tái diễn.
