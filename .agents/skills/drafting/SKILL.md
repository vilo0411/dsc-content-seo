---
name: drafting
description: Chuyển Outline đã duyệt thành bài viết nháp chuẩn Human-centric (Phase 3).
---

# Drafting

Dùng sau khi Outline đã được `/approve`. Chỉ thực hiện Phase 3 (Drafting + QA).
`[slug]` là tên file outline, ví dụ: `lai-suat-tiet-kiem-acb`.

## Quy trình thực thi

### 🔄 Bước 0: Context Load (BẮT BUỘC)
Chỉ đọc file **chưa có trong session** (chạy tiếp ngay sau `/outlining` thì bộ context và outline đã có — không đọc lại):
1. Bộ context bắt buộc ở `CLAUDE.md` §Mandatory Context Protocol.
2. `knowledge/4-content/1-outlines/[slug].md` — Outline đã approve.
3. `knowledge/1-brand/service-operations.md` + `knowledge/1-brand/writers/[Writer_Profile].md` (theo field `Writer_Profile` của outline; không có → `educational`).

> **Kiểm tra trạng thái:** `python scripts/topic_status.py [slug]` — nếu Outline không tồn tại hoặc trạng thái chưa phải `Outline-Approved`: DỪNG LẠI và yêu cầu người dùng chạy `/outlining [keyword]` trước.

### Bước 1: Drafting
- Theo `.antigravity/skills/seo-drafting/SKILL.md` Step 1: giao đủ 5 lời hứa của outline (Thesis, Information_Gain, Entities, PAA, bảng dữ liệu có link nguồn) + câu đầu mỗi H2 trả lời ngay.
- Lưu bản nháp tại: `knowledge/4-content/2-drafts/Draft-[slug].md`.

### Bước 2: Internal Linking
- Quy tắc đặt link: `.antigravity/skills/internal-linking/references/link-rules.md` (2 KB — không cần mở cả SKILL 13 KB).
- Lấy ứng viên: `python scripts/find_links.py "[keyword]" --top 8 --exclude [slug]` — chỉ dùng URL có Sitemap ✓.
- Chèn 3–5 internal link + ít nhất 1 link mở tài khoản `https://www.dsc.com.vn/mo-tai-khoan` (Product Bridge hoặc CTA cuối bài). `qa_lint.py` bắt lỗi đặt link (`LINK-*`).
- Banner CTA: lúc này mới mở `.antigravity/skills/cro-optimization/SKILL.md` (không nạp trước), làm xong rồi mới lint.

### Bước 3: QA 3 tầng (Lint → Slop → Fact → Quality Guardian — BẮT BUỘC)
- **Tầng A + B + dữ liệu — 1 lệnh** (in 1 dòng/tầng + chỉ lỗi CRITICAL/MAJOR, dừng ở tầng FAIL đầu tiên):
  ```bash
  python scripts/qa_gate.py knowledge/4-content/2-drafts/Draft-[slug].md --fix
  ```
  Outline tự tìm theo slug. FAIL → sửa đúng dòng được báo rồi chạy lại đúng lệnh này (tầng trước chạy lại miễn phí, không đọc lại báo cáo dài). `SLOP-*`: cách sửa ở `anti-ai-rules.md` §8.7 — sửa đúng chỗ, không viết lại cả bài. `FACT-index-wrong` / `FACT-ticker` sửa bắt buộc; nguồn dữ liệu chết thì gate tự bỏ qua. Cần xem đủ chi tiết 1 tầng → chạy script riêng (`qa_lint.py` / `slop_check.py -v`).
- **Tầng C** — gate PASS → agent `.antigravity/agents/quality-guardian.md` (checklist ngữ nghĩa + truy từng mục Information_Gain), dùng luôn output gate ở trên, không chạy lại lint. Vòng 1 QG đọc cả bài; QG PASS hoặc trả lỗi → `python scripts/qa_gate.py <draft> --mark-qg`. **Vòng 2 QG chỉ đọc `python scripts/qa_gate.py <draft> --changed`** (các đoạn đã sửa + heading chứa nó), không đọc lại cả bài.
- Kết quả PASS → tiếp tục. FAIL → sửa và QA lại **tối đa 2 vòng**; sau vòng 2 vẫn FAIL → dừng, trình bày kèm `⚠️ Remaining issues`.

### 🚧 APPROVAL GATE:
> `python scripts/article_snapshot.py [slug] --stage gate2` rồi trình bày **tóm tắt ≤ 25 dòng + đường dẫn file** (dòng gate: score · coverage · trust · slop; từng mục Information_Gain kèm câu trích; ảnh thực tế còn thiếu; Remaining issues). Không dán bài vào chat.
> **DỪNG LẠI. Chờ người dùng đọc và gõ `/approve`.**
> Khi approve: trình tự finalize ở `.agents/skills/approve/SKILL.md`.
