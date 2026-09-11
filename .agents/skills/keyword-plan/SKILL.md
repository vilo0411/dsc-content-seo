---
name: keyword-plan
description: Phân tích Topic Clusters và đề xuất N bài viết tiếp theo dựa trên persona và GSC signal.
---

# Lập Kế Hoạch Từ Khóa (Keyword Plan)

## Nhiệm vụ
Phân tích Topic Clusters và đề xuất [N] bài viết tiếp theo nên được ưu tiên triển khai dựa trên chân dung độc giả (persona).

## Quy trình thực thi
1. Đọc file `knowledge/4-content/topic-clusters.md`.
2. Đọc file persona tương ứng trong thư mục `knowledge/2-market/`.
3. **Kiểm tra GSC signal (nếu có data):** Đọc `knowledge/3-pipeline/gsc-opportunities.md` section "Keyword ngủ quên". Nếu có query đang rank (position ≤ 20, clicks ≥ 5) nhưng chưa có bài target chính xác query đó → đưa lên mức ưu tiên cao hơn volume thông thường. Lý do: bài mới sẽ rank nhanh hơn vì domain đã có tín hiệu liên quan. Nếu file không tồn tại, bỏ qua bước này.
4. Phân tích ngữ cảnh, độ khó, và tính cấp thiết để lọc ra [N] từ khóa phù hợp nhất.
5. Ghi nhận các từ khóa này vào `knowledge/4-content/sprint-backlog.md` với trạng thái `Planned`.
