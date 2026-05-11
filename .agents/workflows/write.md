---
description: Kích hoạt quy trình viết bài SEO chuẩn Framework
---

# Lệnh: /write [keyword] [options]

## Options Hỗ Trợ
- `--step`: Viết từng bước (Duyệt Outline -> Draft).
- `--auto`: Tự động viết thẳng ra Final, không cần duyệt.
- `--no-serp`: Bỏ qua bước SERP research.
- `--sprint`: Chế độ viết hàng loạt (batch).

## Quy trình thực thi (Pipeline)
1. **Giai đoạn 1: SEO Outlining**
   - Kích hoạt Skill **`seo-outlining`**.
   - Gọi **SEO Collector** nghiên cứu SERP thực tế.
   - Tạo Outline theo Template và chờ User phê duyệt (`/approve`).
2. **Giai đoạn 2: SEO Drafting**
   - Kích hoạt Skill **`seo-drafting`**.
   - Viết bài nháp dựa trên Outline đã duyệt.
   - Đối soát qua **Brand Guardian** & **Quality Guardian**.
   - Trình bản Draft và chờ User Feedback.
3. **Giai đoạn 3: Finalize & Learn**
   - Áp dụng các chỉnh sửa cuối cùng.
   - Kích hoạt **`content-feedback-loop`** để học hỏi kinh nghiệm.
   - Bàn giao file Final .md.
