"""Prepare account-opening SERP implementation draft; never publish or overwrite Final."""
import json,re,hashlib,sys,urllib.request,difflib
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify
sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[1]
slug="cach-mo-tai-khoan-chung-khoan"
base=ROOT/"knowledge/4-content/audits/account-serp-2026-11-04"
base.mkdir(parents=True,exist_ok=True)
live=ROOT/"knowledge/raw/live/html"/(slug+".html")
raw=live.read_text(encoding="utf-8")
s=BeautifulSoup(raw,"html.parser")
title="Cách mở tài khoản chứng khoán online: Hồ sơ và 5 bước"
meta="Cách mở tài khoản chứng khoán online qua 5 bước, kèm ảnh thao tác DSC, giấy tờ cần có và cách xử lý lỗi eKYC. Chuẩn bị hồ sơ trước khi bắt đầu đăng ký."
assert len(title)<=59 and 140<=len(meta)<=160,(len(title),len(meta))
url="https://www.dsc.com.vn/kien-thuc/"+slug
def fm(t,m):
 return f"---\nTitle: {t}\nMeta_Description: {m}\nTarget_Keyword: cách mở tài khoản chứng khoán\nKeyword: cách mở tài khoản chứng khoán\nSlug: {slug}\nPersona: P2\nDate: 2026-11-04\nSource_URL: {url}\nStatus: Optimizing\n---\n\n"
def md(h):
 soup=BeautifulSoup(h,"html.parser")
 saved={}
 for i,div in enumerate(list(soup.select("div[style]"))):
  if div.find_parent("div") is not None: continue
  token=f"DSCRAWBANNER{i}TOKEN"
  saved[token]=str(div)
  div.replace_with(soup.new_string("\n\n"+token+"\n\n"))
 out=markdownify(str(soup),heading_style="ATX",bullets="*")
 for token,value in saved.items():
  out=out.replace(token,"\n\n"+value+"\n\n")
 out=re.sub(r"(?m)^(#{1,4}) \*\*(.*?)\*\*\s*$",r"\1 \2",out)
 out=re.sub(r"\*\*([^*\n]+):\*\*",r"**\1**:",out)
 return re.sub(r"\n{3,}","\n\n",out).strip()+"\n"
original_title="Cách mở tài khoản chứng khoán online 3 phút cho người mới"
original_meta="Hướng dẫn cách mở tài khoản chứng khoán online eKYC và tại quầy nhanh chóng. Khám phá điều kiện, hồ sơ cần chuẩn bị và ưu đãi từ DSC trong bài viết hôm nay"
baseline=base/("baseline-"+slug+".md")
if not baseline.exists():
 baseline.write_text(fm(original_title,original_meta)+"# "+original_title+"\n\n"+md(raw),encoding="utf-8")
