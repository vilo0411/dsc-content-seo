# Gỡ số liệu rập khuôn “13,66 triệu tài khoản” — kế hoạch sửa CMS (2026-11-04)

Câu “Tính đến tháng 8/2026… 13,66 triệu tài khoản (VSDC)” bị chèn vào 14 bài live, phần lớn không liên quan tới chủ đề, và số đã cũ.
Nguồn: `anti-ai-rules.md` §S3 cũ liệt kê số này là mỏ neo chuẩn. Đã sửa §S3 và thêm check `DATA-boilerplate` vào `qa_lint.py`.

**Cách dùng:** mở bài trên CMS → tìm đoạn **Trước** (Ctrl+F theo vài chữ đầu) → thay bằng **Sau** → lưu → tick ô. Xong hết thì chạy `python scripts/sync_live.py --only <slug,…>` rồi `grep -rl "13,66 triệu" knowledge/raw/live/html` để kiểm tra.
File `Final-*.md` tương ứng đã được sửa sẵn trong repo.

- [ ] **cach-mo-tai-khoan-chung-khoan** — không sửa tay; bản Optimize `-serp-2026-11-04` đã bỏ câu này, sẽ thay khi `/approve` + publish.

## 1. cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam

- [ ] URL: https://www.dsc.com.vn/kien-thuc/cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam
- Vị trí: Sapo (đoạn 1) + YAML Sapo

**Trước:**

> là bước chân đầu tiên bắt buộc để tham gia thị trường tài chính. Tính đến tháng 9/2026, Việt Nam đã có gần 13,66 triệu tài khoản chứng khoán được đăng ký (theo VSDC). Tuy nhiên, nhiều

**Sau:**

> là bước bắt buộc để tham gia thị trường tài chính. Nhiều

## 2. chi-so-p-s-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/chi-so-p-s-la-gi
- Vị trí: Sapo (đoạn 1)

**Trước:**

> Tính đến tháng 8/2026, tổng số tài khoản chứng khoán toàn thị trường đạt gần 13,66 triệu tài khoản theo số liệu từ VSDC. Thanh khoản khớp lệnh bình quân trên sàn HOSE dao động quanh mức 15.000 tỷ đồng/phiên và VN-Index tích lũy quanh vùng 1.700 – 1.735 điểm.

**Sau:**

> Chỉ số P/S (Price to Sales) bằng vốn hóa thị trường chia doanh thu thuần 12 tháng gần nhất. P/S bằng 2 nghĩa là nhà đầu tư trả 2 đồng cho mỗi đồng doanh thu của doanh nghiệp.

## 3. co-phieu-penny-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/co-phieu-penny-la-gi
- Vị trí: Đoạn 2 sau định nghĩa

**Trước:**

> Tính đến tháng 8/2026, toàn thị trường chứng khoán Việt Nam có hơn 13,66 triệu tài khoản nhà đầu tư cá nhân theo dữ liệu VSDC. Nhiều nhà đầu tư mới (F0) lựa chọn nhóm penny vì rào cản vốn thấp.

**Sau:**

> Nhiều nhà đầu tư mới (F0) chọn nhóm penny vì rào cản vốn thấp: ở giá 5.000 đồng, một lô 100 cổ phiếu chỉ cần 500.000 đồng.

## 4. fomo-trong-dau-tu-chung-khoan-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/fomo-trong-dau-tu-chung-khoan-la-gi
- Vị trí: Đoạn ngay trước dòng Xem thêm đầu tiên

**Trước:**

> Tính đến tháng 8/2026, VSDC ghi nhận toàn thị trường có hơn 13,66 triệu tài khoản chứng khoán cá nhân.

**Sau:**

> _(xóa câu/đoạn trên, giữ phần còn lại)_

## 5. luu-ky-chung-khoan-moi-dieu-ban-can-biet

- [ ] URL: https://www.dsc.com.vn/kien-thuc/luu-ky-chung-khoan-moi-dieu-ban-can-biet
- Vị trí: Đoạn 2 sau định nghĩa lưu ký

