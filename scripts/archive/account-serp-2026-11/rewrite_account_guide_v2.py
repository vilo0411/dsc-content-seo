"""User-approved four-part rewrite, based on VPBankS outline; local draft only."""
import sys,re,json,html,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify
sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[1]
slug="cach-mo-tai-khoan-chung-khoan"
OUT=ROOT/"knowledge/4-content/audits/account-serp-2026-11-04/v2"
DRAFT=ROOT/"knowledge/4-content/2-drafts/serp-2026-11-04-v2"/("Optimize-"+slug+".md")
PROP=ROOT/"knowledge/4-content/1-outlines/serp-2026-11-04-v2"/("Proposal-"+slug+".md")
for p in [OUT,DRAFT.parent,PROP.parent]:p.mkdir(parents=True,exist_ok=True)
live=(ROOT/"knowledge/raw/live/html"/(slug+".html")).read_text(encoding="utf-8")
source=BeautifulSoup(live,"html.parser")
imgs=[str(x) for x in source.select("img")]
assert len(imgs)==6
title="Cách mở tài khoản chứng khoán online và tại quầy"
meta="Cách mở tài khoản chứng khoán online, tại quầy và trên App DSC Trading. Xem giấy tờ cần chuẩn bị, các bước đăng ký và lưu ý bảo mật trước khi giao dịch."
assert len(title)<=59 and 140<=len(meta)<=160,(len(title),len(meta))
proposal=f"""---
Title: Proposal sửa gọn bài hướng dẫn mở tài khoản
Target_Keyword: cách mở tài khoản chứng khoán
Slug: {slug}
Persona: P2
Status: Outline approved in chat; execution to draft only
Date: 2026-11-04
---
# Proposal — bản 2 theo outline VPBankS

## 0. Content strategy header

- Target keyword: cách mở tài khoản chứng khoán; phụ: mở tài khoản chứng khoán, mở online.
- Intent: hướng dẫn người mới chuẩn bị và thực hiện đăng ký; không so sánh công ty hoặc phân tích biểu phí.
- Persona: P2, cần thao tác cụ thể với ít thuật ngữ.
- Product bridge: đăng ký trên App DSC Trading; Môi giới 1:1 hỗ trợ tư vấn đầu tư theo dịch vụ đăng ký, không hứa lợi nhuận hoặc mức phí chung.
- Người dùng đã duyệt khung bốn H2 và ba H3. Không tiếp tục bản sửa vụn theo số điểm trước.
- URL giữ nguyên. Chỉ sửa bài hướng dẫn, không sửa bài so sánh trong lượt này.

## 1. Hiện trạng và thay đổi SEO
Live khoảng 2.805 từ, tám H2, nhiều phần quy trình/FAQ lặp. Nội dung đã đủ ảnh thao tác; không tạo ảnh giao diện AI.
Title mới: {title} ({len(title)} ký tự).
Meta mới: {meta} ({len(meta)} ký tự).
Độ dài đi theo nội dung cần thiết, không có mục tiêu tăng hoặc giảm để đạt hạng. Không cam kết lên top.
GSC và ảnh SERP dùng từ rollout-plan.md của vòng trước; không đổi ngày/thiết bị hoặc suy ra quan hệ nhân quả từ vị trí.

## 2. Tham khảo đối thủ

### 2.1 Nguồn chính
https://www.vpbanks.com.vn/trung-tam-kien-thuc/mo-tai-khoan-chung-khoan
Đã đọc toàn thân bài và kiểm tra lại CMS record live trong phiên: khoảng1.660 từ,4H2,3H3. Không dùng word count làm chuẩn cứng.

### 2.2 Outline đối thủ
H1: hướng dẫn mở tài khoản.
H2: điều kiện; đăng ký; lưu ý; lý do chọn thương hiệu.
Ba H3 trong phần đăng ký: website, tại quầy, NEO Invest. Từng bước là danh sách, không tách thành nhiều heading.
Các mục giữ một nhiệm vụ: chuẩn bị, thao tác, an toàn, lựa chọn dịch vụ.
Không sao chép diễn đạt, lời hứa hoặc sản phẩm VPBankS sang DSC.

### 2.3 Intent gap của bản sửa trước
Bước chọn công ty bị chen bảng phí và ví dụ tiền. Các câu ngắn bị cắt cơ học làm bài đọc rời rạc.
Bản2 bỏ phân tích biểu phí dài, không lặp hướng dẫn chung rồi hướng dẫn DSC thêm một lần.

## 3. Seven sweeps
Clarity: đoạn2–3câu cùng ý; không cố chèn câu ngắn.
Voice: hướng dẫn khách quan, không giật gân hoặc hỏi mồi.
So what: bước nào dẫn tới kết quả gì; không đưa số thị trường.
Prove it: thao tác dựa trên form/ảnh DSC, phí chỉ dẫn nguồn chính thức.
Specificity: tên ứng dụng, OTP, NFC và kênh đăng ký thật.
Emotion: giải đáp chỗ người mới vướng bằng hướng dẫn, không kể câu chuyện giả.
Zero risk: phân biệt mở tài khoản và giao dịch, không hứa an toàn/lợi nhuận tuyệt đối.
GEO: câu trả lời rõ và có nguồn; không hứa được AI Overview chọn.

## 4. Heading-by-heading
[GIỮ NGUYÊN] Slug và nguồn6ảnh, đủ13đích body gốc.
[CẬP NHẬT] H1/sapo phù hợp phạm vi online và tại quầy.
[CẬP NHẬT] H2 chuẩn bị: bảng4hạng mục, lưu ý đối tượng.
[CẬP NHẬT] H2 cách mở:3H3 qua website, tại quầy, App DSC Trading. Bước thao tác dùng nhãn trong văn bản.
[CẬP NHẬT] H2 lưu ý: giấy tờ, NFC/OTP, phí và việc sau mở.
[CẬP NHẬT] H2 DSC: giới thiệu hỗ trợ có điều kiện, CTA đúng trang đăng ký.
[XÓA BỎ] FAQ lặp, bảngso sánh phí, ví dụlệnh, số thị trường, phầnquy trình chung bị lặp.
[THÊM MỚI] Chú thích ngắn phân biệt đăng ký form và hoàn tất eKYC/hợp đồng.

## 5. Content gaps và cách xử lý
Học VPBankS cách tách ba kênh và nén lưu ý; không tự thêm nội dung chỉ để có thêmheading.
Bài DSC có6ảnh nên giữ cụm ảnh App theo thứ tự thực tế. Không bịa thời gian xử lý, quyền lợi tự động hoặc tên người kiểm duyệt.

## 6. Link strategy
Giữ href gốc. Link so sánh công ty đặt ở chuẩn bị; link app ở bước tải; hợpđồng ở bước ký; bài phí/bảo mật/giờgiao dịch ở lưu ý.
Link loại tài khoản/chứngchỉquỹ chỉ nêu phạmvi hồsơ; không tạo heading lệchintent. Không backfill thêm.
Cần đối chiếu hồ sơ thực tế trướcCMS nếu live thay đổi.

## 7. Hình ảnh và CTA

### 7.1 Ảnhgốc
"""
for i,img in enumerate(source.select("img"),1):proposal+=f"\n- Ảnh{i}: {img.get('src')} — giữ URL, thứ tự và markup; không ghi là ảnh mới."
proposal+="""

### 7.2 Visual/CTA
Không thêm ảnh minh họaAI; user đã chọn hướng ngắn gọn, giữ ảnhthao tác thật. Bảngchuẩn bị giúp đọc lướt.
Một bannerclosing theo CRO, sau đoạn dẫn. Không ép hai banner cho bài ngắn; không UTM.
Final/CMS chưa sửa. Duyệt chất lượng đọc trước khi finalize.
"""
PROP.write_text(proposal,encoding="utf-8")
body=r"""<p>Cách mở tài khoản chứng khoán online gồm 3 bước: đăng ký thông tin, xác thực danh tính eKYC và ký hợp đồng điện tử. Bạn cần CCCD gắn chip còn hiệu lực, điện thoại có NFC, số điện thoại, email và tài khoản ngân hàng đứng tên mình.</p>
<p>Nếu điện thoại không có NFC hoặc muốn được hướng dẫn trực tiếp, bạn đăng ký tại quầy giao dịch của công ty chứng khoán. Dưới đây là giấy tờ cần có và cách thực hiện qua website, tại quầy hoặc trên App DSC Trading.</p>
%%IMG0%%
<h2>Cần chuẩn bị gì để mở tài khoản chứng khoán?</h2>
<p>Trước khi mở tài khoản, bạn nên chọn công ty chứng khoán được UBCKNN cấp phép và kiểm tra yêu cầu đăng ký trên website chính thức. Nếu chưa chọn được nơi mở, bài <a href="https://www.dsc.com.vn/kien-thuc/nen-mo-tai-khoan-chung-khoan-o-dau">nên mở tài khoản chứng khoán ở đâu</a> giúp bạn đối chiếu phí, ứng dụng và dịch vụ hỗ trợ.</p>
<p>Với cá nhân trong nước tự đăng ký online, những thông tin cần chuẩn bị gồm:</p>
<table><thead><tr><th>Hạng mục</th><th>Cần chuẩn bị</th><th>Lưu ý</th></tr></thead><tbody>
<tr><td>Giấy tờ tùy thân</td><td>Thẻ căn cước hoặc CCCD gắn chip còn hiệu lực</td><td>Dùng bản gốc, ảnh và thông tin trên thẻ rõ nét.</td></tr>
<tr><td>Điện thoại</td><td>Thiết bị có camera và kết nối internet</td><td>Quy trình đọc chip tại DSC cần thiết bị hỗ trợ NFC.</td></tr>
<tr><td>Thông tin liên hệ</td><td>Số điện thoại của bạn và email đang sử dụng</td><td>Cần truy cập được để nhận OTP, thông báo và thông tin tài khoản.</td></tr>
<tr><td>Tài khoản ngân hàng</td><td>Tài khoản đứng tên bạn</td><td>Dùng để liên kết, nộp và rút tiền theo hướng dẫn của công ty.</td></tr>
</tbody></table>
<p>Hướng dẫn online trong bài dành cho công dân Việt Nam từ đủ 18 tuổi, có năng lực hành vi dân sự đầy đủ. Người chưa đủ 18 tuổi làm hồ sơ cùng người đại diện theo pháp luật. Nhà đầu tư nước ngoài và tổ chức cần hỏi công ty về hồ sơ riêng.</p>
<p>Theo khoản 3 Điều 6 Thông tư 120/2020/TT-BTC, bạn được mở tài khoản tại nhiều công ty chứng khoán khác nhau (xem <a href="https://www.dsc.com.vn/kien-thuc/mot-nguoi-duoc-mo-bao-nhieu-tai-khoan-chung-khoan">một người được mở bao nhiêu tài khoản chứng khoán</a>). Khi đăng ký, cần phân biệt <a href="https://www.dsc.com.vn/kien-thuc/cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam">các loại tài khoản chứng khoán</a> để chọn đúng dịch vụ.</p><p>Với chứng chỉ quỹ mở, bạn nên xem riêng <a href="https://www.dsc.com.vn/kien-thuc/huong-dan-mo-tai-khoan-chung-chi-quy">hướng dẫn mở tài khoản chứng chỉ quỹ</a> vì quy trình có thể khác tài khoản giao dịch cổ phiếu.</p>

<h2>Cách mở tài khoản chứng khoán</h2>
<p>Bạn có thể đăng ký qua 3 kênh: website, quầy giao dịch hoặc ứng dụng của công ty chứng khoán. Kênh online cần điện thoại có NFC để đọc chip CCCD; tại quầy, nhân viên đối chiếu giấy tờ thay bước này. Kênh nào cũng phải ký hợp đồng trước khi giao dịch.</p>

<h3>Mở tài khoản chứng khoán qua website</h3>
<p>Đăng ký trên website phù hợp khi bạn muốn nhập thông tin trên máy tính. Bạn vẫn cần điện thoại nếu hệ thống yêu cầu chụp giấy tờ, nhận diện khuôn mặt hoặc đọc chip NFC.</p>
<ol>
<li><strong>Truy cập trang đăng ký:</strong> Vào website chính thức của công ty, chọn mục mở tài khoản. Với DSC, bạn truy cập <a href="https://www.dsc.com.vn/mo-tai-khoan">trang mở tài khoản DSC online</a>.</li>
<li><strong>Điền thông tin:</strong> Nhập họ tên, số giấy tờ, số điện thoại và email. Kiểm tra thông tin trước khi xác nhận OTP.</li>
<li><strong>Hoàn tất xác thực:</strong> Làm theo hướng dẫn eKYC trên hệ thống; chuyển sang điện thoại nếu được yêu cầu.</li>
<li><strong>Ký hợp đồng và nhận tài khoản:</strong> Đọc điều khoản, xác nhận đăng ký và theo dõi thông báo của công ty.</li>
</ol>
<p>Trang đăng ký DSC gồm các bước điền thông tin, xác thực OTP và chọn số tài khoản. Sau đó bạn vẫn phải hoàn tất eKYC và ký hợp đồng. Thông báo nhận đăng ký chưa phải tài khoản đã kích hoạt.</p>

<h3>Mở tài khoản chứng khoán tại quầy</h3>
<p>Nếu không quen thao tác trên điện thoại hoặc cần hỗ trợ hồ sơ, bạn đăng ký trực tiếp tại quầy. Nên liên hệ công ty trước để xác nhận giấy tờ, địa điểm và giờ tiếp nhận.</p>
<ol>
<li><strong>Chuẩn bị hồ sơ:</strong> Mang giấy tờ tùy thân bản gốc còn hiệu lực và những giấy tờ công ty đã hướng dẫn.</li>
<li><strong>Điền thông tin và ký hợp đồng:</strong> Nhân viên đối chiếu giấy tờ, hướng dẫn bạn hoàn thiện phiếu đăng ký và hợp đồng.</li>
<li><strong>Nhận thông tin tài khoản:</strong> Kiểm tra email hoặc tin nhắn, đổi mật khẩu và thực hiện các yêu cầu kích hoạt còn lại.</li>
</ol>
<p>Hồ sơ của tổ chức hoặc nhà đầu tư nước ngoài có thể khác hồ sơ cá nhân trong nước. Bạn cần xác nhận điều kiện trước khi đến, thay vì chỉ chuẩn bị theo hướng dẫn đăng ký online.</p>

<h3>Mở tài khoản trên App DSC Trading</h3>
<p>App DSC Trading cho phép bạn đăng ký và sử dụng tài khoản trên điện thoại. Ảnh dưới đây được giữ từ hướng dẫn trên hệ thống đăng ký DSC. Khi thực hiện trên App, bạn làm theo các yêu cầu đang hiển thị vì giao diện có thể khác.</p>
<p><strong>Bước 1: Tải App DSC Trading.</strong> Truy cập liên kết tải ứng dụng từ website DSC, hoặc tìm đúng ứng dụng trên App Store và CH Play. Chọn đúng <a href="https://www.dsc.com.vn/kien-thuc/app-dau-tu-chung-khoan">app đầu tư chứng khoán</a> của công ty để tránh đăng ký trên ứng dụng giả mạo.</p>
<p><strong>Bước 2: Đăng ký thông tin và xác thực OTP.</strong> Mở ứng dụng, chọn đăng ký rồi nhập thông tin cá nhân theo giấy tờ. Dùng số điện thoại và email của bạn để thuận tiện nhận thông báo, khôi phục tài khoản khi cần.</p>
%%IMG1%%
<p>Nhập OTP trong thời hạn hiển thị trên màn hình. Nếu mã hết hạn, kiểm tra số điện thoại rồi yêu cầu gửi lại. Không đưa mã OTP cho ai.</p>
%%IMG2%%
<p><strong>Bước 3: Kiểm tra thông tin đăng ký.</strong> Rà lại họ tên, số giấy tờ và thông tin liên hệ. Nếu hệ thống hiển thị mục chọn số tài khoản hoặc mã nhân viên hỗ trợ, bạn điền theo nhu cầu.</p>
%%IMG3%%
<p><strong>Bước 4: Xác thực danh tính.</strong> Thực hiện các yêu cầu chụp giấy tờ, đọc chip NFC và nhận diện khuôn mặt trên ứng dụng. Khi đọc chip, đặt thẻ sát vị trí cảm biến của điện thoại và giữ yên tới khi có thông báo hoàn tất.</p>
%%IMG4%%
<p><strong>Bước 5: Kiểm tra thông tin và ký hợp đồng.</strong> Đọc <a href="https://www.dsc.com.vn/kien-thuc/hop-dong-mo-tai-khoan-chung-khoan">hợp đồng mở tài khoản chứng khoán</a>, kiểm tra gói dịch vụ và biểu phí trước khi xác nhận. Sau đó, theo dõi email hoặc ứng dụng để biết trạng thái hồ sơ và thông tin đăng nhập.</p>
%%IMG5%%
<p>Khi tài khoản được kích hoạt, bạn nhận số tài khoản dạng 024Cxxxxxx gồm 2 tiểu khoản: đuôi 1 cho giao dịch thường, đuôi 6 cho giao dịch ký quỹ. Đổi mật khẩu, bật Smart OTP và bổ sung hồ sơ nếu hệ thống còn yêu cầu.</p>

<h2>Lưu ý khi đăng ký và sử dụng tài khoản</h2>
<p>Những lỗi khi đăng ký thường liên quan đến thông tin giấy tờ, OTP hoặc bước xác thực danh tính. Bạn nên kiểm tra lần lượt theo thông báo trên màn hình, tránh tạo thêm hồ sơ khi chưa biết hồ sơ trước đang ở trạng thái nào.</p>
<ul>
<li><strong>Giấy tờ và thông tin phải khớp:</strong> Chụp rõ ảnh, không mất góc hoặc lóa sáng. Nếu vừa đổi giấy tờ, kiểm tra xem mình đang khai báo theo thông tin mới hay cũ.</li>
<li><strong>Đọc chip đúng cách:</strong> Kiểm tra thiết bị có NFC, bật tính năng nếu máy yêu cầu và thử tháo ốp lưng khi không đọc được chip. Nếu không có thiết bị phù hợp, liên hệ DSC để được hướng dẫn.</li>
<li><strong>Giữ kín thông tin đăng nhập:</strong> Không chia sẻ mật khẩu, mã PIN hoặc OTP, kể cả với người tự xưng là nhân viên hỗ trợ. Chỉ thao tác trên website và ứng dụng chính thức.</li>
<li><strong>Phân biệt phí mở và phí sử dụng:</strong> Phí giao dịch, lưu ký và dịch vụ vay có điều kiện riêng. Đọc <a href="https://www.dsc.com.vn/kien-thuc/mo-tai-khoan-chung-khoan-co-mat-phi-khong-can-bao-nhieu-tien">mở tài khoản chứng khoán có mất phí không</a> và kiểm tra biểu phí của gói bạn chọn.</li>
</ul>
<p>Tại DSC, mức phí phụ thuộc nhóm quản lý tài khoản và dịch vụ đăng ký, không áp dụng một mức chung cho mọi nhà đầu tư. Bạn nên đối chiếu <a href="https://www.dsc.com.vn/bieu-phi">biểu phí chính thức DSC</a> trước khi ký; <a href="https://www.dsc.com.vn/kien-thuc/phi-luu-ky-chung-khoan-la-gi">phí lưu ký chứng khoán</a> cũng cần được phân biệt với phí giao dịch.</p>
<p>Sau khi tài khoản hoạt động, 3 việc dưới đây giúp bạn tránh nộp nhầm tiền và đặt lệnh sai phiên:</p>
<ol>
<li><strong>Nộp tiền đúng thông tin:</strong> DSC nhận nộp tiền qua mã định danh 963369 với BIDV và nhiều ngân hàng khác. Đối chiếu tên thụ hưởng và số tài khoản trong hệ thống trước khi chuyển.</li>
<li><strong>Đặt lệnh trong giờ giao dịch:</strong> HOSE, HNX và UPCoM giao dịch từ Thứ 2 đến Thứ 6, nghỉ trưa 11h30–13h00. Trên HOSE, phiên ATO mở lúc 9h00 và phiên ATC đóng lúc 14h45; xem thêm <a href="https://www.dsc.com.vn/kien-thuc/gio-giao-dich-chung-khoan-viet-nam">giờ giao dịch chứng khoán</a> và <a href="https://www.dsc.com.vn/kien-thuc/cac-quy-dinh-giao-dich-chung-khoan-quan-trong-ma-nguoi-moi-can-biet">quy định giao dịch chứng khoán</a>.</li>
<li><strong>Nắm lô và chu kỳ thanh toán:</strong> Lệnh trên HOSE tính theo lô 100 cổ phiếu, cổ phiếu mua về tài khoản vào ngày T+2. Các bước chọn mã, nhập giá và khối lượng có trong bài <a href="https://www.dsc.com.vn/kien-thuc/cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau">cách mua cổ phiếu online cho người mới bắt đầu</a>.</li>
</ol>
<p>Nếu còn lo ngại về bảo mật, bài <a href="https://www.dsc.com.vn/kien-thuc/mo-tai-khoan-chung-khoan-online-co-an-toan-khong">mở tài khoản chứng khoán online có an toàn không</a> giải thích những rủi ro cần nhận biết.</p>

<h2>Mở tài khoản tại DSC và nhận hỗ trợ</h2>
<p>DSC nhận đăng ký eKYC qua website và App DSC Trading; với CCCD gắn chip và điện thoại có NFC, quy trình mất khoảng 3 phút. Trước khi đăng ký dịch vụ, hãy xác nhận loại tài khoản, biểu phí và hình thức hỗ trợ bạn cần.</p>
<p>Nếu muốn có chuyên gia Môi giới 1:1 hỗ trợ tư vấn đầu tư, bạn trao đổi với DSC về gói dịch vụ trước lệnh đầu tiên.</p>
%%CTA%%
<p><strong>Tuyên bố miễn trừ trách nhiệm:</strong> Nội dung mang tính hướng dẫn và tham khảo, không phải khuyến nghị mua bán chứng khoán. Bạn tự quyết định và chịu trách nhiệm với giao dịch của mình.</p>
"""
templates=(ROOT/".antigravity/skills/cro-optimization/assets/banner-templates.md").read_text(encoding="utf-8")
banners=re.findall(r"\x60\x60\x60html\n(.*?)\n\x60\x60\x60",templates,re.S)
cta=banners[2].replace("{{HEADLINE}}","Đăng ký tài khoản trên kênh chính thức DSC").replace("{{SUB}}","eKYC khoảng 3 phút • CCCD gắn chip • Ký hợp đồng điện tử").replace("{{BUTTON}}","Mở tài khoản DSC").replace("{{URL}}","https://www.dsc.com.vn/mo-tai-khoan")
for i,img in enumerate(imgs):body=body.replace("%%IMG"+str(i)+"%%",img)
body=body.replace("%%CTA%%",cta)
parsed=BeautifulSoup(body,"html.parser")
original_hrefs={a["href"] for a in source.select("a[href]")}
assert original_hrefs.issubset({a["href"] for a in parsed.select("a[href]")})
assert [str(i) for i in parsed.select("img")]==imgs
assert len(parsed.select("h2"))==4 and len(parsed.select("h3"))==3
# Keep image tags and real CTA HTML in Markdown, without altering the original source tags.
mds=BeautifulSoup(body,"html.parser");rawblocks={}
for i,n in enumerate(list(mds.select("img"))+[mds.select("div[style]")[0]]):
 token=f"DSCPRESERVE{i}TOKEN";rawblocks[token]=(f'![{n.get("alt", "")} ]({n.get("src", "")})'.replace(" ]", "]") if n.name=="img" else str(n));n.replace_with(mds.new_string("\n\n"+token+"\n\n"))
