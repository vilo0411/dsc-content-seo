---
name: link
description: "Internal link: chèn link cho 1 bài (draft hoặc đã publish), backfill link từ bài cũ sang bài mới, và audit cấu trúc pillar/hub/spoke (orphan, link sai hub) ra plan HTML sửa CMS. Dùng khi hỏi link nội bộ, anchor, orphan page, topical map, link cluster."
---

# Internal Links

## Dữ liệu — mỗi file 1 vai trò
```
strategy/taxonomy.json   kiến trúc: cluster → nhóm → pillar / hub / spoke + anchor của pillar   (sửa tay, hiếm)
strategy/pages.csv       registry: 1 dòng / URL — cluster, subgroup, role, hub, trạng thái, anchor, key chính/phụ
                          (scripts/registry.py · đọc qua find_links.py / topic_status.py, không mở file)
raw/live/                snapshot site thật: html/, links.csv, pages.csv   (sync_live.py)
        │
        ├─► find_links.py           ứng viên link cho 1 bài · backfill nguồn → đích
        ├─► link_audit.py           links/dashboard.md + link-graph.html: orphan, sai hub, thiếu link lên pillar
        ├─► topical_map.py          strategy/topical-map.html: cây cluster → subgroup → bài kèm số link + GSC
        └─► link_plan.py            links/plans/<ngày>-<tên>.json → .html (bản dán CMS) → verify sau khi sync
```
Quy tắc đặt link (đọc trước khi chèn): `.agents/skills/link/references/link-rules.md`. Chi tiết thuật toán / lịch sử: `references/playbook.md` (chỉ mở khi cần).

## Chế độ 1 — Bài mới / bài đang sửa (`/link <file>`)
1. `python scripts/registry.py show <slug>` → role + hub của bài. Spoke phải có link lên hub; hub lên pillar.
2. Ứng viên: `python scripts/find_links.py "<keyword chính>" --top 8 --exclude <slug>` (+ 1 lần với chủ đề phụ). Chỉ dùng dòng **Sitemap ✓**.
3. Chèn 3–6 link bọc cụm từ có sẵn trong câu mang nội dung (không "xem thêm", không câu chỉ để trỏ đi — `LINK-pointer`). ≥ 1 link mở tài khoản theo `.agents/rules/cta-conversion.md` (banner là việc của `/cro`).
4. Kiểm: `python scripts/qa_lint.py <file>` — mọi `LINK-*` sạch.
5. Bài mới finalize: `/approve` tự chạy `find_links.py --add-anchor <slug> --anchor "…" --cluster <subgroup>`.

## Chế độ 2 — Backfill (bài cũ → bài mới vừa live)
1. `python scripts/sync_live.py --only <slug>` rồi `python scripts/registry.py refresh` (nhận bài đã publish, kể cả khác slug).
2. `python scripts/find_links.py --backfill <slug> --top 5` → đoạn văn cụ thể ở bài nguồn có thể bọc anchor.
3. Ghi spec `knowledge/3-seo/links/plans/<YYYY-MM-DD>-backfill-<slug>.json` (op `wrap`) → `python scripts/link_plan.py build <spec>` → user sửa CMS theo file `.html`.
4. Sau khi sửa CMS: `sync_live.py --only <các bài nguồn>` → `python scripts/link_plan.py verify <spec>`. Đủ → chuyển cặp file vào `links/archive/`.
Nhiều bài trong tuần → gom 1 spec trong `/weekly`.

## Chế độ 3 — Audit cấu trúc (hằng tháng hoặc sau khi đổi taxonomy)
1. `python scripts/sync_live.py` → `python scripts/page_groups.py build` → `python scripts/registry.py refresh` → `python scripts/registry.py check` (slug chưa khớp, trùng key chính, bài chưa có cluster).
2. `python .agents/skills/link/scripts/link_audit.py` → đọc `knowledge/3-seo/links/dashboard.md` (orphan, spoke thiếu link lên hub/pillar). `python scripts/topical_map.py` → xem cây bằng trình duyệt.
3. `python scripts/link_plan.py candidates` → chọn P1 → spec → `build` → user sửa CMS → `verify` (như chế độ 2).
4. Đổi kiến trúc (thêm hub, đổi pillar): sửa `strategy/taxonomy.json`, rồi `registry.py refresh`.

## Không làm
Mở `pages.csv`, `link-graph.html`, `topical-map.html` để đọc (dùng script) · mỗi đoạn văn sửa tối đa 1 link trong 1 plan · đặt link trong Kết luận / CTA khi không hợp ngữ cảnh.

## Related Skills
`/approve` (đăng ký bài mới) · `/weekly` (backfill theo lô) · `/optimize` (bài tụt, sửa cả link) · `/cro` (banner)