(base/("baseline-"+slug+".body.html")).write_text(raw,encoding="utf-8")
images=[str(i) for i in s.select("img")]
hrefs={a["href"] for a in s.select("a[href]")}
# Proposal is written before applying edits; the existing old proposal/drafts remain untouched.
proposal=ROOT/"knowledge/4-content/1-outlines"/("Proposal-"+slug+"-serp-2026-11-04.md")
image_rows="\n".join("| "+str(i+1)+" | "+e.get("src","")+" | "+e.get("alt","")+" | Giữ nguồn và thứ tự trong cụm thao tác |" for i,e in enumerate(s.select("img")))
proposal_text=f"""---
Title: Proposal tối ưu cụm mở tài khoản chứng khoán
Target_Keyword: cách mở tài khoản chứng khoán
Persona: P2
Status: Execution authorized in chat; draft pending final approval
Date: 2026-11-04
PAA_Questions:
  - q: Mở tài khoản chứng khoán ở đâu là tốt nhất?
    placement: faq
  - q: Mở tài khoản chứng khoán có bị gì không?
    placement: faq
  - q: Quy định về mở tài khoản chứng khoán là gì?
    placement: faq
---

# Proposal — {slug}

## 0. Content strategy header

| Thuộc tính | Khai báo |
| --- | --- |
| Target keyword | cách mở tài khoản chứng khoán |
| Secondary keywords | mở tài khoản chứng khoán; mở tài khoản chứng khoán online; tạo tài khoản chứng khoán |
| Search intent | Informational/how-to: chuẩn bị, thực hiện, kiểm tra kết quả đăng ký; có lối đi tới đăng ký DSC |
| Persona | P2 — người mới cần biết giấy tờ, thao tác và lỗi trước khi đặt lệnh |
| Product bridge | App DSC Trading/eKYC và Môi giới 1:1 theo dịch vụ đăng ký; không hứa mức phí 0,1% kèm môi giới cho mọi tài khoản |
| URL | Giữ nguyên {url} |
| Word count | Nền live khoảng 2.805 từ; không tăng độ dài để bắt chước đối thủ; ưu tiên bỏ thông tin lạc nhu cầu |

Bản live giống Final chỉ 57% theo sync_live --compare, nên dùng live làm nền. Không ghi đè Final hoặc draft cũ. Người dùng đã yêu cầu lập kế hoạch và triển khai; tự chốt proposal trong phạm vi sửa nháp. Chưa publish.

## 1. Đánh giá tổng quan

Ảnh SERP người dùng cung cấp: bài hướng dẫn VFS #7 cho cách mở và #8 cho mở tài khoản; DSC chưa hiện trang 1 trong ảnh. Ảnh không phải lịch sử thứ hạng. Snapshot DataForSEO khác kết quả người dùng, chỉ dùng làm đối chiếu bổ sung.

GSC 05/10–01/11/2026, Việt Nam, exact query mở tài khoản chứng khoán: bài này 97 impressions, position 41,55; bài lựa chọn 161 impressions, position 17,06. Chưa kết luận cannibalization gây hại. Các số này đi trước snapshot nội dung 03/11.

Title hiện tại: {original_title}.
Title đề xuất: {title} ({len(title)} ký tự).
Meta hiện tại: {original_meta}.
Meta đề xuất: {meta} ({len(meta)} ký tự).

HTTP 200, canonical tự trỏ, nội dung bài hiện trong HTML server trả về; chưa có bằng chứng từ URL Inspection để xác nhận Google-selected canonical/index verdict. Meta robots không thấy noindex. Không đổi URL, redirect, canonical hay schema để ép chọn bài.

## 2. Phân tích đối thủ

### 2.1 Bảng đối chiếu

| Nguồn | Dạng trang | Quan sát | Áp dụng |
| --- | --- | --- | --- |
| VFS — lam-the-nao-de-mo-tai-khoan-chung-khoan-online-mien-phi | Hướng dẫn | Chọn công ty, 5 bước, nạp tiền, làm tại VFS | Cho người đọc lựa chọn nhanh mà không biến bài thành bảng xếp hạng |
| SSI — mo-tai-khoan | Dịch vụ/đăng ký | Đường đi đăng ký và lợi ích | Liên kết hành động đúng đích; không dùng copy sản phẩm đối thủ |
| VCBS — kết quả hỗ trợ trong ảnh | Hỗ trợ giao dịch | Nhiều kênh mở tài khoản | Nêu phạm vi App/Web/Quầy, không cam kết mọi công ty có cùng quy trình |
| VPBankS — huong-dan-mo-tai-khoan | Hướng dẫn | Từng bước và điều kiện | Thêm dấu hiệu hoàn tất mỗi bước; DSC đã có ảnh thật |

### 2.2 Cấu trúc từng đối thủ

#### VFS
URL: https://www.vfs.com.vn/lam-the-nao-de-mo-tai-khoan-chung-khoan-online-mien-phi
H1: Làm thế nào để mở tài khoản chứng khoán online miễn phí? Hướng dẫn CHI TIẾT A-Z.
H2: Chọn công ty chứng khoán uy tín; các bước mở online tại nhà; nạp tiền và giao dịch; hướng dẫn thực tế tại VFS.
H3: Tiêu chí, danh sách công ty; truy cập/tải app; đăng ký; eKYC; ký hợp đồng; nhận tài khoản; chuẩn bị và làm tại VFS.
Gap: DSC đã có ảnh và xử lý lỗi; cần đưa bước thực hiện lên sớm, bỏ số thị trường trước quy trình.

#### SSI
Nguồn ảnh SERP: https://www.ssi.com.vn/mo-tai-khoan
Dạng: landing mở tài khoản và lời hứa thao tác nhanh; chưa suy diễn outline đầy đủ nếu chưa extract đúng URL.
Gap: làm rõ bước tiếp theo khi đọc xong; không khẳng định SSI thắng do landing page.
Các đối thủ đã extract trong API ở lượt trước nằm trong serp-dsc-comparison-2026-11-04.html; API snapshot không tái hiện ảnh nên không dùng làm bảng xếp hạng chuẩn.

#### VCBS
Trong ảnh có trang hỗ trợ Mở tài khoản giao dịch chứng khoán; chưa xác định URL đầy đủ từ breadcrumb bị cắt. Nguồn vận hành bổ sung: https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Dau-tu/Giao-dich-Chung-khoan.
Các mục xác nhận: mở trực tuyến; qua VCB Digibank; tại quầy. Không bịa cấu trúc heading của URL chưa xác định.
Gap: phân biệt kênh và điều kiện thiết bị.

#### VPBankS
Trong ảnh có bài hướng dẫn; chưa xác định URL đầy đủ từ breadcrumb. Không dùng bài app từ API thay thế bài hướng dẫn.
Gap: đối chiếu dấu hiệu hoàn tất từng bước, không bịa heading khi chưa lấy đúng bài.

### 2.3 Intent gap
H2 đầu của live là quy định và ba H3 pháp lý, đặt trước thao tác. Cập nhật bằng tóm tắt chuẩn bị ở đầu, đưa 5 bước lên trước phần quy định chi tiết. Bước chọn công ty chỉ có bảng câu hỏi kiểm tra ngắn, giữ bài so sánh riêng.

## 3. Seven sweeps audit

| Sweep | Vấn đề | Xử lý |
| --- | --- | --- |
| Clarity | Lặp quy trình chung và DSC; ảnh có alt tên file | Phạm vi từng phần rõ; giữ ảnh gốc, chú thích không bịa ảnh chụp mới |
| Voice | Câu hỏi mồi ở xử lý lỗi | Viết thao tác khách quan |
| So what | Số tài khoản toàn thị trường đứng trước bước làm | Bỏ vì không giúp hoàn tất đăng ký |
| Prove it | Cam kết mọi OTP, mọi thời gian kích hoạt, địa chỉ cũ | Nói theo hướng dẫn màn hình; nguồn chính thức; bỏ mốc không kiểm chứng |
| Specificity | Điều kiện NFC áp dụng cả thị trường | Nêu riêng quy trình DSC; công ty khác tùy phương thức xác thực |
| Emotion | Trấn an bằng cam kết | Giải thích tự kiểm tra và nơi hỗ trợ |
| Zero risk | Miễn phí đồng nghĩa không phát sinh phí | Phân biệt phí mở, giao dịch/lưu ký và phí dịch vụ |
| GEO/AEO | FAQ chưa bao phủ câu hỏi trong ảnh | Bổ sung 3 câu có trả lời trực tiếp, không hứa xuất hiện AI Overview |

## 4. Heading-by-heading

[GIỮ NGUYÊN] Slug, 5 bước và ảnh theo thứ tự; H2 6 lỗi; H2 việc sau mở; các link body live.
[CẬP NHẬT] Sapo, title/meta; bỏ mốc số tài khoản; sửa lời hứa OTP/kích hoạt/miễn phí; phân biệt lô chẵn và lô lẻ.
[CẬP NHẬT] H2 quy định: đặt sau phần thao tác, thu gọn phần điều kiện đặc thù, không khẳng định DSC nhận mọi đối tượng.
[CẬP NHẬT] Phần tại quầy: mô tả thao tác thực tế, bỏ bảng thời gian không nguồn và danh sách địa chỉ chưa đối chiếu.
[THÊM MỚI] Bảng 3 câu hỏi trước khi chọn công ty; học từ H2 tiêu chí của VFS; dẫn bài lựa chọn.
[THÊM MỚI] Dấu hiệu hoàn tất từng bước; dựa trên form đăng ký DSC và ảnh live.
[THÊM MỚI] Ba FAQ trong PAA ảnh người dùng.
[XÓA BỎ] Số thị trường trước quy trình; lời hứa khớp lệnh mọi OTP SMS, kích hoạt tức thì và máy nào cũng cần NFC.

## 5. Content gaps và bằng chứng

Bảng chọn công ty học từ VFS, nhưng không lặp Top 7; gồm kiểm tra kênh chính thức, loại dịch vụ và điều kiện phí. Thêm bảng so sánh cùng giá trị giao dịch ở bài lựa chọn, không đưa số đối thủ vào bài này.

FAQ lấy từ ảnh SERP người dùng, không phải DataForSEO (API không trả PAA). Câu Có được phép mở tài khoản chứng khoán không được bao phủ ở mục độ tuổi; không thêm FAQ trùng.
Nguồn DSC: https://www.dsc.com.vn/mo-tai-khoan ; https://www.dsc.com.vn/bieu-phi ; https://www.dsc.com.vn/dich-vu/mo-tai-khoan .
Không thêm người kiểm duyệt hoặc trải nghiệm thực tế do agent tự bịa.

## 6. Internal link strategy

Giữ toàn bộ href body live, gồm 6 link đã thêm trên CMS. Anchor hướng dẫn tới bài này; anchor lựa chọn tới nen-mo-tai-khoan-chung-khoan-o-dau; CTA có DSC tới /mo-tai-khoan. Không backfill hàng loạt vì đã có 53 nguồn body.
Gợi ý backfill từ find_links được lưu làm tham khảo, chưa triển khai vì chưa có thiếu hụt nguồn dẫn được chứng minh.

## 7. Hình ảnh và CTA

### 7.1 Ảnh live cần bảo toàn
| # | URL ảnh | Alt hiện tại | Xử lý |
| --- | --- | --- | --- |
{image_rows}

### 7.2 Visual bổ sung
Giữ 6 ảnh thao tác thật; thêm bảng checkpoint HTML cho đọc lướt. Không tạo ảnh AI mô phỏng giao diện vì sẽ gây hiểu nhầm về thao tác thật. Vị trí ảnh mới nếu cần ở vòng sau: màn hình báo hoàn tất eKYC từ giao diện DSC đã được xác nhận; không chèn placeholder vào bài.
Hai banner P2 theo template CRO, sau 25% thân bài và cách nhau hơn 300 từ; copy không hứa lợi nhuận, không gán 0,1% cho mọi dịch vụ.
"""
proposal.write_text(proposal_text,encoding="utf-8")
def frag(h):return BeautifulSoup(h,"html.parser")
def replace_p(prefix,h):
 node=next((p for p in s.select("p") if p.get_text(" ",strip=True).startswith(prefix)),None)
 if not node:raise ValueError("Missing paragraph: "+prefix)
 node.replace_with(frag(h))
