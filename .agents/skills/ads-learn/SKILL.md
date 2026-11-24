---
name: ads-learn
description: Rút bài học từ kết quả quảng cáo Meta (angle, khung copy, creative, audience thắng/thua) vào learnings.md của domain ads. Chỉ ghi điều có số đo.
---

# /ads-learn [job|--since YYYY-MM-DD]

## Nguồn
- Báo cáo: `knowledge/5-campaigns/*/ads/review-*.md`, cache `knowledge/raw/ads/*.json` (không gọi lại API nếu cache ≤ 7 ngày).
- Copy đã chạy: `<job>/approved/ads-copy-*.md` (để biết khung/angle của từng ad).
- Mẫu ảnh: `<job>/ads/creatives/design.json` — ghép với số Meta qua tên ad `<JOB> | <id> | v<N>` → so theo `layout`, `theme`, khổ, có/không cụm nhấn. Nhóm < 3 ad → ghi "(ít mẫu)", không kết luận.
- Rule hiện có: `.antigravity/domains/ads/learnings.md`.

## Cổng nhận 1 bài học (đủ cả 3)
1. Đủ dữ liệu: mỗi bên so sánh ≥ 1.000 impression và ≥ 3 ngày; chênh KPI chính ≥ 20%.
2. Lặp lại: thấy ở ≥ 2 ad set hoặc ≥ 2 kỳ — nếu chỉ 1 lần, ghi dạng "giả thuyết" và không áp làm mặc định.
3. Áp được: chuyển thành 1 quy tắc cho `/ads-copy` hoặc `/ads-brief`.

Đã có rule cùng chủ đề → sửa tại chỗ (giữ ID, cập nhật số), không thêm trùng. Lỗi compliance lặp lại mà regex bắt được → đề xuất thêm vào `scripts/mkt_lint.py` thay vì ghi learnings.

## Ghi
Mục mới lên đầu `learnings.md`, ID `A<nnn>` tăng dần, theo mẫu trong file. Trình bày các mục thêm/sửa, chờ user duyệt trước khi lưu.
Bài học dùng chung cho social (hook, angle) → ghi thêm 1 dòng tham chiếu trong `.antigravity/domains/social/learnings.md`.