**Trước:**

> Tính đến tháng 8/2026, VSDC đang quản lý dữ liệu lưu ký cho hơn 13,66 triệu tài khoản chứng khoán trên toàn thị trường Việt Nam. Trong đó, nhà đầu tư cá nhân trong nước chiếm tới 13,58 triệu tài khoản. Điều này chứng minh toàn bộ hạ tầng giao dịch hiện đại đều vận hành hoàn toàn dựa trên nền tảng lưu ký điện tử tập trung.

**Sau:**

> Theo Luật Chứng khoán 2019, VSDC thực hiện đăng ký, lưu ký, bù trừ và thanh toán chứng khoán. Cổ phiếu bạn mua qua bất kỳ công ty chứng khoán nào cũng được ghi nhận tại VSDC, đứng tên chính bạn.

## 6. no-xau-trong-cac-co-phieu-ngan-hang-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/no-xau-trong-cac-co-phieu-ngan-hang-la-gi
- Vị trí: Đoạn ngay trước dòng Xem thêm đầu tiên

**Trước:**

> Tính đến tháng 8/2026, toàn thị trường chứng khoán Việt Nam ghi nhận gần 13,66 triệu tài khoản giao dịch theo dữ liệu VSDC. Cổ phiếu ngân hàng chiếm tỷ trọng vốn hóa lớn nhất sàn VN-Index.

**Sau:**

> Cổ phiếu ngân hàng là nhóm ngành chiếm tỷ trọng vốn hóa lớn nhất trong VN-Index.

## 7. phan-biet-co-phieu-va-trai-phieu

- [ ] URL: https://www.dsc.com.vn/kien-thuc/phan-biet-co-phieu-va-trai-phieu
- Vị trí: Đoạn ngay sau bảng so sánh, trước H2 Ưu và nhược điểm

**Trước:**

> Tính đến tháng 8/2026, toàn thị trường chứng khoán Việt Nam ghi nhận 13,66 triệu tài khoản nhà đầu tư cá nhân theo VSDC. Sự phát triển hạ tầng giúp nhà đầu tư dễ dàng giao dịch cả hai lớp tài sản này.

**Sau:**

> Với cùng một tài khoản chứng khoán, nhà đầu tư giao dịch được cả cổ phiếu và trái phiếu niêm yết. Trái phiếu doanh nghiệp phát hành riêng lẻ giao dịch trên hệ thống riêng của HNX, chỉ dành cho nhà đầu tư chuyên nghiệp.

## 8. pivot-points-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/pivot-points-la-gi
- Vị trí: Sapo (đoạn 1)

**Trước:**

> Tính đến tháng 8/2026, thị trường chứng khoán Việt Nam ghi nhận gần 13,66 triệu tài khoản nhà đầu tư theo số liệu từ VSDC. Với thanh khoản bình quân duy trì quanh mốc 15.000 tỷ đồng/phiên trên sàn HOSE, VN-Index liên tục có những nhịp biến động phức tạp quanh vùng 1.700–1.735 điểm.

**Sau:**

> Pivot Points là chỉ báo tính các mức hỗ trợ, kháng cự trong phiên từ giá cao nhất, thấp nhất và giá đóng cửa của phiên trước. Điểm xoay P = (Cao + Thấp + Đóng cửa) / 3.
>
> Phiên 3/11/2026, VN-Index đạt cao nhất 1.713,02, thấp nhất 1.689,32 và đóng cửa 1.699,62 điểm. Điểm xoay cho phiên 4/11/2026 vì vậy là 1.700,65 điểm.

## 9. thi-truong-tai-chinh-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/thi-truong-tai-chinh-la-gi
- Vị trí: Đầu H2 Vai trò của thị trường tài chính

**Trước:**