def insert_after(node,h):node.insert_after(frag(h))
def find_h(text):return next(h for h in s.select("h2,h3") if h.get_text(" ",strip=True)==text)
def set_text(node,text):node.clear();node.append(text)
# Execute only updates declared above.
ps=s.select("p")
ps[0].replace_with(frag("<p>Cách mở tài khoản chứng khoán online gồm 5 bước: chọn công ty, đăng ký thông tin, xác thực eKYC, ký hợp đồng và nhận tài khoản. Bạn cần giấy tờ còn hiệu lực, số điện thoại nhận OTP và tài khoản ngân hàng đứng tên mình.</p>"))
ps=s.select("p")
ps[1].replace_with(frag("<p>Hướng dẫn dưới đây kèm ảnh thao tác trên App DSC Trading, cách mở tại quầy và xử lý 6 lỗi thường gặp. Với quy trình đọc chip CCCD tại DSC, hãy chuẩn bị điện thoại hỗ trợ NFC trước khi đăng ký.</p>"))
condition=find_h("Quy định tạo tài khoản chứng khoán")
steps=find_h("Cách mở tài khoản chứng khoán online qua 5 bước")
nodes=[]
cur=condition
while cur and cur!=steps:
 nxt=cur.next_sibling;nodes.append(cur.extract());cur=nxt
