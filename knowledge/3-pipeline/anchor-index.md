# Anchor Index — Internal Linking Registry

File này là danh sách tập trung của tất cả bài viết đã publish, dùng để:
1. **Internal Linking Skill** tìm link phù hợp khi viết bài mới.
2. **Backfill Mode** xác định bài cũ nào cần được link tới bài mới.

> **Cập nhật thủ công hoặc auto** sau mỗi lần bài được finalized.
> Format: `| Anchor Text (gợi ý) | URL | Từ khóa liên quan | Cluster |`

---

## Cluster 1: So sánh Lãi suất & Tối ưu dòng vốn

| Anchor Text Gợi ý | URL | Từ khóa Liên quan | Trạng thái |
| :--- | :--- | :--- | :--- |
| lãi suất tiết kiệm ACB | `/blog/lai-suat-tiet-kiem-acb/` | lãi suất ACB, tiết kiệm ACB 2026 | Finalized |
| lãi suất tiết kiệm BIDV | `/blog/lai-suat-tiet-kiem-bidv/` | lãi suất BIDV, tiết kiệm BIDV 2026 | Finalized |
| lãi suất tiết kiệm VPBank | `/blog/lai-suat-tiet-kiem-vpbank/` | lãi suất VPBank, tiết kiệm VPBank | Finalized |
| lãi suất tiết kiệm Bắc Á | `/blog/lai-suat-tiet-kiem-bac-a/` | lãi suất Bắc Á Bank | Finalized |
| lãi suất tiết kiệm VIB | `/blog/lai-suat-tiet-kiem-vib/` | lãi suất VIB, tiết kiệm VIB | Finalized |

---

## Hướng dẫn cập nhật

Khi một bài viết được finalized, thêm một dòng mới vào cluster tương ứng:
```
| [Anchor text tự nhiên nhất] | [URL production] | [2-3 từ khóa liên quan] | Finalized |
```

Nếu bài thuộc cluster mới, tạo thêm section `## Cluster N: [Tên cluster]`.

---
*Cập nhật: 2026-05-15*
