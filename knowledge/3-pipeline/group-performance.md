# Performance theo nhóm bài /kien-thuc

Nguồn: `knowledge\raw\audit\2026-11-10` · GA4: ga4-matrix.json (MCP, thiếu scroll/avg time) · ranking query: có · sinh bởi `python scripts/page_groups.py report`. Chi tiết từng bài: `knowledge/3-pipeline/page-audit.csv`.

Lưu ý số liệu: GSC 90 ngày so 90 ngày trước. Chỉ số query (top 10, striking) tính trên tối đa 500 cặp page×query nhiều impression nhất của mỗi nhóm con — đủ cho query chính, thiếu đuôi dài. GA4 lấy từ MCP Content Matrix: mọi kênh (không riêng Organic), không có thời gian tương tác/scroll — export GA4 theo spec trong `page_groups.py` (AUDIT_FILES) để có đủ.

Bản đồ cụm + link pillar/hub: [`internal-links/topical-map.html`](internal-links/topical-map.html) (bấm tên nhóm con bên dưới để mở đúng nhóm).

Nhãn: `rank-drop` mất clicks/top 10 · `ctr-low` pos ≤ 8 nhưng CTR < 70% trung vị nhóm · `striking` ≥ 5 query pos 4–15 · `engage-low` thời gian/tỷ lệ tương tác dưới trung vị nhóm · `convert-low` đọc tốt nhưng 0 key event · `dead` 0 impression.

## Theo cluster

| Cluster | Bài | Clicks | Δ kỳ trước | Impr | CTR | Pos | Sessions | Eng. rate | Time (s) | Key events |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Mở TK & Giao dịch cơ bản | 42 | 1,374 | -34% | 174,376 | 0.79% | 8.8 | 2,893 | 68% | 0 | 44 |
| 2. Nhập môn & Thị trường chứng khoán | 73 | 3,004 | -11% | 420,972 | 0.71% | 8.7 | 12,569 | 67% | 0 | 964 |
| 3. Phân tích kỹ thuật & Chỉ báo | 128 | 5,342 | -18% | 309,986 | 1.72% | 7.9 | 7,913 | 75% | 0 | 13 |
| 4. Phân tích cơ bản & Tài chính DN | 107 | 2,939 | -23% | 273,413 | 1.07% | 7.1 | 4,233 | 74% | 0 | 6 |
| 5. Cổ phiếu cụ thể & Ngành | 222 | 19,231 | -22% | 1,511,001 | 1.27% | 7.7 | 32,015 | 70% | 0 | 1468 |
| 6. Chiến lược, Phương pháp & Quản trị rủi ro | 52 | 1,114 | -6% | 525,009 | 0.21% | 4.6 | 1,467 | 71% | 0 | 19 |
| 7. Quỹ & ETF | 23 | 481 | -30% | 54,495 | 0.88% | 16.7 | 906 | 71% | 0 | 9 |
| 8. Phái sinh & Chứng quyền | 11 | 240 | -50% | 17,026 | 1.41% | 13.1 | 334 | 71% | 0 | 0 |
| 9. Vĩ mô & Chính sách | 80 | 5,281 | +14% | 459,009 | 1.15% | 5.8 | 6,896 | 67% | 0 | 2 |
| 10. Tiết kiệm & Kênh đầu tư | 47 | 3,644 | -39% | 263,339 | 1.38% | 7.1 | 4,245 | 65% | 0 | 33 |
| 11. Vàng | 17 | 498 | +136% | 40,526 | 1.23% | 8.5 | 515 | 59% | 0 | 3 |
| 12. Trái phiếu | 11 | 196 | +6% | 30,336 | 0.65% | 9.4 | 257 | 75% | 0 | 0 |
| 13. Học & nghề tài chính | 30 | 1,806 | -35% | 78,286 | 2.31% | 9.1 | 2,659 | 72% | 0 | 8 |
| 14. Bạc | 2 | 0 | – | 94 | 0.00% | 19.9 | 0 | 0% | 0 | 0 |

## Theo nhóm con (thứ tự audit = điểm ưu tiên giảm dần)