counter=find_h("Cách mở tài khoản chứng khoán trực tiếp tại quầy")
for n in nodes:counter.insert_before(n)
replace_p("Tháng 8/2026, Việt Nam","<p>Quy trình mở tài khoản chứng khoán online có 5 bước chính. Tên nút và phương thức xác thực tùy công ty; phần minh họa dưới đây dùng App DSC Trading.</p>")
replace_p("Chọn công ty có giấy phép","<p>Trước khi tải ứng dụng, kiểm tra tên công ty và đường dẫn đăng ký trên website chính thức. Chỉ so phí khi đã biết tài khoản thuộc gói tự giao dịch hay có môi giới hỗ trợ tư vấn.</p>")
p=next(p for p in s.select("p") if p.get_text(" ",strip=True).startswith("Nếu còn phân vân"))
insert_after(p,"""<table><thead><tr><th>Kiểm tra trước khi mở</th><th>Bạn cần biết điều gì?</th><th>Hành động</th></tr></thead><tbody>
<tr><td>Kênh đăng ký</td><td>Website và ứng dụng có thuộc công ty chứng khoán không?</td><td>Tải từ liên kết trên website chính thức.</td></tr>
<tr><td>Gói dịch vụ</td><td>Tự đặt lệnh hay cần Môi giới 1:1 hỗ trợ tư vấn đầu tư?</td><td>Chọn gói phù hợp trước khi ký.</td></tr>
<tr><td>Chi phí sử dụng</td><td>Phí giao dịch, lưu ký và điều kiện ưu đãi áp dụng thế nào?</td><td>Đọc biểu phí của đúng gói đăng ký.</td></tr></tbody></table>""")
replace_p("Mở ứng dụng, chọn", "<p>Mở ứng dụng chính thức, chọn <strong>Mở tài khoản</strong> rồi nhập họ tên có dấu, số giấy tờ, điện thoại và email. Dùng thông tin của chính bạn để thuận tiện nhận OTP và đối chiếu hồ sơ.</p>")
replace_p("Hệ thống gửi mã OTP","<p>Nhập OTP trong thời hạn ứng dụng hiển thị. Nếu mã hết hạn, kiểm tra số điện thoại rồi yêu cầu gửi lại; không chuyển mã cho người khác.</p>")
replace_p("DSC cho phép chọn số tài khoản","<p>Form đăng ký DSC có bước chọn số tài khoản. Chọn số theo hướng dẫn và kiểm tra thông tin dịch vụ trước khi tiếp tục.</p>")
replace_p("Chứng khoán DSC xác thực bằng quét chip NFC","<p>Ảnh thao tác DSC dưới đây minh họa quy trình đọc chip CCCD bằng NFC. Bạn làm theo từng yêu cầu trên ứng dụng; thứ tự kiểm tra giấy tờ và khuôn mặt tùy phiên bản.</p>")
# Remove the unsupported market-wide NFC/VNeID comparison while preserving actual instructions.
ekh=find_h("Bước 3: Xác thực danh tính eKYC")
et=ekh.find_next("table")
if et and "Chia sẻ qua VNeID" in et.get_text():
 et.replace_with(frag("<p>NFC là tính năng đọc chip trên giấy tờ; eKYC là quy trình xác minh danh tính trực tuyến. Công ty khác có thể dùng phương thức xác thực khác, nên hãy đọc yêu cầu thiết bị trước khi đăng ký.</p>"))
