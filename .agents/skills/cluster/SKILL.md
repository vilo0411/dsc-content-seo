---
name: cluster
description: "Gom keyword từ file CSV thành Topic Cluster map (hub & spoke) → dòng mới trong registry pages.csv (topic_status --add). Dùng khi có file keyword mới cần phân nhóm. Chọn bài để viết tiếp thì dùng /keyword-plan."
---

# Topic Clustering

`/cluster [file.csv]` — mặc định `knowledge/raw/DSC - Keyword.csv`. Chỉ đề xuất; ghi vào index sau khi user duyệt.

## Context
`python scripts/topic_status.py --summary` (danh sách cluster hiện có). Không đọc `pages.csv` (400 KB).

## Quy trình
1. Đọc CSV bằng script (`python -c` với `csv`), lấy cột keyword + volume; bỏ trùng, bỏ keyword brand đối thủ.
2. Loại keyword đã có bài: với mỗi keyword ứng viên chạy `python scripts/topic_status.py --find "<kw>"` (gộp nhiều keyword vào 1 lệnh lặp) và `python scripts/find_links.py "<kw>" --top 1`.
3. Gom theo intent (cùng 1 SERP = cùng 1 bài, không tách bài): mỗi nhóm có 1 keyword chính (volume cao nhất, đúng intent) + secondary. Nghi ngờ 2 keyword cùng SERP → so cache `knowledge/raw/serp/` hoặc để `/outlining` kiểm.
4. Xếp nhóm vào cluster có sẵn; chỉ tạo cluster mới khi ≥ 5 bài không vừa cluster nào.
5. Trình user: bảng cluster → keyword chính → secondary → volume → ghi chú (≤ 25 dòng, phần còn lại ghi file `knowledge/3-seo/cluster-proposal-YYYY-MM-DD.md`).
6. Sau khi user duyệt: mỗi bài mới `python scripts/topic_status.py <slug> --add --keyword "<kw>" --cluster "<cluster>" --set Planned`.

## Related Skills
`/keyword-plan` (chọn bài viết tiếp từ cluster map) · `/outlining`
