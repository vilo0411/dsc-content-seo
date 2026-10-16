---
name: seo-dashboard
description: Dùng SEO Dashboard MCP (GSC · GA4 · Ads · cannibalization · content decay) trong các luồng /optimize, /gsc-sync, /keyword-plan, /write, /link — kèm cache dùng chung cho agent không có MCP.
---

# SEO Dashboard MCP — Playbook dùng chung cho mọi agent

> Áp dụng cho **Claude Code, Antigravity, Cursor** và mọi agent khác. Agent nào có MCP thì gọi tool rồi **lưu cache**; agent không có MCP thì **đọc cache**. Không agent nào phải tự đoán số GSC.

## 1. Nhận diện MCP

| Agent | Tên tool thường thấy | Cấu hình |
| :--- | :--- | :--- |
| Claude Code / claude.ai | `mcp__claude_ai_SEO_Dashboard__<tool>` | Connector claude.ai (tự có khi đăng nhập) |
| Antigravity | `<tool>` trong server `seo-dashboard` | `~/.gemini/antigravity/mcp_config.json` — xem `.antigravity/config/seo-dashboard-mcp.md` |
| Khác | `<tool>` | Theo client |

Tool là **read-only**. Gọi `list_properties` 1 lần/session nếu chưa chắc property.

**Hằng số DSC:**
- `property_url`: `sc-domain:dsc.com.vn` (copy nguyên văn)
- URL bài: `https://www.dsc.com.vn/kien-thuc/<slug>` → filter `page_value: "/kien-thuc/<slug>"`
- GSC trễ 2–4 ngày. CTR trả về là **%** (0–100). Position âm ở `position_change` = lên hạng.
- Tổng/nhóm đã tính sẵn ở `meta.totals` / `groups` — **không tự cộng rows**.

## 2. Luồng → Tool → Cache

| Luồng | Tool + tham số | Lưu cache (bắt buộc sau khi gọi) |
| :--- | :--- | :--- |
| `/optimize` Bước 2.3 Part A | `query_search_analytics` · `dimensions: ["query"]` · `page_value: "/kien-thuc/<slug>"` · `days: 90` · `compare_mode: "prev_period"` · `limit: 30` | `save page-queries <slug>` → rồi `report <slug>` |
| `/optimize` Bước 1.2 (cannibalization) | `query_search_analytics` · `dimensions: ["page"]` · `query_value: "<keyword>"` · `days: 90` · `limit: 10` | không cần lưu — ghi kết luận vào Proposal |
| `/optimize` chọn bài nào để làm | `get_content_decay` · `get_opportunities` | không cần lưu |
| `/write`, `/outlining` trước khi tạo bài mới | `query_search_analytics` · `dimensions: ["page"]` · `query_value: "<keyword>"` · `days: 90` · `limit: 10` | không cần lưu |
| `/gsc-sync` (thay `sync_gsc.py` khi không có credentials) | (a) `dimensions: ["page"]` · `page_value: "/kien-thuc/"` · `days: 30` · `limit: 500`; (b) `dimensions: ["page","query"]` · `page_value: "/kien-thuc/"` · `days: 30` · `limit: 500` | (a) `save pages` → `pages.csv`; (b) `save page-query` → `queries.csv`; rồi `python scripts/process_gsc.py` |
| `/gsc-sync` cannibalization | `get_cannibalization` · `days: 90` · `limit: 100` | `save cannibalization` |
| `/keyword-plan` | `get_opportunities`, `get_topic_clusters` | không cần lưu |
| `/link` ưu tiên trang có traffic | đọc `pages.csv` (đã có từ `/gsc-sync`) | — |

Lệnh cache (`scripts/dashboard_cache.py`, 0 network):
```bash
python scripts/dashboard_cache.py save page-queries <slug> --file <result.json>   # hoặc pipe JSON qua stdin
python scripts/dashboard_cache.py save pages|page-query|cannibalization --file <result.json>
python scripts/dashboard_cache.py report <slug>    # in block "📊 GSC Performance Context" cho Proposal
python scripts/dashboard_cache.py status           # cache nào có, bao nhiêu ngày tuổi
```

**Cách lưu output tool thành file:** ghi nguyên JSON tool trả về vào `scratch/dashboard-<kind>.json` (không sửa, không rút gọn field) rồi `save ... --file`, xong xóa file scratch. Script nhận cả dạng `[{"type":"text","text":"..."}]`. Với `limit: 500`, chỉ lưu khi thật sự chạy `/gsc-sync` — mỗi lần ghi tốn token tương ứng.

## 3. Thứ tự fallback (mọi agent)

1. **Có MCP** → gọi tool → `save` → dùng `report` / CSV.
2. **Không có MCP, có cache ≤ 7 ngày** → `report <slug>` / đọc CSV. Cache > 7 ngày → vẫn dùng nhưng ghi `⚠️ data cũ N ngày` vào Proposal.
3. **Không MCP, không cache** → `report` trả exit 3 → log `[GSC] Chưa có data cho bài này — bỏ qua`, workflow chạy tiếp. **Không bịa số.**

## 4. Đọc số đúng cách

- So sánh kỳ: luôn báo cả số kỳ trước (`prev_*`) và % thay đổi, không chỉ số hiện tại.
- Flag title rewrite khi CTR < 3% **và** impressions ≥ 1.000.
- Query đang mang click nhiều nhất phải có mặt trong sapo hoặc H2/H3 của bài (instinct "Re-optimize pillar").
- Query dạng câu hỏi có impressions ≥ 300 mà CTR < 1% → ứng viên H2 hoặc câu FAQ.
- `query_search_analytics` không áp brand filter của dashboard; `get_queries` có — chọn đúng tool khi cần tách brand.
- Data traffic là nhạy cảm: cache nằm ở `knowledge/raw/gsc/` (gitignored). Không chép bảng số thô vào file được commit ngoài Proposal/revision-log.
