# Slop Audit — toàn bộ corpus Final (2026-10-16)

Công cụ: `python scripts/slop_check.py --baseline --csv knowledge/3-pipeline/slop-baseline.csv`
Phạm vi: **188 file** trong `knowledge/4-content/3-finalized/` (toàn bộ, không lấy mẫu) — 182 file `Final-<slug>.md` + 6 file tên thô chưa chuẩn hoá.
Số liệu chi tiết từng bài: `slop-baseline.csv` (sắp theo `slop_score` tăng dần).

Tầng kiểm tra: A = `qa_lint.py` (từ vựng + format) · **B = `slop_check.py` (hành vi văn bản)** · tầng dữ liệu = `market_facts.py --verify` · C = Quality Guardian.

> Bộ 3 script này port từ repo `hvs-company-info` (2026-10-15) và **đã hiệu chỉnh lại ngưỡng theo corpus DSC** — ngưỡng của HVS áp thẳng vào DSC cho FAIL 43%, không dùng được làm gate.

---

## 1. Tầng A không thấy được slop

| | |
|---|---|
| Bài PASS `qa_lint --no-sitemap` | 54 / 182 |
| Trong đó **FAIL `slop_check`** | **2 (4%)** |
| Bài có `qa_lint` ≥ 95 nhưng slop FAIL | 2 |
| Ví dụ | `cac-mau-trong-chung-khoan-...`: qa_lint **100/100**, slop **67** |
| | `lam-the-nao-de-mua-co-phieu-mbb-...`: qa_lint **100**, slop **77** |

Tỷ lệ chồng lấn thấp hơn HVS (26%) vì phần lớn corpus DSC còn FAIL ngay ở tầng A (128/182), nên chưa tới được tầng B. Kết luận vẫn giữ: **sạch 100% từ cấm không đồng nghĩa với không phải slop**.

## 2. Phân bố metric trên 188 bài

| metric | hướng xấu | p10 | p25 | p50 | p75 | p90 | min | max |
|---|---|---|---|---|---|---|---|---|
| burstiness (stdev độ dài câu) | thấp | 3.4 | 4.2 | **5.3** | 7.8 | 9.9 | 2.2 | 15.7 |
| mean_sent (từ/câu) | – | 16.6 | 18.1 | 19.6 | 22.0 | 25.8 | 13.7 | 32.6 |
| uniform_run (câu liên tiếp 14–24 từ) | cao | 2 | 4 | **8** | 12 | 18 | 1 | 49 |
| rhythm_gap (câu liên tiếp không có câu ≤7 từ) | cao | 19 | 28 | **40** | 54 | 68 | 8 | 123 |
| **short_share** (tỷ lệ câu ≤7 từ) | thấp | 0.00 | 0.00 | **0.00** | 0.03 | 0.09 | 0.00 | 0.45 |
| evidence_per_100w | thấp | 1.01 | 1.42 | **2.20** | 3.31 | 4.22 | 0.29 | 7.16 |
| unanchored_ratio | cao | 0.23 | 0.36 | 0.50 | 0.63 | 0.77 | 0.05 | 0.92 |
| vague_per_1000w | cao | 0.00 | 0.00 | 0.00 | 0.51 | 0.82 | 0.00 | 1.74 |
| hedge_para_max | cao | 1 | 1 | 1 | 2 | 2 | 0 | 3 |
| synonym_variants | cao | 1 | 1 | 1 | 2 | 2 | 1 | 4 |
| h2_def_open (H2 mở bằng "X là…") | cao | 0.00 | 0.12 | 0.20 | 0.30 | 0.38 | 0.00 | 0.67 |
| para_shape_sd | thấp | 0.50 | 0.57 | 0.65 | 0.77 | 0.85 | 0.33 | 1.26 |
| template_sim (khung H2 vs bài gần nhất) | cao | 0.23 | 0.27 | 0.32 | 0.37 | 0.46 | 0.17 | 1.00 |
| words | – | 1089 | 1275 | 1580 | 1846 | 2175 | 601 | 3196 |

**Vấn đề hệ thống — nhịp câu, không phải bằng chứng:**

1. **Nhịp phẳng toàn corpus.** `short_share` median = **0.00** — bài trung bình **không có một câu nào ≤7 từ**. Median `burstiness` 5.3 từ (HVS 9.4), median `uniform_run` 8 câu liên tiếp cùng khoảng 14–24 từ. Nguyên nhân cấu trúc: `anti-ai-rules.md` §4.1 chỉ chặn câu **quá dài** (≤30 từ) và ép đoạn 2–3 câu, không có rule nào ép câu **ngắn** → mọi câu dồn về khoảng giữa. Rule `rhythm_break` vừa được thêm ở §8.7f để đóng lỗ này.
2. **Mật độ bằng chứng là điểm mạnh.** Median 2.20 token/100 từ, cao hơn HVS (1.58) 39%. Nhóm bài có mã/ngành cụ thể đạt 3.41. Không cần siết `evidence` thêm ở giai đoạn này.

