---
name: learn
description: Kích hoạt Content Feedback Loop để học hỏi từ lịch sử sửa bài.
---

# Content Feedback Loop

Phân tích lịch sử chỉnh sửa và cập nhật bộ quy tắc của hệ thống.

## Options
- `/learn` — Tổng hợp patterns từ các mục 30 ngày gần nhất trong `revision-log.md` (+ `optimize_instincts.py --stats` xem rule nào còn tái diễn).
- `/learn [slug]` — Phân tích sâu một bài cụ thể (VD: `/learn lai-suat-tiet-kiem-acb`).

## Quy trình thực thi

### 🔄 Bước 0: Context Load (đọc tối thiểu)
1. **Bằng chứng chính:** `python scripts/article_snapshot.py <slug> --diff` — các đoạn user đã sửa giữa bản Gate 2 và Final (đọc diff, không đọc 2 bài). Log: **không đọc cả file** — `grep -rn "<slug>" knowledge/3-pipeline/revision-log*`. Không có slug: `python scripts/revision_log.py brief` — 1 dòng/mục, chỉ các mục từ lần `/learn` trước (chưa có mốc → 30 ngày), ~14 KB thay vì 95 KB. Cần chi tiết 1 mục: `grep -n -A4 "<slug>" knowledge/3-pipeline/revision-log.md`.
2. `.antigravity/memory/instincts.md` (đã có trong context nếu load ở Step 0 của session). Tra rule cùng chủ đề: `python scripts/optimize_instincts.py --show <tag|ID>` (chỉ in block khớp). Không mở cả archive.
3. `knowledge/3-pipeline/anti-ai-rules-blacklist.md` (nếu bài học là cụm từ cấm).
4. Có `[slug]`: `knowledge/4-content/3-finalized/Final-[slug].md`.

### Bước 1: Kích hoạt Content Feedback Loop
- Kích hoạt skill `.antigravity/skills/content-feedback-loop/SKILL.md`.
- Nếu có `[slug]`: phân tích sâu bài đó.
- Nếu không có `[slug]`: phân tích output của `revision_log.py brief` (gom mục cùng Scope / cùng ý) + `optimize_instincts.py --stats`.
- Qua **cổng nhận rule** (lặp ở bài khác? máy bắt được? đã có rule cùng Tag?) — chi tiết trong skill.
- **Bắt buộc:** sau khi sửa/thêm rule trong archive, chạy `python scripts/optimize_instincts.py --check` — phải sạch audit (LONG / TAG-DUP / BUDGET / ORPHAN).

### Bước 2: Xác nhận Updates
Hiển thị cho người dùng:
- Danh sách quy tắc mới được thêm vào `anti-ai-rules.md`.
- Danh sách bản năng mới được thêm vào `instincts-archive.md` và đồng bộ qua `instincts.md`.
- Số pattern được tổng hợp.

Cuối cùng (chỉ khi chạy `/learn` không slug): `python scripts/revision_log.py mark-learn` — lần sau `brief` chỉ in mục mới.

> Rule cùng chủ đề → **sửa tại chỗ (giữ ID)**, không append bản mới. Rule bị thay → `DEPRECATED` + `Thay bởi:`, không xoá. Hỏi người dùng chỉ khi phản hồi mơ hồ hoặc muốn DEPRECATE rule mà user từng xác nhận rõ.
