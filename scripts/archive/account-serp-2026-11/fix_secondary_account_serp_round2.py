from pathlib import Path
p=Path("knowledge/4-content/2-drafts/Optimize-nen-mo-tai-khoan-chung-khoan-o-dau-serp-2026-11-04.md")
s=p.read_text(encoding="utf-8")
s=s.replace("Khi so [phí giao dịch chứng khoán]","So đúng kênh đặt lệnh.\n\nKhi so [phí giao dịch chứng khoán]")
s=s.replace("Hãy so cùng điều kiện.","So đúng loại tài khoản.")
s=s.replace("| Trên 500 triệu đồng | 0,15% |\n","| Trên 500 triệu đồng | 0,15% |\n\nTháng 11/2026: [biểu giá có chuyên viên tư vấn của SSI](https://www.ssi.com.vn/khach-hang-ca-nhan/bieu-phi/bieu-gia-dich-vu-giao-dich-chung-khoan) công bố phí online 0,25% cho giao dịch dưới 100 triệu đồng/ngày.\n\nVới cùng giá trị giao dịch 10 triệu đồng, mức 0,25% tương ứng 25.000 đồng. So với mức 0,3%, chênh lệch là 5.000 đồng cho giao dịch này. Ví dụ chỉ so phí đặt lệnh.\n")
s=s.replace("Nếu đã sử dụng Vietcombank, hãy kiểm tra tiện ích liên kết phù hợp với nhu cầu của bạn.","Nếu đã sử dụng Vietcombank, hãy kiểm tra tính năng nộp tiền chứng khoán trên VCB Digibank.")
# Specific list breaks a long advice run without inventing visual data.
s=s.replace("Trước khi đăng ký, kiểm tra ưu đãi có thời hạn hay không và chi phí sau khi ưu đãi kết thúc.","Trước khi đăng ký, hãy kiểm tra hai điều kiện.\n\n- Thời hạn của ưu đãi phí đang được quảng bá.\n- Biểu phí áp dụng sau khi ưu đãi kết thúc.")
p.write_text(s,encoding="utf-8");print(p)

