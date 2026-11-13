from pathlib import Path
import json,re,html
from bs4 import BeautifulSoup
from markdownify import markdownify
root=Path.cwd();slug="nen-mo-tai-khoan-chung-khoan-o-dau";out=root/"knowledge/4-content/audits/account-serp-2026-11-04";out.mkdir(parents=True,exist_ok=True)
live=(root/"knowledge/raw/live/html"/(slug+".html")).read_text(encoding="utf-8");soup=BeautifulSoup(live,"html.parser")
imgs=[(x.get("alt",""),x["src"]) for x in soup.select("img[src]")];links=[a["href"] for a in soup.select("a[href]")]
title="Nên mở tài khoản chứng khoán ở đâu? Top 7 công ty uy tín"
meta="Nên mở tài khoản chứng khoán ở đâu? So sánh 7 công ty theo kênh đăng ký, điều kiện phí và hỗ trợ tư vấn để chọn nơi phù hợp trước khi mở tài khoản."
fm=f"""---
Title: {title}
Meta_Description: {meta}
Target_Keyword: nên mở tài khoản chứng khoán ở đâu
Slug: {slug}
Persona: P2
Search_Intent: Commercial investigation
Product_Bridge: Mở tài khoản eKYC và Môi giới 1:1
Status: Optimize draft - pending human approval
Source_URL: https://www.dsc.com.vn/kien-thuc/{slug}
Reviewed_At: 2026-11-04
---
"""
baseline=fm+"\n# "+title+"\n\n"+markdownify(live,heading_style="ATX").strip()+"\n"
(out/("baseline-"+slug+".md")).write_text(baseline,encoding="utf-8")
def im(i): return "!["+imgs[i][0]+"]("+imgs[i][1]+")"
draft=fm+"\n# "+title+"\n\n"+"""Nên mở tài khoản chứng khoán ở đâu phụ thuộc vào cách bạn giao dịch: tự đặt lệnh hay cần người hỗ trợ tư vấn. Hãy so cùng loại tài khoản, kênh đặt lệnh và điều kiện phí trước khi chọn công ty.

VPS, SSI, TCBS, HSC, VNDIRECT, VCBS và DSC đều có kênh đăng ký trực tuyến. Danh sách dưới đây giúp bạn đối chiếu dịch vụ, không phải bảng xếp hạng lợi nhuận hoặc mức độ an toàn.

## 5 tiêu chí quan trọng khi lựa chọn công ty chứng khoán

Tháng 11/2026: [biểu phí DSC](https://www.dsc.com.vn/bieu-phi/bieu-phi-giao-dich-chung-khoan-niem-yet) phân biệt tài khoản do Tư vấn số và Môi giới quản lý. Hai người cùng mở tại một công ty vẫn có thể chịu mức phí khác nhau.

### Thương hiệu và tiềm lực tài chính của công ty

Kiểm tra tên pháp nhân, kênh liên hệ và thông tin công bố trên website chính thức. Sau đó, đọc báo cáo tài chính cùng điều kiện sử dụng dịch vụ.

Vốn điều lệ và thị phần giúp bạn tìm hiểu quy mô doanh nghiệp. Hai chỉ tiêu này không cam kết lợi nhuận hay loại bỏ rủi ro đầu tư.

Đừng chỉ nhìn thương hiệu. Bạn cần biết nơi tiếp nhận yêu cầu khi có sai lệch số dư, lỗi đăng nhập hoặc chậm xử lý hồ sơ.

### Chi phí giao dịch và lãi suất vay ký quỹ

Cần tách phí mở tài khoản khỏi phí phát sinh khi sử dụng. Bài [mở tài khoản chứng khoán có mất phí không](https://www.dsc.com.vn/kien-thuc/mo-tai-khoan-chung-khoan-co-mat-phi-khong-can-bao-nhieu-tien) giải thích những khoản cần kiểm tra.

Khi so [phí giao dịch chứng khoán](https://www.dsc.com.vn/kien-thuc/phi-giao-dich-chung-khoan), hãy hỏi mức áp dụng cho đúng kênh đặt lệnh. Tài khoản tự giao dịch và tài khoản có tư vấn không nhất thiết dùng chung biểu phí.

Theo biểu phí DSC có hiệu lực từ 20/08/2025, tài khoản Tư vấn số có mức phí 0,1% giá trị giao dịch. Tài khoản do Môi giới quản lý áp dụng các bậc 0,15–0,3% theo giá trị giao dịch trong ngày.

Với giao dịch trị giá 10 triệu đồng, mức 0,1% tương ứng 10.000 đồng; mức 0,3% tương ứng 30.000 đồng. Đây là ví dụ tính phí, chưa gồm những khoản thuế và dịch vụ khác.

Hãy so cùng điều kiện. Trước khi đăng ký, kiểm tra ưu đãi có thời hạn hay không và chi phí sau khi ưu đãi kết thúc.

Lãi vay cần đối chiếu khi bạn định sử dụng giao dịch ký quỹ. Phân biệt [các loại tài khoản chứng khoán](https://www.dsc.com.vn/kien-thuc/cac-loai-tai-khoan-chung-khoan-pho-bien-tai-viet-nam) giúp bạn chọn đúng dịch vụ, tránh đăng ký theo quảng cáo.

### Hệ sinh thái sản phẩm và dịch vụ đa dạng

Chọn công ty theo sản phẩm bạn cần: cổ phiếu, chứng chỉ quỹ hoặc trái phiếu. Kiểm tra điều kiện giao dịch của từng sản phẩm trên kênh chính thức.

Nếu mới tìm hiểu cổ phiếu, bạn chưa cần lấy số lượng sản phẩm làm tiêu chí quyết định. Chứng khoán DSC không cung cấp giao dịch phái sinh; không nhầm dịch vụ của công ty khác với dịch vụ tại DSC.

### Hệ thống công nghệ và trải nghiệm ứng dụng giao dịch

Trải nghiệm bảng giá, cách xem số dư và vị trí tìm hỗ trợ trước khi chọn nơi giao dịch. Kiểm tra cả kênh thay thế khi điện thoại hoặc ứng dụng không sử dụng được.

Ứng dụng có nhiều công cụ chưa chắc phù hợp với người mới. Bạn cần tìm được lệnh đặt mua, lịch sử giao dịch và hướng dẫn nạp rút tiền mà không phải đoán.

Đọc về [mở tài khoản chứng khoán online có an toàn không](https://www.dsc.com.vn/kien-thuc/mo-tai-khoan-chung-khoan-online-co-an-toan-khong) trước khi cung cấp giấy tờ. Chỉ tải ứng dụng qua liên kết trên website chính thức và không chia sẻ mã xác thực.

### Chất lượng dịch vụ tư vấn và đội ngũ môi giới đồng hành

Phân biệt hỗ trợ kỹ thuật với hỗ trợ tư vấn đầu tư. Bộ phận hỗ trợ kỹ thuật xử lý tài khoản; chuyên viên tư vấn giúp bạn trao đổi về quyết định giao dịch.

Hãy hỏi phạm vi hỗ trợ, kênh liên hệ và biểu phí của gói dịch vụ. Không mặc định một chương trình phí thấp bao gồm tư vấn riêng.

Nếu chưa biết đọc báo cáo hoặc kiểm tra rủi ro trước lệnh đầu tiên, người hỗ trợ có thể là tiêu chí ưu tiên. Tuy vậy, khuyến nghị không bảo đảm kết quả đầu tư.

## So sánh Top 7 công ty chứng khoán uy tín tại Việt Nam

Tính đến tháng 11/2026, các nguồn chính thức dưới đây mô tả những kênh đăng ký và điều kiện dịch vụ khác nhau. Bảng tập trung vào điều cần xác nhận trước khi mở, thay vì xếp hạng bằng thị phần chưa đối chiếu.

| Công ty | Kênh đăng ký được công bố | Điều cần kiểm tra trước khi chọn |
|---|---|---|
| VPS | SmartOne | Phí của gói tài khoản và phạm vi hỗ trợ; đối chiếu [hướng dẫn VPS](https://www.vps.com.vn/Sites/QuoteVN/SiteRoot/Huong_dan_mo_tai_khoan_chung_khoan_tren_VPS_SmartOne.pdf). |
| SSI | Trang đăng ký iBoard | Tự giao dịch hay có chuyên viên tư vấn; kiểm tra [kênh đăng ký SSI](https://www.ssi.com.vn/khach-hang-ca-nhan/mo-tai-khoan). |
| TCBS | Trang mở tài khoản trực tuyến | Khoản miễn phí, khoản thu hộ và điều kiện đi kèm; đọc [thông tin mở tài khoản TCBS](https://www.tcbs.com.vn/ca-nhan/uu-dai/mo-tai-khoan-chung-khoan-tcbs/). |
| HSC | HSC ONE hoặc website | Yêu cầu kích hoạt và hoàn thiện hồ sơ; đối chiếu [hướng dẫn HSC](https://www.hsc.com.vn/vi/tai-khoan). |
| VNDIRECT | DGO, DSTOCK hoặc mydgo | Kích hoạt tài khoản và điều kiện rút tiền; xem [trung tâm hỗ trợ VNDIRECT](https://www.vndirect.com.vn/mo-tai-khoan-chung-khoan/). |
| VCBS | VCBS Mobile, website, VCB Digibank hoặc quầy | Gói chủ động hay tư vấn; xem [dịch vụ VCBS tại Vietcombank](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Dau-tu/Giao-dich-Chung-khoan). |
| DSC | App DSC Trading hoặc website | Khối quản lý tài khoản và phạm vi tư vấn; đối chiếu [biểu phí DSC](https://www.dsc.com.vn/bieu-phi/bieu-phi-giao-dich-chung-khoan-niem-yet). |

Bảng được rà soát ngày 04/11/2026. Không xem vị trí trong danh sách là thứ hạng; điều kiện phê duyệt và chương trình phí có thể thay đổi.

Bạn tự giao dịch thì ưu tiên chi phí của đúng gói và thao tác trên ứng dụng. Bạn cần người trao đổi trước khi đặt lệnh thì hỏi dịch vụ tư vấn được bao gồm.

"""+im(0)+"""

*Ảnh lưu từ phiên bản trước của bài. Chưa đối chiếu nguồn số liệu trong ảnh; không dùng ảnh này để kết luận về thị phần hiện tại.*

### Công ty Cổ phần Chứng khoán VPS

[VPS công bố hướng dẫn SmartOne](https://www.vps.com.vn/Sites/QuoteVN/SiteRoot/Huong_dan_mo_tai_khoan_chung_khoan_tren_VPS_SmartOne.pdf) để nhà đầu tư đăng ký trên điện thoại. Nếu bạn chọn nền tảng này, hãy xác nhận gói tài khoản cùng dịch vụ hỗ trợ đi kèm.

Không dùng quy mô cộng đồng làm bằng chứng rằng mọi tài khoản có cùng chất lượng tư vấn. Hãy hỏi ai phụ trách hỗ trợ và nơi gửi yêu cầu khi có vấn đề.

### Công ty Cổ phần Chứng khoán SSI

[Trang mở tài khoản SSI](https://www.ssi.com.vn/khach-hang-ca-nhan/mo-tai-khoan) chuyển tới hệ thống đăng ký iBoard. Bạn cần đối chiếu biểu giá giữa giao dịch chủ động và dịch vụ có chuyên viên tư vấn.

"""+im(1)+"""

*Ảnh minh họa được giữ từ phiên bản trước. Vị trí thị phần trong chú thích ảnh chưa được dùng làm tiêu chí xếp hạng ở bảng trên.*

SSI công bố riêng [biểu giá dịch vụ có chuyên viên tư vấn](https://www.ssi.com.vn/khach-hang-ca-nhan/bieu-phi/bieu-gia-dich-vu-giao-dich-chung-khoan). Đọc đúng biểu giá của gói dự định sử dụng, thay vì lấy một mức phí đại diện cho mọi tài khoản.

### Công ty Cổ phần Chứng khoán Kỹ Thương (TCBS)

[Trang mở tài khoản TCBS](https://www.tcbs.com.vn/ca-nhan/uu-dai/mo-tai-khoan-chung-khoan-tcbs/) trình bày quyền lợi cùng các bước đăng ký trực tuyến. Nếu quan tâm ưu đãi phí, bạn cần xem khoản miễn thuộc về dịch vụ nào và còn khoản thu hộ nào.

Không đồng nhất miễn phí mở tài khoản với miễn mọi chi phí sử dụng. Các chương trình trên landing page cần được đọc cùng điều khoản áp dụng khi đăng ký.

### Công ty Cổ phần Chứng khoán TP.HCM (HSC)

[HSC hướng dẫn mở tài khoản](https://www.hsc.com.vn/vi/tai-khoan) qua HSC ONE hoặc website. Nhà đầu tư cần kiểm tra yêu cầu kích hoạt dịch vụ sau khi hoàn tất đăng ký.

Đừng suy ra HSC chỉ phù hợp người có vốn lớn từ hình ảnh thương hiệu. Hãy đối chiếu biểu phí và điều kiện tài khoản với số tiền bạn dự kiến sử dụng.

### Công ty Cổ phần Chứng khoán VNDIRECT

[VNDIRECT giới thiệu đăng ký qua DSTOCK](https://www.vndirect.com.vn/mo-tai-khoan-chung-khoan/) và công bố hướng dẫn trên trung tâm hỗ trợ. Khi chọn nền tảng, kiểm tra kênh đăng ký hiện hành được công ty dẫn tới.

"""+im(2)+"""

Bạn cần xác nhận thời điểm tài khoản được phép giao dịch và điều kiện rút tiền. Đây là các bước khác với việc chỉ tạo thông tin đăng nhập thành công.

### Công ty Cổ phần Chứng khoán VCBS

[Vietcombank mô tả dịch vụ VCBS](https://www.vietcombank.com.vn/vi-VN/KHCN/SPDV/Dau-tu/Giao-dich-Chung-khoan) gồm gói chủ động và gói tư vấn đầu tư. Trang này cũng nêu lựa chọn mở qua VCBS Mobile, website hoặc VCB Digibank.

Nếu đã sử dụng Vietcombank, hãy kiểm tra tiện ích liên kết phù hợp với nhu cầu của bạn. Sự thuận tiện của một kênh ngân hàng không thay thế việc đọc điều kiện giao dịch chứng khoán.

### Công ty Cổ phần Chứng khoán DSC

[DSC](https://www.dsc.com.vn/) cung cấp đăng ký trực tuyến qua App DSC Trading và website. Nếu cần hỗ trợ tư vấn đầu tư từ Môi giới 1:1, hãy xác nhận khối quản lý tài khoản và biểu phí trước khi mở.

"""+im(3)+"""

Theo biểu phí công khai được kiểm tra tháng 11/2026, mức 0,1% áp dụng cho tài khoản do khối Tư vấn số quản lý. Không tự áp mức này cho tài khoản Môi giới quản lý.

Bạn không cần biết hết mọi công cụ trước khi bắt đầu. Khi chọn dịch vụ DSC, hãy hỏi kênh hỗ trợ tư vấn đầu tư và phạm vi đồng hành của Môi giới 1:1.

## Đã chọn được công ty chứng khoán, bước tiếp theo là gì?

DSC có [hướng dẫn cách mở tài khoản chứng khoán](https://www.dsc.com.vn/kien-thuc/cach-mo-tai-khoan-chung-khoan) riêng về đăng ký, xác thực và lỗi thao tác. Sau khi chọn nơi mở, dùng bài hướng dẫn này để chuẩn bị giấy tờ và thực hiện từng bước.

Nếu đang cân nhắc trải nghiệm nhiều bên, xem giải đáp [một người được mở bao nhiêu tài khoản chứng khoán](https://www.dsc.com.vn/kien-thuc/mot-nguoi-duoc-mo-bao-nhieu-tai-khoan-chung-khoan). Không mở nhiều tài khoản chỉ vì ưu đãi nếu bạn chưa biết cách quản lý thông tin đăng nhập.

Bạn đã chọn DSC và cần thực hiện đăng ký thì dùng kênh chính thức dưới đây. Trước khi xác nhận, đối chiếu loại tài khoản, biểu phí và dịch vụ hỗ trợ với nhu cầu của bạn.

[Mở tài khoản eKYC DSC ngay để nhận hỗ trợ 1:1 từ chuyên gia](https://www.dsc.com.vn/mo-tai-khoan)

<div style="border-left: 4px solid #00AD14; background: #E8F8F2; border-radius: 0 8px 8px 0; padding: 18px 22px; margin: 28px 0; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
  <p style="margin: 0; font-size: 16px; line-height: 1.5; color: #0D1B2A; flex: 1 1 240px;">Chọn đúng loại tài khoản DSC trước khi xác nhận đăng ký</p>
  <a href="https://www.dsc.com.vn/mo-tai-khoan" style="background: #0D1B2A; color: #ffffff; padding: 11px 24px; border-radius: 24px; text-decoration: none; font-weight: 600; font-size: 15px; display: inline-block;">Mở tài khoản DSC</a>
</div>
"""
draftpath=root/"knowledge/4-content/2-drafts"/("Optimize-"+slug+"-serp-2026-11-04.md");draftpath.write_text(draft,encoding="utf-8")
proposal=f"""---
Title: Proposal tối ưu lựa chọn công ty chứng khoán
Target_Keyword: nên mở tài khoản chứng khoán ở đâu
Slug: {slug}
Persona: P2
Status: Proposal implemented to draft only
Evidence_Source: User incognito screenshots
---
# Proposal: {title}

## 0. Content strategy header

| Thông số | Quyết định |
|---|---|
| Target keyword | nên mở tài khoản chứng khoán ở đâu |
| Secondary | nên mở tài khoản chứng khoán ở công ty nào; chọn công ty chứng khoán |
| Intent | Commercial investigation: chọn nơi mở theo dịch vụ. |
| Persona | P2, người mới cần lựa chọn kênh và người hỗ trợ. |
| Tone | Comparison, trung lập, cùng điều kiện, không xếp hạng an toàn. |
| Product bridge | eKYC và Môi giới 1:1; xác nhận khối quản lý và biểu phí. |
| URL | Giữ URL, H1 hiện hành, thứ tự công ty. |
| Baseline | Live đồng bộ 04/11/2026; Final chỉ tương đồng khoảng 13%. |

Ảnh người dùng: DSC #3, VFS #2 cho truy vấn so sánh, bỏ AI Overview. Proposal chạy auto theo yêu cầu triển khai; Final/CMS vẫn chờ phê duyệt cụ thể.

## 1. Đánh giá tổng quan

Live có bốn ảnh, tám href phải giữ. Mở bài vĩ mô, số liệu vốn/thị phần/phí thiếu nguồn, phê bình đối thủ không nguồn cần sửa.

- Title hiện tại và đề xuất: {title}
- Meta đề xuất: {meta}
- Không dùng word count đối thủ làm mục tiêu.

### GSC performance context

Kỳ 05/10–01/11/2026 tại Việt Nam: query chính rộng mở tài khoản chứng khoán có 161 impressions, vị trí 17,06 ở URL này. Query nên mở tài khoản chứng khoán ở đâu có 115 impressions, vị trí 5,69. Query mở tài khoản chứng khoán ở đâu tốt nhất có 173 impressions, vị trí 3,84. Không đồng nhất vị trí trung bình với ảnh SERP.

### Backfill

Không thêm inlink hàng loạt: snapshot có 14 nguồn body dẫn tới bài. Giữ phân vai anchor so sánh/hướng dẫn.

## 2. Phân tích đối thủ SERP

### 2.1 Tổng quan

VFS là đối chứng từ ảnh #2, DSC #3. Cải thiện tính trực quan và nguồn kiểm chứng, không sao chép số liệu cũ.

### 2.2 Outline từng đối thủ

**VFS — https://www.vfs.com.vn/mo-tai-khoan-cong-ty-chung-khoan-nao**
- H1: Mở tài khoản công ty chứng khoán nào? TOP 5 công ty uy tín.
- H2: 5+ tiêu chí chọn công ty chứng khoán tốt nhất.
- H3: Thương hiệu; phí; sản phẩm; công nghệ; chuyên viên.
- H2: Top công ty chứng khoán nên mở tài khoản.
- H3: VPS; SSI; HSC; VNDIRECT; VFS.
- H2: Cách mở tài khoản chứng khoán nhanh gọn.
- Yếu tố: bảng so sánh, tiêu chí lựa chọn.
- Gap DSC: giải đáp sớm và bảng điều kiện có nguồn.
- Không học phần pháp lý cũ hay suy luận thị phần thành an toàn.

Các competitor API đã có báo cáo riêng; root đưa mỗi outline vào appendix chung. Không dùng API không tái hiện ảnh để xác định rank hiện tại.

### 2.3 Intent gap

DSC đã phục vụ intent chọn công ty. Khoảng trống là so sánh đúng điều kiện và số liệu xác minh được, không phải thiếu quy trình mở. Giữ hướng dẫn riêng ở URL cach-mo-tai-khoan-chung-khoan.

### PAA refresh từ ảnh, không phải API

| Câu hỏi trong ảnh | Cách xử lý |
|---|---|
| Đăng ký tài khoản chứng khoán ở đâu tốt nhất? | Trả lời bằng tiêu chí, bảng và đoạn lựa chọn; không lặp FAQ. |
| Mã chứng khoán ngân hàng nào tốt nhất hiện nay? | Khác intent, không chèn. |
| Việc không đóng tài khoản chứng khoán có ảnh hưởng gì không? | Chưa đủ nguồn; không bịa pháp lý, để bài chuyên sâu sau. |
| Công ty chứng khoán nào tốt nhất hiện nay tại Việt Nam? | Giải đáp theo nhu cầu, không xếp hạng tuyệt đối. |

API PAA rỗng; không giả nhãn API. Không đặt PAA_Questions YAML vì không yêu cầu draft chép nguyên bốn câu khác intent.

## 3. Sweeps audit

| Sweep | Lỗi và xử lý |
|---|---|
| Clarity | Sapo dài, sửa trả lời trực tiếp. |
| Voice | Bỏ siêu ngữ và phê bình thiếu nguồn. |
| So what | Thêm điều cần hỏi trước đăng ký. |
| Prove it | Dùng nguồn chính thức, phân biệt hai nhóm phí DSC. |
| Specificity | Kênh và điều kiện thay tốt/nhanh/an toàn tuyệt đối. |
| Emotion | Giúp quyết định, không thúc FOMO. |
| Zero risk | Không hứa lợi nhuận hay hỗ trợ 24/7. |
| GEO/AEO | Claim tự kiểm chứng, có ngày rà soát. |

## 4. Heading-by-heading

| Heading | Nhãn | Xử lý |
|---|---|---|
| Sapo | CẬP NHẬT | Trả lời chọn loại dịch vụ, bỏ vĩ mô. |
| 5 tiêu chí và 5 H3 | CẬP NHẬT | Giữ nhóm, sửa bằng chứng/giọng văn. |
| So sánh Top 7 | CẬP NHẬT | Bảng kênh/điều kiện thay vốn/thị phần chưa xác minh. |
| Bảy công ty | CẬP NHẬT | Giữ thứ tự, ảnh; nguồn chính thức thay nhận xét không nguồn. |
| Kết luận | CẬP NHẬT | Đổi thành bước sau lựa chọn, dẫn bài hướng dẫn. |

## 5. Nội dung thêm mới

- Bảng kênh/điều kiện: học cấu trúc bảng từ VFS, xác minh từng công ty.
- Ví dụ phí 10 triệu đồng: từ biểu phí DSC; không so phí hai loại tài khoản để xếp hạng.
- Ghi chú ảnh lịch sử: phát hiện nội bộ, không dùng ảnh để xác nhận thị phần.
- Không thêm H2 thao tác eKYC; không tạo bài mới.

## 6. Internal links

Bảo toàn tám href live: phí mở, phí giao dịch, loại tài khoản, an toàn, hướng dẫn, số lượng, homepage và trang đăng ký. Anchor hướng dẫn chỉ dẫn bài Cách mở; CTA dẫn mo-tai-khoan. Nguồn mới là website chính thức từng công ty.

## 7. Hình ảnh

### 7.1 Ảnh gốc
"""
for i,(alt,url) in enumerate(imgs): proposal+="\n- "+im(i)+" — giữ ở "+["sau bảng tổng hợp","mục SSI","mục VNDIRECT","mục DSC"][i]+"."
proposal+="""\n\nHai ảnh đầu chứa claim thị phần chưa đối chiếu. Giữ asset và ghi chú lịch sử; đây là hạng mục biên tập phải giải quyết trước CMS, không tự xác nhận nguồn.

### 7.2 Vị trí trực quan

Dùng bảng mới và bốn ảnh thực đang có. Không tạo screenshot giả hoặc thêm stock chỉ để đạt số lượng ảnh.
"""
proppath=root/"knowledge/4-content/1-outlines"/("Proposal-"+slug+"-serp-2026-11-04.md");proppath.write_text(proposal,encoding="utf-8")
checks={"slug":slug,"title_characters":len(title),"meta_characters":len(meta),"missing_images":[u for _,u in imgs if u not in draft],"missing_links":[u for u in links if u not in draft],"editorial_open":["Original market-share graphic and SSI alt still need editorial verification before CMS"],"published":False}
(out/("preservation-"+slug+".json")).write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(checks,ensure_ascii=False))

