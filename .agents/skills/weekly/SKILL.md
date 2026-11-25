---
name: weekly
description: "Việc sau publish gom 1 lần/tuần: sync live, backfill link theo lô, đo GSC bài live ≥ 14 ngày (→ /optimize), dọn log (weekly_review.py). Dùng khi /weekly, 'việc tuần này', 'kiểm tra bài mới publish'."
---

# /weekly — Rà soát sau publish (chạy mỗi tuần, ~15 phút)

Thay cho các lời nhắc rời rạc ("nhớ sync_live", "đo lại GSC sau 4–6 tuần"). Nguồn: `knowledge/3-seo/logs/publish-ledger.csv` (do `article_snapshot.py` ghi ở outline / gate2 / final) + snapshot live.

**Context:** không load `profile.md` / `anti-ai-rules.md` / instincts — đây là việc vận hành, không viết bài.

## Bước 1 — Báo cáo
```bash
python scripts/weekly_review.py
```
In: (0) việc 7 ngày qua từ sổ + link plan + báo cáo tuần trước (đối chiếu "Cần làm tuần này" → đã xong / còn tồn), (1) Final chưa thấy trên live, (2) bài live chưa backfill link, (3) bài live ≥ 14 ngày chưa đo GSC, (3b) bài optimize đã cập nhật live ≥ 14 ngày chưa đo lại (kèm khung ngày before/after), (3c) sắp đến hạn trong 7 ngày, (4) dọn dẹp. Bài optimize chưa thấy bản mới trên live nằm ở nhóm 1.

## Bước 2 — Publish & sync (nhóm 1)
User dán `knowledge/3-seo/content/4-cms/<slug>.html` vào CMS → chạy đúng lệnh `sync_live.py --only …` script in ra → `python scripts/registry.py refresh` (nhận bài đã publish, kể cả khi CMS đổi slug; slug không tự khớp được → `registry.py check` liệt kê để sửa cột `slug`) → chạy lại `weekly_review.py` (bài đã live tự chuyển sang nhóm 2).

## Bước 3 — Backfill link theo lô (nhóm 2)
- Mỗi bài: `python scripts/find_links.py --backfill <slug>` (chỉ đọc output gợi ý, không mở bài nguồn trừ block cần sửa).
- Gộp tất cả vào **1 spec** `knowledge/3-seo/links/plans/<ngày>-weekly-backfill.json` theo `link/references/link-rules.md` (khớp câu trước/sau, ưu tiên `wrap`, không mặc định đoạn Kết luận, không hợp thì bỏ).
- `python scripts/link_plan.py build <spec>` → user sửa CMS một lượt → `sync_live.py --only <các bài nguồn>` → `link_plan.py verify <spec>`.
- `python scripts/weekly_review.py --done backfill <slug…>`

## Bước 4 — Đo GSC (nhóm 3)
Với từng bài (agent có SEO Dashboard MCP):
- `query_search_analytics` · `property_url: "sc-domain:dsc.com.vn"` · `dimensions: ["query"]` · lọc page = URL script in ra · `days: 14` → `python scripts/dashboard_cache.py save page-queries <slug>`.
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
- **Nhóm 3b — bài đã `/optimize`:** cùng truy vấn MCP, so với `baseline` script in ra (vị trí, clicks, impressions). Tệ hơn baseline → `python scripts/article_snapshot.py <slug> --diff --from final.prev --to final` xem bản trước/sau rồi mới đề xuất sửa tiếp. Ghi: `--done gsc <slug> --result "…"` (script tự ghi vào vòng optimize). Lịch sử các lần: `--outcomes`.
- **Nội dung đang giảm:** MCP `get_content_decay` (90 ngày, chỉ `/kien-thuc/` ≥ 150 clicks) + `query_search_analytics` page `/kien-thuc/` 28d `prev_period` sort `click_change` asc → tối đa 5 bài đề xuất `/optimize`; bài vừa optimize < 30 ngày ghi "đang chờ đo". Đối chiếu `get_google_updates`: cả site cùng giảm trong core update → không quy cho bài.
- **Annotations (MCP `list_annotations`, 14 ngày):** dashboard tự ghi mỗi lần Title/Meta/H1 đổi. Cảnh báo Title chung/chuyên mục, Title trùng giữa 2 URL, Title lệch slug, đổi rồi đổi ngược; thay đổi không có trong sổ = sửa CMS ngoài quy trình; `get_annotation_impact` cho thay đổi đã đủ khung đo. MCP chỉ đọc → bài optimize/publish chưa có annotation thì nhắc user thêm tay.
- **Chạy tự động thứ Hai:** `scripts/weekly_auto.ps1` (Task Scheduler) → `knowledge/5-analytics/weekly/<ngày>.md`.

## Bước 4b — Brand facts (grounding layer, 1 lần/tuần)
- `python scripts/fact_consistency.py --due` → fact nào chưa xác nhận / quá hạn review: gửi owner (cột `owner` trong `knowledge/1-brand/brand-facts.json`), xác nhận xong sửa `value` / `verified_at` / `status`.
- `python scripts/fact_consistency.py --source live` → bài live ghi fact lệch register (vd. eKYC "5 phút" vs chuẩn). Gộp vào 1 spec sửa CMS như backfill link; khi 1 fact đổi giá trị: `--changed <id>` ra danh sách bài cần cập nhật.

## Bước 4c — Đối thủ (thứ Hai)
Làm theo `/competitor-watch`: `python scripts/competitor_watch.py run` → `report` → trình bảng tóm tắt + chủ đề DSC chưa có (đưa vào `/keyword-plan`).

## Bước 5 — Dọn dẹp
- `python scripts/rotate_revision_log.py`
- `python scripts/optimize_instincts.py --stats` — rule nào còn tái diễn ở các bài tuần này → đưa vào `/learn`.
- File cũ trong `2-drafts/`: **hỏi user** trước khi xoá hay chuyển vào `knowledge/3-seo/content/archive/`.

## Báo cáo cho user
Bảng ngắn: bài nào cần dán CMS · spec backfill (số mục) · bài nào cần `/optimize` và vì sao · fact quá hạn / bài lệch fact · rule tái diễn.