| Nhóm | Bài | Clicks | Δ | CTR | Pos | 0 click | Query top10 | Striking | Sessions | Eng. | Time (s) | Scroll | KE | Inlink TB | Nhãn | Ưu tiên |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| [5b CP BĐS, KCN, xây dựng](internal-links/topical-map.html#5b) | 36 | 3,486 | -29% | 0.98% | 7.8 | 1 | 290 | 289 | 6,291 | 68% | 0 | – | 506 | 1.1 | rank-drop 19, striking 18, convert-low 4, ctr-low 2 | 2,958 |
| [5o Danh sách cổ phiếu tiềm năng](internal-links/topical-map.html#5o) | 7 | 2,262 | -33% | 4.17% | 5.6 | 0 | 172 | 40 | 4,973 | 70% | 0 | – | 115 | 4.1 | rank-drop 3, ctr-low 2, striking 2, convert-low 1 | 2,496 |
| [5d CP Dầu khí, điện, năng lượng](internal-links/topical-map.html#5d) | 25 | 2,314 | -27% | 1.00% | 8.0 | 0 | 284 | 294 | 2,876 | 70% | 0 | – | 9 | 0.9 | striking 17, rank-drop 13, engage-low 4, convert-low 2 | 2,413 |
| [10a Lãi suất tiết kiệm & so sánh ngân hàng](internal-links/topical-map.html#10a) | 19 | 2,599 | -41% | 1.28% | 6.9 | 4 | 397 | 376 | 3,116 | 63% | 0 | – | 5 | 1.0 | striking 13, rank-drop 7, ctr-low 1, convert-low 1 | 2,287 |
| [6b Chiến lược giao dịch](internal-links/topical-map.html#6b) | 17 | 497 | -17% | 0.11% | 4.3 | 3 | 217 | 122 | 551 | 65% | 0 | – | 15 | 2.4 | striking 6, rank-drop 3, ctr-low 2, engage-low 1 | 1,575 |
| [5a CP Ngân hàng](internal-links/topical-map.html#5a) | 34 | 1,767 | -19% | 0.92% | 8.5 | 0 | 237 | 317 | 5,422 | 68% | 0 | – | 578 | 1.4 | striking 26, rank-drop 15, convert-low 2 | 1,389 |
| [5e CP Bán lẻ, tiêu dùng](internal-links/topical-map.html#5e) | 18 | 1,788 | -6% | 1.40% | 7.7 | 0 | 234 | 241 | 2,581 | 69% | 0 | – | 138 | 1.7 | striking 13, rank-drop 10, engage-low 1, convert-low 1 | 1,103 |
| [2d Chỉ số chứng khoán VN & thế giới](internal-links/topical-map.html#2d) | 21 | 355 | -39% | 0.21% | 9.0 | 1 | 193 | 195 | 379 | 59% | 0 | – | 1 | 3.6 | striking 11, rank-drop 6, convert-low 1, engage-low 1 | 973 |
| [13a Khoá học & sách](internal-links/topical-map.html#13a) | 19 | 1,216 | -38% | 3.27% | 10.4 | 3 | 99 | 95 | 1,815 | 72% | 0 | – | 6 | 1.5 | striking 9, rank-drop 7, engage-low 3, convert-low 2 | 927 |
| [5f CP Chứng khoán, bảo hiểm](internal-links/topical-map.html#5f) | 13 | 1,566 | -28% | 1.78% | 7.1 | 0 | 222 | 153 | 1,881 | 69% | 0 | – | 13 | 0.8 | striking 8, rank-drop 5 | 911 |
| [10b Kênh đầu tư & phân bổ tiền nhàn rỗi](internal-links/topical-map.html#10b) | 23 | 980 | -35% | 1.89% | 7.4 | 2 | 179 | 116 | 1,082 | 69% | 0 | – | 28 | 1.7 | rank-drop 11, striking 7, ctr-low 3, convert-low 1 | 871 |
| [1b Lệnh, quy định & phiên giao dịch](internal-links/topical-map.html#1b) | 20 | 602 | -46% | 0.61% | 7.6 | 5 | 189 | 137 | 1,270 | 71% | 0 | – | 4 | 5.3 | rank-drop 10, striking 9, convert-low 2 | 804 |
| [5j Chuỗi giá trị & phân tích ngành](internal-links/topical-map.html#5j) | 13 | 643 | -10% | 4.83% | 6.3 | 0 | 89 | 11 | 1,295 | 80% | 0 | – | 0 | 1.0 | rank-drop 7, ctr-low 4, convert-low 4, striking 1 | 648 |
| [3d Mô hình nến](internal-links/topical-map.html#3d) | 18 | 2,066 | -14% | 2.90% | 7.0 | 0 | 214 | 117 | 3,119 | 73% | 0 | – | 4 | 3.0 | striking 9, rank-drop 4, ctr-low 4, convert-low 3 | 621 |
| [5c CP Thép, VLXD, nhựa](internal-links/topical-map.html#5c) | 14 | 857 | -23% | 1.16% | 8.3 | 0 | 223 | 138 | 1,205 | 71% | 0 | – | 53 | 0.8 | rank-drop 7, striking 6, convert-low 3 | 618 |
| [3a Chỉ báo xu hướng (MA, MACD, ADX…)](internal-links/topical-map.html#3a) | 23 | 660 | -32% | 1.29% | 8.7 | 3 | 160 | 87 | 986 | 72% | 0 | – | 1 | 3.7 | rank-drop 8, striking 6, ctr-low 4, convert-low 2 | 611 |
| [2f Thị trường, chủ thể & thuật ngữ](internal-links/topical-map.html#2f) | 25 | 1,144 | +5% | 0.86% | 5.5 | 1 | 254 | 145 | 1,493 | 74% | 0 | – | 17 | 1.4 | striking 11, rank-drop 5, ctr-low 4, engage-low 1 | 610 |
| [9b Chính sách tiền tệ, tài khoá & lãi suất](internal-links/topical-map.html#9b) | 25 | 1,469 | -11% | 1.62% | 4.7 | 7 | 261 | 98 | 2,183 | 69% | 0 | – | 1 | 3.2 | rank-drop 8, striking 7, convert-low 3, ctr-low 2 | 493 |
| [4c Định giá cổ phiếu & doanh nghiệp](internal-links/topical-map.html#4c) | 15 | 609 | -35% | 1.88% | 7.0 | 1 | 287 | 59 | 813 | 84% | 0 | – | 0 | 3.7 | striking 8, ctr-low 5, rank-drop 3, convert-low 2 | 485 |
| [3b Chỉ báo động lượng/dao động (RSI, Stoch…)](internal-links/topical-map.html#3b) | 13 | 831 | -21% | 2.05% | 8.6 | 0 | 185 | 59 | 1,463 | 75% | 0 | – | 1 | 3.8 | rank-drop 6, striking 6, ctr-low 4, convert-low 2 | 460 |
| [9a Chỉ số kinh tế](internal-links/topical-map.html#9a) | 21 | 1,277 | +26% | 0.99% | 6.1 | 3 | 233 | 131 | 1,680 | 69% | 0 | – | 0 | 4.8 | striking 10, rank-drop 3, convert-low 2, engage-low 1 | 458 |
| [9e Khái niệm kinh tế học](internal-links/topical-map.html#9e) | 15 | 1,936 | +44% | 1.47% | 5.5 | 2 | 363 | 131 | 2,350 | 65% | 0 | – | 1 | 1.3 | striking 8, rank-drop 3, convert-low 3, engage-low 3 | 456 |
| [1a Tài khoản, app, phí & margin](internal-links/topical-map.html#1a) | 22 | 772 | -18% | 1.03% | 10.4 | 3 | 128 | 109 | 1,623 | 66% | 0 | – | 40 | 7.0 | striking 11, rank-drop 8, ctr-low 1, convert-low 1 | 451 |
| [4d Thanh khoản, đòn bẩy, hiệu quả hoạt động](internal-links/topical-map.html#4d) | 21 | 731 | -22% | 1.13% | 6.4 | 0 | 244 | 115 | 940 | 78% | 0 | – | 0 | 1.5 | striking 9, rank-drop 8, ctr-low 3, convert-low 3 | 436 |
| [5i CP Công nghệ & truyền thông](internal-links/topical-map.html#5i) | 5 | 878 | -26% | 3.85% | 5.4 | 0 | 92 | 20 | 1,376 | 68% | 0 | – | 55 | 0.6 | rank-drop 4, striking 2, convert-low 2 | 429 |
| [4a BCTC, kế toán & chi phí](internal-links/topical-map.html#4a) | 18 | 452 | -28% | 0.49% | 5.1 | 4 | 231 | 61 | 618 | 69% | 0 | – | 3 | 4.6 | rank-drop 5, striking 5, ctr-low 3, engage-low 1 | 400 |
| [13b Chứng chỉ & nghề nghiệp](internal-links/topical-map.html#13b) | 11 | 590 | -29% | 1.43% | 7.8 | 1 | 80 | 67 | 844 | 72% | 0 | – | 2 | 2.4 | striking 6, rank-drop 5, convert-low 1 | 393 |
| [5g CP Cảng biển & logistics](internal-links/topical-map.html#5g) | 7 | 1,647 | -6% | 1.23% | 7.0 | 0 | 167 | 107 | 1,993 | 75% | 0 | – | 1 | 1.3 | striking 5, convert-low 3, rank-drop 2, ctr-low 1 | 391 |
| [5h CP Nông nghiệp, thuỷ sản, cao su](internal-links/topical-map.html#5h) | 17 | 982 | -2% | 1.63% | 7.6 | 0 | 155 | 114 | 1,128 | 72% | 0 | – | 0 | 0.7 | striking 10, rank-drop 4, convert-low 2, engage-low 2 | 366 |
| [7a Chứng chỉ quỹ, quỹ mở & ETF](internal-links/topical-map.html#7a) | 23 | 481 | -30% | 0.88% | 16.7 | 6 | 99 | 86 | 906 | 71% | 0 | – | 9 | 3.8 | rank-drop 5, striking 5, ctr-low 2, dead 1 | 330 |
| [2b Thao tác mua/bán](internal-links/topical-map.html#2b) | 10 | 515 | -25% | 0.97% | 10.4 | 1 | 152 | 90 | 1,056 | 65% | 0 | – | 75 | 5.1 | striking 5, rank-drop 2 | 326 |
| [6c Quản trị rủi ro & danh mục](internal-links/topical-map.html#6c) | 20 | 526 | +9% | 0.92% | 6.4 | 5 | 270 | 85 | 816 | 75% | 0 | – | 4 | 3.5 | striking 6, ctr-low 3, convert-low 2, dead 2 | 321 |
| [5m CP Hoá chất, phân bón](internal-links/topical-map.html#5m) | 5 | 360 | -35% | 0.54% | 8.3 | 0 | 80 | 69 | 455 | 66% | 0 | – | 0 | 1.0 | rank-drop 5, striking 4, convert-low 1, engage-low 1 | 320 |
| [3h Lý thuyết, phương pháp & công cụ PTKT](internal-links/topical-map.html#3h) | 16 | 649 | -16% | 1.61% | 8.5 | 4 | 185 | 92 | 1,004 | 78% | 0 | – | 4 | 6.2 | striking 4, rank-drop 3, engage-low 1, convert-low 1 | 289 |
| [8a Phái sinh](internal-links/topical-map.html#8a) | 8 | 235 | -51% | 1.48% | 12.1 | 4 | 98 | 14 | 334 | 71% | 0 | – | 0 | 3.4 | rank-drop 1, striking 1 | 261 |
| [3f Hỗ trợ–kháng cự, xu hướng, trap, gap](internal-links/topical-map.html#3f) | 20 | 422 | -2% | 0.84% | 7.4 | 1 | 214 | 80 | 498 | 73% | 0 | – | 0 | 3.5 | striking 7, rank-drop 6, ctr-low 4 | 240 |
| [9d Tỷ giá, thương mại, dòng vốn ngoại](internal-links/topical-map.html#9d) | 11 | 260 | -6% | 0.31% | 7.3 | 1 | 225 | 98 | 274 | 66% | 0 | – | 0 | 0.7 | striking 5, rank-drop 3, ctr-low 2, engage-low 1 | 223 |
| [3c Khối lượng & dòng tiền](internal-links/topical-map.html#3c) | 11 | 371 | -9% | 1.51% | 6.8 | 0 | 210 | 43 | 479 | 79% | 0 | – | 3 | 2.4 | rank-drop 4, striking 4, ctr-low 2 | 217 |
| [3g Chỉ báo khác (ATR, Bollinger, Keltner…)](internal-links/topical-map.html#3g) | 13 | 159 | -47% | 1.02% | 8.3 | 1 | 217 | 22 | 116 | 84% | 0 | – | 0 | 2.2 | rank-drop 4, ctr-low 3, convert-low 1, striking 1 | 215 |
| [2a Nền tảng, kinh nghiệm & rủi ro cho người mới](internal-links/topical-map.html#2a) | 17 | 990 | -1% | 1.43% | 12.6 | 5 | 142 | 103 | 9,641 | 67% | 0 | – | 871 | 7.6 | striking 2, rank-drop 2 | 196 |
| [4e Vốn, cổ phần & niêm yết](internal-links/topical-map.html#4e) | 18 | 194 | -23% | 0.73% | 8.9 | 1 | 147 | 46 | 139 | 71% | 0 | – | 0 | 2.1 | rank-drop 6, striking 5, engage-low 1 | 187 |
| [5l CP Hàng không](internal-links/topical-map.html#5l) | 7 | 165 | -34% | 0.87% | 8.4 | 0 | 64 | 49 | 101 | 63% | 0 | – | 0 | 0.9 | striking 4, rank-drop 3 | 176 |
| [11a Vàng](internal-links/topical-map.html#11a) | 17 | 498 | +136% | 1.23% | 8.5 | 4 | 176 | 104 | 515 | 59% | 0 | – | 3 | 0.9 | striking 5, ctr-low 1, rank-drop 1 | 165 |
| [4f Cổ tức & quyền cổ đông](internal-links/topical-map.html#4f) | 6 | 179 | -40% | 1.24% | 9.2 | 1 | 42 | 17 | 264 | 66% | 0 | – | 3 | 2.8 | rank-drop 2, convert-low 1, striking 1, engage-low 1 | 160 |
| [5n CP Dệt may](internal-links/topical-map.html#5n) | 6 | 225 | -23% | 0.71% | 7.8 | 0 | 107 | 48 | 220 | 75% | 0 | – | 0 | 0.7 | striking 5, rank-drop 4 | 147 |
| [4g Phân tích BCTC doanh nghiệp cụ thể](internal-links/topical-map.html#4g) | 9 | 675 | +6% | 3.85% | 7.5 | 1 | 228 | 47 | 1,397 | 70% | 0 | – | 0 | 0.6 | rank-drop 7, striking 5, convert-low 4 | 127 |
| [5p Chỉ số phân tích ngân hàng (NIM, CASA, LDR…)](internal-links/topical-map.html#5p) | 7 | 208 | +395% | 0.73% | 7.6 | 1 | 185 | 84 | 218 | 78% | 0 | – | 0 | 2.6 | striking 6, rank-drop 2 | 111 |
| [3e Mô hình giá](internal-links/topical-map.html#3e) | 14 | 184 | +3% | 1.13% | 8.6 | 4 | 161 | 69 | 248 | 79% | 0 | – | 0 | 1.9 | striking 5, rank-drop 1, convert-low 1, engage-low 1 | 104 |
| [9f Khủng hoảng & sự kiện](internal-links/topical-map.html#9f) | 8 | 339 | -5% | 1.49% | 5.8 | 0 | 68 | 40 | 409 | 68% | 0 | – | 0 | 0.8 | striking 4, convert-low 1, rank-drop 1 | 96 |
| [4b Chỉ số sinh lời](internal-links/topical-map.html#4b) | 14 | 69 | -27% | 0.32% | 14.0 | 2 | 144 | 44 | 62 | 87% | 0 | – | 0 | 7.2 | striking 5, rank-drop 3 | 90 |
| [5k Loại cổ phiếu & cách chọn](internal-links/topical-map.html#5k) | 8 | 83 | -19% | 0.73% | 7.8 | 1 | 31 | 17 | 0 | 0% | 0 | – | 0 | 5.5 | rank-drop 2, ctr-low 1, striking 1 | 86 |
| [12a Trái phiếu & lợi suất](internal-links/topical-map.html#12a) | 11 | 196 | +6% | 0.65% | 9.4 | 3 | 111 | 48 | 257 | 75% | 0 | – | 0 | 2.8 | striking 3, rank-drop 2, engage-low 1 | 82 |
| [10d Ngoài phạm vi: tiền số, forex, tài chính cá nhân](internal-links/topical-map.html#10d) | 5 | 65 | +160% | 0.76% | 8.1 | 2 | 61 | 32 | 47 | 72% | 0 | – | 0 | 0.2 | striking 2 | 55 |
| [6d Tâm lý & hành vi](internal-links/topical-map.html#6d) | 8 | 45 | -25% | 0.96% | 10.5 | 2 | 76 | 15 | 44 | 66% | 0 | – | 0 | 1.9 | rank-drop 2, striking 1 | 38 |
| [4h Phân tích định tính doanh nghiệp](internal-links/topical-map.html#4h) | 6 | 30 | -40% | 0.70% | 7.8 | 4 | 39 | 10 | 0 | 0% | 0 | – | 0 | 2.8 | rank-drop 1, striking 1 | 30 |
| [6a Trường phái & nhà đầu tư nổi tiếng](internal-links/topical-map.html#6a) | 7 | 46 | +18% | 1.90% | 15.1 | 4 | 28 | 7 | 56 | 70% | 0 | – | 0 | 2.4 | rank-drop 4 | 11 |
| [8b Chứng quyền](internal-links/topical-map.html#8b) | 3 | 5 | +150% | 0.44% | 27.3 | 2 | 6 | 0 | 0 | 0% | 0 | – | 0 | 0.7 |  | 1 |
| [14a Bạc](internal-links/topical-map.html#14a) | 2 | 0 | – | 0.00% | 19.9 | 2 | 2 | 1 | 0 | 0% | 0 | – | 0 | 1.0 |  | 1 |

## Theo dạng bài (intent)

| Intent | Bài | Clicks | CTR | Pos | Eng. | Time (s) |
|---|---:|---:|---:|---:|---:|---:|
| dinh-nghia | 333 | 9,776 | 0.66% | 6.3 | 72% | 0 |
| ma-cp | 154 | 8,823 | 0.75% | 8.3 | 70% | 0 |
| khac | 118 | 10,388 | 1.98% | 7.3 | 69% | 0 |
| so-sanh | 108 | 5,686 | 1.35% | 6.5 | 71% | 0 |
| huong-dan | 50 | 2,772 | 1.58% | 11.0 | 68% | 0 |
| list | 41 | 4,881 | 1.79% | 8.5 | 70% | 0 |
| co-nen | 41 | 2,824 | 2.61% | 7.7 | 71% | 0 |

## Bài 0 impression (4) — xem xét prune/merge

`hieu-ung-thang-gieng-trong-dau-tu-chung-khoan-la-gi`, `huong-dan-phan-bo-va-da-dang-hoa-tai-san`, `rui-ro-va-loi-ich-khi-tham-gia-thi-truong-tai-chinh`, `quy-trinh-hoan-doi-danh-muc-etf`

## URL có impression nhưng không còn trong snapshot live (37) — kiểm tra redirect / đổi slug

| URL | Clicks | Impr | Clicks kỳ trước | Impr kỳ trước |
|---|---:|---:|---:|---:|
| `co-nen-mua-co-phieu-stb-hay-khong` | 18 | 2846 | 19 | 4579 |
| `tim-hieu-phuong-phap-cua-wyckoff-ve-phan-tich-thi-truong` | 21 | 2567 | 39 | 4517 |
| `co-phieu-pow-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat-2025` | 23 | 3605 | 30 | 4278 |
| `thuc-trang-thi-truong-tai-chinh-viet-nam-hien-nay` | 0 | 0 | 155 | 3038 |
| `tat-ca-kien-thuc` | 0 | 2558 | 0 | 46 |
| `co-nen-mua-co-phieu-msb-hay-khong` | 14 | 2491 | 21 | 2394 |
| `san-otc-la-gi-tim-hieu-thi-truong-chung-khoan-phi-tap-trung` | 3 | 875 | 5 | 1532 |
| `yoy-la-gi-cach-tinh-va-y-nghia-chi-so-yoy` | 0 | 1070 | 0 | 0 |
| `danh-sach-cac-quy-etf-uy-tin-tai-viet-nam-cap-nhat` | 0 | 0 | 5 | 988 |
| `huong-dan-cach-mua-chung-chi-quy-etf-cho-nguoi-moi-bat-dau` | 0 | 0 | 9 | 889 |
| `chi-bao-bollinger-bandwidth-bbw-la-gi` | 0 | 0 | 2 | 454 |
| `yoy-la-gi-cach-tinh-y-nghia-cua-chi-so-yoy` | 0 | 382 | 0 | 0 |
| `cac-loai-lenh-trong-giao-dich-chung-khoan-tai-viet-nam` | 0 | 0 | 1 | 381 |
| `thuc-tap-so-dsc-giai-phap-thuc-tap-chung-khoan-cho-sinh-vien` | 2 | 37 | 14 | 339 |
| `cach-mua-co-phieu-msn` | 0 | 59 | 13 | 318 |
| `huong-dan-chi-tiet-giao-dich-theo-xu-huong-va-vi-du-minh-hoa` | 0 | 0 | 0 | 308 |
| `cach-mua-co-phieu-vib` | 1 | 94 | 2 | 287 |
| `cac-sai-lam-dan-toi-pha-san-trong-dau-tu-chung-khoan` | 0 | 49 | 3 | 286 |
| `phan-tich-ky-thuat` | 0 | 183 | 0 | 230 |
| `mua-co-phieu-o-dau-san-chung-khoan-hay-cty-chung-khoan` | 1 | 55 | 0 | 221 |
| `cach-mua-co-phieu-gas` | 2 | 62 | 4 | 206 |
| `cac-phuong-phap-dau-tu-chung-khoan-pho-bien-va-hieu-qua` | 0 | 0 | 3 | 206 |
| `thuc-tap-sinh-tai-chinh-la-gi` | 0 | 0 | 3 | 159 |
| `yoy-la-gi-cach-tinh-va-y-nghia-cho-chi-so-yoy` | 0 | 150 | 0 | 0 |
| `10-phuong-phap-giao-dich-theo-phan-tich-ky-thuat-cua-john-murphy` | 0 | 0 | 1 | 144 |
| `chien-luoc-follow-trade-la-gi-huong-dan-cach-ap-dung-cho-nguoi-moi` | 2 | 20 | 0 | 141 |
| `cac-tu-long-thuong-gap-khi-dau-tu-chung-khoan` | 2 | 71 | 3 | 129 |
| `hop-dong-tuong-lai-chi-so-chung-khoan-vn-30-huong-dan-chi-tiet` | 0 | 39 | 0 | 127 |
| `cho-nguoi-moi-bat-dau` | 1 | 121 | 0 | 66 |
| `dong-tien-trong-chung-khoan-yeu-to-quan-trong-bac-nhat` | 1 | 115 | 0 | 54 |
| `cach-mua-co-phieu-bcm` | 0 | 37 | 5 | 113 |
| `con-hao-kinh-te-la-gi-cach-tao-ra-va-tam-quan-trong-con-hao-kinh-te` | 0 | 110 | 0 | 0 |
| `loi-nhuan-trong-dau-tu-chung-khoan-bi-kip-khai-pha-tiem-nang` | 0 | 24 | 0 | 109 |
| `phan-tich-co-ban` | 0 | 105 | 0 | 86 |
| `chi-bao-bollinger-band-squeeze-la-gi` | 0 | 0 | 2 | 95 |
| `sec-la-giai-thich-chi-tiet-ve-uy-ban-chung-khoan-va-hoi-doai-hoa-ky` | 0 | 63 | 0 | 0 |
| `cach-mua-co-phieu-pdr` | 0 | 12 | 1 | 60 |