for li in s.select("li"):
 if li.get_text(" ",strip=True).startswith("Đọc chip NFC:"):
  li.clear();li.append(frag("<strong>Đọc chip NFC:</strong> Đặt thẻ sát vị trí đọc chip của điện thoại và giữ yên tới khi ứng dụng báo hoàn tất."))
replace_p("Một số công ty yêu cầu gửi thêm hợp đồng giấy","<p>Sau khi ký, kiểm tra email xác nhận và các yêu cầu bổ sung của công ty chứng khoán. Lưu bản hợp đồng để đối chiếu gói dịch vụ và biểu phí khi cần.</p>")
replace_p("Thời gian kích hoạt tùy công ty","<p>Hoàn tất form đăng ký chưa đồng nghĩa đã đủ điều kiện giao dịch. Kiểm tra trạng thái eKYC, hợp đồng và thông báo kích hoạt trước khi nạp tiền.</p>")
# Conditions: target adult domestic individuals; no unsupported universal onboarding for minors/foreigners.
replace_p("Trước khi tạo tài khoản chứng khoán","<p>Hướng dẫn này dành cho nhà đầu tư cá nhân trong nước tự mở tài khoản chứng khoán. Trước khi đăng ký, kiểm tra 3 nhóm thông tin: độ tuổi, giấy tờ và số tài khoản đã mở.</p>")
replace_p("Công dân Việt Nam từ đủ 18 tuổi","<p>Người từ đủ 18 tuổi có năng lực hành vi dân sự đầy đủ được tự đăng ký tài khoản chứng khoán. Nếu chưa đủ 18 tuổi, liên hệ công ty để kiểm tra điều kiện tiếp nhận và hồ sơ của người đại diện.</p>")
replace_p("Trường hợp dưới 18 tuổi cần làm hồ sơ","<p>Nhà đầu tư nước ngoài và tổ chức có bộ hồ sơ riêng. Không dùng quy trình eKYC dành cho cá nhân trong nước để thay thế các thủ tục này.</p>")
replace_p("Nhà đầu tư cá nhân cần CCCD","<p>Với quy trình DSC minh họa trong bài, bạn chuẩn bị giấy tờ gắn chip và điện thoại hỗ trợ NFC. Kiểm tra 4 hạng mục sau trước khi bắt đầu.</p>")
for td in s.select("td"):
 if td.get_text(" ",strip=True)=="Đứng tên chính chủ":set_text(td,"Dùng số điện thoại của bạn và email đang truy cập được")
replace_p("Thông tin bạn khai báo sẽ được đối chiếu","<p>Thông tin bạn khai báo phải khớp giấy tờ dùng để xác thực. Nếu vừa đổi giấy tờ hoặc không có thiết bị phù hợp, hỏi DSC cách hoàn thiện hồ sơ trước khi đăng ký.</p>")
replace_p("Mỗi nhà đầu tư chỉ được mở 1 tài khoản","<p>Bạn được mở tài khoản tại nhiều công ty chứng khoán; từng loại tài khoản có điều kiện riêng. Chi tiết có trong bài <a href='https://www.dsc.com.vn/kien-thuc/mot-nguoi-duoc-mo-bao-nhieu-tai-khoan-chung-khoan'>một người được mở bao nhiêu tài khoản chứng khoán</a>.</p>")
replace_p("Mở tại quầy chậm hơn online","<p>Mở tài khoản tại quầy là lựa chọn khi bạn cần hỗ trợ kiểm tra hồ sơ trực tiếp. Liên hệ DSC để xác nhận giấy tờ, địa điểm và giờ tiếp nhận trước khi đến.</p>")
qh=find_h("Cách mở tài khoản chứng khoán trực tiếp tại quầy")
qt=qh.find_next("table")
if qt and "15–30" in qt.get_text():
 qt.decompose()
