---
name: Content Brief Template — DSC SEO Outline
description: Khung outline chuẩn. Field nào `scripts/outline_lint.py` kiểm tra được đánh dấu (lint). Giữ đúng tên field — drafting, qa_lint và outline_lint parse theo tên.
---

<!--
Quy tắc dùng template:
- Khi lưu outline: khối YAML nằm ngay đầu file, mở/đóng bằng `---` (KHÔNG bọc ```yaml).
- Xoá hết dòng hướng dẫn trong [ngoặc vuông] khi điền. Placeholder còn sót → outline_lint báo.
- Heading cấu trúc bài PHẢI viết dạng `### H2: ...` / `#### H3: ...` (count_words.py + qa_lint --outline dựa vào đó).
- Số từ mỗi section ghi `**Target:** N` (chỉ 1 số). Tổng các Target phải khớp Word_Count_Target ±10% (lint).
- H2 có H3 con: `**Target:**` của H2 chỉ tính thân riêng của H2 (trước H3 đầu tiên) — count_words không cộng H3 vào H2. Câu hỏi FAQ không ghi Target riêng; ghi 1 Target tổng cho H2 FAQ.
-->

```yaml
---
Author: Chứng khoán DSC
Status: Outline
Pipeline_Mode: Express | Guided | Auto
SERP_Research: true
SERP_Status: ok | degraded            # (lint) degraded = DataForSEO < 5 organic hoặc dùng fallback
SERP_Format:                          # copy từ block "SERP Format & Intent" của serp_research.py
  dominant: toplist | howto | definition | comparison | review | guide
  share: [%]
  verdict: BẮT BUỘC | NGHIÊNG VỀ | HỖN HỢP
  list_count_median: [N — chỉ khi toplist]

# SEO Technical
Target_Keyword: [từ khoá chính]
Secondary_Keywords: [...]
LSI_Keywords: [...]
Entities: [...]                       # (lint) chép mục "Thuật ngữ BẮT BUỘC phủ" của block Topic Coverage + thực thể riêng của bài
Entities_Skipped: []                  # [cụm — lý do] cho thuật ngữ bắt buộc mà bài cố ý không phủ
Search_Intent: Informational | Commercial | Transactional | Navigational
Content_Type: Toplist | How-to | Definition | Comparison | Review | Comprehensive Guide   # (lint) phải khớp SERP_Format
Format_Deviation: ""                  # chỉ điền khi Content_Type ≠ khung SERP: lý do + user đã đồng ý
Featured_Snippet: Paragraph | List | Table | None
Word_Count_Target: [lo – hi]          # theo intent + median top 5 (SERP ok) / theo intent (degraded)

# Lập trường
Thesis: "[1–2 câu: bài này kết luận gì mà người đọc chưa nghe ở bài khác. Không phải chủ đề.]"
Information_Gain:                     # (lint) ≥ 2 mục; qa_lint tìm đúng `proof` trong draft, QG trích câu giao nó
  - claim: "[điều cụ thể top 5 KHÔNG có]"
    h2: "[tiêu đề H2 sẽ giao nó]"
    type: calc | dsc-data | regulation | screenshot | comparison
    proof: "[con số / cụm từ chắc chắn xuất hiện trong bài, ví dụ: 35.046]"
  - claim: "[...]"
    h2: "[...]"
    type: calc
    proof: "[...]"

# Audience & Brand
Persona: [P1–P4 — tên]
Tone: [...]
Writer_Profile: educational | analytical | comparison
Writing_Method: PAS | AIDA | 4Cs
Core_Products:
  - product: "[...]"
    benefit: "[lợi ích gắn với ngữ cảnh bài]"

# Anti-AI
Anti_AI_Flags:
  - [lỗi cụ thể dễ mắc ở chủ đề này]

# GEO/AEO
GEO_Compliance: true
PAA_Questions:          # copy nguyên văn từ serp_research.py; qa_lint đối chiếu với Draft
  - q: "[câu PAA]"
    placement: body | faq
    google_source: "[domain Google đang trích]"
  - q: "[câu tự suy ra khi SERP không có PAA]"
    placement: faq
    source: inferred    # (lint) bắt buộc khi không có google_source
Related_Searches:
  same_intent: [...]
  spin_off: [...]

# Cluster
Cluster: [...]
Cluster_Role: Pillar | Cluster
Internal_Links:         # (lint) 3–6 link /kien-thuc/ + mở tài khoản; mỗi link gắn với 1 ý cụ thể
  - anchor: "[...]"
    url: "https://www.dsc.com.vn/kien-thuc/[slug]"
    suggested_placement: "[H2/H3 nào, câu nào dẫn tới]"
---
```

# SEO Content Outline: [Tên bài]

- **Title:** [≤ 59 ký tự, chứa nguyên keyword. Toplist → có số N]
- **H1:** [chứa keyword. Toplist → có số N]
- **Sapo:** [Đoạn 1: chứa nguyên keyword + trả lời thẳng + 1 mốc có ngày. Đoạn 2: nhắc DSC + 1 câu dẫn vào bài, ví dụ "Trong bài này, DSC phân tích …"]
- **Meta description:** [140–160 ký tự, chứa keyword]

## 1. SERP & Intent

**Khung bài thắng SERP:** [dán bảng "SERP Format & Intent" từ serp_research.py: rank · domain · loại bài · số mục · số từ]
**Kết luận khung:** [Content_Type đã chọn + vì sao. Toplist → N mục, mỗi mục cùng cấu trúc con. How-to → số bước. Lệch khung → lý do]
**Intent:** [người gõ keyword này muốn làm gì sau khi đọc xong — 1 câu]

### Competitor 1: [domain]
- URL: [...]
- Khung: [...] · [N] từ
- Điểm: Độ sâu [1–10] · Trình bày [1–10] · SEO [1–10] · UX [1–10] = [x]/40
- Mạnh: [...] · Thiếu: [...]
<!-- Không chép cây heading của đối thủ: nó nằm trong cache, chạy lại serp_research.py để xem (không tốn phí). -->

### Competitor 2: [domain]
### Competitor 3: [domain]
<!-- SERP degraded: ghi "Không có — SERP degraded" thay cho các block Competitor -->

## 2. Competitor Gap Synthesis
- **Gaps:** [cái top 3 thật sự bỏ qua — so với đối thủ đang rank, không so với bài yếu]
- **Chủ đề con đối thủ đều có:** [từng chủ đề ở block Topic Coverage → nằm ở H2/H3 nào của bài, hoặc lý do bỏ]
- **Unique angle DSC:** [...]
- **Featured Snippet target:** [dạng + lý do]
- **PAA plan:** [body / faq / spin-off]
- **Cannibalization:** [URL DSC nào đang có impression, ranh giới intent]

## 3. Dữ liệu dùng trong bài

| Dữ kiện | Số liệu | Mốc thời gian | Nguồn | Trạng thái |
|---|---|---|---|---|
| [...] | [...] | [ưu tiên năm hiện tại] | [URL nguồn gốc (source-whitelist.md) / market_facts / DSC nội bộ] | ✓ đã kiểm |

<!-- (lint DATA-source) Mỗi dòng phải có URL nguồn, `market_facts` hoặc `DSC nội bộ`. Quy định / phí / hạn mức → URL văn bản gốc; draft link đúng URL đó tại câu trích. -->
<!-- Dữ kiện chưa xác minh được → BỎ khỏi outline, không để [CẦN XÁC NHẬN] trôi sang drafting (lint). Không có số năm hiện tại → báo user. -->

## 4. Brand Context (output Brand Guardian)
- **Writer Profile:** [profile] — 3 đặc điểm tone: [1] · [2] · [3]
- **USP bắt buộc:** [chỉ USP khớp intent bài]
- **Lỗi cũ cần tránh với chủ đề này:** [từ instincts / revision-log]
- **Xung đột instinct ↔ phản hồi user:** [nếu có — ghi rõ theo bên nào]

## 5. Cấu trúc nội dung

<!-- Mỗi H2 thân bài BẮT BUỘC có 2 dòng đầu (lint). "Ý chính" là câu người đọc mang về; Nội dung chính phục vụ câu đó. -->

### H1: [...]
- **Max word count:** [sapo, ~110]

### H2: [Heading chứa keyword / câu hỏi keyword — trả lời thẳng]
- **Câu hỏi người đọc:** [người đọc đang hỏi gì khi tới đây]
- **Ý chính:** [1 câu kết luận của section — có lập trường]
- **Nội dung chính:** [luận điểm theo thứ tự]
- **Bằng chứng thực tế:** [dòng nào trong mục 3]
- **GEO_Load_Bearing:** [1 câu entity + số + mốc thời gian]
- **Chuyển ý → H2 sau:** [vì sao người đọc cần đọc tiếp section sau]
- **Không viết:** [phần thuộc bài khác / H2 khác — tránh lặp]
- **Target:** [N]

<!-- Toplist: H2 khung danh sách + N mục H3 cùng cấu trúc (mỗi H3: là gì → ví dụ có ngày → cách xử lý). Không nhồi H3 tản mạn. -->
#### H3: [Mục 1]
- **Nội dung chính:** [...]
- **Target:** [N]

### H2: [Bridge sang giải pháp DSC — tên có DSC]
- **Câu dẫn từ kết luận bài:** [nối từ ý chính của bài sang việc người đọc cần làm]
- **Bước cụ thể tại DSC:** [2–4 bước thật, không chỉ list tính năng]
- **Target:** [N]

### H2: Câu hỏi thường gặp về [keyword]
- `#### Câu hỏi?` → câu đầu ≤ 60 từ, có entity + số/mốc. ≥ 3 câu từ PAA placement: faq.
- **Q1:** [...] · **Q2:** [...] · **Q3:** [...]
- **Target:** [tổng số từ cả FAQ]

### H2: Kết luận
- **Ý chính:** [tóm tắt 2–3 insight của bài — không mở bằng "Tóm lại"]
- **CTA:** [hành động cụ thể + link mở tài khoản]
- **Target:** [N]

## 6. Liên kết & yếu tố trực quan
- **External links:** [URL nguồn gốc lấy từ bảng mục 3 — chỉ domain trong source-whitelist.md; đặt tại câu trích]
- **Bằng chứng thực tế (first-hand):** [ảnh chụp màn hình app / bảng phí thật / phép tính riêng. Bài hướng dẫn thao tác, đánh giá app: liệt kê từng `[ẢNH THỰC TẾ: màn hình cần chụp]`]
- **Spin-off candidates:** [keyword → đã có bài / ghi vào serp-opportunities]
- **Yếu tố trực quan:** [bảng / ví dụ tính / banner]

## 7. Revision Log
- **v1.0 ([YYYY-MM-DD]):** [nguồn SERP, số đối thủ extract, ghi chú]
