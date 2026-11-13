---
name: approve
description: Phê duyệt giai đoạn hiện tại (Outline → Draft/Final/Optimize) trong Content Pipeline.
---

# Phê duyệt giai đoạn hiện tại

## Nhiệm vụ
Cho phép người dùng phê duyệt một bản nháp, outline, hoặc bản tối ưu để đẩy nó sang giai đoạn tiếp theo trong Content Pipeline.

## 🔄 Context Load (Trước khi thực thi)
1. `python scripts/topic_status.py [slug]` — xác nhận slug/trạng thái (không đọc `topic-clusters.md`)
2. Không mở `instincts-archive.md` / `revision-log.md`. Bài học mới: cổng nhận rule của `content-feedback-loop` (sửa rule cùng Tag theo ID — xem bằng `python scripts/optimize_instincts.py --show <ID|tag>`), rồi `optimize_instincts.py --check`. Log: `python scripts/revision_log.py add …`.

> File này là **nguồn duy nhất** cho trình tự finalize. `/write`, `seo-drafting`, `qa-qc`, `quality-guardian` chỉ trỏ về đây.

## Quy trình thực thi

### Bước 1: Xác định context
Xác định file đang ở stage nào dựa trên tên file hoặc stage đang được thảo luận trong conversation:

### Bước 2: Thực thi theo stage

**Nếu stage là Outline (`knowledge/4-content/1-outlines/[slug].md`):**
- `python scripts/topic_status.py [slug] --set Outline-Approved`
- `python scripts/article_snapshot.py [slug] --stage outline`
- Thông báo: "Outline đã được approve. Gõ `/drafting [slug]` để bắt đầu viết bài."

**Nếu stage là Draft (`knowledge/4-content/2-drafts/Draft-[slug].md`):**
- **BẮT BUỘC — Hỏi trước khi finalize:**
  > *"Ngoài các chỉnh sửa đã trao đổi trong chat, bạn có tự sửa thêm gì trong file không? Mô tả ngắn để tôi ghi log. (Gõ 'không' để bỏ qua.)"*
- Tổng hợp **toàn bộ** những gì đã sửa trong session này (từ chat + file trực tiếp nếu user khai báo) → ghi log bằng `python scripts/revision_log.py add <slug> --fix "…" --pattern "…" --rule "…" --scope <Global|topic>` (mỗi trường ≤ 400 ký tự). **Không** mở `revision-log.md` (~95 KB) để Edit.
- **GATE trước khi move file** (DSC không có `finalize.py`, nên gate chạy tay ở đây):
  ```bash
  python scripts/qa_gate.py [đường dẫn file đang approve] --all
  ```
  **KHÔNG move file** khi còn: `CRITICAL` (tầng A) · `MAJOR` thuộc nhóm thực chất — `ENT-*`, `IG-*`, `PAA-*`, `DUP-*`, `SRC-*`, `YMYL-*`, `EEAT-*`, `CL5-fact` (đây là các lỗi quyết định bài có rank / được AI trích hay không) · slop score < 80 (tầng B) · cảnh báo "Không có outline". Báo lại cho user kèm danh sách lỗi và chờ quyết định. `MAJOR` hình thức còn lại + `FACT-*`: in ra cho user, không chặn (exit 3 = nguồn dữ liệu chết, bỏ qua). Chỉ bỏ qua gate khi user nói rõ "cứ finalize".
- **BẮT BUỘC**: Di chuyển file sang `knowledge/4-content/3-finalized/Final-[slug].md`.
- **BẮT BUỘC**: `python scripts/article_snapshot.py [slug] --stage final` — lưu bản Final + **chuyển** outline vào `knowledge/4-content/archive/[slug]/` (không xoá). Exit 3 = bài không có outline ở đâu cả → báo user (Thesis / Information_Gain của bài không còn được lưu).
- `python scripts/topic_status.py [slug] --set Finalized`
- **BẮT BUỘC**: `python scripts/md_to_cms_html.py [slug]` → xuất `knowledge/4-content/4-cms/[slug].html` (thân bài HTML đúng định dạng CMS, không gồm H1) + in Title / Meta / H1 để dán vào các ô của CMS.
- `python scripts/qa_lint.py knowledge/4-content/3-finalized/Final-[slug].md --log` — 1 dòng `qa-score-log.csv` (tự kèm slop score) + từng check vào `qa-check-log.csv` (đo rule nào còn tái diễn: `optimize_instincts.py --stats`).
- Auto-trigger: Kích hoạt skill `.antigravity/skills/content-feedback-loop/SKILL.md` để tổng hợp bài học → cổng nhận rule → sửa/thêm trong `instincts-archive.md` → `python scripts/optimize_instincts.py --check`.
- Thêm bài vào chỉ mục link: `python scripts/find_links.py --add-anchor [slug] --anchor "<anchor chính>" --cluster "<tên cluster>"` (script chèn 1 dòng vào `anchor-index.md`; **không** mở file 189 KB đó).
- Nhắc user: sau khi publish lên CMS, mỗi tuần chạy `/weekly` — tự gom sync_live, backfill link theo lô và lịch đo GSC (sổ `publish-ledger.csv` đã được `article_snapshot` ghi).

