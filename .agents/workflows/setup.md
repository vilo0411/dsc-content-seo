---
description: Build Knowledge Base — chạy 1 lần khi khởi tạo project
---

# Lệnh: /setup [all|company|market|audience|icp]

## Nhiệm vụ
Khởi tạo và xây dựng Knowledge Base cho hệ thống.

## Quy trình thực thi
1. Gọi **Research Agent** để thu thập thông tin.
2. Nếu tham số là `company`, thu thập Profile công ty. Lưu vào `knowledge/1-brand/profile.md`.
3. Nếu tham số là `audience` hoặc `icp`, định hình chân dung khách hàng. Lưu vào `knowledge/2-market/persona.md`.
4. Thiết lập các quy tắc viết bài và glossary lưu vào `knowledge/3-pipeline/`.
5. Nếu tham số là `all`, chạy toàn bộ quy trình thiết lập.
6. Lưu kết quả chuẩn hóa vào cấu trúc thư mục `knowledge/`.