replace_p("Nếu chọn mở tại quầy","<p>Quy trình tại quầy gồm 3 việc chính. Hồ sơ cho tổ chức hoặc nhà đầu tư nước ngoài cần được công ty kiểm tra trước.</p>")
replace_p("Tại DSC, bạn mang CCCD gốc","<p>Đối chiếu địa chỉ và kênh hỗ trợ trên <a href='https://www.dsc.com.vn/lien-he'>trang liên hệ DSC</a> trước khi đi. Không chuyển giấy tờ hoặc tiền cho người tự nhận hỗ trợ ngoài kênh chính thức.</p>")
# Remove old branch directory rather than publish unchecked addresses.
for ul in list(s.select("ul")):
 if any(li.get_text(" ",strip=True).startswith("Trụ sở chính Hà Nội") for li in ul.select("li")):ul.decompose()
replace_p("Chứng khoán DSC cho phép mở tài khoản eKYC","<p>Chứng khoán DSC cho phép đăng ký online qua App DSC Trading hoặc website. Hãy hoàn tất xác thực danh tính và hợp đồng, rồi kiểm tra thông báo kích hoạt tài khoản.</p>")
replace_p("Người mới nên dùng tiểu khoản đuôi 1","<p>Người mới nên dùng tiểu khoản đuôi 1 trước khi tìm hiểu vay ký quỹ. Dịch vụ Môi giới 1:1 hỗ trợ tư vấn đầu tư theo gói bạn đăng ký; hãy xác nhận phí và phạm vi hỗ trợ.</p><p>Tiểu khoản ký quỹ chỉ là một trong <a href='https://www.dsc.com.vn/kien-thuc/cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam'>các loại tài khoản chứng khoán</a>. Tài khoản cho tổ chức hoặc chứng chỉ quỹ có thủ tục riêng.</p>")
replace_p("Nếu quen thao tác trên máy tính","<p>Nếu thao tác trên máy tính, bạn vào trang <a href='https://www.dsc.com.vn/mo-tai-khoan'>mở tài khoản DSC online</a> và điền thông tin đăng ký. Đến bước xác thực, làm theo hướng dẫn chuyển tiếp sang thiết bị phù hợp.</p>")
replace_p("Lỗi phổ biến nhất là điện thoại","<p>Nếu điện thoại chưa đọc được chip CCCD, kiểm tra NFC, ốp lưng và vị trí đặt thẻ trước khi thử lại. Bảng dưới đây nêu 6 tình huống và bước kiểm tra tương ứng.</p>")
for td in s.select("td"):
 if "Mượn điện thoại có NFC hoặc ra quầy" in td.get_text():set_text(td,"Dùng thiết bị hỗ trợ NFC do bạn trực tiếp thao tác, hoặc liên hệ DSC để được hướng dẫn tại quầy.")
 if td.get_text(" ",strip=True)=="Chờ dữ liệu cập nhật hoặc liên hệ công an nơi cấp thẻ":set_text(td,"Kiểm tra giấy tờ đang dùng, rồi liên hệ DSC để xác định thông tin cần bổ sung.")
