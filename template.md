---
name: Content Brief Template — HVS SEO (Expert & Rich Metadata)
description: Template dàn ý SEO chi tiết với YAML Metadata đầy đủ và cấu trúc phân rã yêu cầu chuyên sâu.
---

# SEO Content Outline: [Tên bài viết]

## 1. Thông số kỹ thuật (Metadata)

```yaml
---
Author: Claude Code
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
Writing_Method: [PAS | AIDA | 4Cs]
HVS_Products: # Đây là "menu" sản phẩm để lồng ghép vào bài. Hãy chọn sản phẩm phù hợp nhất.
  - product: HVS Tài chính số
    benefit: "[Lợi ích tùy biến theo ngữ cảnh bài viết]"
  - product: HVS Demo
    benefit: "[Lợi ích tùy biến theo ngữ cảnh bài viết]"
  - product: HVS Forum
    benefit: "[Lợi ích tùy biến theo ngữ cảnh bài viết]"

# Anti-AI
Anti_AI_Flags:
  - [List các cụm từ cần tránh cho riêng topic này]

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

### H2: [Tiêu đề Section 1]
- **Nội dung chính:** [Nhiệm vụ của đoạn này, các luận điểm chính]
- **Entities & Keywords:** [List cụ thể]
- **Bằng chứng thực tế:** [BẮT BUỘC: Mã cổ phiếu, số liệu %, sự kiện thị trường]
- **Target:** [Số từ]

#### H3: [Tiêu đề con của H2]
- **Nội dung chính:** [Chi tiết hóa luận điểm của H2]
- **Target:** [Số từ]

---

### H2: [Tiêu đề tích hợp HVS Tài chính số / Thực tập số]
- **Mục tiêu:** Dẫn dắt tự nhiên từ chủ đề sang giải pháp đào tạo/thực tập của HVS.
- **Nội dung chính:** 
    - [Nêu vấn đề cụ thể liên quan đến chủ đề bài viết]
    - [Lồng ghép HVS Tài chính số/Thực tập số làm giải pháp]
- **Entities & Keywords:** [HVS Tài chính số, Thực tập số...]
- **Competitive Edge:** [Đề xuất Bảng biểu / Infographic / Box chuyên gia]
- **Max word count:** [Số từ]

---

### H2: Câu hỏi thường gặp (FAQ)
- **Q1:** [Câu hỏi 1]
- **Q2:** [Câu hỏi 2]
- **Target:** Trả lời súc tích, trực diện để hỗ trợ người đọc.

### Kết bài & CTA
- **Mục tiêu:** Tóm tắt insight đắt giá nhất + Lời khuyên chuyên gia.
- **CTA:** [Lời kêu gọi hành động cụ thể - Chỉ dùng các quyền lợi ĐÃ XÁC MINH trong Knowledge Base]

---

## 3. Chiến lược liên kết & Tối ưu hóa

- **External Links:** [Đề xuất nguồn uy tín: Chính phủ, Tài chính quốc tế]
- **Internal Links:** [Đề xuất Anchor text + nội dung liên kết]
- **Yếu tố cạnh tranh:** [Đề xuất Bảng biểu / Infographic / Box chuyên gia]
- **Brand Voice Checklist:** 
    - [ ] Thể hiện sự chuyên nghiệp, tin cậy.
    - [ ] Phù hợp với đối tượng hướng đến.

---

## 4. Nhật ký chỉnh sửa (Revision Log)
> Phần này ghi lại các phản hồi từ người dùng để Agent học hỏi cho các bài sau.
- **v1.0 (2026-05-08):** Tạo dàn ý lần đầu.
