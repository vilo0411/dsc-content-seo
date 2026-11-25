# Kế hoạch refresh bài kém chất lượng (AI slop) — 2026-11

**Nguồn:** `slop_check` chấm 825 bài live (snapshot 2026-11-19) → 150 bài score < 80. GSC 90 ngày.
**Theo dõi:** `tracker.csv` (cùng thư mục) — 1 dòng/bài, cột `wave` · `status` · số trước/sau.
**Năng lực giả định:** 4 bài/tuần (mỗi bài 2 gate duyệt + dán CMS).

---

## 1. Chia đợt

| Đợt | Bài | Click 90d | Cách làm | Thời gian |
|---|---|---|---|---|
| 1 | 4 bài nhiều click nhất (cảng biển, ngành công nghệ, cạnh tranh hoàn hảo, nến búa ngược) | 2.044 | `/optimize` — đều ở vị trí ≤ 5 → chỉ cập nhật/thêm, **không đổi khung** | 24/11 – 05/12 |
| 2 | 16 bài kiến thức ≥ 50 click | 1.849 | `/optimize` đầy đủ | 08/12 – 02/01 |
| 3 | 33 bài cổ phiếu / ngành / BCTC (cùng 1 khuôn) | 1.345 | Pilot 2 bài (SHB, MBB) cùng đợt 2 → đo 28 ngày → khuôn mới → làm theo lô | pilot 12/2026, lô từ 02/2027 |
| 4 | 97 bài còn lại (63 bài 0 click) | 942 | **Phân loại trước, chưa viết lại**: gộp + 301 / giữ / optimize khi rảnh. Kiểm cannibalization (`get_cannibalization`) | 01/2027 |

Lưu ý trước đợt 2: `thi-truong-so-cap-va-thu-cap-la-gi` và `phan-biet-thi-truong-tien-te-va-thi-truong-von…` viết gần như giống nhau → kiểm cannibalization trước khi optimize.

## 2. Mỗi bài (luồng `/optimize` có sẵn)

1. Baseline: slop + qa_lint + **SERP top 10** (`serp_research.py`) + GSC.
2. Proposal → **Gate 1** (user duyệt) → rewrite → `qa_gate` (slop ≥ 80 và ≥ baseline) → **Gate 2** → `/approve`.
3. User dán CMS → `sync_live.py --only <slug>` → ghi `live_on` vào tracker.
4. Ngay lúc live: lấy GSC **28 ngày trước live** của trang (clicks, vị trí) → `base28_*`. Thêm annotation trên dashboard (user thêm tay — MCP chỉ đọc).

## 3. Đo hiệu quả

| Mốc | Làm gì |
|---|---|
| +14 ngày | Đọc sớm (chỉ cảnh báo, chưa kết luận) → điền `d14_*`. Vị trí tụt > 3 ở bài top 5 → khôi phục ngay |
| +28 ngày | Kết luận → điền `d28_*` + `verdict` (`/weekly` nhóm 3 cũng nhắc mốc này) |

Mốc ngắn → nhiễu cao: so theo cùng thứ trong tuần (14/28 ngày tròn tuần), trừ 3 ngày trễ GSC.

- **Nhóm đối chứng** = các bài đợt 4 chưa sửa, cùng khung thời gian. Hiệu quả thật = % thay đổi của bài − % thay đổi của nhóm đối chứng. Cách này loại được ảnh hưởng của Tết (06/02/2027), core update và mùa vụ thị trường.
- Mỗi lần đo: xem `get_google_updates` có update nào trong khoảng đó không.

**Đọc GSC đúng cấp** (bài học 23/11/2026): số tổng luôn lấy **cấp trang** (`dimensions: ["page"]`, `page_match: equals`). Cộng các dòng query sẽ hụt 65–85% vì GSC ẩn query ẩn danh. Cấp query chỉ dùng để chẩn đoán: từ khoá nào mất click, mất do vị trí, impression hay CTR, và từ khoá tiềm năng (impression cao, vị trí 4–20, bài chưa có cụm đó). Trước khi thêm, kiểm tra trang DSC khác đã phục vụ từ khoá đó chưa.

**Phạm vi theo chẩn đoán:** các bài top 1–5 ở đợt 2 mất click so với cùng kỳ 2025 chủ yếu do CTR (vị trí giữ nguyên, CTR 30–47% xuống 2–16%, nghi AI Overview) và impression giảm, không do tụt hạng. Bài như vậy chỉ làm nhẹ: Title/Meta, sapo trả lời thẳng, sửa lỗi fact/slop, thêm FAQ hoặc H3 cho từ khoá tiềm năng. Không kéo dài gấp đôi. Bài mỏng có vị trí > 5 hoặc tụt vị trí mới làm sâu.

**Chỉ số chính:** **CTR và vị trí** của trang cùng các từ khoá chính. Click chỉ là chỉ số phụ, vì impression dao động theo nhu cầu tìm kiếm.

**Phân loại kết quả (so với baseline, đã trừ phần thay đổi của nhóm đối chứng):**
| Verdict | Điều kiện | Xử lý |
|---|---|---|
| Thắng | click ≥ +15%, vị trí không tụt quá 1 | Giữ, áp cách làm cho đợt sau |
| Hoà | trong khoảng ±15% | Giữ; xem CTR → sửa Title/Meta |
| Thua | click ≤ −15% hoặc vị trí tụt > 2 | Bài từng ở top 5 → **khôi phục bản cũ** (`archive/<slug>/`); bài khác → xem lại query bị mất |

## 4. Điểm quyết định

- **~15/12/2026** (đợt 1 đủ 14 ngày): chỉ xem cảnh báo tụt hạng.
- **~29/12/2026** (đợt 1 đủ 28 ngày): ≥ 3/4 bài Thắng hoặc Hoà → làm tiếp như kế hoạch. ≥ 2 bài Thua → dừng, xem lại cách optimize.
- **~cuối 12/2026** (pilot cổ phiếu đủ 28 ngày): khuôn mới không tụt → làm 31 bài cổ phiếu còn lại theo lô.
- **Tổng kết 03/2027:** tổng click 150 bài so với baseline, số bài còn FAIL slop.