**Nếu stage là Optimize (`knowledge/4-content/2-drafts/Optimize-[slug].md`):**
- **BẮT BUỘC — Hỏi trước khi finalize:**
  > *"Ngoài các chỉnh sửa đã trao đổi trong chat, bạn có tự sửa thêm gì trong file không? Mô tả ngắn để tôi ghi log. (Gõ 'không' để bỏ qua.)"*
- Tổng hợp **toàn bộ** những gì đã sửa trong session này (từ chat + file trực tiếp nếu user khai báo) → ghi log bằng `python scripts/revision_log.py add <slug> --fix "…" --pattern "…" --rule "…" --scope <Global|topic>` (mỗi trường ≤ 400 ký tự). **Không** mở `revision-log.md` (~95 KB) để Edit.
- **GATE trước khi move file** (DSC không có `finalize.py`, nên gate chạy tay ở đây):
  ```bash
  python scripts/qa_gate.py [đường dẫn file đang approve] --all
  ```
  **KHÔNG move file** khi còn: `CRITICAL` (tầng A) · `MAJOR` thuộc nhóm thực chất — `ENT-*`, `IG-*`, `PAA-*`, `DUP-*`, `SRC-*`, `YMYL-*`, `EEAT-*`, `CL5-fact` (đây là các lỗi quyết định bài có rank / được AI trích hay không) · slop score < 80 (tầng B) · cảnh báo "Không có outline". Báo lại cho user kèm danh sách lỗi và chờ quyết định. `MAJOR` hình thức còn lại + `FACT-*`: in ra cho user, không chặn (exit 3 = nguồn dữ liệu chết, bỏ qua). Chỉ bỏ qua gate khi user nói rõ "cứ finalize".
- Ghi đè bản nâng cấp lên file gốc: `knowledge/4-content/3-finalized/Final-[slug].md`.
- `python scripts/article_snapshot.py [slug] --stage final` (lưu Final + chuyển Proposal vào `archive/[slug]/outline.md`), rồi xóa `Optimize-[slug].md` trong `2-drafts/` (bản trình duyệt đã có ở `archive/[slug]/gate2.md`).
- `python scripts/topic_status.py [slug] --set Finalized`
- **BẮT BUỘC**: `python scripts/md_to_cms_html.py [slug]` → xuất `knowledge/4-content/4-cms/[slug].html` (thân bài HTML đúng định dạng CMS, không gồm H1) + in Title / Meta / H1 để dán vào các ô của CMS.
- `python scripts/qa_lint.py knowledge/4-content/3-finalized/Final-[slug].md --log` — 1 dòng `qa-score-log.csv` (tự kèm slop score) + `qa-check-log.csv`.
- Auto-trigger: Kích hoạt skill `.antigravity/skills/content-feedback-loop/SKILL.md` để tổng hợp bài học → cổng nhận rule → sửa/thêm trong `instincts-archive.md` → `python scripts/optimize_instincts.py --check`.

### Bước 3: Xác nhận
Sau khi hoàn thành, báo cáo cho người dùng:
- Đường dẫn file final.
- Đường dẫn file HTML cho CMS (`knowledge/4-content/4-cms/[slug].html`) kèm Title / Meta / H1 in ra từ script — user copy thẳng vào CMS (chế độ Source).
- Trạng thái mới (output của `topic_status.py`) + 1 dòng điểm: score · **coverage** · **trust** · slop.
- Việc user phải tự làm trên CMS: ảnh thực tế còn thiếu (`[ẢNH THỰC TẾ: …]`), nếu có.
- Tóm tắt bài học mới từ Content Feedback Loop.
