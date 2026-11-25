---
name: keyword-plan
description: "Chọn N việc SEO nên làm tiếp (bài mới + làm lại bài cũ) theo chiến lược cụm (core/outer, thuộc tính còn thiếu), queue toàn site, tín hiệu GSC và SERP → ghi Planned vào registry. Dùng khi hỏi 'viết gì tiếp', 'kế hoạch nội dung', 'chọn keyword'."
---

# Lập Kế Hoạch Từ Khóa (Keyword Plan)

## Nhiệm vụ
Đề xuất [N] việc tiếp theo, cân giữa **bài mới** và **làm lại bài cũ**, ưu tiên cụm Core đang yếu. Chiến lược (định vị, core/outer, `bridge_to`, thuộc tính) không tự quyết ở đây — đọc từ nguồn duy nhất (`knowledge/README.md` → Thuật ngữ chiến lược).

## Tỷ lệ mặc định mỗi tháng
**40% refresh · 20% bridge · 40% bài mới** (user đổi trong chat thì theo user). refresh / bridge lấy từ queue; bài mới lấy từ gap thuộc tính + GSC + SERP.

## Quy trình thực thi
1. **Chiến lược cụm:** `python scripts/registry.py cluster` (bảng section, thực thể, bridge_to, % qua pipeline, thuộc tính phủ) + `python scripts/registry.py suggest-core` (clicks / key events từng cụm). Cụm `core` mất clicks hoặc phủ thuộc tính thấp → ưu tiên. Cụm `off` chỉ nhận bài có góc dẫn về đầu tư chứng khoán (`profile.md` §0).
2. **Queue bài cũ (refresh / bridge):** đọc top theo `priority` của `knowledge/3-seo/strategy/page-audit.csv` cột `action` (dashboard mục Queue toàn site hiển thị sẵn) — dùng `grep -E ",(refresh|bridge)$"` hoặc đọc ở dashboard, không mở cả file. refresh → `/optimize <slug>`; bridge → `/cro <slug>` (đoạn cầu nối + link về `bridge_to`).
3. **Bài mới — gap thuộc tính:** `python scripts/registry.py cluster <mã>` với cụm ưu tiên → dòng `Gap` = thuộc tính chưa bài nào phủ → ứng viên keyword.
4. `python scripts/topic_status.py --summary` — bảng cluster × trạng thái + danh sách bài chưa Finalized. **Không** đọc `pages.csv` (400 KB); tra theo chủ đề: `topic_status.py --find "<từ>"` (tránh trùng bài đã có).
5. Persona: `python scripts/persona.py P<n>` (danh sách: `--list`).
6. **GSC signal (nếu có data):** `knowledge/3-seo/strategy/gsc-opportunities.md` section "Keyword ngủ quên". Query đang rank (position ≤ 20, clicks ≥ 5) mà chưa có bài target đúng query → ưu tiên cao hơn volume thông thường. Không có file: MCP `SEO Dashboard` → `get_opportunities` (`property_url: "sc-domain:dsc.com.vn"`, playbook `.agents/skills/seo-dashboard/SKILL.md`); không có MCP thì bỏ qua.
7. **SERP signal:** `python scripts/serp_opportunities.py` (0 API call) → section "1. Chưa có bài" của `knowledge/3-seo/strategy/serp-opportunities.md`. PAA / related search xuất hiện ở ≥ 2 keyword đã research và chưa có bài → ưu tiên ngang GSC. Related search khác intent (VD "cách mua cổ phiếu Vingroup") là bài riêng, không phải secondary keyword.
8. Lọc ra [N] việc theo tỷ lệ trên; mỗi việc ghi: cụm + section, loại (refresh / bridge / mới), lý do bằng số (clicks mất, gap thuộc tính, query GSC…).
9. **Ghi vào registry (nguồn trạng thái duy nhất):** bài mới → `python scripts/topic_status.py <slug> --add --keyword "<kw>" --cluster "<mã nhóm con> | <tên>" --set Planned`. Việc refresh / bridge không cần ghi — queue đã giữ. **Không** ghi `sprint-backlog.md` (bản cũ, chỉ để tham khảo).
10. Trình user ≤ 25 dòng: bảng [việc · cụm/section · lý do · lệnh tiếp theo]. Chạy `python scripts/build_content_index.py` để dashboard cập nhật.