## 3. Tỷ lệ flag theo rule (ngưỡng relative, MAJOR≈p95 / MINOR≈p80 của corpus DSC)

| rule | MAJOR | MINOR | % bài bị flag |
|---|---|---|---|
| SLOP-burstiness | 12 | 36 | 26% |
| SLOP-para-shape | 10 | 30 | 21% |
| SLOP-vague | 7 | 33 | 21% |
| SLOP-anchor | 11 | 27 | 20% |
| SLOP-rhythm | 10 | 27 | 20% |
| SLOP-uniform-run | 10 | 26 | 19% |
| SLOP-evidence | 10 | 25 | 19% |
| SLOP-template | 12 | 9 | 11% |
| SLOP-h2-open | 4 | 17 | 11% |
| SLOP-inline-header | 7 | 9 | 9% |
| SLOP-synonym | 1 | 9 | 5% |
| SLOP-table-thin | 0 | 8 | 4% |
| SLOP-hedge-para | 0 | 2 | 1% |

Slop score: p10 = 79 · p50 = 94 · p90 = 100 · **FAIL (score < 80): 19/188 = 10%**

Hiệu chỉnh ngưỡng: thử MAJOR p90/MINOR p75 → FAIL 26% (quá nhiều để làm gate), p92/p78 → 19%, **p95/p80 → 10%** (chọn). Profile này khớp HVS sau hiệu chỉnh (8%, p10=80 p50=94 p90=100), nên gate có cùng độ chặt ở hai repo dù corpus khác nhau.

## 4. Slop theo nhóm chủ đề

| nhóm | n | slop p50 | evidence p50 | burstiness p50 | FAIL% |
|---|---|---|---|---|---|
| vàng / bạc / kênh khác | 15 | 87 | 2.33 | 5.9 | **27%** |
| mô hình giá / nến / biểu đồ | 10 | 87 | 1.84 | 5.3 | 10% |
| mã / ngành cụ thể | 8 | 94 | 3.41 | 4.6 | 12% |
| vĩ mô / phân tích cơ bản | 30 | 94 | 1.69 | 5.4 | 3% |
| chỉ báo / chỉ số kỹ thuật | 18 | 97 | 2.48 | 6.6 | 11% |
| hướng dẫn / thao tác | 15 | 97 | 2.74 | 5.5 | 7% |
| khác | 92 | 94 | 2.17 | 4.9 | 10% |

**Chẩn đoán:** khác HVS (slop tập trung ở bài TA trừu tượng vì thiếu số liệu bám). Ở DSC, nhóm tệ nhất là **vàng/bạc** — bằng chứng không thiếu (2.33) nhưng `burstiness` thấp và nhiều câu sáo rỗng kiểu "thị trường luôn biến động", "tùy thuộc vào nhiều yếu tố". Đây là chủ đề tư vấn quyết định ("có nên mua vàng không") mà bài né khuyến nghị → văn trôi thành trung lập vô vị.

→ Hành động đúng với nhóm này không phải thêm số, mà là **chốt lập trường** (§3.1) + ngắt nhịp câu.

## 5. 15 bài cần ưu tiên sửa

| slop | slug | MAJOR |
|---|---|---|
| 54 | `khung-hoang-kinh-te-la-gi` | evidence, anchor, vague, para-shape |
| 61 | `cac-mo-hinh-gia-chung-khoan` | burstiness, uniform-run, anchor |
| 64 | `chinh-sach-tai-khoa-la-gi` | evidence, anchor, para-shape |
| 64 | `dau-tu-vang-nen-mua-loai-na` | burstiness, uniform-run, vague |
| 67 | `cac-mau-trong-chung-khoan-...` | rhythm, anchor, para-shape |
| 67 | `chien-luoc-dau-tu-chung-khoan-ngan-han-la-gi` | anchor, h2-open, para-shape |
| 68 | `chi-so-gia-tieu-dung-cpi-la-gi-...` | burstiness, uniform-run |
| 68 | `phuong-phap-canslim-trong-dau-tu-chung-khoan-la-gi` | rhythm, para-shape |
| 71 | `cach-choi-chung-khoan-cho-sinh-vien` | burstiness, uniform-run |
| 72 | `target-trong-chung-khoan-la-gi` | burstiness |
| 74 | `chi-bao-ky-thuat-la-gi` | burstiness, rhythm |
| 74 | `co-nen-ban-vang-thoi-diem-nay` | burstiness, uniform-run |
| 74 | `dau-tu-gia-tri-hay-dau-tu-tang-truong-...` | burstiness, anchor |
| 77 | `cach-dau-tu-vang` | rhythm, anchor |
| 77 | `quy-tuong-ho-la-gi` | uniform-run, vague |

