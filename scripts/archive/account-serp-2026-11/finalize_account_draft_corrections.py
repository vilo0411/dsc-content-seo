from pathlib import Path
p=Path("scripts/account_serp_rollout.py");s=p.read_text(encoding="utf-8-sig")
# Raw HTML final CTA before the disclaimer, immediately after its lead-in.
s=s.replace('s.append(frag(banner(2,','s.select("p")[-1].insert_before(frag(banner(2,')
marker="# Normalize internal target behavior; preserve all original destinations."
pairs={
"Không dùng lại mật khẩu email hoặc ngân hàng.":"Không dùng lại mật khẩu ngân hàng.",
"Chọn số theo hướng dẫn và kiểm tra thông tin dịch vụ trước khi tiếp tục.":"Kiểm tra gói trước khi tiếp tục.",
"Không chụp ảnh mờ, lệch góc hay bị lóa.":"Ảnh CCCD cần rõ, không lóa.",
"Lưu bản hợp đồng để đối chiếu gói dịch vụ và biểu phí.":"Lưu hợp đồng và biểu phí.",
"Số tài khoản và mật khẩu được gửi về email hoặc tin nhắn.":"Kiểm tra email hoặc SMS cấp tài khoản.",
"Chỉ nạp tiền sau khi kiểm tra thông báo kích hoạt.":"Kiểm tra kích hoạt trước khi nạp.",
"Liên hệ DSC để xác nhận giấy tờ, địa điểm và giờ tiếp nhận trước khi đến.":"Gọi DSC xác nhận hồ sơ trước.",
"Quy trình tại quầy gồm 3 việc chính.":"Tại quầy, bạn làm 3 việc:",
"Các bước còn lại giống trên ứng dụng.":"Làm theo hướng dẫn trên ứng dụng.",
"Có tài khoản rồi, bạn đăng nhập App DSC Trading để đặt lệnh.":"Đăng nhập App DSC Trading.",
"Hãy kiểm tra giá và khối lượng trước khi xác nhận.":"Kiểm tra giá và khối lượng lệnh.",
"Mức phí phải khớp gói dịch vụ của bạn.":"Đối chiếu phí của đúng gói.",
"Về bản chất, tài khoản vẫn được mở tại công ty chứng khoán.":"Tài khoản thuộc công ty chứng khoán.",
"Đăng ký tài khoản không tự tạo ra lệnh mua bán.":"Đăng ký không tự tạo giao dịch.",
"Hồ sơ cho tổ chức hoặc nhà đầu tư nước ngoài cần được công ty kiểm tra trước.":"DSC kiểm tra hồ sơ đặc thù trước.",
"Hãy hoàn tất xác thực danh tính và hợp đồng, rồi kiểm tra thông báo kích hoạt tài khoản.":"Hoàn tất eKYC rồi kiểm tra kích hoạt.",
"Thị trường hiện có 2 phương thức xác thực phổ biến.":"Bạn cần hoàn tất eKYC trước khi giao dịch.",
"Giao diện ở công ty khác có thể khác, nhưng thứ tự các bước giống nhau.":"Tên nút có thể khác giữa các ứng dụng.",
}
insertion='''# Clarity pass: shorten action checkpoints while retaining facts and source links.
plain=str(s)
for before,after in '''+repr(pairs)+'''.items():
 plain=plain.replace(before,after)
s=BeautifulSoup(plain,"html.parser")
'''
s=s.replace(marker,insertion+"\n"+marker)
p.write_text(s,encoding="utf-8")
print("Final correction pass: clarity and CTA placement.")

