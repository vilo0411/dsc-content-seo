from pathlib import Path
p=Path("scripts/account_serp_rollout.py")
s=p.read_text(encoding="utf-8-sig")
old=s[s.index("def md(h):"):s.index('original_title=')]
new='''def md(h):
 soup=BeautifulSoup(h,"html.parser")
 saved={}
 for i,div in enumerate(list(soup.select("div[style]"))):
  if div.find_parent("div") is not None: continue
  token=f"DSCRAWBANNER{i}TOKEN"
  saved[token]=str(div)
  div.replace_with(soup.new_string("\\\\n\\\\n"+token+"\\\\n\\\\n"))
 out=markdownify(str(soup),heading_style="ATX",bullets="*")
 for token,value in saved.items():
  out=out.replace(token,"\\\\n\\\\n"+value+"\\\\n\\\\n")
 out=re.sub(r"(?m)^(#{1,4}) \\\\*\\\\*(.*?)\\\\*\\\\*\\\\s*$",r"\\\\1 \\\\2",out)
 out=re.sub(r"\\\\*\\\\*([^*\\\\n]+):\\\\*\\\\*",r"**\\\\1**:",out)
 return re.sub(r"\\\\n{3,}","\\\\n\\\\n",out).strip()+"\\\\n"
'''
# new source must contain Python escape sequences, not double escaped literals.
new=new.replace("\\\\","\\")
s=s.replace(old,new)
marker="# Two real HTML CRO blocks; no fabricated UI screenshots."
addition='''# Add verified operational checkpoints and fee conditions, not unrelated market statistics.
p=next(p for p in s.select("p") if p.get_text(" ",strip=True).startswith("Trước khi tải ứng dụng"))
insert_after(p,"""<p><a href="https://www.dsc.com.vn/bieu-phi">Biểu phí DSC</a> áp dụng từ 20/08/2025 phân biệt nhóm phí 0,1% và tài khoản do Môi giới quản lý. Với Môi giới, giao dịch dưới 100 triệu đồng/ngày áp dụng 0,3%; hãy xác nhận nhóm tài khoản trước khi ký.</p><p>Ví dụ minh họa, một lệnh khớp 10 triệu đồng chịu phí 10.000 đồng ở mức 0,1%, hoặc 30.000 đồng ở mức 0,3%. Hai mức thuộc điều kiện dịch vụ khác nhau, không phải lựa chọn phí cho mọi tài khoản.</p>""")
p=next(p for p in s.select("p") if p.get_text(" ",strip=True).startswith("Mở ứng dụng chính thức"))
insert_after(p,"""<p>Form đăng ký trên website DSC yêu cầu mật khẩu tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt. Không dùng lại mật khẩu email hoặc ngân hàng.</p>""")
replace_p("Sau khi ký, kiểm tra email xác nhận","<p>Sau khi ký bằng OTP, kiểm tra email xác nhận và yêu cầu hồ sơ bổ sung của công ty chứng khoán. Lưu bản hợp đồng để đối chiếu gói dịch vụ và biểu phí.</p>")
replace_p("Hoàn tất form đăng ký chưa đồng nghĩa","<p>Form DSC tách điền thông tin, xác thực OTP và chọn số tài khoản; bước eKYC và hợp đồng vẫn cần hoàn tất. Chỉ nạp tiền sau khi kiểm tra thông báo kích hoạt.</p>")
replace_p("Trên App DSC Trading, bạn làm đúng 5 bước","<p>Trên App DSC Trading, bạn thực hiện 5 bước đã minh họa phía trên. Tài khoản DSC có dạng 024Cxxxxxx; chọn tiểu khoản đuôi 1 để giao dịch bằng tiền của bạn, không vay ký quỹ.</p>")
p=next(p for p in s.select("p") if p.get_text(" ",strip=True).startswith("Người mới nên dùng tiểu khoản đuôi 1"))
# Break a long prose run with a useful checkpoint list rather than filler.
p.replace_with(frag("<p>Với DSC, hãy xác nhận 3 nội dung trước khi sử dụng dịch vụ:</p><ul><li><strong>Tài khoản:</strong> Kiểm tra trạng thái eKYC và hợp đồng.</li><li><strong>Chi phí:</strong> Đối chiếu nhóm tài khoản trong biểu phí.</li><li><strong>Hỗ trợ:</strong> Xác nhận Môi giới 1:1 hỗ trợ tư vấn đầu tư theo gói đăng ký.</li></ul>"))
p=next(p for p in s.select("p") if p.get_text(" ",strip=True).startswith("Tiểu khoản ký quỹ chỉ là"))
set_text(p,"")
p.append(frag('Tiểu khoản đuôi 6 dùng cho giao dịch ký quỹ; xem <a href="https://www.dsc.com.vn/kien-thuc/cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam">các loại tài khoản chứng khoán</a> trước khi lựa chọn. Với DSC, bạn đăng ký eKYC online và hỏi về gói hỗ trợ trước lệnh đầu tiên.'))
# Keep FAQ answer cohesive; don't scatter standalone closing fragments.
replace_p("Nơi phù hợp phụ thuộc việc bạn tự giao dịch","<p>Nơi phù hợp phụ thuộc việc bạn tự giao dịch hay cần Môi giới 1:1 hỗ trợ tư vấn. So cùng gói dịch vụ và điều kiện phí trong bài <a href="https://www.dsc.com.vn/kien-thuc/nen-mo-tai-khoan-chung-khoan-o-dau">nên mở tài khoản chứng khoán ở đâu</a>.</p>")
'''
s=s.replace(marker,addition+"\n"+marker)
p.write_text(s,encoding="utf-8")
print("Updated generator: raw CTA preservation and verified operational detail.")