Danh sách đầy đủ 19 bài FAIL: `slop-baseline.csv`, cột `slop_score < 80`.

## 6. Hai cặp file trùng trong `3-finalized/`

`template_sim` = **1.00** (khung H2 giống hệt) ở 2 cặp — không phải lỗi viết mà là **file trùng**:

| bản tên thô | bản chuẩn |
|---|---|
| `Cách mua cổ phiếu MBB (Ngân hàng Quân Đội) cho người mới.md` | `Final-lam-the-nao-de-mua-co-phieu-mbb-ngan-hang-quan-doi.md` |
| `Cách mua cổ phiếu VCB - Ngân hàng Vietcombank cho người mới.md` | `Final-cach-mua-co-phieu-vcb-ngan-hang-vietcombank.md` |

Ngoài ra `5 Cách Đầu Tư Tiền Ảo Từ A-Z...` ↔ `Final-cach-dau-tu-tien-ao` trùng khung 100% nhưng khác nội dung. Cần quyết định giữ bản nào rồi xoá bản còn lại — chừng nào còn trùng thì `SLOP-template` sẽ báo MAJOR trên cả hai.

## 6b. Tầng dữ liệu: 4 bài có số liệu lỗi thời

`python scripts/market_facts.py --verify` quét toàn bộ 188 file: **0 lỗi `FACT-index-wrong`**, **4 lỗi `FACT-stale`** (mọi mốc số liệu trong bài đều cũ hơn 18 tháng):

| bài | mốc cũ nhất còn dùng |
|---|---|
| `Final-vn-diamond-la-gi` | 11/2019, 5/2020 |
| `Final-ultimate-oscillator-la-gi` | 4–8/2022 |
| `Final-loi-the-canh-tranh-la-gi` | 3/2024 |
| `Final-nen-mo-tai-khoan-chung-khoan-o-dau` | 9/2024 |

Đây là ứng viên `/optimize` ưu tiên cao: nội dung không sai nhưng mốc số liệu làm bài bị đọc là lỗi thời. Nhiễu còn lại của rule `FACT-ticker` là 2/188 bài (`VDR`, `SCA`) — advisory, không chặn.

## 7. Giới hạn đã biết của tầng B

- Ngưỡng là **relative** (so với corpus DSC hiện tại), không phải chuẩn tuyệt đối. Mục tiêu tuyệt đối ghi trong comment đầu `slop_check.py`: `rhythm_gap ≤ 12`, `burstiness ≥ 8`, `uniform_run ≤ 9`, `evidence_per_100w ≥ 2.5` — siết dần từng bước, re-derive bằng `--baseline` sau mỗi đợt content lớn.
- `SLOP-anchor` là proxy: câu khái niệm có thể thiếu mỏ neo một cách hợp lý. Chỉ fire ở mật độ đuôi phân bố.
- `SLOP-vague` precision ~80%; hit trong câu đã có ≥2 mỏ neo được tha (trừ nhóm filler thuần).
- `SLOP-template` bỏ qua bài cùng series có chủ ý (`cach-mua-co-phieu-<mã>`).
- Metric **không** đánh giá được: tính đúng của số liệu (→ `market_facts.py`), POV, content gap thật so với SERP (→ tầng C).

## 8. Điều chỉnh khi port từ HVS

| Hạng mục | HVS | DSC |
|---|---|---|
| Ngưỡng `T` | calibrate trên 435 bài | **calibrate lại** trên 182 bài (xem §3) |
| Footer boilerplate | bỏ qua khối "Về HVS Tài chính số" khi đo | DSC không có footer text cố định (CTA là khối HTML, `classify()` đã bỏ qua) → **xoá nhánh skip** |
| `TICKER_STOP` | chặn `HVS` (không phải mã) | **không chặn `DSC`** — là mã niêm yết thật (HNX), cần được kiểm chứng |
| Nhận diện mã trong `market_facts` | `(XYZ)` bất kỳ | siết: `(XYZ)` phải đứng sau **danh từ riêng viết hoa** + bổ sung ~90 acronym ngành (ADX, EMA, NIM, NPM, BTC, LSE, FED…). Trước khi siết: ~25 false positive / 40 bài; sau: **2 / 188 bài** |
| `_common.py` | có sẵn | **tạo mới** với path DSC (`knowledge/4-content/…`) |
| Gate finalize | trong `scripts/finalize.py` | DSC không có `finalize.py` → gate chạy tay trong `.agents/skills/approve/SKILL.md` |
| Rule viết | `anti-ai-rules.md §0` (YAML REQUIRED) | `anti-ai-rules.md` **§8.7** (prose, theo cấu trúc §8 GEO/AEO sẵn có) |

---