replace_p("Đã thử các cách trên","<p>Nếu chưa hoàn tất sau khi kiểm tra, dừng thao tác và liên hệ DSC qua kênh chính thức. Mô tả bước đang lỗi; không gửi mật khẩu, mã PIN hoặc OTP.</p>")
# Replace unverified money-transfer formula example with in-app verified beneficiary instructions; retain structural KB identifier.
replace_p("Với tài khoản 024C123456","<p>Mã định danh 963369 là kênh nộp tiền DSC nêu trong hướng dẫn vận hành. Trước khi chuyển, sao chép thông tin thụ hưởng từ tài khoản của bạn và đối chiếu tên, số tài khoản, tiểu khoản.</p>")
replace_p("Có tiền trong tài khoản, bạn đặt lệnh","<p>Khi tiền đã về, bạn đặt lệnh trong <a href='https://www.dsc.com.vn/kien-thuc/gio-giao-dich-chung-khoan-viet-nam'>giờ giao dịch chứng khoán</a>. Lô chẵn là 100 cổ phiếu; giao dịch 1–99 cổ phiếu thực hiện theo cơ chế lô lẻ.</p><p>Các bước chọn mã và đặt lệnh có trong bài <a href='https://www.dsc.com.vn/kien-thuc/cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau'>cách mua cổ phiếu online cho người mới bắt đầu</a>. Hãy kiểm tra giá và khối lượng trước khi xác nhận.</p>")
replace_p("DSC miễn phí mở và duy trì tài khoản chứng khoán","<p>Mở tài khoản DSC không đồng nghĩa mọi dịch vụ sử dụng đều miễn phí. Phí giao dịch, lưu ký và các khoản phát sinh được công bố trong <a href='https://www.dsc.com.vn/bieu-phi'>biểu phí DSC</a>.</p><p>Phân biệt từng khoản tại bài <a href='https://www.dsc.com.vn/kien-thuc/mo-tai-khoan-chung-khoan-co-mat-phi-khong-can-bao-nhieu-tien'>mở tài khoản chứng khoán có mất phí không</a>. Mức phí phải khớp gói dịch vụ của bạn.</p>")
replace_p("Được. Bạn đăng ký online qua eKYC","<p>Bạn có thể gửi đăng ký online ngoài giờ hành chính. Thời điểm kích hoạt phụ thuộc việc hoàn tất hồ sơ và xác nhận của công ty; giao dịch tuân theo lịch của từng thị trường.</p>")
replace_p("Ngoài giờ giao dịch, lệnh còn phải đúng lô","<p>Khi đặt lệnh, kiểm tra khối lượng lô chẵn hoặc lô lẻ và biên độ giá. Các điều kiện có trong <a href='https://www.dsc.com.vn/kien-thuc/cac-quy-dinh-giao-dich-chung-khoan-quan-trong-ma-nguoi-moi-can-biet'>quy định giao dịch chứng khoán</a> của từng sàn.</p>")
replace_p("Bước tiếp theo của bạn chỉ mất 3 phút","<p>Khi đã chuẩn bị giấy tờ, bạn đăng ký tại trang <a href='https://www.dsc.com.vn/mo-tai-khoan'>mở tài khoản chứng khoán DSC online</a>. Nếu cần Môi giới 1:1 hỗ trợ tư vấn đầu tư, xác nhận gói dịch vụ trước khi đặt lệnh đầu tiên.</p>")
faq=find_h("Câu hỏi thường gặp về tạo tài khoản chứng khoán")
set_text(faq,"Câu hỏi thường gặp khi mở tài khoản chứng khoán")
closing=find_h("Mở tài khoản và hỏi chuyên gia trước lệnh đầu tiên")
closing.insert_before(frag("""<h3>Mở tài khoản chứng khoán ở đâu là tốt nhất?</h3><p>Nơi phù hợp phụ thuộc việc bạn tự giao dịch hay cần hỗ trợ tư vấn. So cùng gói dịch vụ, phí và kênh hỗ trợ trong bài <a href="https://www.dsc.com.vn/kien-thuc/nen-mo-tai-khoan-chung-khoan-o-dau">nên mở tài khoản chứng khoán ở đâu</a>.</p>
<h3>Mở tài khoản chứng khoán có bị gì không?</h3><p>Đăng ký tài khoản không tự tạo ra lệnh mua bán. Bạn cần bảo vệ thông tin và đọc điều kiện phí; rủi ro đầu tư phát sinh khi giao dịch hoặc sử dụng dịch vụ vay.</p>
<h3>Quy định về mở tài khoản chứng khoán là gì?</h3><p>Hồ sơ phải khớp giấy tờ xác thực, đối tượng đăng ký và điều kiện của công ty chứng khoán. Kiểm tra hợp đồng trước khi ký; tổ chức hoặc nhà đầu tư nước ngoài có thủ tục riêng.</p>"""))
# Add verified operational checkpoints and fee conditions, not unrelated market statistics.
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
replace_p("Nơi phù hợp phụ thuộc việc bạn tự giao dịch","""<p>Nơi phù hợp phụ thuộc việc bạn tự giao dịch hay cần Môi giới 1:1 hỗ trợ tư vấn. So cùng gói dịch vụ và điều kiện phí trong bài <a href="https://www.dsc.com.vn/kien-thuc/nen-mo-tai-khoan-chung-khoan-o-dau">nên mở tài khoản chứng khoán ở đâu</a>.</p>""")

# Two real HTML CRO blocks; no fabricated UI screenshots.
template=(ROOT/".antigravity/skills/cro-optimization/assets/banner-templates.md").read_text(encoding="utf-8")
blocks=re.findall(r" \x60", "") if False else re.findall(r"\x60\x60\x60html\n(.*?)\n\x60\x60\x60",template,re.S)
def banner(i,headline,sub,button):
 return blocks[i].replace("{{HEADLINE}}",headline).replace("{{SUB}}",sub).replace("{{BUTTON}}",button).replace("{{URL}}","https://www.dsc.com.vn/mo-tai-khoan")
