# Performance theo nhóm bài /kien-thuc

Nguồn: `knowledge\raw\audit\2026-11-10` · GA4: ga4-matrix.json (MCP, thiếu scroll/avg time) · ranking query: có · sinh bởi `python scripts/page_groups.py report`. Chi tiết từng bài: `knowledge/3-seo/strategy/page-audit.csv`.

Lưu ý số liệu: GSC 90 ngày so 90 ngày trước. Chỉ số query (top 10, striking) tính trên tối đa 500 cặp page×query nhiều impression nhất của mỗi nhóm con — đủ cho query chính, thiếu đuôi dài. GA4 lấy từ MCP Content Matrix: mọi kênh (không riêng Organic), không có thời gian tương tác/scroll — export GA4 theo spec trong `page_groups.py` (AUDIT_FILES) để có đủ.

Bản đồ cụm + link pillar/hub: [`topical-map.html`](topical-map.html) (bấm tên nhóm con bên dưới để mở đúng nhóm).

Nhãn: `rank-drop` mất clicks/top 10 · `ctr-low` pos ≤ 8 nhưng CTR < 70% trung vị nhóm · `striking` ≥ 5 query pos 4–15 · `engage-low` thời gian/tỷ lệ tương tác dưới trung vị nhóm · `convert-low` đọc tốt nhưng 0 key event · `dead` 0 impression.

## Theo cluster

| Cluster | Bài | Clicks | Δ kỳ trước | Impr | CTR | Pos | Sessions | Eng. rate | Time (s) | Key events |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Mở TK & Giao dịch cơ bản | 43 | 1,374 | -34% | 174,376 | 0.79% | 8.8 | 2,893 | 68% | 0 | 44 |
| 2. Nhập môn & Thị trường chứng khoán | 73 | 3,004 | -11% | 420,972 | 0.71% | 8.7 | 12,569 | 67% | 0 | 964 |
| 3. Phân tích kỹ thuật & Chỉ báo | 127 | 5,331 | -18% | 309,225 | 1.72% | 7.9 | 7,913 | 75% | 0 | 13 |
| 4. Phân tích cơ bản & Tài chính DN | 107 | 2,939 | -23% | 273,413 | 1.07% | 7.1 | 4,233 | 74% | 0 | 6 |
| 5. Cổ phiếu cụ thể & Ngành | 207 | 18,679 | -22% | 1,435,747 | 1.30% | 7.6 | 31,464 | 70% | 0 | 1467 |
| 6. Chiến lược, Phương pháp & Quản trị rủi ro | 50 | 1,114 | -6% | 525,009 | 0.21% | 4.6 | 1,467 | 71% | 0 | 19 |
| 7. Quỹ & ETF | 21 | 481 | -30% | 54,161 | 0.89% | 16.5 | 906 | 71% | 0 | 9 |
| 8. Phái sinh & Chứng quyền | 11 | 240 | -50% | 17,026 | 1.41% | 13.1 | 334 | 71% | 0 | 0 |
| 9. Vĩ mô & Chính sách | 80 | 5,281 | +14% | 459,009 | 1.15% | 5.8 | 6,896 | 67% | 0 | 2 |
| 10. Tiết kiệm & Kênh đầu tư | 47 | 3,644 | -39% | 263,339 | 1.38% | 7.1 | 4,245 | 65% | 0 | 33 |
| 11. Vàng | 16 | 498 | +136% | 40,525 | 1.23% | 8.5 | 515 | 59% | 0 | 3 |
| 12. Trái phiếu | 11 | 196 | +6% | 30,336 | 0.65% | 9.4 | 257 | 75% | 0 | 0 |
| 13. Học & nghề tài chính | 30 | 1,806 | -35% | 78,286 | 2.31% | 9.1 | 2,659 | 72% | 0 | 8 |
| 14. Bạc | 2 | 0 | – | 94 | 0.00% | 19.9 | 0 | 0% | 0 | 0 |

## Theo nhóm con (thứ tự audit = điểm ưu tiên giảm dần)

