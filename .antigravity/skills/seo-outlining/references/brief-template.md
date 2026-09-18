---
name: Content Brief Template — Master SEO (Multi-Project)
description: Template dàn ý SEO chi tiết với YAML Metadata đầy đủ và cấu trúc phân rã yêu cầu chuyên sâu cho mọi dự án.
---

# SEO Content Outline: [Tên bài viết]

## 1. Thông số kỹ thuật (Metadata)

```yaml
---
Author: Antigravity
Status: Outline
Pipeline_Mode: Express | Guided | Auto
SERP_Research: true

# SEO Technical
Target_Keyword: [Từ khóa chính]
Secondary_Keywords: [Từ khóa phụ 1, phụ 2...]
LSI_Keywords: [Từ khóa LSI]
Entities: [List các thực thể quan trọng: tên người, tổ chức, khái niệm chuyên ngành]
Search_Intent: [Informational | Transactional | Commercial]
Content_Type: [Comprehensive Guide | How-to | Listicle | Comparison]
Featured_Snippet: [Paragraph | List | Table | None]
Word_Count_Target: [Số từ - Đề xuất dựa trên Top 1-3 đối thủ + 10%]

# Audience & Brand
Persona: [Tên Persona - Ví dụ: F0, Sinh viên...]
Tone: [Ví dụ: Conversational + Authoritative]
Writer_Profile: [educational | analytical | comparison]  # xem knowledge/1-brand/writers/README.md
Writing_Method: [PAS | AIDA | 4Cs]
Core_Products: # Lấy từ Knowledge Base của dự án hiện tại
  - product: "[Tên sản phẩm 1]"
    benefit: "[Lợi ích tùy biến theo ngữ cảnh bài viết]"
  - product: "[Tên sản phẩm 2]"
    benefit: "[Lợi ích tùy biến theo ngữ cảnh bài viết]"

# Anti-AI
Anti_AI_Flags:
  - [List các cụm từ cần tránh từ anti-ai-rules.md]

# GEO/AEO
GEO_Compliance: true  # Mỗi H2 phải có Load-Bearing Claim theo Phần 8 của anti-ai-rules.md
PAA_Questions:  # BẮT BUỘC khi SERP_Research: true — copy nguyên văn từ output serp_research.py. qa_lint sẽ đối chiếu với Draft.
  - q: "[Câu hỏi PAA 1]"
    placement: body      # body = thành H2/H3 trong thân bài (intent chính) | faq = vào H2 FAQ
    google_source: "[domain đang giữ PAA, nếu có]"
  - q: "[Câu hỏi PAA 2]"
    placement: faq
Related_Searches:
  same_intent: [từ khoá cùng intent → đưa vào Secondary_Keywords/LSI, chèn vào heading hoặc thân bài]
  spin_off: [từ khoá khác intent / hẹp hơn → KHÔNG nhồi vào bài này; ứng viên bài mới hoặc internal link nếu đã có bài]

# Cluster info
Cluster: [Tên Cluster]
Cluster_Role: [Pillar | Cluster]
Internal_Links: []
---
```

- **Title:** [Tối đa 59 ký tự, chứa từ khóa chính]
- **Sapo:** [Chứa từ khóa chính, bao quát nội dung, kêu gọi cuộn xuống]
- **Meta description:** [~155 ký tự, chứa từ khóa chính, tóm tắt nội dung, kêu gọi đọc bài]

---

## 2. Cấu trúc nội dung chi tiết (Headings)

### H1: [Tiêu đề chính - Chứa keyword]
- **Nội dung chính:** [Mô tả chi tiết những gì đoạn này cần truyền tải]
- **Entities & Keywords:** [List cụ thể]
- **Max word count:** [Số từ]

---

### ## 2. SERP Data Points (Verified [Tháng/Năm])
- **Dữ liệu thực tế:** [Bắt buộc: Số liệu %, bảng giá, sự kiện thị trường thực tế từ Research]
- **Đối thủ cạnh tranh:** [Điểm yếu/thiếu sót của đối thủ để mình tối ưu hơn]

---

### H2: [Tiêu đề Section 1]
- **Nội dung chính:** [Nhiệm vụ của đoạn này, các luận điểm chính]
- **Entities & Keywords:** [List cụ thể]
- **Bằng chứng thực tế:** [BẮT BUỘC: Số liệu %, sự kiện thị trường]
- **GEO_Load_Bearing:** [BẮT BUỘC: 1 câu extract-friendly — entity + số liệu + temporal marker. VD: "Tính đến tháng 8/2026, DSC thu phí giao dịch 0,1% — thấp hơn mức TB 0,25% của 5 CTCK lớn (nguồn: UBCKNN)."]
- **Target:** [Số từ]

#### H3: [Tiêu đề con của H2]
- **Nội dung chính:** [Chi tiết hóa luận điểm của H2]
- **Target:** [Số từ]

---

### H2: [Tiêu đề tích hợp Sản phẩm/Giải pháp]
- **Mục tiêu:** Dẫn dắt tự nhiên từ chủ đề sang giải pháp cốt lõi của dự án.
- **Nội dung chính:** 
    - [Nêu vấn đề cụ thể liên quan đến chủ đề bài viết]
    - [Lồng ghép sản phẩm/dịch vụ phù hợp làm giải pháp]
- **Entities & Keywords:** [Tên thương hiệu, tên sản phẩm...]
- **Competitive Edge:** [Đề xuất Bảng biểu / Infographic / Box chuyên gia]
- **Max word count: [Số từ]**

---

### H2: Câu hỏi thường gặp (FAQ)
- **Nguồn câu hỏi:** Tối thiểu 3 câu lấy từ `PAA_Questions` có `placement: faq` (giữ nguyên văn hoặc Việt hoá tự nhiên, không đổi ý). Có thể thêm 1–2 câu từ `Related_Searches.same_intent`.
- **Format mỗi câu:** `#### [Câu hỏi?]` → câu đầu tiên trả lời trực diện ≤ 60 từ, có entity + số liệu + mốc thời gian (extract-friendly cho PAA/AI Overview) → 1–2 câu bổ sung nếu cần. Không mở bằng "Câu trả lời là", "Như đã đề cập".
- **Q1:** [Câu hỏi PAA — placement: faq]
- **Q2:** [Câu hỏi PAA — placement: faq]
- **Q3:** [Câu hỏi PAA — placement: faq]
- **Target:** ~50–80 từ / câu.

### Kết bài & CTA
- **Mục tiêu:** Tóm tắt insight đắt giá nhất + Lời khuyên chuyên gia.
- **CTA:** [Lời kêu gọi hành động cụ thể]

---

## 3. Chiến lược liên kết & Tối ưu hóa

- **External Links:** [Đề xuất nguồn uy tín]
- **Internal Links:** [Đề xuất Anchor text + nội dung liên kết]
- **Spin-off candidates (từ Related Searches / PAA khác intent):** [keyword → đã có bài? (chạy `find_links.py`) → link tới | chưa có → ghi vào `knowledge/raw/intel/dump.md` hoặc `serp-opportunities.md`]
- **Yếu tố cạnh tranh:** [Bảng biểu / Infographic / Box chuyên gia]
- **Brand Voice Checklist:** 
    - [ ] Thể hiện sự chuyên nghiệp, tin cậy.
    - [ ] Phù hợp với đối tượng hướng đến.

---

## 4. Nhật ký chỉnh sửa (Revision Log)
- **v1.0 (2026-05-11):** Khởi tạo từ template chuyên sâu của dự án.