p=next(p for p in s.select("p") if p.get_text(" ",strip=True).startswith("Tiểu khoản đuôi 6"))
insert_after(p,banner(0,"Đăng ký DSC sau khi đã kiểm tra giấy tờ","App DSC Trading • Xác thực eKYC • Kiểm tra gói hỗ trợ trước khi giao dịch","Mở tài khoản DSC"))
s.select("p")[-1].insert_before(frag(banner(2,"Hoàn tất đăng ký, kiểm tra trạng thái trước lệnh đầu tiên","Giữ OTP cho riêng bạn • Xem điều kiện phí • Chọn hỗ trợ tư vấn theo nhu cầu","Đăng ký tài khoản DSC")))
# Clarity pass: shorten action checkpoints while retaining facts and source links.
plain=str(s)
for before,after in {'Không dùng lại mật khẩu email hoặc ngân hàng.': 'Không dùng lại mật khẩu ngân hàng.', 'Chọn số theo hướng dẫn và kiểm tra thông tin dịch vụ trước khi tiếp tục.': 'Kiểm tra gói trước khi tiếp tục.', 'Không chụp ảnh mờ, lệch góc hay bị lóa.': 'Ảnh CCCD cần rõ, không lóa.', 'Lưu bản hợp đồng để đối chiếu gói dịch vụ và biểu phí.': 'Lưu hợp đồng và biểu phí.', 'Số tài khoản và mật khẩu được gửi về email hoặc tin nhắn.': 'Kiểm tra email hoặc SMS cấp tài khoản.', 'Chỉ nạp tiền sau khi kiểm tra thông báo kích hoạt.': 'Kiểm tra kích hoạt trước khi nạp.', 'Liên hệ DSC để xác nhận giấy tờ, địa điểm và giờ tiếp nhận trước khi đến.': 'Gọi DSC xác nhận hồ sơ trước.', 'Quy trình tại quầy gồm 3 việc chính.': 'Tại quầy, bạn làm 3 việc:', 'Các bước còn lại giống trên ứng dụng.': 'Làm theo hướng dẫn trên ứng dụng.', 'Có tài khoản rồi, bạn đăng nhập App DSC Trading để đặt lệnh.': 'Đăng nhập App DSC Trading.', 'Hãy kiểm tra giá và khối lượng trước khi xác nhận.': 'Kiểm tra giá và khối lượng lệnh.', 'Mức phí phải khớp gói dịch vụ của bạn.': 'Đối chiếu phí của đúng gói.', 'Về bản chất, tài khoản vẫn được mở tại công ty chứng khoán.': 'Tài khoản thuộc công ty chứng khoán.', 'Đăng ký tài khoản không tự tạo ra lệnh mua bán.': 'Đăng ký không tự tạo giao dịch.', 'Hồ sơ cho tổ chức hoặc nhà đầu tư nước ngoài cần được công ty kiểm tra trước.': 'DSC kiểm tra hồ sơ đặc thù trước.', 'Hãy hoàn tất xác thực danh tính và hợp đồng, rồi kiểm tra thông báo kích hoạt tài khoản.': 'Hoàn tất eKYC rồi kiểm tra kích hoạt.', 'Thị trường hiện có 2 phương thức xác thực phổ biến.': 'Bạn cần hoàn tất eKYC trước khi giao dịch.', 'Giao diện ở công ty khác có thể khác, nhưng thứ tự các bước giống nhau.': 'Tên nút có thể khác giữa các ứng dụng.'}.items():
 plain=plain.replace(before,after)
s=BeautifulSoup(plain,"html.parser")

# Normalize internal target behavior; preserve all original destinations.
for a in s.select("a[href]"):
 if "dsc.com.vn" in a["href"]:a.attrs.pop("target",None)
# Preserve exact IMG source/alt tags.
assert [str(i) for i in s.select("img")]==images,"Original image markup changed"
assert hrefs.issubset({a["href"] for a in s.select("a[href]")}),hrefs-{a["href"] for a in s.select("a[href]")}
body=str(s)
draft=ROOT/"knowledge/4-content/2-drafts"/("Optimize-"+slug+"-serp-2026-11-04.md")
draft.write_text(fm(title,meta)+"# "+title+"\n\n"+md(body),encoding="utf-8")
(base/(slug+".body.html")).write_text(body,encoding="utf-8")
(base/(slug+".metadata.json")).write_text(json.dumps({"slug":slug,"url":url,"title":title,"meta_description":meta,"state":"draft-not-published","source_sha256":hashlib.sha256(raw.encode()).hexdigest(),"date_prepared":"2026-11-04","preserved_images":len(images),"preserved_original_destinations":len(hrefs)},ensure_ascii=False,indent=2),encoding="utf-8")
(base/(slug+".diff.txt")).write_text("\n".join(difflib.unified_diff(raw.splitlines(),body.splitlines(),fromfile="live-before",tofile="proposed-after")),encoding="utf-8")
print("PROPOSAL",proposal)
print("DRAFT",draft)
print("PRESERVED",len(images),"images;",len(hrefs),"original destinations")
print("TITLE/META",len(title),len(meta))


