# START HERE — DSC Content SEO

Hướng dẫn nhanh cho lần đầu dùng hoặc sau thời gian không đụng project.

---

## Slash Commands

| Lệnh | Mô tả |
|---|---|
| `/write [keyword]` | Full pipeline: Research → Outline → Draft → QA → Finalize |
| `/outlining [keyword]` | Chỉ làm Phase 1–2: SERP research + Expert Outline (dừng trước drafting) |
| `/drafting [slug]` | Chỉ làm Phase 3: Draft bài từ Outline đã approve |
| `/approve` | Phê duyệt stage hiện tại (Outline hoặc Draft) để tiếp tục |
| `/revise [slug]` | Sửa đoạn/section cụ thể trong bài |
| `/optimize [path]` | Re-optimize bài cũ với 7 Sweeps Framework |
| `/learn [slug?]` | Tổng hợp feedback → cập nhật anti-ai-rules + instincts |
| `/image [slug]` | Tạo chiến lược hình ảnh cho bài viết |
| `/link` | Backfill internal links từ bài cũ sang bài mới |
| `/cluster` | Keyword clustering từ `knowledge/3-pipeline/keywords.csv` |
| `/keyword-plan [N]` | Chọn N bài nên viết tiếp từ cluster map |
| `/setup` | Build Knowledge Base lần đầu (chạy 1 lần duy nhất) |

---

## Folder Map

```
knowledge/
├── 1-brand/
│   ├── profile.md              ← Thông tin DSC, sản phẩm, USP
│   ├── personas.md             ← 4 reader personas (P1–P4)
│   ├── writers/                ← 3 writer profiles (educational / analytical / comparison)
│   └── icp.md, visual-brand-guidelines.md...
├── 2-market/                   ← Market landscape, đối thủ
├── 3-pipeline/
│   ├── anti-ai-rules.md        ← Blacklist phrases + quy tắc viết
│   ├── glossary.md             ← Tên sản phẩm chuẩn + forbidden terms
│   ├── anchor-index.md         ← Index bài đã publish, dùng cho internal linking
│   └── keywords.csv            ← Keyword backlog
├── 4-content/
│   ├── 0-sources/              ← Bài DSC cũ cần refresh/repurpose
│   ├── 1-outlines/             ← Outline đã research (sau /outlining)
│   ├── 2-drafts/               ← Bản nháp đang viết (sau /drafting)
│   └── 3-finalized/            ← Bài đã publish (Final-[slug].md)
└── raw/
    └── intel/                  ← Topic ideas + data insights từ research
        └── dump.md             ← Quick capture (30-second rule)

.antigravity/
├── agents/                     ← Sub-agent personas
├── rules/                      ← Master rules (workflow, anti-ai, naming...)
├── skills/                     ← Execution logic (outlining, drafting, QA...)
├── internal-templates/         ← Templates tái sử dụng (brief, intel capture...)
└── memory/
    ├── instincts.md            ← Bài học từ feedback thực tế
    └── DECISIONS.md            ← Quyết định kiến trúc dài hạn

.agents/workflows/              ← Slash command workflows
```

---

## Workflow A→Z

Từ "có keyword" đến "bài đã publish":

```
1. Chọn keyword từ keywords.csv hoặc cluster map
2. /outlining [keyword]
   → Đọc SERP top 10, tạo Expert Outline
   → Lưu: knowledge/4-content/1-outlines/[slug].md
3. Review Outline → /approve nếu OK (hoặc sửa và /approve)
4. /drafting [slug]
   → Viết draft theo Outline + Writer Profile
   → QA tự động (7 checklist)
   → Lưu: knowledge/4-content/2-drafts/Draft-[slug].md
5. Review Draft → /approve nếu OK
6. File tự động move → knowledge/4-content/3-finalized/Final-[slug].md
7. Cập nhật anchor-index.md với bài mới
8. /link → backfill internal links từ bài cũ sang bài mới
```

---

## Files quan trọng nhất cần biết

| File | Tác dụng |
|---|---|
| `knowledge/3-pipeline/anti-ai-rules.md` | Blacklist phrases + self-audit checklist |
| `knowledge/3-pipeline/glossary.md` | Tên sản phẩm chuẩn + số liệu DSC |
| `knowledge/1-brand/personas.md` | 4 personas + ma trận chọn tone/CTA |
| `.antigravity/memory/instincts.md` | Lỗi đã gặp + bài học từ feedback thực tế |
| `knowledge/3-pipeline/anchor-index.md` | Index bài đã publish (internal linking) |
