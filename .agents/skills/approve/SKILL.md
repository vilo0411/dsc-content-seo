---
name: approve
description: "Duyệt giai đoạn hiện tại của bài SEO (Outline → Draft → Final, hoặc proposal /optimize): kiểm trạng thái, ghi revision-log, chuyển file, cập nhật topic_status. Dùng khi user gõ /approve, 'duyệt', 'ok chốt', 'approve outline/draft'."
---

# Phê duyệt giai đoạn hiện tại

**Nguồn duy nhất** cho trình tự finalize — `/write`, `drafting`, `qa-qc`, `quality-guardian` chỉ trỏ về đây.

## Bước 0: Xác định stage (1 lệnh)
`python scripts/topic_status.py <slug>` → stage theo file đang thảo luận:
- `knowledge/3-seo/content/1-outlines/<slug>.md` → **A. Outline**
- `knowledge/3-seo/content/2-drafts/Draft-<slug>.md` → **B. Draft**
- `knowledge/3-seo/content/2-drafts/Optimize-<slug>.md` → **C. Optimize**

Không mở `revision-log.md`, `instincts-archive.md`, `pages.csv` (registry) — mọi bước dưới đây đều có script.

## A. Outline
1. `python scripts/topic_status.py <slug> --set Outline-Approved`
2. `python scripts/article_snapshot.py <slug> --stage outline`
3. Báo: "Outline đã duyệt. Gõ `/drafting <slug>` để viết bài."

## B. Draft và C. Optimize — trình tự chung
1. **Hỏi user (bắt buộc):** *"Ngoài các chỉnh sửa đã trao đổi trong chat, bạn có tự sửa thêm gì trong file không? Mô tả ngắn để tôi ghi log. (Gõ 'không' để bỏ qua.)"* Có bản AI đã trình → `python scripts/article_snapshot.py <slug> --diff` để thấy phần user tự sửa.
2. **Ghi log** toàn bộ sửa đổi của session: `python scripts/revision_log.py add <slug> --fix "…" --pattern "…" --rule "…" --scope <Global|topic>` (mỗi trường ≤ 400 ký tự).
3. **Gate:** `python scripts/qa_gate.py <file> --all`. **Không chuyển file** khi còn: `CRITICAL` · `MAJOR` thực chất (`ENT-*`, `IG-*`, `PAA-*`, `DUP-*`, `SRC-*`, `YMYL-*`, `EEAT-*`, `CL5-fact`) · slop < 80 · cảnh báo "Không có outline" → báo user danh sách lỗi, chờ quyết định. `MAJOR` hình thức + `FACT-*`: in ra, không chặn (exit 3 = nguồn dữ liệu chết). Chỉ bỏ gate khi user nói rõ "cứ finalize".
4. **Chuyển file:**
   - B: move → `knowledge/3-seo/content/3-finalized/Final-<slug>.md`.
   - C: ghi đè nội dung lên `Final-<slug>.md`, rồi xoá `Optimize-<slug>.md` (bản trình duyệt đã lưu ở `archive/<slug>/gate2.md`).
5. `python scripts/article_snapshot.py <slug> --stage final` — lưu Final + chuyển outline/proposal vào `knowledge/3-seo/content/archive/<slug>/`. Exit 3 = không có outline → báo user.
6. `python scripts/topic_status.py <slug> --set Finalized`
7. `python scripts/md_to_cms_html.py <slug>` → `knowledge/3-seo/content/4-cms/<slug>.html` + Title / Meta / H1. Script báo `⚠️ Ảnh sai kích thước` → vẽ lại (bìa 1000×600, trong bài 800×500) trước khi báo user.
8. `python scripts/qa_lint.py knowledge/3-seo/content/3-finalized/Final-<slug>.md --log` (ghi `qa-score-log.csv` + `qa-check-log.csv`).
9. **Chỉ B (bài mới):** `python scripts/find_links.py --add-anchor <slug> --anchor "<anchor chính>" --cluster "<cluster>"`.
10. **Học:** session có ghi revision-log ở bước 2 (khác "không") → làm theo `.agents/skills/learn/references/playbook.md` cho slug này (cổng nhận rule → sửa rule cùng Tag theo ID → `python scripts/optimize_instincts.py --check`). Không có sửa đổi → bỏ qua bước này.

## Báo cáo cho user (≤ 15 dòng)
- Đường dẫn Final + HTML CMS kèm Title / Meta / H1 (user dán vào CMS chế độ Source).
- Trạng thái mới + 1 dòng điểm: score · **coverage** · **trust** · slop.
- Việc tay trên CMS: tải ảnh `knowledge/3-seo/content/images/<slug>-*.jpg`, thay `src` bằng `/uploads/…`, ảnh bìa vào ô featured; ảnh `[ẢNH THỰC TẾ: …]` còn thiếu (nếu có).
- Bài học mới (nếu bước 10 chạy). Nhắc: sau publish, mỗi tuần chạy `/weekly`.
