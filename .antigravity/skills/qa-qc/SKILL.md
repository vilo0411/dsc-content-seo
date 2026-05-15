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

### Step 1 — Load context

```
- knowledge/4-content/2-drafts/[slug].md       ← Bài cần audit
- knowledge/4-content/1-outlines/[slug].md     ← Outline gốc để đối chiếu
- knowledge/1-brand/personas.md                ← Xác định persona
- knowledge/3-pipeline/anti-ai-rules.md        ← Blacklist & quy tắc viết
- knowledge/3-pipeline/glossary.md             ← Tên chuẩn & forbidden terms
- knowledge/1-brand/profile.md                 ← Fact-check sản phẩm DSC
- .antigravity/memory/instincts.md             ← Lỗi đã gặp từ trước
```

### Step 2 — Invoke Quality Guardian

Chạy toàn bộ 7 checklist theo `.antigravity/agents/quality-guardian.md`:

| Checklist | Phạm vi | Mức fail |
|---|---|---|
| CL1 — SEO Kỹ thuật | Keyword, H-tags, Meta | CRITICAL |
| CL2 — Anti-AI | Blacklist trigger phrases, emphatic quotes | CRITICAL |
| CL3 — Glossary & Brand | Tên sản phẩm, forbidden terms, format số | CRITICAL |
| CL4 — Persona Alignment | Tone, CTA, product bridge, jargon level | MAJOR |
| CL5 — Fact Accuracy | Số liệu DSC, thống kê thị trường | CRITICAL |
| CL6 — Readability | Sentence/paragraph length, word count | MAJOR |
| CL7 — Instincts | Lỗi đã biết từ instincts.md | MAJOR |

### Step 3 — Output báo cáo

Dùng template trong `quality-guardian.md` mục "Template báo cáo".

**PASS** (0 CRITICAL + 0 MAJOR): Chuyển sang Step 4.  
**FAIL**: Gửi báo cáo cho Main Agent sửa, quay lại Step 1 sau khi nhận bản sửa.

### Step 4 — Finalization (chỉ sau khi PASS + user `/approve`)

1. Di chuyển: `2-drafts/[slug].md` → `3-finalized/Final-[slug].md`
2. Cập nhật `knowledge/4-content/topic-clusters.md` → trạng thái `Finalized`
3. Trigger `content-feedback-loop` skill để học từ vòng viết này
4. Confirm đường dẫn file cuối với user

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
- **Bỏ qua instincts.md:** File này lưu lỗi đã lặp lại nhiều lần — đọc kỹ trước mỗi audit
- **PASS vì "trông ổn":** Nếu không chạy đủ 7 checklist, không được ghi PASS
- **Sửa thay vì báo cáo:** Quality Guardian không sửa bài — chỉ audit và báo lỗi chi tiết để Main Agent sửa