| Nhóm | Bài | Clicks | Δ | CTR | Pos | 0 click | Query top10 | Striking | Sessions | Eng. | Time (s) | Scroll | KE | Inlink TB | Nhãn | Ưu tiên |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| [5b CP BĐS, KCN, xây dựng](topical-map.html#5b) | 34 | 3,315 | -29% | 0.98% | 7.7 | 0 | 281 | 278 | 6,099 | 68% | 0 | – | 505 | 1.6 | rank-drop 18, striking 17, convert-low 4, ctr-low 3 | 2,921 |
| [5o Danh sách cổ phiếu tiềm năng](topical-map.html#5o) | 7 | 2,262 | -33% | 4.17% | 5.6 | 0 | 172 | 40 | 4,973 | 70% | 0 | – | 115 | 5.4 | rank-drop 3, ctr-low 2, striking 2, convert-low 1 | 2,496 |
| [10a Lãi suất tiết kiệm & so sánh ngân hàng](topical-map.html#10a) | 19 | 2,599 | -41% | 1.28% | 6.9 | 4 | 397 | 376 | 3,116 | 63% | 0 | – | 5 | 1.8 | striking 13, rank-drop 7, ctr-low 1, convert-low 1 | 2,287 |
| [5d CP Dầu khí, điện, năng lượng](topical-map.html#5d) | 21 | 2,184 | -28% | 1.06% | 7.8 | 0 | 261 | 263 | 2,749 | 70% | 0 | – | 9 | 1.8 | striking 15, rank-drop 11, engage-low 4, convert-low 2 | 2,109 |
| [5a CP Ngân hàng](topical-map.html#5a) | 29 | 1,614 | -19% | 0.94% | 8.5 | 0 | 206 | 275 | 5,313 | 68% | 0 | – | 578 | 1.9 | striking 22, rank-drop 13, convert-low 1, ctr-low 1 | 1,640 |
| [6b Chiến lược giao dịch](topical-map.html#6b) | 17 | 497 | -17% | 0.11% | 4.3 | 3 | 217 | 122 | 551 | 65% | 0 | – | 15 | 4.2 | striking 6, rank-drop 3, ctr-low 2, engage-low 1 | 1,575 |
| [5e CP Bán lẻ, tiêu dùng](topical-map.html#5e) | 17 | 1,757 | -6% | 1.44% | 7.6 | 0 | 212 | 213 | 2,544 | 69% | 0 | – | 138 | 2.3 | striking 12, rank-drop 9, engage-low 1, convert-low 1 | 1,066 |
| [2d Chỉ số chứng khoán VN & thế giới](topical-map.html#2d) | 21 | 355 | -39% | 0.21% | 9.0 | 1 | 193 | 195 | 379 | 59% | 0 | – | 1 | 4.9 | striking 11, rank-drop 6, convert-low 1, engage-low 1 | 973 |
| [13a Khoá học & sách](topical-map.html#13a) | 19 | 1,216 | -38% | 3.27% | 10.4 | 3 | 99 | 95 | 1,815 | 72% | 0 | – | 6 | 1.8 | striking 9, rank-drop 7, engage-low 3, convert-low 2 | 927 |
| [10b Kênh đầu tư & phân bổ tiền nhàn rỗi](topical-map.html#10b) | 23 | 980 | -35% | 1.89% | 7.4 | 2 | 179 | 116 | 1,082 | 69% | 0 | – | 28 | 2.2 | rank-drop 11, striking 7, ctr-low 3, convert-low 1 | 871 |
| [5f CP Chứng khoán, bảo hiểm](topical-map.html#5f) | 12 | 1,528 | -28% | 1.80% | 7.0 | 0 | 212 | 144 | 1,832 | 69% | 0 | – | 13 | 0.8 | striking 7, rank-drop 4 | 870 |
| [1b Lệnh, quy định & phiên giao dịch](topical-map.html#1b) | 20 | 602 | -46% | 0.61% | 7.6 | 5 | 189 | 137 | 1,270 | 71% | 0 | – | 4 | 5.3 | rank-drop 10, striking 9, convert-low 2 | 804 |
| [5j Chuỗi giá trị & phân tích ngành](topical-map.html#5j) | 13 | 643 | -10% | 4.83% | 6.3 | 0 | 89 | 11 | 1,295 | 80% | 0 | – | 0 | 2.0 | rank-drop 7, ctr-low 4, convert-low 4, striking 1 | 648 |
| [3d Mô hình nến](topical-map.html#3d) | 18 | 2,066 | -14% | 2.90% | 7.0 | 0 | 214 | 117 | 3,119 | 73% | 0 | – | 4 | 3.2 | striking 9, rank-drop 4, ctr-low 4, convert-low 3 | 621 |
| [2f Thị trường, chủ thể & thuật ngữ](topical-map.html#2f) | 25 | 1,144 | +5% | 0.86% | 5.5 | 1 | 254 | 145 | 1,493 | 74% | 0 | – | 17 | 1.6 | striking 11, rank-drop 5, ctr-low 4, engage-low 1 | 610 |
| [3a Chỉ báo xu hướng (MA, MACD, ADX…)](topical-map.html#3a) | 22 | 649 | -33% | 1.29% | 8.6 | 3 | 158 | 86 | 986 | 72% | 0 | – | 1 | 4.5 | rank-drop 8, striking 6, ctr-low 4, convert-low 2 | 560 |
| [5c CP Thép, VLXD, nhựa](topical-map.html#5c) | 13 | 834 | -23% | 1.16% | 8.2 | 0 | 215 | 134 | 1,168 | 72% | 0 | – | 53 | 1.1 | rank-drop 6, striking 6, convert-low 2 | 559 |
| [9b Chính sách tiền tệ, tài khoá & lãi suất](topical-map.html#9b) | 25 | 1,469 | -11% | 1.62% | 4.7 | 7 | 261 | 98 | 2,183 | 69% | 0 | – | 1 | 4.3 | rank-drop 8, striking 7, convert-low 3, ctr-low 2 | 493 |
| [4c Định giá cổ phiếu & doanh nghiệp](topical-map.html#4c) | 15 | 609 | -35% | 1.88% | 7.0 | 1 | 287 | 59 | 813 | 84% | 0 | – | 0 | 4.8 | striking 8, ctr-low 5, rank-drop 3, convert-low 2 | 485 |
| [3b Chỉ báo động lượng/dao động (RSI, Stoch…)](topical-map.html#3b) | 13 | 831 | -21% | 2.05% | 8.6 | 0 | 185 | 59 | 1,463 | 75% | 0 | – | 1 | 3.8 | rank-drop 6, striking 6, ctr-low 4, convert-low 2 | 460 |
| [9a Chỉ số kinh tế](topical-map.html#9a) | 21 | 1,277 | +26% | 0.99% | 6.1 | 3 | 233 | 131 | 1,680 | 69% | 0 | – | 0 | 6.6 | striking 10, rank-drop 3, convert-low 2, engage-low 1 | 458 |
| [9e Khái niệm kinh tế học](topical-map.html#9e) | 15 | 1,936 | +44% | 1.47% | 5.5 | 2 | 363 | 131 | 2,350 | 65% | 0 | – | 1 | 2.6 | striking 8, rank-drop 3, convert-low 3, engage-low 3 | 456 |
| [1a Tài khoản, app, phí & margin](topical-map.html#1a) | 23 | 772 | -18% | 1.03% | 10.4 | 4 | 128 | 109 | 1,623 | 66% | 0 | – | 40 | 7.1 | striking 11, rank-drop 8, ctr-low 1, convert-low 1 | 451 |
| [4d Thanh khoản, đòn bẩy, hiệu quả hoạt động](topical-map.html#4d) | 21 | 731 | -22% | 1.13% | 6.4 | 0 | 244 | 115 | 940 | 78% | 0 | – | 0 | 2.0 | striking 9, rank-drop 8, ctr-low 3, convert-low 3 | 436 |
| [5i CP Công nghệ & truyền thông](topical-map.html#5i) | 5 | 878 | -26% | 3.85% | 5.4 | 0 | 92 | 20 | 1,376 | 68% | 0 | – | 55 | 1.8 | rank-drop 4, striking 2, convert-low 2 | 429 |
| [4a BCTC, kế toán & chi phí](topical-map.html#4a) | 18 | 452 | -28% | 0.49% | 5.1 | 4 | 231 | 61 | 618 | 69% | 0 | – | 3 | 11.4 | rank-drop 5, striking 5, ctr-low 3, engage-low 1 | 400 |
| [13b Chứng chỉ & nghề nghiệp](topical-map.html#13b) | 11 | 590 | -29% | 1.43% | 7.8 | 1 | 80 | 67 | 844 | 72% | 0 | – | 2 | 2.5 | striking 6, rank-drop 5, convert-low 1 | 393 |
| [5g CP Cảng biển & logistics](topical-map.html#5g) | 7 | 1,647 | -6% | 1.23% | 7.0 | 0 | 167 | 107 | 1,993 | 75% | 0 | – | 1 | 1.9 | striking 5, convert-low 3, rank-drop 2, ctr-low 1 | 391 |
| [5h CP Nông nghiệp, thuỷ sản, cao su](topical-map.html#5h) | 17 | 982 | -2% | 1.63% | 7.6 | 0 | 155 | 114 | 1,128 | 72% | 0 | – | 0 | 1.5 | striking 10, rank-drop 4, convert-low 2, engage-low 2 | 366 |
| [7a Chứng chỉ quỹ, quỹ mở & ETF](topical-map.html#7a) | 21 | 481 | -30% | 0.89% | 16.5 | 4 | 99 | 86 | 906 | 71% | 0 | – | 9 | 5.0 | rank-drop 5, striking 5, ctr-low 2 | 328 |
| [2b Thao tác mua/bán](topical-map.html#2b) | 10 | 515 | -25% | 0.97% | 10.4 | 1 | 152 | 90 | 1,056 | 65% | 0 | – | 75 | 4.7 | striking 5, rank-drop 2 | 326 |
| [6c Quản trị rủi ro & danh mục](topical-map.html#6c) | 18 | 526 | +9% | 0.92% | 6.4 | 3 | 270 | 85 | 816 | 75% | 0 | – | 4 | 5.1 | striking 6, ctr-low 3, convert-low 2, rank-drop 1 | 321 |
| [5m CP Hoá chất, phân bón](topical-map.html#5m) | 5 | 360 | -35% | 0.54% | 8.3 | 0 | 80 | 69 | 455 | 66% | 0 | – | 0 | 1.8 | rank-drop 5, striking 4, convert-low 1, engage-low 1 | 320 |
| [3h Lý thuyết, phương pháp & công cụ PTKT](topical-map.html#3h) | 16 | 649 | -16% | 1.61% | 8.5 | 4 | 185 | 92 | 1,004 | 78% | 0 | – | 4 | 9.6 | striking 4, rank-drop 3, engage-low 1, convert-low 1 | 289 |
| [8a Phái sinh](topical-map.html#8a) | 8 | 235 | -51% | 1.48% | 12.1 | 4 | 98 | 14 | 334 | 71% | 0 | – | 0 | 3.6 | rank-drop 1, striking 1 | 261 |
| [3f Hỗ trợ–kháng cự, xu hướng, trap, gap](topical-map.html#3f) | 20 | 422 | -2% | 0.84% | 7.4 | 1 | 214 | 80 | 498 | 73% | 0 | – | 0 | 4.0 | striking 7, rank-drop 6, ctr-low 4 | 240 |
| [9d Tỷ giá, thương mại, dòng vốn ngoại](topical-map.html#9d) | 11 | 260 | -6% | 0.31% | 7.3 | 1 | 225 | 98 | 274 | 66% | 0 | – | 0 | 1.3 | striking 5, rank-drop 3, ctr-low 2, engage-low 1 | 223 |
| [3c Khối lượng & dòng tiền](topical-map.html#3c) | 11 | 371 | -9% | 1.51% | 6.8 | 0 | 210 | 43 | 479 | 79% | 0 | – | 3 | 3.3 | rank-drop 4, striking 4, ctr-low 2 | 217 |
| [3g Chỉ báo khác (ATR, Bollinger, Keltner…)](topical-map.html#3g) | 13 | 159 | -47% | 1.02% | 8.3 | 1 | 217 | 22 | 116 | 84% | 0 | – | 0 | 2.8 | rank-drop 4, ctr-low 3, convert-low 1, striking 1 | 215 |
| [2a Nền tảng, kinh nghiệm & rủi ro cho người mới](topical-map.html#2a) | 17 | 990 | -1% | 1.43% | 12.6 | 5 | 142 | 103 | 9,641 | 67% | 0 | – | 871 | 8.5 | striking 2, rank-drop 2 | 196 |
| [4e Vốn, cổ phần & niêm yết](topical-map.html#4e) | 18 | 194 | -23% | 0.73% | 8.9 | 1 | 147 | 46 | 139 | 71% | 0 | – | 0 | 2.8 | rank-drop 6, striking 5, engage-low 1 | 187 |
| [11a Vàng](topical-map.html#11a) | 16 | 498 | +136% | 1.23% | 8.5 | 3 | 176 | 104 | 515 | 59% | 0 | – | 3 | 1.9 | striking 5, ctr-low 1, rank-drop 1 | 165 |
| [5l CP Hàng không](topical-map.html#5l) | 6 | 159 | -32% | 0.85% | 8.4 | 0 | 63 | 49 | 101 | 63% | 0 | – | 0 | 1.8 | striking 4, rank-drop 3 | 162 |
| [4f Cổ tức & quyền cổ đông](topical-map.html#4f) | 6 | 179 | -40% | 1.24% | 9.2 | 1 | 42 | 17 | 264 | 66% | 0 | – | 3 | 3.3 | rank-drop 2, convert-low 1, striking 1, engage-low 1 | 160 |
| [5n CP Dệt may](topical-map.html#5n) | 6 | 225 | -23% | 0.71% | 7.8 | 0 | 107 | 48 | 220 | 75% | 0 | – | 0 | 1.7 | striking 5, rank-drop 4 | 147 |
| [4g Phân tích BCTC doanh nghiệp cụ thể](topical-map.html#4g) | 9 | 675 | +6% | 3.85% | 7.5 | 1 | 228 | 47 | 1,397 | 70% | 0 | – | 0 | 0.4 | rank-drop 7, striking 5, convert-low 4 | 127 |
| [5p Chỉ số phân tích ngân hàng (NIM, CASA, LDR…)](topical-map.html#5p) | 7 | 208 | +395% | 0.73% | 7.6 | 1 | 185 | 84 | 218 | 78% | 0 | – | 0 | 2.6 | striking 6, rank-drop 2 | 111 |
| [3e Mô hình giá](topical-map.html#3e) | 14 | 184 | +3% | 1.13% | 8.6 | 4 | 161 | 69 | 248 | 79% | 0 | – | 0 | 2.4 | striking 5, rank-drop 1, convert-low 1, engage-low 1 | 104 |
| [9f Khủng hoảng & sự kiện](topical-map.html#9f) | 8 | 339 | -5% | 1.49% | 5.8 | 0 | 68 | 40 | 409 | 68% | 0 | – | 0 | 1.4 | striking 4, convert-low 1, rank-drop 1 | 96 |
| [4b Chỉ số sinh lời](topical-map.html#4b) | 14 | 69 | -27% | 0.32% | 14.0 | 2 | 144 | 44 | 62 | 87% | 0 | – | 0 | 8.4 | striking 5, rank-drop 3 | 90 |
| [5k Loại cổ phiếu & cách chọn](topical-map.html#5k) | 8 | 83 | -19% | 0.73% | 7.8 | 1 | 31 | 17 | 0 | 0% | 0 | – | 0 | 5.5 | rank-drop 2, ctr-low 1, striking 1 | 86 |
| [12a Trái phiếu & lợi suất](topical-map.html#12a) | 11 | 196 | +6% | 0.65% | 9.4 | 3 | 111 | 48 | 257 | 75% | 0 | – | 0 | 3.3 | striking 3, rank-drop 2, engage-low 1 | 82 |
| [10d Ngoài phạm vi: tiền số, forex, tài chính cá nhân](topical-map.html#10d) | 5 | 65 | +160% | 0.76% | 8.1 | 2 | 61 | 32 | 47 | 72% | 0 | – | 0 | 0.2 | striking 2 | 55 |
| [6d Tâm lý & hành vi](topical-map.html#6d) | 8 | 45 | -25% | 0.96% | 10.5 | 2 | 76 | 15 | 44 | 66% | 0 | – | 0 | 2.8 | rank-drop 2, striking 1 | 38 |
| [4h Phân tích định tính doanh nghiệp](topical-map.html#4h) | 6 | 30 | -40% | 0.70% | 7.8 | 4 | 39 | 10 | 0 | 0% | 0 | – | 0 | 3.7 | rank-drop 1, striking 1 | 30 |
| [6a Trường phái & nhà đầu tư nổi tiếng](topical-map.html#6a) | 7 | 46 | +18% | 1.90% | 15.1 | 4 | 28 | 7 | 56 | 70% | 0 | – | 0 | 2.4 | rank-drop 4 | 11 |
| [8b Chứng quyền](topical-map.html#8b) | 3 | 5 | +150% | 0.44% | 27.3 | 2 | 6 | 0 | 0 | 0% | 0 | – | 0 | 1.0 |  | 1 |
| [14a Bạc](topical-map.html#14a) | 2 | 0 | – | 0.00% | 19.9 | 2 | 2 | 1 | 0 | 0% | 0 | – | 0 | 1.5 |  | 1 |

## Theo dạng bài (intent)

| Intent | Bài | Clicks | CTR | Pos | Eng. | Time (s) |
|---|---:|---:|---:|---:|---:|---:|
| dinh-nghia | 332 | 9,776 | 0.66% | 6.2 | 72% | 0 |
| ma-cp | 139 | 8,271 | 0.75% | 8.2 | 70% | 0 |
| khac | 119 | 10,388 | 1.98% | 7.3 | 69% | 0 |
| so-sanh | 104 | 5,675 | 1.35% | 6.5 | 71% | 0 |
| huong-dan | 49 | 2,772 | 1.58% | 11.0 | 68% | 0 |
| list | 41 | 4,881 | 1.79% | 8.5 | 70% | 0 |
| co-nen | 41 | 2,824 | 2.61% | 7.7 | 71% | 0 |

## Bài 0 impression (2) — xem xét prune/merge

`app-mua-chung-chi-quy`, `hieu-ung-thang-gieng-trong-dau-tu-chung-khoan-la-gi`

## URL có impression nhưng không còn trong snapshot live (55) — kiểm tra redirect / đổi slug

| URL | Clicks | Impr | Clicks kỳ trước | Impr kỳ trước |
|---|---:|---:|---:|---:|
| `co-phieu-plx-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat` | 71 | 22101 | 79 | 17903 |
| `co-nen-mua-co-phieu-dig-hay-khong` | 171 | 17154 | 265 | 21029 |
| `co-nen-mua-co-phieu-lpb-hay-khong` | 101 | 7088 | 100 | 10764 |
| `co-nen-mua-co-phieu-mwg-hay-khong` | 31 | 6313 | 22 | 5930 |
| `co-phieu-vpb-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat` | 10 | 4927 | 18 | 1762 |
| `co-nen-mua-co-phieu-stb-hay-khong` | 18 | 2846 | 19 | 4579 |
| `tim-hieu-phuong-phap-cua-wyckoff-ve-phan-tich-thi-truong` | 21 | 2567 | 39 | 4517 |
| `co-phieu-pow-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat-2025` | 23 | 3605 | 30 | 4278 |
| `co-phieu-gas-tong-quan-danh-gia-va-ket-qua-kinh-doanh-moi-nhat` | 31 | 2285 | 35 | 3892 |
| `co-phieu-ssi-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat` | 38 | 3125 | 49 | 1816 |
| `thuc-trang-thi-truong-tai-chinh-viet-nam-hien-nay` | 0 | 0 | 155 | 3038 |
| `co-phieu-hpg-tong-quan-dinh-gia-ket-qua-kinh-doanh-moi-nhat` | 23 | 2066 | 36 | 3035 |
| `co-phieu-vib-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat` | 16 | 2989 | 34 | 1365 |
| `co-nen-mua-co-phieu-bid-hay-khong` | 10 | 2777 | 10 | 1801 |
| `co-nen-mua-co-phieu-ree-hay-khong` | 25 | 1450 | 58 | 2745 |
| `tat-ca-kien-thuc` | 0 | 2558 | 0 | 46 |
| `co-nen-mua-co-phieu-msb-hay-khong` | 14 | 2491 | 21 | 2394 |
| `co-phieu-acb-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat` | 16 | 2169 | 35 | 2271 |
| `san-otc-la-gi-tim-hieu-thi-truong-chung-khoan-phi-tap-trung` | 3 | 875 | 5 | 1532 |
| `chien-luoc-giao-dich-ket-hop-bollinger-bands-va-duong-ma` | 11 | 761 | 9 | 1146 |
| `yoy-la-gi-cach-tinh-va-y-nghia-chi-so-yoy` | 0 | 1070 | 0 | 0 |
| `danh-sach-cac-quy-etf-uy-tin-tai-viet-nam-cap-nhat` | 0 | 0 | 5 | 988 |
| `co-phieu-vjc-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat` | 6 | 350 | 15 | 986 |
| `huong-dan-cach-mua-chung-chi-quy-etf-cho-nguoi-moi-bat-dau` | 0 | 0 | 9 | 889 |
| `hoat-dong-uy-thac-dau-tu-chung-khoan-la-gi` | 0 | 334 | 1 | 825 |
| `chi-bao-bollinger-bandwidth-bbw-la-gi` | 0 | 0 | 2 | 454 |
| `yoy-la-gi-cach-tinh-y-nghia-cua-chi-so-yoy` | 0 | 382 | 0 | 0 |
| `cac-loai-lenh-trong-giao-dich-chung-khoan-tai-viet-nam` | 0 | 0 | 1 | 381 |
| `thuc-tap-so-dsc-giai-phap-thuc-tap-chung-khoan-cho-sinh-vien` | 2 | 37 | 14 | 339 |
| `cach-mua-co-phieu-msn` | 0 | 59 | 13 | 318 |
| `huong-dan-chi-tiet-giao-dich-theo-xu-huong-va-vi-du-minh-hoa` | 0 | 0 | 0 | 308 |
| `cach-mua-co-phieu-vre` | 0 | 231 | 1 | 301 |
| `cach-mua-co-phieu-vib` | 1 | 94 | 2 | 287 |
| `cac-sai-lam-dan-toi-pha-san-trong-dau-tu-chung-khoan` | 0 | 49 | 3 | 286 |
| `phan-tich-ky-thuat` | 0 | 183 | 0 | 230 |
| `cach-mua-co-phieu-pow` | 3 | 229 | 3 | 193 |
| `mua-co-phieu-o-dau-san-chung-khoan-hay-cty-chung-khoan` | 1 | 55 | 0 | 221 |
| `cach-mua-co-phieu-gas` | 2 | 62 | 4 | 206 |
| `cac-phuong-phap-dau-tu-chung-khoan-pho-bien-va-hieu-qua` | 0 | 0 | 3 | 206 |
| `quy-trinh-hoan-doi-danh-muc-etf` | 0 | 0 | 4 | 159 |
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