> Năm 2026, quy mô thị trường vốn Việt Nam mở rộng với hơn 13,66 triệu tài khoản chứng khoán cá nhân (theo dữ liệu VSDC). Thị trường tài chính mang lại vai trò to lớn trên hai góc độ.

**Sau:**

> Thị trường tài chính có vai trò trên hai góc độ: với nền kinh tế vĩ mô và với từng nhà đầu tư. Doanh nghiệp Việt Nam huy động vốn dài hạn qua cổ phiếu, trái phiếu niêm yết trên 3 sàn HOSE, HNX và UPCoM.

## 10. rui-ro-va-loi-ich-khi-tham-gia-thi-truong-tai-chinh

- [ ] URL: https://www.dsc.com.vn/kien-thuc/rui-ro-va-loi-ich-khi-tham-gia-thi-truong-tai-chinh
- Vị trí: Đầu H2 Vai trò của thị trường tài chính (không có file Final)

**Trước:**

> Năm 2026, quy mô thị trường vốn Việt Nam mở rộng với hơn 13,66 triệu tài khoản chứng khoán cá nhân (theo dữ liệu VSDC). Thị trường tài chính mang lại vai trò to lớn trên hai góc độ.

**Sau:**

> Thị trường tài chính có vai trò trên hai góc độ: với nền kinh tế vĩ mô và với từng nhà đầu tư. Doanh nghiệp Việt Nam huy động vốn dài hạn qua cổ phiếu, trái phiếu niêm yết trên 3 sàn HOSE, HNX và UPCoM.

## 11. san-giao-dich-chung-khoan-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/san-giao-dich-chung-khoan-la-gi
- Vị trí: Sapo (đoạn 2)

**Trước:**

> Tính đến tháng 8/2026, thị trường ghi nhận gần 13,66 triệu tài khoản chứng khoán theo số liệu chính thức từ VSDC.

**Sau:**

> Mỗi sàn có biên độ giá riêng: HOSE 7%, HNX 10%, UPCoM 15%.

## 12. so-sanh-dau-tu-co-phieu-va-dau-tu-chung-chi-quy

- [ ] URL: https://www.dsc.com.vn/kien-thuc/so-sanh-dau-tu-co-phieu-va-dau-tu-chung-chi-quy
- Vị trí: Đoạn ngay trước H2 Phân biệt Quỹ mở và Quỹ ETF — xóa cả đoạn

**Trước:**

> Theo dữ liệu VSDC, tính đến tháng 9/2026, toàn thị trường đạt hơn 13,66 triệu tài khoản chứng khoán. Dòng tiền cá nhân đang dịch chuyển mạnh mẽ vào thị trường chứng khoán để tìm kiếm lợi nhuận.

**Sau:**

> _(xóa câu/đoạn trên, giữ phần còn lại)_

## 13. von-luu-dong-la-gi

- [ ] URL: https://www.dsc.com.vn/kien-thuc/von-luu-dong-la-gi
- Vị trí: Đoạn ngay trước H2 Công thức tính

**Trước:**

> Tính đến tháng 8/2026, toàn thị trường có hơn 13,66 triệu tài khoản chứng khoán niêm yết.

**Sau:**

> _(xóa câu/đoạn trên, giữ phần còn lại)_

## Ghi chú

- `thi-truong-tai-chinh-la-gi` và `rui-ro-va-loi-ich-khi-tham-gia-thi-truong-tai-chinh` có H2 “Vai trò của thị trường tài chính…” giống hệt nhau — nghi trùng nội dung giữa 2 URL, nên kiểm tra riêng.
- Hai số đi kèm trong §S3 cũ (15.000 tỷ đồng/phiên, VN-Index 1.700–1.735) cũng đã lặp ở 4 và 2 bài live; 2 sapo chứa chúng (chi-so-p-s, pivot-points) đã được thay ở trên.
- Ví dụ pivot dùng phiên VN-Index 03/11/2026 (cao 1.713,02 · thấp 1.689,32 · đóng 1.699,62 → P = 1.700,65), nguồn `market_facts.py`.
