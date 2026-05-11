---
description: Tạo Topic Cluster map từ file keyword csv hoặc raw file
---

# Lệnh: /cluster [csv|raw file]

## Nhiệm vụ
Phân nhóm từ khóa (Topic Clustering) từ file dữ liệu đầu vào.

## Quy trình thực thi
1. Đọc file keyword từ đường dẫn được cung cấp hoặc mặc định tại `knowledge/raw/keyword-hvs.csv`.
2. Phân tích semantic (ngữ nghĩa) và nhóm các từ khóa thành các Cluster (Hub & Spoke).
3. Tạo ra cấu trúc Topic Clusters.
4. Cập nhật và lưu vào file `knowledge/4-content/topic-clusters.md`.