md=markdownify(str(mds),heading_style="ATX",bullets="*")
for token,raw in rawblocks.items():md=md.replace(token,"\n\n"+raw+"\n\n")
md=re.sub(r"\*\*([^*\n]+):\*\*",r"**\1**:",md)
md=re.sub(r"\n{3,}","\n\n",md).strip()+"\n"
front=f"---\nTitle: {title}\nMeta_Description: {meta}\nTarget_Keyword: cách mở tài khoản chứng khoán\nSlug: {slug}\nPersona: P2\nDate: 2026-11-04\nStatus: Draft — user review\n---\n\n"
DRAFT.write_text(front+"# "+title+"\n\n"+md,encoding="utf-8")
(OUT/(slug+".body.html")).write_text(body,encoding="utf-8")
(OUT/"metadata.json").write_text(json.dumps({"url":"https://www.dsc.com.vn/kien-thuc/"+slug,"title":title,"meta_description":meta,"status":"draft-not-published","proposal":str(PROP.relative_to(ROOT)),"draft":str(DRAFT.relative_to(ROOT)),"original_images":6,"preserved_original_destinations":len(original_hrefs),"word_count_body":len(parsed.get_text(" ",strip=True).split()),"h2":4,"h3":3},ensure_ascii=False,indent=2),encoding="utf-8")
css="body{font:16px/1.75 system-ui,sans-serif;color:#182b3c;max-width:880px;margin:30px auto;padding:0 22px}h1{font-size:30px;line-height:1.3}h2{font-size:25px;margin-top:35px}h3{font-size:21px;margin-top:28px}img{max-width:100%;height:auto;display:block;margin:20px auto}table{width:100%;border-collapse:collapse;display:block;overflow-x:auto}td,th{padding:12px;border:1px solid #dce5ea;text-align:left;min-width:130px}a{color:#1264ac}li{margin:9px 0}.notice{font-size:14px;background:#edf7f1;padding:13px;border-radius:8px}.toolbar{display:flex;gap:10px;flex-wrap:wrap}button{padding:8px 13px;font:inherit;border:1px solid #ccd9e3;background:white;border-radius:6px;cursor:pointer}iframe{width:100%;height:900px;border:1px solid #dce5ea;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere}textarea{width:100%;height:250px}small{color:#5d6b79}"
def page(h,title):return "<!doctype html><html lang='vi'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>"+html.escape(title)+"</title><style>"+css+"</style>"+h+"</html>"
(OUT/"article.html").write_text(page("<h1>"+html.escape(title)+"</h1>"+body,title),encoding="utf-8")
review="<h1>Bản sửa gọn bài hướng dẫn DSC</h1><p class='notice'>Bản2 theo khung VPBankS người dùng đã duyệt · Chưa cập nhật CMS/Final. Không tiếp tục bản sửa dài trước.</p><p><a href='article.html'>Đọc riêng bài mới</a> · <a href='"+slug+".body.html'>HTML body</a> · <a href='metadata.json'>Title/meta</a></p><div class='toolbar'><button data-view='new'>Bài mới</button><button data-view='old'>Live trước sửa</button></div><iframe id='preview' title='Bài viết' sandbox='allow-popups' src='article.html'></iframe><details><summary>HTML để copy sau khi duyệt</summary><textarea readonly>"+html.escape(body)+"</textarea></details><p>Ảnh và các đích link live được giữ. Nội dung đã tách thành4H2,3H3; phần phí chỉ là lưu ý, không còn bảng tính phí hoặc FAQ lặp.</p><script>document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>document.getElementById('preview').src=b.dataset.view==='new'?'article.html':'before.html');</script>"
(OUT/"before.html").write_text(page("<h1>Live trước sửa</h1>"+live,"DSC — live trước sửa"),encoding="utf-8")
(OUT/"index.html").write_text(page(review,"DSC — bản sửa gọn theo outline VPBankS"),encoding="utf-8")
print("DRAFT",DRAFT)
print("REVIEW",OUT/"index.html")
print("WORDS",len(parsed.get_text(" ",strip=True).split()),"H2",len(parsed.select("h2")),"H3",len(parsed.select("h3")),"IMAGES",len(imgs),"ORIGINAL_DESTINATIONS",len(original_hrefs))


