from pathlib import Path
p=Path("scripts/rewrite_account_guide_v2.py")
s=p.read_text(encoding="utf-8-sig")
s=s.replace('Các ảnh dưới đây minh họa thao tác tại DSC; tên nút và cách bố trí có thể thay đổi theo phiên bản ứng dụng.','Ảnh dưới đây được giữ từ hướng dẫn trên hệ thống đăng ký DSC. Khi thực hiện trên App, bạn làm theo các yêu cầu đang hiển thị vì giao diện có thể khác.')
s=s.replace('<p><strong>Bước 3: Chọn số tài khoản.</strong> Lựa chọn theo hướng dẫn của ứng dụng và kiểm tra thông tin đã khai báo. Nếu có mã nhân viên hỗ trợ, bạn nhập đúng mã ở mục tương ứng.</p>','<p><strong>Bước 3: Kiểm tra thông tin đăng ký.</strong> Rà lại họ tên, số giấy tờ và thông tin liên hệ. Nếu hệ thống hiển thị mục chọn số tài khoản hoặc mã nhân viên hỗ trợ, bạn điền theo nhu cầu.</p>')
ccq='Với chứng chỉ quỹ mở, bạn nên xem riêng <a href="https://www.dsc.com.vn/kien-thuc/huong-dan-mo-tai-khoan-chung-chi-quy">hướng dẫn mở tài khoản chứng chỉ quỹ</a> vì quy trình có thể khác tài khoản giao dịch cổ phiếu.'
s=s.replace(' '+ccq,'')
needle='Khi đăng ký, cần phân biệt <a href="https://www.dsc.com.vn/kien-thuc/cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam">các loại tài khoản chứng khoán</a> để chọn đúng dịch vụ.</p>'
s=s.replace(needle,needle+'<p>'+ccq+'</p>')
s=s.replace(' Bạn không cần nắm hết kiến thức mới bắt đầu tìm hiểu, nhưng cần hiểu khoản phí và rủi ro của dịch vụ mình sử dụng.','')
p.write_text(s,encoding="utf-8")
print("Reader-review corrections applied.")

