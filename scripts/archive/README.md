# scripts/archive — one-off scripts (không dùng trong pipeline)

Giữ lại để tra cách đã làm, **không chạy lại**: đường dẫn input/draft hard-code theo đợt, nhiều file patch lẫn nhau.

| Thư mục / file | Đợt | Ghi chú |
|---|---|---|
| `account-serp-2026-11/` | 04/11/2026 — rollout SERP nhóm bài mở tài khoản (`cach-mo-tai-khoan…`, `nen-mo-tai-khoan…-o-dau`) | Kết quả ở `knowledge/4-content/audits/account-serp-2026-11-04/`. Việc tương tự lần sau: `/optimize` + `link_plan.py` / `stale_refresh.py`. |
| `content-mapping-2026-05/` | 26/05/2026 — phân tích `knowledge/raw/DSC - Content Mapping*.csv` để dựng cluster/hub | Đã thay bằng `topic-clusters.md` + `topic_status.py`, `link_audit.py`. (gitignored như cũ) |
| `fix_anchor_diacritics.py` | 03/11/2026 — sửa dấu tiếng Việt trong `anchor-index.md` | Đã chạy xong; anchor-index giờ sinh từ snapshot live. |
