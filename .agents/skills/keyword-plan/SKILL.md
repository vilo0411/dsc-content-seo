---
name: keyword-plan
description: "Chọn N bài SEO nên viết tiếp theo persona, tín hiệu GSC và SERP (topic_status --summary, gsc-opportunities, serp_opportunities) → sprint-backlog.md. Dùng khi hỏi 'viết gì tiếp', 'kế hoạch nội dung', 'chọn keyword'."
---

# Lập Kế Hoạch Từ Khóa (Keyword Plan)

## Nhiệm vụ
Phân tích Topic Clusters và đề xuất [N] bài viết tiếp theo nên được ưu tiên triển khai dựa trên chân dung độc giả (persona).

## Quy trình thực thi
1. `python scripts/topic_status.py --summary` — bảng cluster × trạng thái + danh sách bài chưa Finalized (~4 KB). **Không** đọc `pages.csv` (400 KB); tra thêm theo chủ đề: `topic_status.py --find "<từ>"`.
2. Persona: `python scripts/persona.py P<n>` (danh sách: `--list`).
3. **Kiểm tra GSC signal (nếu có data):** Đọc `knowledge/3-seo/strategy/gsc-opportunities.md` section "Keyword ngủ quên". Nếu có query đang rank (position ≤ 20, clicks ≥ 5) nhưng chưa có bài target chính xác query đó → đưa lên mức ưu tiên cao hơn volume thông thường. Lý do: bài mới sẽ rank nhanh hơn vì domain đã có tín hiệu liên quan. Nếu file không tồn tại: agent có MCP `SEO Dashboard` gọi `get_opportunities` (`property_url: "sc-domain:dsc.com.vn"`) thay thế (playbook `.agents/skills/seo-dashboard/SKILL.md`); không có MCP thì bỏ qua bước này.
4. **Kiểm tra SERP signal:** chạy `python scripts/serp_opportunities.py` (0 API call) rồi đọc section "1. Chưa có bài" trong `knowledge/3-seo/strategy/serp-opportunities.md`. Câu PAA / related search xuất hiện ở ≥ 2 keyword đã research và chưa có bài → ưu tiên ngang GSC signal (Google đã xác nhận nhu cầu). Related search khác intent với bài gốc (VD "cách mua cổ phiếu Vingroup") là ứng viên bài riêng, không phải secondary keyword.
5. Phân tích ngữ cảnh, độ khó, và tính cấp thiết để lọc ra [N] từ khóa phù hợp nhất.
6. Ghi nhận các từ khóa này vào `knowledge/3-seo/strategy/sprint-backlog.md` với trạng thái `Planned`.
