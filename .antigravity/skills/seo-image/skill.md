# Skill: SEO Image — Gemini Paste Pipeline

> Tạo Gemini prompts cho ảnh SEO. 1 ảnh = 1 prompt. Paste vào Gemini app.

---

## Trigger

`/image [slug]` — chạy sau Draft hoặc Final approve.

---

## Assets

| File | Nội dung |
|------|---------|
| `assets/brand.md` | [BRAND] block — paste cố định |
| `assets/negative.md` | [NEGATIVE] block — paste cố định |
| `assets/styles/abstract-finance.md` | Chỉ báo kỹ thuật, oscillator, chart |
| `assets/styles/editorial-photo.md` | Phân tích, lifestyle tài chính |
| `assets/styles/flat-illustration.md` | Hướng dẫn, checklist, step-by-step |
| `assets/templates/featured.md` | [IMAGE] block — 1200×630 |
| `assets/templates/inline.md` | [IMAGE] block — 800×450 |
| `assets/templates/infographic.md` | [IMAGE] block — 800×1200 |

---

## Quy trình

**Bước 1 — Đọc bài**
- Đọc `Final-[slug].md` (hoặc Draft nếu chưa final)
- Xác định: topic, tone, các H2 section, có table/step-by-step không

**Bước 2 — Chọn style + lập manifest**
- Chọn 1 style từ bảng assets
- Announce manifest:
```
📸 [slug] — [style]
- featured-01: [concept 5 từ] → đầu bài
- inline-01:   [concept 5 từ] → H2 "[tên section]"
- inline-02:   [concept 5 từ] → H2 "[tên section]"
```

**Bước 3 — Compose prompt mỗi ảnh**

Cấu trúc cố định — theo thứ tự:
```
[BRAND]    ← assets/brand.md
[IMAGE]    ← assets/templates/[type].md (điền {{SECTION_NAME}} nếu inline)
[STYLE]    ← assets/styles/[style].md
[SCENE]    ← điền theo bài (xem schema bên dưới)
[NEGATIVE] ← assets/negative.md
```

**Bước 4 — Save + show**
- Save: `knowledge/4-content/2-drafts/[slug]-image-prompts.md`
- Show: từng prompt trong code block

**Bước 5 — QA sau khi nhận ảnh**
- Chạy checklist cuối file

---

## [SCENE] Schema

Agent chỉ cần điền block này. Dùng `{}` cho nested objects, `[]` cho arrays.

```
[SCENE] {
  subject: {{main visual element — 1 line EN}}

  bg: { color: {{hex}}, mood: {{1 word}} }

  fg: {
    element: {{primary visual object}}
    color:   {{hex hoặc gradient}}
    detail:  {{1 đặc điểm quan trọng}}
  }

  accent: { element: {{DSC green xuất hiện như thế nào}}, max: 15% canvas }

  depth: {{secondary layer — hoặc none}}

  composition: {
    focus:   {{focal element + vị trí trong frame}}
    balance: {{left | center | right | asymmetric | split}}
    space:   {{tight | balanced | airy}}
  }

  mood: {{analytical | trustworthy | dynamic | calm}}
  tone: {{cinematic | editorial | clean | dramatic}}

  constraints: {
    no-text:    true
    no-faces:   true
    no-red:     true
    no-collage: {{true | "intentional split only"}}
  }
}
```

**Infographic thêm vào `constraints {}`:**
```
    structure:  {{3-step | comparison | timeline | ranked-list}}
    data:       [{{item 1}}, {{item 2}}, {{item 3}}]
    text-rule:  numbers + max 3-word labels only
```

---

## QA Checklist

| # | Check | Pass |
|---|-------|------|
| 1 | No text | Không có chữ trong featured/inline |
| 2 | Brand green | Màu #00AD14 xuất hiện tự nhiên |
| 3 | No red | Không có đỏ bất kỳ dạng nào |
| 4 | No cliché | Không bắt tay, không chỉ màn hình |
| 5 | Ratio đúng | 16:9 featured/inline — 2:3 infographic |
| 6 | Tone match | Mood ảnh khớp tone bài viết |

Fail → regen: `"Regenerate. Fix: [vấn đề]. Keep everything else identical."`
