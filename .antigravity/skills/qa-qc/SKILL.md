---
name: Independent Quality Assurance
description: >
  Rigorous final audit of content before publication. Enforces SEO, Anti-AI, Brand, Persona, 
  Fact-check, and Readability standards. Delegates to Quality Guardian agent for execution.
---

# Skill: Independent Quality Assurance (QA/QC)

> Skill này là entry point cho quy trình QA. Execution chi tiết nằm trong `.antigravity/agents/quality-guardian.md`.

---

## Khi nào dùng skill này

- Sau khi draft hoàn thành, trước khi submit cho user review
- Khi user yêu cầu audit một bài đã có
- Khi re-audit sau khi sửa lỗi từ báo cáo FAIL trước

---

## Quy trình thực thi

### Step 1 — Load context (chỉ phần chưa có trong session)

```
- knowledge/4-content/2-drafts/[slug].md       ← Bài cần audit
- knowledge/4-content/1-outlines/[slug].md     ← Outline gốc để đối chiếu
```
Nếu chạy QA **độc lập** (ngoài pipeline) thì thêm: `personas.md`, `glossary.md`, `profile.md`, `instincts.md`.
**Không** đọc `anti-ai-rules.md` cho QA — blacklist đã nằm trong lint.

### Step 1.5 — Lint deterministic (Bắt buộc, chạy trước checklist ngữ nghĩa)

```bash
python scripts/qa_lint.py knowledge/4-content/2-drafts/[slug].md \
  --outline knowledge/4-content/1-outlines/[slug].md
# Bài optimize: thêm  --original knowledge/4-content/3-finalized/Final-[slug].md
# Sửa nhanh lỗi cơ học (unicode ẩn, VN-Index, dấu thập phân, callout, nhãn bold, ---):  thêm --fix
```

Lint gộp luôn word count từng section (logic `count_words.py`) + ~25 check cơ học của CL1/CL2/CL3/CL5/CL6/Link/GEO. Output là bảng CRITICAL/MAJOR/MINOR có số dòng + Score 0–100.

| Kết quả | Hành động |
|---|---|
| Exit 0 (PASS) | Paste dòng Score vào báo cáo → Step 2 |
| Exit 1 (FAIL) | **Dừng ngay.** Gửi bảng CRITICAL/MAJOR cho Main Agent. **Chỉ sửa đúng các dòng được liệt kê — không rewrite toàn bài.** Re-run sau khi nhận bản sửa. |
| Exit 2 (error) | Kiểm tra đường dẫn file, báo lỗi cho user |

> Lint FAIL = bài không thể PASS, kể cả khi checklist ngữ nghĩa đều OK.

### Step 2 — Invoke Quality Guardian (chỉ checklist ngữ nghĩa)

Chạy theo `.antigravity/agents/quality-guardian.md`:

| Checklist | Phạm vi (phần máy không làm được) | Mức fail |
|---|---|---|
| CL1 — SEO ngữ nghĩa | Secondary keyword trong H2, bám outline | MAJOR |
| CL2 — Anti-AI cấu trúc | Ưu/nhược giả tạo, mở/kết bài, mô tả vs tình huống | CRITICAL |
| CL3 — Glossary & Brand | Dùng đúng sản phẩm theo ngữ cảnh | CRITICAL |
| CL4 — Persona Alignment | Tone, CTA, product bridge, jargon level | MAJOR |
| CL5 — Fact Accuracy | Số liệu thị trường có nguồn + thời điểm | CRITICAL |
| CL6 — So-What · Prove-It · E-E-A-T | Mỗi H2 có lợi ích + bằng chứng | MAJOR |
| CL7 — Instincts ngoài lint | Product bridge, cấu trúc bảng, v.v. | MAJOR |
| CL9 — GEO/AEO | Load-bearing claim, chủ thể rõ | MAJOR |

### Step 3 — Output báo cáo

Dùng template trong `quality-guardian.md`.

**PASS** (lint 0 + 0 CRITICAL + 0 MAJOR): Chuyển sang Step 4.
**FAIL**: Gửi báo cáo cho Main Agent sửa → quay lại Step 1.5.
**Giới hạn: tối đa 2 vòng sửa.** Sau vòng 2 vẫn FAIL → dừng, trình bày cho user kèm `⚠️ Remaining issues`. Không lặp vòng 3.

### Step 4 — Finalization (chỉ sau khi PASS + user `/approve`)

1. Di chuyển: `2-drafts/[slug].md` → `3-finalized/Final-[slug].md`
2. `python scripts/topic_status.py [slug] --set Finalized`
3. `python scripts/qa_lint.py knowledge/4-content/3-finalized/Final-[slug].md --log` — ghi score vào `revision-log.md` để theo dõi xu hướng
4. Trigger `content-feedback-loop` skill để học từ vòng viết này
5. Confirm đường dẫn file cuối với user

---

## PASS / FAIL Criteria

| Kết quả | Điều kiện |
|---|---|
| **PASS** | 0 CRITICAL + 0 MAJOR |
| **PASS with notes** | 0 CRITICAL + 0 MAJOR + có MINOR |
| **FAIL** | Bất kỳ 1 CRITICAL hoặc 1+ MAJOR |

---

## Gotchas — Những lỗi thường bỏ sót

- **Tin tưởng mù quáng Main Agent:** Luôn đối chiếu draft với outline gốc — Main Agent hay bỏ sót section hoặc đổi angle mà không báo
- **Fact-check từ internet:** Chỉ dùng `knowledge/1-brand/profile.md` cho số liệu DSC — không Google
- **Bỏ qua instincts.md:** Chỉ đọc các mục ngoài bảng "Đã tự động hoá" — phần còn lại lint đã bắt
- **PASS không có output lint:** Không có dòng Score từ `qa_lint.py` → không được ghi PASS
- **Lặp lại việc của lint bằng mắt:** Đếm câu, tìm blacklist, check title dài… là việc của script — tốn token và kém chính xác hơn
- **Sửa thay vì báo cáo:** Quality Guardian không sửa bài — chỉ audit và báo lỗi chi tiết để Main Agent sửa
